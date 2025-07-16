__author__ = "Emilio Petrozzi"

"""
Unemployment Analysis Workflow Driver - Authored by Emilio Petrozzi
- Orchestrates data collection, analysis, and reporting
"""
import pandas as pd
import os
from analysis_framework import (
    decompose_unemployment,
    analyze_sectoral_shifts,
    calculate_skills_gap,
    regional_disparity_index,
    demographic_disparity_analysis
)
from report_generator import ReportGenerator

def main():
    print("Starting unemployment root cause analysis...")
    print("Note: Ensure data collection has been run to generate CSV files in data/ directory")
    
    # Phase 1: Enhanced data validation
    print("\n=== ENHANCED DATA VALIDATION ===")
    try:
        # Load labor market indicators from CSV files
        unemployment_rate = pd.read_csv("data/unemployment_rate.csv")
        youth_unemployment = pd.read_csv("data/youth_unemployment.csv")
        long_term_unemployment = pd.read_csv("data/long_term_unemployment.csv")
        sectoral_employment = pd.read_csv("data/sectoral_employment.csv")
        
        # Validate data coverage (last 5 years)
        current_year = pd.Timestamp.now().year
        min_year = current_year - 5
        datasets = {
            "Unemployment rate": unemployment_rate,
            "Youth unemployment": youth_unemployment,
            "Long-term unemployment": long_term_unemployment,
            "Sectoral employment": sectoral_employment
        }
        
        validation_report = {
            'time_period_coverage': f"{min_year}-{current_year}",
            'record_counts': {},
            'missing_values': {},
            'source_authenticity': {},
            'temporal_coverage_score': 0
        }
        
        total_score = 0
        for name, df in datasets.items():
            # Temporal coverage
            if df['TIME_PERIOD'].min() > min_year:
                raise ValueError(f"{name} data doesn't cover last 5 years")
                
            # Record count
            validation_report['record_counts'][name.lower().replace(" ", "_")] = len(df)
            
            # Missing value percentage
            missing_pct = df['OBS_VALUE'].isna().mean() * 100
            validation_report['missing_values'][name] = f"{missing_pct:.1f}%"
            
            # Source authenticity (placeholder)
            validation_report['source_authenticity'][name] = "Verified" if "ISTAT" in name else "External"
            
            # Temporal coverage score (1 point per year covered)
            years_covered = df['TIME_PERIOD'].nunique()
            coverage_score = min(5, years_covered) / 5 * 100
            total_score += coverage_score
            
        # Calculate average temporal coverage score
        validation_report['temporal_coverage_score'] = f"{total_score / len(datasets):.1f}%"
        print("Enhanced validation complete - all checks passed")
        
    except Exception as e:
        print(f"Enhanced data validation failed: {str(e)}")
        return
    
    # Phase 2: Analytical processing
    print("\n=== ANALYTICAL PROCESSING ===")
    decomposition = decompose_unemployment(unemployment_rate['OBS_VALUE'])
    sector_shifts = analyze_sectoral_shifts(sectoral_employment)
    regional_disparity = regional_disparity_index(unemployment_rate.groupby('REGION')['OBS_VALUE'].mean())
    
    # Phase 3: Report compilation and validation
    print("\n=== REPORT GENERATION ===")
    analysis_results = {
        'executive_summary': "ISTAT data analysis reveals key unemployment drivers...",
        'structural_analysis': {
            'narrative': f"Structural unemployment accounts for {decomposition['structural'].mean():.1f}% of total unemployment",
            'trend_table': pd.DataFrame({
                'Component': ['Structural', 'Cyclical'],
                'Contribution (%)': [
                    decomposition['structural'].mean(),
                    decomposition['cyclical'].mean()
                ]
            })
        },
        'sectoral_analysis': {
            'declining_industries': sector_shifts['declining'],
            'emerging_industries': sector_shifts['emerging']
        },
        'regional_disparity_index': regional_disparity,
        'validation_report': validation_report
    }
    
    generator = ReportGenerator(analysis_results)
    report_path = "unemployment_root_cause_analysis.md"
    with open(report_path, "w") as f:
        f.write(generator.generate_report())
    
    print(f"Analysis complete! Report saved as {report_path}")
    print("Validation report included in analysis results")

if __name__ == "__main__":
    main()