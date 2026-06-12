import os
import pandas as pd
import numpy as np

# Set random seed for reproducibility
np.random.seed(42)

# Define Indian states and their relative weight factors (based on size/GDP/population)
states_metadata = {
    'Maharashtra': {'weight': 1.8, 'base_conviction': 38.5},
    'Uttar Pradesh': {'weight': 2.0, 'base_conviction': 55.2},
    'Karnataka': {'weight': 1.4, 'base_conviction': 42.0},
    'Tamil Nadu': {'weight': 1.5, 'base_conviction': 48.1},
    'Delhi': {'weight': 1.2, 'base_conviction': 32.4},
    'Gujarat': {'weight': 1.3, 'base_conviction': 40.5},
    'Rajasthan': {'weight': 1.2, 'base_conviction': 28.9},
    'West Bengal': {'weight': 1.1, 'base_conviction': 22.4},
    'Andhra Pradesh': {'weight': 1.0, 'base_conviction': 35.1},
    'Telangana': {'weight': 0.9, 'base_conviction': 37.0},
    'Bihar': {'weight': 1.3, 'base_conviction': 25.6},
    'Madhya Pradesh': {'weight': 1.1, 'base_conviction': 45.3},
    'Kerala': {'weight': 0.6, 'base_conviction': 58.0},
    'Punjab': {'weight': 0.7, 'base_conviction': 34.2},
    'Haryana': {'weight': 0.8, 'base_conviction': 30.1},
    'Odisha': {'weight': 0.7, 'base_conviction': 36.8},
    'Assam': {'weight': 0.6, 'base_conviction': 20.2}
}

years = list(range(2019, 2026))
data = []

for state, meta in states_metadata.items():
    weight = meta['weight']
    base_conviction = meta['base_conviction']
    
    for year in years:
        # Define year-on-year growth trends (especially high growth for cyber fraud)
        year_idx = year - 2019
        growth_factor = 1.0 + (year_idx * 0.05)  # General 5% YoY increase in reports
        cyber_growth_factor = (1.25) ** year_idx   # 25% exponential growth YoY for cyber fraud
        
        # Base values randomized around weight
        corruption_cases = int(np.random.normal(250 * weight, 50) * growth_factor)
        corruption_cases = max(10, corruption_cases)
        
        cheating_fraud_cases = int(np.random.normal(5000 * weight, 800) * growth_factor)
        cheating_fraud_cases = max(100, cheating_fraud_cases)
        
        forgery_cases = int(np.random.normal(800 * weight, 150) * growth_factor)
        forgery_cases = max(20, forgery_cases)
        
        # Cyber financial fraud (exponential trend)
        cyber_fraud_cases = int(np.random.normal(400 * weight, 80) * cyber_growth_factor)
        cyber_fraud_cases = max(10, cyber_fraud_cases)
        
        # Value lost in Crores INR (correlated with cases but highly variable due to outlier scams)
        base_value = (corruption_cases * 0.5 + cheating_fraud_cases * 0.3 + cyber_fraud_cases * 0.15)
        value_loss = round(base_value * np.random.uniform(0.7, 1.5), 2)
        
        # Conviction rates have a slight downward trend over time due to court backlogs
        conviction_rate = round(max(5.0, min(95.0, base_conviction + np.random.normal(-1.0 * year_idx, 2.0))), 2)
        
        data.append({
            'State': state,
            'Year': year,
            'Corruption_Cases': corruption_cases,
            'Cheating_Fraud_Cases': cheating_fraud_cases,
            'Forgery_Cases': forgery_cases,
            'Cyber_Fraud_Cases': cyber_fraud_cases,
            'Total_Economic_Offences': corruption_cases + cheating_fraud_cases + forgery_cases + cyber_fraud_cases,
            'Financial_Loss_Crores_INR': value_loss,
            'Conviction_Rate_Pct': conviction_rate
        })

df = pd.DataFrame(data)

# Ensure the output directories exist
os.makedirs('C:/Users/Likith.N/.gemini/antigravity/scratch/financial-corruption-app/data/processed', exist_ok=True)
output_path = 'C:/Users/Likith.N/.gemini/antigravity/scratch/financial-corruption-app/data/processed/india_corruption_state_wise.csv'
df.to_csv(output_path, index=False)

print(f"Successfully generated dataset with {len(df)} records and saved to {output_path}")
