import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import io

# --- Page Configuration ---
st.set_page_config(
    page_title="Academic Performance Dashboard",
    page_icon="🎓",
    layout="wide"
)

# --- Helper Functions ---

def generate_sample_excel():
    """Creates a sample Excel file in memory."""
    data = {
        'Semester': [
            'Fall 2023', 'Fall 2023', 'Fall 2023', 
            'Spring 2024', 'Spring 2024', 'Spring 2024',
            'Fall 2024', 'Fall 2024'
        ],
        'Code': ['CS101', 'MATH101', 'ENG101', 'CS102', 'MATH102', 'PHY101', 'CS201', 'HIST201'],
        'Course Name': [
            'Intro to Programming', 'Calculus I', 'English Composition',
            'Data Structures', 'Calculus II', 'Physics I', 'Algorithms', 'World History'
        ],
        'CrdHrs': [3, 4, 3, 4, 4, 4, 3, 3],
        'Grade': ['A', 'B+', 'A', 'A-', 'B', 'A', 'A', 'A-'],
        'Points': [4.0, 3.3, 4.0, 3.7, 3.0, 4.0, 4.0, 3.7]
    }
    df = pd.DataFrame(data)
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Transcript')
    output.seek(0)
    return output

def clean_data(df):
    """Strips whitespace and ensures numeric types."""
    df.columns = df.columns.str.strip()
    numeric_cols = ['CrdHrs', 'Points']
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
    return df

def calculate_semester_sort(semester_series):
    """Creates a sort key for chronological order."""
    season_map = {'Spring': 1, 'Summer': 2, 'Fall': 3, 'Winter': 4}
    def get_sort_key(sem_str):
        try:
            parts = sem_str.split()
            season = parts[0]
            year = int(parts[1])
            season_val = season_map.get(season, 0)
            return (year, season_val)
        except:
            return (9999, 99)
    return semester_series.apply(get_sort_key)

def process_data(df):
    """Calculates Quality Points, SGPA, and CGPA."""
    df['Quality Points'] = df['CrdHrs'] * df['Points']
    
    grouped = df.groupby('Semester').agg({
        'CrdHrs': 'sum',
        'Quality Points': 'sum',
        'Code': 'count'
    }).rename(columns={'Code': 'Course Count'}).reset_index()
    
    grouped['SGPA'] = grouped.apply(
        lambda row: row['Quality Points'] / row['CrdHrs'] if row['CrdHrs'] > 0 else 0, 
        axis=1
    )
    
    sort_keys = calculate_semester_sort(grouped['Semester'])
    grouped['_sort_key'] = sort_keys
    grouped = grouped.sort_values('_sort_key').drop('_sort_key', axis=1)
    
    grouped['Cumulative CrdHrs'] = grouped['CrdHrs'].cumsum()
    grouped['Cumulative QP'] = grouped['Quality Points'].cumsum()
    grouped['CGPA'] = grouped.apply(
        lambda row: row['Cumulative QP'] / row['Cumulative CrdHrs'] if row['Cumulative CrdHrs'] > 0 else 0, 
        axis=1
    )
    
    return grouped, df

# --- Main Application UI ---

st.title("🎓 Academic Performance & Forecasting Dashboard")

with st.sidebar:
    st.header("Settings")
    uploaded_file = st.file_uploader("Upload Excel File", type=['xlsx'])
    st.info("""
    **Required Columns:**
    - Semester
    - Code
    - Course Name
    - CrdHrs
    - Grade
    - Points
    """)
    
    # --- NEW: FORECASTING SIDEBAR ---
    st.markdown("---")
    with st.expander("🔮 GPA Forecaster"):
        st.markdown("**Scenario Planner**")
        st.caption("Estimate your final CGPA based on future performance.")
        
        # Inputs for forecasting
        rem_credits = st.slider(
            "Remaining Credit Hours", 
            min_value=0, max_value=60, value=15, step=1
        )
        expected_sgpa = st.slider(
            "Expected Future SGPA", 
            min_value=0.0, max_value=4.0, value=3.5, step=0.1
        )
        
        enable_forecast = st.checkbox("Enable Forecast on Chart", value=True)

