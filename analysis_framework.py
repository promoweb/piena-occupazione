"""
Unemployment Root Cause Analysis Framework
- Implements diagnostic methodologies for:
    - Structural/cyclical/frictional decomposition
    - Sectoral analysis
    - Skills gap assessment
    - Geographic/demographic disparities
"""
import pandas as pd
import numpy as np
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.tsa.filters.hp_filter import hpfilter

def decompose_unemployment(series):
    """
    Decompose unemployment rate into structural and cyclical components
    using Hodrick-Prescott filter for small datasets
    """
    # Convert series to numeric and drop NaNs
    series = pd.Series(series).astype(float).dropna()
    
    # HP filter works well with small datasets (minimum 5 observations)
    if len(series) < 5:
        raise ValueError("HP filter requires at least 5 observations")
    
    cycle, trend = hpfilter(series, lamb=1600)  # Standard lambda for annual data
    return {
        'structural': trend,
        'cyclical': cycle
    }

def analyze_sectoral_shifts(sector_data):
    """Identify declining vs emerging industries"""
    # Convert to numeric and drop non-numeric columns
    sector_data = sector_data.apply(pd.to_numeric, errors='coerce')
    sector_data = sector_data.dropna(axis=1, how='all')
    
    # Calculate growth rates
    growth_rates = sector_data.pct_change(periods=4).mean()
    
    return {
        'declining': growth_rates[growth_rates < 0].index.tolist(),
        'emerging': growth_rates[growth_rates > 0.05].index.tolist()
    }

def calculate_skills_gap(education_data, job_requirements):
    """Quantify mismatch between skills supply and demand"""
    gap = education_data.sub(job_requirements, fill_value=0)
    return gap[gap < 0].abs().sum()

def regional_disparity_index(regional_rates):
    """Calculate geographic inequality metric"""
    return regional_rates.std() / regional_rates.mean()

def demographic_disparity_analysis(data, groups):
    """Compute unemployment disparities across demographic segments"""
    disparities = {}
    for group in groups:
        group_rates = data.groupby(group)['unemployment_rate'].mean()
        disparities[group] = group_rates.max() - group_rates.min()
    return disparities

# Example usage
if __name__ == "__main__":
    print("Unemployment analysis framework loaded")