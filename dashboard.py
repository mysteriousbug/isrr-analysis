"""
Streamlit Dashboard for ISRR Analysis
Interactive, dynamic dashboard with real-time data visualization
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import sys
import os

# Add the logic folder to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'logic'))
import config

# Page configuration
st.set_page_config(
    page_title="ISRR Analysis Dashboard",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main-header {
        font-size: 3rem;
        font-weight: 700;
        text-align: center;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        padding: 1rem 0;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
        text-align: center;
    }
    .stMetric {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 8px;
    }
    </style>
""", unsafe_allow_html=True)

@st.cache_data
def load_results():
    """Load analysis results from Excel files"""
    try:
        results_path = os.path.join('results', config.OUTPUT_FILES['complete_analysis'])
        results_df = pd.read_excel(results_path)
        
        try:
            mismatches_path = os.path.join('results', config.OUTPUT_FILES['mismatches'])
            mismatches_df = pd.read_excel(mismatches_path)
        except:
            mismatches_df = pd.DataFrame()
        
        return results_df, mismatches_df
    except Exception as e:
        st.error(f"Error loading results: {e}")
        st.info("Please run the analysis first: `python run.py`")
        return None, None

def create_isrr_comparison_chart(results_df):
    """Create interactive comparison chart for existing vs calculated ISRR"""
    isrr_levels = ['Minor', 'Low', 'Moderate', 'High', 'Critical']
    
    existing_counts = [len(results_df[results_df['Existing_ISRR_Value'] == level]) for level in isrr_levels]
    calculated_counts = [len(results_df[results_df['Calculated_Final_ISRR'] == level]) for level in isrr_levels]
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        name='Existing ISRR',
        x=isrr_levels,
        y=existing_counts,
        marker_color='rgb(52, 152, 219)',
        text=existing_counts,
        textposition='auto',
    ))
    
    fig.add_trace(go.Bar(
        name='Calculated ISRR',
        x=isrr_levels,
        y=calculated_counts,
        marker_color='rgb(231, 76, 60)',
        text=calculated_counts,
        textposition='auto',
    ))
    
    fig.update_layout(
        title='Existing vs Calculated ISRR Distribution',
        xaxis_title='ISRR Level',
        yaxis_title='Number of EGIDs',
        barmode='group',
        height=400,
        hovermode='x unified'
    )
    
    return fig

def create_risk_changes_chart(results_df):
    """Create pie chart showing risk level changes"""
    changes = results_df['Interim_to_Final_Change'].value_counts()
    
    fig = go.Figure(data=[go.Pie(
        labels=changes.index,
        values=changes.values,
        hole=.3,
        marker_colors=['#e74c3c', '#27ae60']
    )])
    
    fig.update_layout(
        title='Interim to Final ISRR Changes',
        height=400
    )
    
    return fig

def create_mismatch_severity_chart(mismatches_df):
    """Create chart showing mismatch severity analysis"""
    if len(mismatches_df) == 0:
        return None
    
    risk_levels = ['Minor', 'Low', 'Moderate', 'High', 'Critical']
    severity_increases = 0
    severity_decreases = 0
    same_level = 0
    
    for _, row in mismatches_df.iterrows():
        existing = row['Existing_ISRR']
        calculated = row['Calculated_Final_ISRR']
        
        if existing in risk_levels and calculated in risk_levels:
            existing_idx = risk_levels.index(existing)
            calculated_idx = risk_levels.index(calculated)
            
            if calculated_idx > existing_idx:
                severity_increases += 1
            elif calculated_idx < existing_idx:
                severity_decreases += 1
            else:
                same_level += 1
    
    fig = go.Figure(data=[go.Bar(
        x=['Risk Increased', 'Risk Decreased', 'Same Level'],
        y=[severity_increases, severity_decreases, same_level],
        marker_color=['#e74c3c', '#27ae60', '#95a5a6'],
        text=[severity_increases, severity_decreases, same_level],
        textposition='auto',
    )])
    
    fig.update_layout(
        title='Mismatch Severity Analysis',
        yaxis_title='Number of EGIDs',
        height=400
    )
    
    return fig

