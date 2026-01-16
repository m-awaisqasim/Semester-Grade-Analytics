import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

# --- Page Configuration ---
st.set_page_config(
    page_title="Academic Performance Dashboard",
    page_icon="🎓",
    layout="wide"
)

# --- Helper Functions ---

def clean_data(df):
    """Strips whitespace and ensures numeric types."""
    df.columns = df.columns.str.strip()
    numeric_cols = ['CrdHrs', 'Points']
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
    return df

def calculate_semester_sort(semester_series):
    """
    Creates a sort key to ensure chronological order.
    Assumes format like 'Fall 2024' or 'Spring 2025'.
    """
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
    
    # SGPA Calculation
    grouped['SGPA'] = grouped.apply(
        lambda row: row['Quality Points'] / row['CrdHrs'] if row['CrdHrs'] > 0 else 0, 
        axis=1
    )
    
    # Chronological Sort
    sort_keys = calculate_semester_sort(grouped['Semester'])
    grouped['_sort_key'] = sort_keys
    grouped = grouped.sort_values('_sort_key').drop('_sort_key', axis=1)
    
    # CGPA Calculation
    grouped['Cumulative CrdHrs'] = grouped['CrdHrs'].cumsum()
    grouped['Cumulative QP'] = grouped['Quality Points'].cumsum()
    grouped['CGPA'] = grouped.apply(
        lambda row: row['Cumulative QP'] / row['Cumulative CrdHrs'] if row['Cumulative CrdHrs'] > 0 else 0, 
        axis=1
    )
    
    return grouped, df

# --- Main Application UI ---

st.title("🎓 Multi-Semester Academic Dashboard")

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

if uploaded_file:
    try:
        df_raw = pd.read_excel(uploaded_file)
        df_raw = clean_data(df_raw)
        
        required_cols = ['Semester', 'Code', 'Course Name', 'CrdHrs', 'Grade', 'Points']
        if not all(col in df_raw.columns for col in required_cols):
            st.error(f"Missing columns! Please ensure your Excel file has: {', '.join(required_cols)}")
        else:
            df_semester_stats, df_full = process_data(df_raw)
            
            # --- METRICS SECTION ---
            latest_stats = df_semester_stats.iloc[-1]
            total_credits = df_full['CrdHrs'].sum()
            total_courses = len(df_full)
            
            col1, col2, col3 = st.columns(3)
            col1.metric(label="Latest CGPA", value=f"{latest_stats['CGPA']:.2f}")
            col2.metric(label="Total Credit Hours", value=f"{total_credits:.1f}")
            col3.metric(label="Total Courses", value=f"{total_courses}")
            
            st.markdown("---")
            
            # --- TABS FOR ORGANIZATION ---
            tab1, tab2 = st.tabs(["Overview", "Detailed Analytics"])
            
            # ===========================
            # TAB 1: OVERVIEW
            # ===========================
            with tab1:
                col_left, col_right = st.columns([2, 1])
                
                with col_left:
                    st.subheader("GPA Trends")
                    fig_trend = go.Figure()
                    fig_trend.add_trace(go.Scatter(
                        x=df_semester_stats['Semester'], y=df_semester_stats['SGPA'],
                        mode='lines+markers', name='SGPA (Semester)',
                        line=dict(color='#1f77b4', width=3)
                    ))
                    fig_trend.add_trace(go.Scatter(
                        x=df_semester_stats['Semester'], y=df_semester_stats['CGPA'],
                        mode='lines+markers', name='CGPA (Cumulative)',
                        line=dict(color='#ff7f0e', width=3, dash='dash')
                    ))
                    fig_trend.update_layout(yaxis_title="GPA", hovermode="x unified", template="plotly_white")
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
            
            # ===========================
            # TAB 2: DETAILED ANALYTICS
            # ===========================
            with tab2:
                st.subheader("Detailed Performance Breakdown")
                
                # Row 1: Credit Workload & Quality Contribution
                c1, c2 = st.columns(2)
                
                with c1:
                    st.markdown("### **Credit Workload per Semester**")
                    # Insight: Shows intensity of study load
                    fig_load = px.bar(
                        df_semester_stats, 
                        x='Semester', 
                        y='CrdHrs', 
                        color='CrdHrs',
                        title="Course Intensity",
                        labels={'CrdHrs': 'Credit Hours'},
                        color_continuous_scale='Blues'
                    )
                    fig_load.update_layout(xaxis_title="", template="plotly_white")
                    st.plotly_chart(fig_load, use_container_width=True)
                
                with c2:
                    st.markdown("### **Quality Points Contribution**")
                    # Insight: Which semesters contributed most to the overall score?
                    fig_qp = px.bar(
                        df_semester_stats,
                        x='Semester',
                        y='Quality Points',
                        title="Academic Momentum",
                        labels={'Quality Points': 'Points Earned'},
                        color='SGPA', # Color by SGPA to show efficiency
                        color_continuous_scale='Viridis'
                    )
                    fig_qp.update_layout(xaxis_title="", template="plotly_white")
                    st.plotly_chart(fig_qp, use_container_width=True)
                
                # Row 2: Scatter Plot
                st.markdown("### **Performance vs. Course Weight**")
                st.caption("Do you perform better in lighter or heavier courses?")
                
                # Scatter Plot: Credits vs Points
                fig_scatter = px.scatter(
                    df_full,
                    x='CrdHrs',
                    y='Points',
                    color='Grade',
                    hover_data=['Course Name', 'Semester'],
                    title="Grade Distribution by Course Credit Weight",
                    labels={'CrdHrs': 'Credit Hours', 'Points': 'Grade Points'},
                    category_orders={"Grade": sorted(df_full['Grade'].unique())}
                )
                # Add a line for average points (optional, but helpful)
                avg_points = df_full['Points'].mean()
                fig_scatter.add_hline(y=avg_points, line_dash="dot", 
                                      annotation_text=f"Average: {avg_points:.2f}")
                
                fig_scatter.update_layout(template="plotly_white")
                st.plotly_chart(fig_scatter, use_container_width=True)

            # ===========================
            # BOTTOM: DATA TABLE
            # ===========================
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