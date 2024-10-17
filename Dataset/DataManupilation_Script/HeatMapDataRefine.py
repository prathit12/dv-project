import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# File paths
procedures_file_path = r'C:\DV\Project\dv-project\Dataset\hospital\procedures_icd.csv'
admissions_file_path = r'C:\DV\Project\dv-project\Dataset\hospital\admissions.csv'
icd_procedures_file_path = r'C:\DV\Project\dv-project\Dataset\hospital\d_icd_procedures.csv' 

# Load data
procedures_df = pd.read_csv(procedures_file_path)
admissions_df = pd.read_csv(admissions_file_path)
icd_procedures_df = pd.read_csv(icd_procedures_file_path)

print(procedures_df.isnull().sum())
print(admissions_df.isnull().sum())
print(icd_procedures_df.isnull().sum())

# Drop missing values if necessary
procedures_df.dropna(subset=['subject_id', 'hadm_id', 'icd_code'], inplace=True)
admissions_df.dropna(subset=['subject_id', 'hadm_id'], inplace=True)


admissions_df['outcome'] = admissions_df['deathtime'].apply(lambda x: 0 if pd.notnull(x) else 1)


merged_df = pd.merge(procedures_df, admissions_df[['subject_id', 'hadm_id', 'outcome']], on=['subject_id', 'hadm_id'])


merged_df = pd.merge(merged_df, icd_procedures_df[['icd_code', 'long_title']], on='icd_code', how='left')


agg_data = merged_df.groupby(['long_title', 'outcome']).size().unstack(fill_value=0)
agg_data_norm = agg_data.div(agg_data.sum(axis=1), axis=0)
agg_data_norm.to_csv('procedure_outcome_aggregation_normalized.csv', index=True)

# Plot heatmap using procedure names
plt.figure(figsize=(12, 8))
sns.heatmap(agg_data_norm, annot=True, fmt=".2f", cmap='coolwarm', cbar_kws={'label': 'Proportion of Outcomes'})
plt.title('Heatmap of Medical Procedures vs Patient Outcomes (Alive vs Dead)')
plt.xlabel('Outcome (1=Alive, 0=Dead)')
plt.ylabel('Procedure Name')  
plt.show()