def create_sankey_diagram(results_df):
    """Create Sankey diagram showing ISRR flow"""
    # Sample a subset for better visualization
    sample_size = min(100, len(results_df))
    sample_df = results_df.sample(n=sample_size, random_state=42)
    
    # Create mappings
    interim_isrr = sample_df['Calculated_Interim_ISRR'].tolist()
    final_isrr = sample_df['Calculated_Final_ISRR'].tolist()
    
    risk_levels = ['Minor', 'Low', 'Moderate', 'High', 'Critical']
    
    # Create source and target indices
    source = []
    target = []
    value = []
    
    for interim, final in zip(interim_isrr, final_isrr):
        if interim in risk_levels and final in risk_levels:
            source.append(risk_levels.index(interim))
            target.append(len(risk_levels) + risk_levels.index(final))
            value.append(1)
    
    # Create labels
    labels = [f"Interim: {level}" for level in risk_levels] + [f"Final: {level}" for level in risk_levels]
    
    fig = go.Figure(data=[go.Sankey(
        node=dict(
            pad=15,
            thickness=20,
            line=dict(color="black", width=0.5),
            label=labels,
            color=['#3498db', '#5dade2', '#85c1e2', '#aed6f1', '#d6eaf8',
                   '#e74c3c', '#ec7063', '#f1948a', '#f5b7b1', '#fadbd8']
        ),
        link=dict(
            source=source,
            target=target,
            value=value
        )
    )])
    
    fig.update_layout(
        title=f"ISRR Flow: Interim → Final (Sample of {sample_size} EGIDs)",
        height=600
    )
    
    return fig

def create_data_groups_chart(results_df):
    """Create scatter plot of transactional vs non-transactional groups"""
    fig = px.scatter(
        results_df,
        x='Transactional_Groups',
        y='Non_Transactional_Groups',
        color='Calculated_Final_ISRR',
        size='Transactional_Groups',
        hover_data=['EGID', 'Nature_of_Data'],
        color_discrete_map={
            'Minor': '#3498db',
            'Low': '#27ae60',
            'Moderate': '#f39c12',
            'High': '#e67e22',
            'Critical': '#e74c3c'
        },
        title='Data Groups Distribution by Final ISRR'
    )
    
    fig.update_layout(height=500)
    
    return fig

