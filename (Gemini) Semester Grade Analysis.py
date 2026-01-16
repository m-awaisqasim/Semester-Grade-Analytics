import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
# Streamlit Page Configuration

st.set_page_config(page_title="Semester Analytics", layout="wide")

st.title("🎓 Multi-Semester Grade Dashboard")
st.markdown("Upload your Excel file to visualize your academic journey.")

# 1. File Uploader
uploaded_file = st.file_uploader("Choose an Excel file", type="xlsx")

if uploaded_file:
    # Load data
    df = pd.read_excel(uploaded_file)
    
    # Standardize column names (lowercase/strip spaces)
    df.columns = [c.strip() for c in df.columns]

    # 2. Processing & Calculations
    # Calculate Quality Points (Points * Credits)
    df['Quality_Points'] = df['Points'] * df['CrdHrs']

    # Group by Semester for SGPA
    sem_stats = df.groupby('Semester').agg({
        'Quality_Points': 'sum',
        'CrdHrs': 'sum'
    }).reset_index()
    
    sem_stats['SGPA'] = sem_stats['Quality_Points'] / sem_stats['CrdHrs']
    
    # Calculate Cumulative GPA (Running Total)
    sem_stats['Cum_QP'] = sem_stats['Quality_Points'].cumsum()
    sem_stats['Cum_Hrs'] = sem_stats['CrdHrs'].cumsum()
    sem_stats['CGPA'] = sem_stats['Cum_QP'] / sem_stats['Cum_Hrs']

    # 3. KPI Metrics
    total_credits = df['CrdHrs'].sum()
    final_cgpa = sem_stats['CGPA'].iloc[-1]
    total_courses = len(df)

    col1, col2, col3 = st.columns(3)
    col1.metric("Cumulative GPA", f"{final_cgpa:.2f}")
    col2.metric("Total Credits", int(total_credits))
    col3.metric("Courses Completed", total_courses)

    # 4. Visualizations
    st.divider()
    chart_col, dist_col = st.columns([2, 1])

    with chart_col:
        st.subheader("GPA Trend Analysis")
        fig = go.Figure()
        # SGPA Line
        fig.add_trace(go.Scatter(x=sem_stats['Semester'], y=sem_stats['SGPA'],
                                mode='lines+markers', name='Semester GPA (SGPA)',
                                line=dict(color='#6366f1', width=4)))
        # CGPA Line
        fig.add_trace(go.Scatter(x=sem_stats['Semester'], y=sem_stats['CGPA'],
                                mode='lines', name='Cumulative GPA (CGPA)',
                                line=dict(color='#94a3b8', width=2, dash='dash')))
        
        fig.update_layout(yaxis_range=[0, 4.3], hovermode="x unified")
        st.plotly_chart(fig, use_container_width=True)

    with dist_col:
        st.subheader("Grade Distribution")
        grade_counts = df['Grade'].value_counts().reset_index()
        fig_pie = px.pie(grade_counts, values='count', names='Grade', 
                         hole=0.4, color_discrete_sequence=px.colors.qualitative.Pastel)
        st.plotly_chart(fig_pie, use_container_width=True)

    # 5. Detailed Data Table
    st.subheader("Semester Breakdown")
    selected_sem = st.selectbox("Filter by Semester", ["All"] + list(sem_stats['Semester']))
    
    display_df = df.copy()
    if selected_sem != "All":
        display_df = df[df['Semester'] == selected_sem]
    
    st.dataframe(display_df[['Semester', 'Code', 'Course Name', 'CrdHrs', 'Grade', 'Points']], 
                 use_container_width=True, hide_index=True)

else:
    st.info("Please upload an Excel file with columns: Semester, Code, Course Name, CrdHrs, Grade, Points")