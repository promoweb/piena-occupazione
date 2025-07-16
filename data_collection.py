"""
Mock Data Generation Module
- Generates synthetic labor market indicators
- Maintains same data structure as original API
"""
import pandas as pd
import numpy as np

# Configuration
MOCK_DATA_RANGES = {
    "unemployment_rate": (7.0, 10.0),
    "youth_unemployment": (25.0, 32.0),
    "long_term_unemployment": (3.0, 5.0),
    "sectoral_employment": (22.0, 26.0)
}

# Dimension mappings
DIMENSION_MAP = {
    "unemployment_rate": {"AGE": "Y_GE15", "REGION": "IT"},
    "youth_unemployment": {"AGE": "Y15-24", "REGION": "IT"},
    "long_term_unemployment": {"REGION": "IT"},
    "sectoral_employment": {"NACE_R2": "TOTAL", "REGION": "IT"}
}

def generate_mock_dataset(indicator, dimensions):
    """Generate synthetic dataset for an indicator"""
    base_value, variation = MOCK_DATA_RANGES[indicator]
    
    # Generate data with slight yearly variation
    data = []
    for year in range(2020, 2025):
        value = round(base_value + (year-2020)*0.5 - np.random.uniform(0.2, 0.8), 1)
        entry = {'TIME_PERIOD': year, 'OBS_VALUE': value, **dimensions}
        data.append(entry)
        
    return pd.DataFrame(data)

if __name__ == "__main__":
    print("Starting mock labor market data generation...")
    
    for key, desc in [
        ("unemployment_rate", "Unemployment rate (15+ years)"),
        ("youth_unemployment", "Youth unemployment (15-24 years)"),
        ("long_term_unemployment", "Long-term unemployment"),
        ("sectoral_employment", "Sectoral employment breakdown")
    ]:
        print(f"Generating {desc} data...")
        try:
            dimensions = DIMENSION_MAP[key]
            df = generate_mock_dataset(key, dimensions)
            
            # Save as CSV
            df.to_csv(f"data/{key}.csv", index=False)
            print(f"Saved mock data (2020-2024) to data/{key}.csv")
            
        except Exception as e:
            print(f"Error generating {desc} data: {str(e)}")
    
    print("Mock data generation complete! CSV files saved to data/ directory")