def main():
    """Main dashboard function"""
    
    # Header
    st.markdown('<h1 class="main-header">🏦 ISRR Analysis Dashboard</h1>', unsafe_allow_html=True)
    st.markdown("### Comprehensive Inherent Security Risk Rating Analysis")
    st.markdown("---")
    
    # Load data
    with st.spinner("Loading analysis results..."):
        results_df, mismatches_df = load_results()
    
    if results_df is None:
        st.stop()
    
    # Sidebar - Filters
    st.sidebar.header("🔍 Filters")
    
    # ISRR level filter
    selected_isrr = st.sidebar.multiselect(
        "Filter by Final ISRR Level",
        options=['Minor', 'Low', 'Moderate', 'High', 'Critical'],
        default=['Minor', 'Low', 'Moderate', 'High', 'Critical']
    )
    
    # Match status filter
    match_filter = st.sidebar.radio(
        "Filter by Match Status",
        options=['All', 'Matched Only', 'Mismatched Only'],
        index=0
    )
    
    # Apply filters
    filtered_df = results_df.copy()
    if selected_isrr:
        filtered_df = filtered_df[filtered_df['Calculated_Final_ISRR'].isin(selected_isrr)]
    
    if match_filter == 'Matched Only':
        filtered_df = filtered_df[filtered_df['ISRR_Match'] == 'Yes']
    elif match_filter == 'Mismatched Only':
        filtered_df = filtered_df[filtered_df['ISRR_Match'] == 'No']
    
    # Key Metrics
    st.header("📊 Key Metrics")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="Total EGIDs",
            value=f"{len(results_df):,}",
            delta=f"{len(filtered_df):,} filtered"
        )
    
    with col2:
        match_rate = ((len(results_df) - len(mismatches_df)) / len(results_df) * 100) if len(results_df) > 0 else 0
        st.metric(
            label="Match Rate",
            value=f"{match_rate:.1f}%",
            delta="Good" if match_rate > 90 else "Needs Review",
            delta_color="normal" if match_rate > 90 else "inverse"
        )
    
    with col3:
        st.metric(
            label="Mismatches",
            value=f"{len(mismatches_df):,}",
            delta=f"{(len(mismatches_df)/len(results_df)*100):.1f}%",
            delta_color="inverse"
        )
    
    with col4:
        changes = len(results_df[results_df['Interim_to_Final_Change'] == 'Yes'])
        st.metric(
            label="Interim→Final Changes",
            value=f"{changes:,}",
            delta=f"{(changes/len(results_df)*100):.1f}%"
        )
    
    st.markdown("---")
    
    # Tabs for different views
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📈 Overview", 
        "⚠️ Mismatches", 
        "🔄 Flow Analysis", 
        "📋 Data Table", 
        "💾 Export"
    ])
    
    # Tab 1: Overview
    with tab1:
        st.header("ISRR Distribution Analysis")
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig1 = create_isrr_comparison_chart(filtered_df)
            st.plotly_chart(fig1, use_container_width=True)
        
        with col2:
            fig2 = create_risk_changes_chart(filtered_df)
            st.plotly_chart(fig2, use_container_width=True)
        
        st.subheader("Data Groups Distribution")
        fig3 = create_data_groups_chart(filtered_df)
        st.plotly_chart(fig3, use_container_width=True)
        
        # Summary statistics
        st.subheader("📊 Summary Statistics")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.write("**Most Common Final ISRR:**")
            most_common = filtered_df['Calculated_Final_ISRR'].value_counts().iloc[0]
            most_common_level = filtered_df['Calculated_Final_ISRR'].value_counts().index[0]
            st.info(f"{most_common_level}: {most_common} EGIDs ({most_common/len(filtered_df)*100:.1f}%)")
        
        with col2:
            st.write("**Average Data Groups:**")
            avg_trans = filtered_df['Transactional_Groups'].mean()
            avg_non_trans = filtered_df['Non_Transactional_Groups'].mean()
            st.info(f"Transactional: {avg_trans:.2f}\nNon-Transactional: {avg_non_trans:.2f}")
        
        with col3:
            st.write("**Risk Distribution:**")
            critical_high = len(filtered_df[filtered_df['Calculated_Final_ISRR'].isin(['Critical', 'High'])])
            st.info(f"Critical/High: {critical_high} ({critical_high/len(filtered_df)*100:.1f}%)")
    
    # Tab 2: Mismatches
    with tab2:
        st.header("⚠️ ISRR Mismatches Analysis")
        
        if len(mismatches_df) > 0:
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader(f"Total Mismatches: {len(mismatches_df)}")
                
                # Top mismatch patterns
                patterns = mismatches_df['Difference'].value_counts().head(10)
                st.write("**Top Mismatch Patterns:**")
                for pattern, count in patterns.items():
                    st.write(f"• {pattern}: {count} cases")
            
            with col2:
                fig_severity = create_mismatch_severity_chart(mismatches_df)
                if fig_severity:
                    st.plotly_chart(fig_severity, use_container_width=True)
            
            st.subheader("Detailed Mismatch Records")
            
            # Search functionality
            search = st.text_input("🔍 Search EGID in mismatches", "")
            
            if search:
                filtered_mismatches = mismatches_df[mismatches_df['EGID'].astype(str).str.contains(search, case=False)]
            else:
                filtered_mismatches = mismatches_df
            
            st.dataframe(
                filtered_mismatches,
                use_container_width=True,
                height=400
            )
            
            # Download mismatches
            csv = filtered_mismatches.to_csv(index=False)
            st.download_button(
                label="📥 Download Mismatches as CSV",
                data=csv,
                file_name="isrr_mismatches.csv",
                mime="text/csv"
            )
        else:
            st.success("🎉 No mismatches found! All calculated ISRR values match existing values.")
    
    # Tab 3: Flow Analysis
    with tab3:
        st.header("🔄 ISRR Calculation Flow")
        
        fig_sankey = create_sankey_diagram(filtered_df)
        st.plotly_chart(fig_sankey, use_container_width=True)
        
        st.info("This Sankey diagram shows how Interim ISRR values flow to Final ISRR values after applying modifiers.")
        
        # Modifier analysis
        st.subheader("Modifier Application Analysis")
        modifier_counts = filtered_df['Modifier_Applied'].value_counts()
        
        fig_modifiers = go.Figure(data=[go.Bar(
            x=modifier_counts.index,
            y=modifier_counts.values,
            marker_color='rgb(142, 68, 173)',
            text=modifier_counts.values,
            textposition='auto'
        )])
        
        fig_modifiers.update_layout(
            title='Modifiers Applied Distribution',
            xaxis_title='Modifier Type',
            yaxis_title='Number of EGIDs',
            height=400
        )
        
        st.plotly_chart(fig_modifiers, use_container_width=True)
    
    # Tab 4: Data Table
    with tab4:
        st.header("📋 Complete Analysis Data")
        
        # Search functionality
        search_term = st.text_input("🔍 Search in all columns", "")
        
        # Column selection
        all_columns = filtered_df.columns.tolist()
        selected_columns = st.multiselect(
            "Select columns to display",
            options=all_columns,
            default=['EGID', 'Existing_ISRR_Value', 'Calculated_Interim_ISRR', 
                     'Calculated_Final_ISRR', 'ISRR_Match', 'Modifier_Applied']
        )
        
        # Apply search filter
        if search_term:
            mask = filtered_df.astype(str).apply(lambda x: x.str.contains(search_term, case=False)).any(axis=1)
            display_df = filtered_df[mask]
        else:
            display_df = filtered_df
        
        if selected_columns:
            display_df = display_df[selected_columns]
        
        st.dataframe(
            display_df,
            use_container_width=True,
            height=500
        )
        
        st.write(f"Showing {len(display_df)} of {len(filtered_df)} records")
    
    # Tab 5: Export
    with tab5:
        st.header("💾 Export Options")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Download Complete Analysis")
            csv_complete = filtered_df.to_csv(index=False)
            st.download_button(
                label="📥 Download as CSV",
                data=csv_complete,
                file_name="isrr_complete_analysis.csv",
                mime="text/csv"
            )
            
            st.download_button(
                label="📊 Download as Excel",
                data=open(os.path.join('results', config.OUTPUT_FILES['complete_analysis']), 'rb').read(),
                file_name="isrr_complete_analysis.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
        
        with col2:
            st.subheader("Download Mismatches")
            if len(mismatches_df) > 0:
                csv_mismatches = mismatches_df.to_csv(index=False)
                st.download_button(
                    label="📥 Download Mismatches CSV",
                    data=csv_mismatches,
                    file_name="isrr_mismatches.csv",
                    mime="text/csv"
                )
            else:
                st.info("No mismatches to export")
        
        st.subheader("Summary Report")
        summary_text = f"""
        ISRR ANALYSIS SUMMARY REPORT
        =============================
        
        Total EGIDs Processed: {len(results_df):,}
        Match Rate: {match_rate:.1f}%
        Total Mismatches: {len(mismatches_df):,}
        Interim to Final Changes: {changes:,}
        
        ISRR Distribution:
        {results_df['Calculated_Final_ISRR'].value_counts().to_string()}
        
        Generated: {pd.Timestamp.now()}
        """
        
        st.download_button(
            label="📄 Download Summary Report (TXT)",
            data=summary_text,
            file_name="isrr_summary_report.txt",
            mime="text/plain"
        )

if __name__ == "__main__":
    main()
