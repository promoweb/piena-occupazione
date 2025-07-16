__author__ = "Emilio Petrozzi"

"""
Automated Report Generation for Unemployment Analysis - Authored by Emilio Petrozzi
- Compiles analytical findings into structured Markdown
- Embeds data citations and visualizations
"""
import pandas as pd
import datetime

class ReportGenerator:
    def __init__(self, analysis_results):
        self.results = analysis_results
        self.report = []
        self.timestamp = datetime.datetime.now().strftime("%Y-%m-%d")
        
    def add_header(self, level, text):
        self.report.append(f"{'#' * level} {text}\n")
        
    def add_paragraph(self, text):
        self.report.append(f"{text}\n\n")
        
    def add_table(self, df, caption):
        self.report.append(f"**{caption}**\n\n")
        self.report.append(df.to_markdown(index=False) + "\n\n")
        
    def add_citation(self, indicator, source, dataset_id=None):
        if dataset_id:
            self.report.append(f"*Source: {indicator} ({source}), Dataset ID: {dataset_id}*\n\n")
        else:
            self.report.append(f"*Source: {indicator} ({source})*\n\n")
        
    def generate_report(self):
        # Report structure
        self.add_header(1, f"Unemployment Root Cause Analysis - {self.timestamp}")
        self.add_header(2, "Executive Summary")
        self.add_paragraph(self.results['executive_summary'])
        
        self.add_header(2, "Methodology")
        self.add_paragraph("Analysis based on decomposition techniques and comparative statistics using:")
        if 'validation_report' in self.results:
            validation = self.results['validation_report']
            self.add_paragraph(f"**Time Period Coverage:** {validation['time_period_coverage']}")
            
            # Add data quality metrics section
            self.add_header(3, "Data Quality Metrics")
            # Calculate average missing value percentage properly
            missing_vals = [float(v.strip('%')) for v in validation['missing_values'].values()]
            avg_missing = sum(missing_vals) / len(missing_vals)
            
            self.add_table(pd.DataFrame({
                'Metric': ['Record Count', 'Missing Values', 'Source Authenticity', 'Temporal Coverage Score'],
                'Value': [
                    sum(validation['record_counts'].values()),
                    f"{avg_missing:.1f}% average",
                    f"{len([v for v in validation['source_authenticity'].values() if v=='Verified'])}/{len(validation['source_authenticity'])} verified",
                    validation['temporal_coverage_score']
                ]
            }), "Summary Data Quality Metrics")
            
            # Detailed metrics tables
            self.add_header(4, "Detailed Record Counts")
            self.add_table(pd.DataFrame({
                'Dataset': validation['record_counts'].keys(),
                'Records': validation['record_counts'].values()
            }), "Record Counts by Dataset")
            
            self.add_header(4, "Missing Values")
            self.add_table(pd.DataFrame({
                'Dataset': validation['missing_values'].keys(),
                'Missing %': validation['missing_values'].values()
            }), "Missing Values by Dataset")
            
            self.add_header(4, "Source Verification")
            self.add_table(pd.DataFrame({
                'Dataset': validation['source_authenticity'].keys(),
                'Status': validation['source_authenticity'].values()
            }), "Source Authenticity")
            
            # Data limitations subsection
            self.add_header(3, "Data Limitations")
            self.add_paragraph("Key limitations impacting analysis:")
            self.add_paragraph("- Temporal coverage varies across datasets")
            self.add_paragraph("- Source verification relies on provided metadata")
            self.add_paragraph(f"- Overall data quality score: {validation['temporal_coverage_score']}")
        
        # Structural analysis section
        self.add_header(2, "Structural Factors")
        self.add_paragraph(self.results['structural_analysis']['narrative'])
        self.add_table(self.results['structural_analysis']['trend_table'], "Long-term Unemployment Trends")
        self.add_citation("ISTAT: Rilevazione sulle forze di lavoro", "2024Q2")
        
        # Additional sections would follow the same pattern
        # ...
        
        return "\n".join(self.report)

# Example usage
if __name__ == "__main__":
    sample_results = {
        'executive_summary': "Preliminary analysis indicates significant structural components...",
        'data_sources': [
            {'Indicator': 'Long-term unemployment', 'Source': 'ISTAT'},
            {'Indicator': 'GDP growth', 'Source': 'Eurostat'}
        ],
        'structural_analysis': {
            'narrative': "Structural unemployment shows persistent increase since 2020...",
            'trend_table': pd.DataFrame({
                'Year': [2020, 2021, 2022, 2023],
                'Rate (%)': [5.2, 6.1, 6.8, 7.2]
            })
        }
    }
    
    generator = ReportGenerator(sample_results)
    with open("analysis_report.md", "w") as f:
        f.write(generator.generate_report())
    print("Report generated successfully")