if uploaded_file:
    try:
        df_raw = pd.read_excel(uploaded_file)
        df_raw = clean_data(df_raw)
        
        required_cols = ['Semester', 'Code', 'Course Name', 'CrdHrs', 'Grade', 'Points']
        if not all(col in df_raw.columns for col in required_cols):
            st.error(f"Missing columns! Please ensure your Excel file has: {', '.join(required_cols)}")
        else:
            df_semester_stats, df_full = process_data(df_raw)
            
            # --- Forecasting Logic ---
            # Get latest cumulative totals
            current_creds = df_semester_stats['Cumulative CrdHrs'].iloc[-1]
            current_qp = df_semester_stats['Cumulative QP'].iloc[-1]
            current_cgpa = df_semester_stats['CGPA'].iloc[-1]
            last_semester_name = df_semester_stats['Semester'].iloc[-1]
            
            # Calculate Projection
            future_qp = rem_credits * expected_sgpa
            total_proj_qp = current_qp + future_qp
            total_proj_creds = current_creds + rem_credits
            projected_cgpa = total_proj_qp / total_proj_creds if total_proj_creds > 0 else 0
            
            # --- METRICS SECTION ---
            col1, col2, col3 = st.columns(3)
            
            # Metric 1: Current CGPA (updates if forecast enabled? usually better to keep separate)
            col1.metric(label="Current CGPA", value=f"{current_cgpa:.2f}")
            
            # Metric 2: Projected CGPA (Only visible if forecasting is enabled and credits > 0)
            if enable_forecast and rem_credits > 0:
                col2.metric(label="Projected Final CGPA", value=f"{projected_cgpa:.2f}")
            else:
                col2.metric(label="Projected Final CGPA", value="--")
                
            col3.metric(label="Total Credit Hours", value=f"{total_proj_creds:.1f}" if enable_forecast else f"{current_creds:.1f}")
            
            st.markdown("---")
            
            # --- TABS FOR ORGANIZATION ---
            tab1, tab2 = st.tabs(["Overview", "Detailed Analytics"])
            
            with tab1:
                col_left, col_right = st.columns([2, 1])
                
                with col_left:
                    st.subheader("GPA Trends")
                    fig_trend = go.Figure()
                    
                    # 1. ACTUAL SGPA LINE (Solid)
                    fig_trend.add_trace(go.Scatter(
                        x=df_semester_stats['Semester'], y=df_semester_stats['SGPA'],
                        mode='lines+markers', name='SGPA (Actual)',
                        line=dict(color='#1f77b4', width=3)
                    ))
                    
                    # 2. ACTUAL CGPA LINE (Solid)
                    fig_trend.add_trace(go.Scatter(
                        x=df_semester_stats['Semester'], y=df_semester_stats['CGPA'],
                        mode='lines+markers', name='CGPA (Actual)',
                        line=dict(color='#ff7f0e', width=3)
                    ))
                    
                    # 3. PROJECTED CGPA LINE (Dashed "Ghost" Line)
                    if enable_forecast and rem_credits > 0:
                        # We draw a line from the last known point to the projected point
                        # X coordinates: [Last Semester, "Projected Graduation"]
                        # Y coordinates: [Current CGPA, Projected CGPA]
                        
                        fig_trend.add_trace(go.Scatter(
                            x=[last_semester_name, "Projected Graduation"],
                            y=[current_cgpa, projected_cgpa],
                            mode='lines+markers',
                            name=f'Projected (if {expected_sgpa} SGPA)',
                            line=dict(color='#00cc96', width=3, dash='dash'),
                            marker=dict(size=10) # Make the end dot bigger
                        ))
                        
                        # Add a vertical line to separate past from future
                        fig_trend.add_vline(
                            x=len(df_semester_stats['Semester']) - 0.5, 
                            line_dash="dot", line_color="gray", opacity=0.5,
                            annotation_text="Future"
                        )

                    fig_trend.update_layout(
                        yaxis_title="GPA", 
                        hovermode="x unified", 
                        template="plotly_white",
                        legend=dict(orientation="h", y=-0.2) # Move legend to bottom to make room
                    )
                    st.plotly_chart(fig_trend, use_container_width=True)
                
                with col_right:
                    st.subheader("Grade Distribution")
                    grade_counts = df_full['Grade'].value_counts().reset_index()
                    grade_counts.columns = ['Grade', 'Count']
                    fig_donut = px.pie(grade_counts, values='Count', names='Grade', hole=0.5, 
                                       color_discrete_sequence=px.colors.qualitative.Pastel)
                    fig_donut.update_traces(textposition='inside', textinfo='percent+label')
                    fig_donut.update_layout(showlegend=False, margin=dict(t=0, b=0, l=0, r=0))
                    st.plotly_chart(fig_donut, use_container_width=True)

            with tab2:
                st.subheader("Detailed Performance Breakdown")
                c1, c2 = st.columns(2)
                
                with c1:
                    st.markdown("### **Credit Workload per Semester**")
                    fig_load = px.bar(
                        df_semester_stats, x='Semester', y='CrdHrs', color='CrdHrs',
                        title="Course Intensity", color_continuous_scale='Blues'
                    )
                    fig_load.update_layout(xaxis_title="", template="plotly_white")
                    st.plotly_chart(fig_load, use_container_width=True)
                
                with c2:
                    st.markdown("### **Quality Points Contribution**")
                    fig_qp = px.bar(
                        df_semester_stats, x='Semester', y='Quality Points',
                        title="Academic Momentum", color='SGPA', color_continuous_scale='Viridis'
                    )
                    fig_qp.update_layout(xaxis_title="", template="plotly_white")
                    st.plotly_chart(fig_qp, use_container_width=True)
                
                st.markdown("### **Performance vs. Course Weight**")
                st.caption("Do you perform better in lighter or heavier courses?")
                fig_scatter = px.scatter(
                    df_full, x='CrdHrs', y='Points', color='Grade',
                    hover_data=['Course Name', 'Semester'],
                    title="Grade Distribution by Course Credit Weight",
                    labels={'CrdHrs': 'Credit Hours', 'Points': 'Grade Points'},
                    category_orders={"Grade": sorted(df_full['Grade'].unique())}
                )
                avg_points = df_full['Points'].mean()
                fig_scatter.add_hline(y=avg_points, line_dash="dot", annotation_text=f"Average: {avg_points:.2f}")
                fig_scatter.update_layout(template="plotly_white")
                st.plotly_chart(fig_scatter, use_container_width=True)

            st.markdown("---")
            st.subheader("Raw Course Data")
            unique_semesters = df_full['Semester'].unique()
            selected_semester = st.selectbox("Filter by Semester", options=["All Semesters"] + list(unique_semesters))
            
            if selected_semester == "All Semesters":
                st.dataframe(df_full, use_container_width=True)
            else:
                st.dataframe(df_full[df_full['Semester'] == selected_semester], use_container_width=True)

    except Exception as e:
        st.error(f"An error occurred: {e}")
else:
    st.info("👆 Please upload an Excel file to generate the dashboard.")
    st.markdown("---")
    st.subheader("Don't have a file? Try a Sample!")
    col_a, col_b, col_c = st.columns([1,2,1])
    with col_b:
        st.write("Click the button below to download a pre-formatted Excel file.")
        sample_file = generate_sample_excel()
        st.download_button(
            label="📥 Download Sample Excel File",
            data=sample_file,
            file_name="sample_transcript.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            type="primary"
        )