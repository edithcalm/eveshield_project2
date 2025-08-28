import gradio as gr
import pandas as pd
import json
import os
from datetime import datetime
from typing import List, Dict
from config import Config
from models.emergency_classifier import EmergencyClassifier
import matplotlib.pyplot as plt
import seaborn as sns

class DashboardService:
    def __init__(self):
        self.classifier = EmergencyClassifier()
        self.emergency_data = []
        self.load_existing_data()
    
    def load_existing_data(self):
        """Load existing emergency data from files"""
        if not os.path.exists(Config.DATA_DIR):
            return
        
        for filename in os.listdir(Config.DATA_DIR):
            if filename.endswith('.json'):
                try:
                    with open(f"{Config.DATA_DIR}/{filename}", 'r') as f:
                        data = json.load(f)
                        self.emergency_data.append(data)
                except Exception as e:
                    print(f"Error loading {filename}: {e}")
    
    def add_emergency_report(self, report_data: Dict):
        """Add new emergency report to dashboard data"""
        report_data['timestamp'] = datetime.now().isoformat()
        self.emergency_data.append(report_data)
    
    def get_dashboard_summary(self) -> str:
        """Get summary statistics for dashboard"""
        if not self.emergency_data:
            return "No emergency reports available."
        
        total_reports = len(self.emergency_data)
        high_severity = len([r for r in self.emergency_data if r.get('severity') == 'HIGH'])
        
        emergency_types = {}
        for report in self.emergency_data:
            etype = report.get('emergency_type', 'unknown')
            emergency_types[etype] = emergency_types.get(etype, 0) + 1
        
        summary = f"""
        ## Emergency Response Dashboard Summary
        
        **Total Reports:** {total_reports}
        **High Severity Cases:** {high_severity}
        **Emergency Types Distribution:**
        """
        
        for etype, count in emergency_types.items():
            summary += f"\n- {etype.title()}: {count}"
        
        return summary
    
    def get_recent_emergencies(self, limit: int = 10) -> pd.DataFrame:
        """Get recent emergency reports as DataFrame"""
        if not self.emergency_data:
            return pd.DataFrame()
        
        recent = sorted(
            self.emergency_data, 
            key=lambda x: x.get('timestamp', ''), 
            reverse=True
        )[:limit]
        
        df_data = []
        for report in recent:
            df_data.append({
                'Time': report.get('timestamp', 'Unknown'),
                'Type': report.get('emergency_type', 'Unknown'),
                'Severity': report.get('severity', 'Unknown'),
                'Location': report.get('location', 'Unknown'),
                'Summary': report.get('summary', 'No summary')[:100] + '...'
            })
        
        return pd.DataFrame(df_data)
    
    def process_new_report(self, audio_text: str) -> Dict:
        """Process new emergency report from audio text"""
        if not audio_text.strip():
            return {"error": "No text provided"}
        
        # Process with ML model
        analysis = self.classifier.process_emergency_report(audio_text)
        
        # Add to dashboard data
        self.add_emergency_report(analysis)
        
        return analysis
    
    def create_visualizations(self):
        """Create visualizations for emergency data"""
        if not self.emergency_data:
            return None, None
        
        # Emergency types pie chart
        emergency_types = {}
        severity_counts = {'HIGH': 0, 'MEDIUM': 0, 'LOW': 0}
        
        for report in self.emergency_data:
            etype = report.get('emergency_type', 'unknown')
            emergency_types[etype] = emergency_types.get(etype, 0) + 1
            
            severity = report.get('severity', 'MEDIUM')
            if severity in severity_counts:
                severity_counts[severity] += 1
        
        # Create plots
        fig1, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
        
        # Emergency types pie chart
        if emergency_types:
            ax1.pie(emergency_types.values(), labels=emergency_types.keys(), autopct='%1.1f%%')
            ax1.set_title('Emergency Types Distribution')
        
        # Severity bar chart
        if any(severity_counts.values()):
            ax2.bar(severity_counts.keys(), severity_counts.values(), 
                   color=['red', 'orange', 'green'])
            ax2.set_title('Severity Distribution')
            ax2.set_ylabel('Count')
        
        plt.tight_layout()
        return fig1

def create_dashboard():
    """Create and launch the Gradio dashboard"""
    dashboard = DashboardService()
    
    with gr.Blocks(title="Emergency Response Dashboard", theme=gr.themes.Soft()) as app:
        gr.Markdown("# 🚨 Emergency Response Dashboard")
        gr.Markdown("Real-time monitoring and analysis of emergency calls with ML-powered insights")
        
        with gr.Row():
            with gr.Column(scale=2):
                # Summary section
                summary_display = gr.Markdown(value=dashboard.get_dashboard_summary())
                
                # Recent emergencies table
                gr.Markdown("## Recent Emergency Reports")
                recent_table = gr.Dataframe(
                    value=dashboard.get_recent_emergencies(),
                    headers=['Time', 'Type', 'Severity', 'Location', 'Summary']
                )
            
            with gr.Column(scale=1):
                # Control panel
                gr.Markdown("## Test Emergency Report")
                test_input = gr.Textbox(
                    label="Simulate Emergency Call Text",
                    placeholder="Enter emergency description in English or Swahili...",
                    lines=3
                )
                process_btn = gr.Button("Process Emergency Report", variant="primary")
                
                # Results display
                gr.Markdown("## Analysis Results")
                result_display = gr.JSON(label="ML Analysis Results")
        
        # Visualizations
        with gr.Row():
            plot_display = gr.Plot(label="Emergency Statistics")
        
        # Auto-refresh functionality
        def refresh_dashboard():
            return (
                dashboard.get_dashboard_summary(),
                dashboard.get_recent_emergencies(),
                dashboard.create_visualizations()
            )
        
        def process_test_report(text):
            result = dashboard.process_new_report(text)
            # Refresh displays
            summary = dashboard.get_dashboard_summary()
            table = dashboard.get_recent_emergencies()
            plot = dashboard.create_visualizations()
            return result, summary, table, plot
        
        # Event handlers
        process_btn.click(
            fn=process_test_report,
            inputs=[test_input],
            outputs=[result_display, summary_display, recent_table, plot_display]
        )
        
        # Auto-refresh every 30 seconds
        app.load(
            fn=refresh_dashboard,
            inputs=[],
            outputs=[summary_display, recent_table, plot_display],
            every=30
        )
    
    return app
