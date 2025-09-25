import pandas as pd
import json
from pathlib import Path

# Make directories
RAW_DIR = Path('data/raw')
PROCESSED_DIR = Path('data/processed')
ARTICLE_WITH_SCORES = Path('data/articles_with_scores')
ARTICLE_WITH_SCORES.mkdir(parents=True, exist_ok=True)

df = pd.read_csv(PROCESSED_DIR/"articles_with_summaries.csv")
print(df.head(3))

Priority_words = ['newsletters','exclusive','update', 'updates','breaking',
                  'media','live','report','urgent']

# Helper function to calculate the priorirty score
def score_calculate(text):
    score=0
    for i in Priority_words:
        if i in text.lower():
            score+=1
    return score
    

# count the no of time each unique title appeared
df['Freq_score'] = df['Title'].map(df['Title'].value_counts())

df['Priority_score'] = df['Title'].apply(score_calculate)

df['Total_Score'] = df['Freq_score'] + df['Priority_score']

highlights = {}
for cat, group in df.groupby('Category'):
    top_values_of_respective_categories = group.sort_values(by='Total_Score',ascending=False).head(5) # Sort by score and take Top 5 highest score articles of each category
    highlights[cat] = top_values_of_respective_categories.to_dict(orient='records')

df["Authors"] = df["Authors"].fillna("N/A")

#Save to csv
df.to_csv(ARTICLE_WITH_SCORES/"article_scores.csv", index=False, encoding="utf-8")

#save to json
with open("data/highlights.json", "w", encoding="utf-8") as f:
    json.dump(highlights, f, indent=2, ensure_ascii=False)

