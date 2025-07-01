import pandas as pd
import numpy as np
import random

# Load the original dataset
df = pd.read_csv('Sleep_health_and_lifestyle_dataset.csv')
print(f"Original dataset size: {len(df)} entries")

# Get unique values and distributions from original data
occupations = df['Occupation'].unique()
bmi_categories = df['BMI Category'].unique() 
genders = df['Gender'].unique()
sleep_disorders = df['Sleep Disorder'].unique()
blood_pressures = df['Blood Pressure'].unique()

# Define a function to create new synthetic records
def generate_synthetic_record(person_id):
    gender = np.random.choice(genders, p=[0.5, 0.5])
    
    # Age distribution based on gender (from original dataset patterns)
    if gender == 'Male':
        age = np.random.randint(27, 49)  # Males tend to be younger in the dataset
    else:
        age = np.random.randint(29, 60)  # Females tend to be older
    
    # Select occupation with probabilities based on original distribution
    occupation_counts = df['Occupation'].value_counts(normalize=True)
    occupation = np.random.choice(occupation_counts.index, p=occupation_counts.values)
    
    # Sleep duration, varies by occupation
    if occupation == 'Doctor':
        sleep_duration = round(np.random.normal(7.2, 0.8), 1)
    elif occupation == 'Nurse':
        sleep_duration = round(np.random.normal(7.5, 1.0), 1)
    elif occupation == 'Engineer':
        sleep_duration = round(np.random.normal(8.0, 0.5), 1)
    else:
        sleep_duration = round(np.random.normal(6.8, 0.7), 1)
    
    # Bound sleep duration to reasonable values
    sleep_duration = max(5.5, min(sleep_duration, 9.0))
    
    # Quality of sleep (roughly correlated with sleep duration)
    base_quality = int(sleep_duration) - 1
    quality_of_sleep = np.random.choice([base_quality-1, base_quality, base_quality+1], 
                                        p=[0.2, 0.5, 0.3])
    quality_of_sleep = max(3, min(quality_of_sleep, 9))
    
    # Physical activity level based on occupation
    if occupation in ['Doctor', 'Engineer']:
        physical_activity = np.random.randint(40, 90)
    else:
        physical_activity = np.random.randint(30, 75)
    
    # Stress level (inversely correlated with sleep quality)
    stress_level = np.random.randint(3, 9)
    if quality_of_sleep >= 7:
        stress_level = max(3, stress_level - 2)
    
    # BMI Category (related to activity level)
    if physical_activity > 70:
        bmi_probs = [0.7, 0.2, 0.1]  # More likely Normal
    elif physical_activity > 50:
        bmi_probs = [0.4, 0.5, 0.1]  # More likely Overweight
    else:
        bmi_probs = [0.3, 0.4, 0.3]  # More likely Overweight/Obese
        
    bmi_category = np.random.choice(['Normal', 'Overweight', 'Obese'], p=bmi_probs)
    
    # Blood pressure (related to BMI and stress)
    if bmi_category == 'Normal' and stress_level < 5:
        bp = np.random.choice(['120/80', '115/75', '125/80'])
    elif bmi_category == 'Obese' or stress_level > 6:
        bp = np.random.choice(['140/90', '135/88', '142/92', '140/95'])
    else:
        bp = np.random.choice(['130/85', '128/84', '125/82'])
    
    # Heart rate (related to activity and BMI)
    if physical_activity > 60 and bmi_category == 'Normal':
        heart_rate = np.random.randint(65, 72)
    elif bmi_category == 'Obese':
        heart_rate = np.random.randint(80, 86)
    else:
        heart_rate = np.random.randint(70, 79)
    
    # Daily steps
    if occupation in ['Doctor', 'Nurse']:
        daily_steps = np.random.randint(7000, 10000)
    elif occupation == 'Software Engineer':
        daily_steps = np.random.randint(4000, 6000)
    else:
        daily_steps = np.random.randint(5000, 8000)
    
    # Sleep disorder (related to quality of sleep, BMI, and stress)
    if quality_of_sleep < 6 or (bmi_category == 'Obese' and stress_level > 6):
        sleep_disorder_probs = [0.3, 0.35, 0.35]  # Higher chance of disorder
    elif bmi_category == 'Overweight' and quality_of_sleep < 7:
        sleep_disorder_probs = [0.5, 0.25, 0.25]
    else:
        sleep_disorder_probs = [0.7, 0.15, 0.15]
        
    sleep_disorder = np.random.choice(['None', 'Insomnia', 'Sleep Apnea'], p=sleep_disorder_probs)
    
    return {
        'Person ID': person_id,
        'Gender': gender,
        'Age': age,
        'Occupation': occupation,
        'Sleep Duration': sleep_duration,
        'Quality of Sleep': quality_of_sleep,
        'Physical Activity Level': physical_activity,
        'Stress Level': stress_level,
        'BMI Category': bmi_category,
        'Blood Pressure': bp,
        'Heart Rate': heart_rate,
        'Daily Steps': daily_steps,
        'Sleep Disorder': sleep_disorder
    }

# Generate new records
synthetic_records = []
last_id = df['Person ID'].max()
num_new_records = 800 - len(df)

for i in range(1, num_new_records + 1):
    new_id = last_id + i
    synthetic_records.append(generate_synthetic_record(new_id))

# Create DataFrame of new records
new_df = pd.DataFrame(synthetic_records)

# Combine original and new data
expanded_df = pd.concat([df, new_df], ignore_index=False)

# Save the expanded dataset
expanded_df.to_csv('Sleep_health_and_lifestyle_dataset.csv', index=False)
print(f"Expanded dataset created with {len(expanded_df)} entries")