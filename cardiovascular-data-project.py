import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Reading csv data
df = pd.read_csv('CVD_cleaned.csv')

# Set up subplots using gridspec for precise layout
fig, axes = plt.subplots(nrows=2, ncols=2, figsize=(14, 12))

# Create subplots using the gridspec object
ax1 = axes[0, 0]
ax2 = axes[0, 1]
ax3 = axes[1, 0]
ax4 = axes[1, 1]

# Calculating smoking history frequency by general health:
smoking_health_relation = df.groupby('General_Health')['Smoking_History'].value_counts().unstack().fillna(0)
smoking_health_relation.plot(kind='bar', ax=ax1, rot=0)
ax1.set_title('General Health by Smoking History')
ax1.set_ylabel('Count')
ax1.legend(title='Smoking History')

# Calculating heart disease frequency by age category
age_disease_relation = df.groupby('Age_Category')['Heart_Disease'].value_counts().unstack().fillna(0)
age_disease_relation.plot(kind='bar', ax=ax2, rot=0)
ax2.set_title('Relation between Age and Heart Disease')
ax2.set_ylabel('Count')
ax2.legend(title='Heart Disease')

# Selecting top 10 alcohol consumption values
top_alcohol_values = df['Alcohol_Consumption'].value_counts().head(10).index
filtered_df = df[df['Alcohol_Consumption'].isin(top_alcohol_values)]

# Creating count plot for alcohol consumption and general health:
sns.countplot(data=filtered_df, x='Alcohol_Consumption', hue='General_Health', ax=ax3)
ax3.set_title('Relationship between Alcohol Consumption and General Health (Top 10 values)')
ax3.set_xlabel('Alcohol Consumption')
ax3.set_ylabel('Count')
ax3.legend(title='General Health')

# Calculating cancer percentages by general health
cancer_by_health = df.groupby('General_Health')[['Skin_Cancer', 'Other_Cancer']].apply(lambda x: (x == 'Yes').mean()).reset_index()
cancer_by_health.columns = ['General_Health', 'Skin_Cancer_Percentage', 'Other_Cancer_Percentage']

# Reshaping DataFrame
cancer_by_health = pd.melt(cancer_by_health, id_vars='General_Health', var_name='Cancer_Type', value_name='Percentage')

# Creating grouped bar chart for cancer occurrence and general health
sns.barplot(data=cancer_by_health, x='General_Health', y='Percentage', hue='Cancer_Type', ax=ax4)
ax4.set_title('Relationship between General Health and Cancer Occurrence')
ax4.set_xlabel('General Health')
ax4.set_ylabel('Percentage (%)')
ax4.legend(title='Cancer Type')

# Adjust spacing and remove empty space automatically
plt.tight_layout()

current_directory = os.getcwd()

# Save the figure in the same folder as the script
plt.savefig(os.path.join(current_directory, 'cardiovascular-info.png'))

plt.show()
