import json
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report
from sentence_transformers import SentenceTransformer, util
from openai import OpenAI
from dotenv import load_dotenv
from pathlib import Path
import os
import streamlit as st

model_embed = SentenceTransformer('all-MiniLM-L6-v2')

load_dotenv()

# Use API key
client = OpenAI(api_key = st.secrets.get("OPENAI_API_KEY") or os.getenv("OPENAI_API_KEY"))


###### Train Model ######
def training_model(df):

    # Create Training and Testing set
    X = df['Title and text of article']
    Y = df['Category']

    X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=42, stratify = Y)

    model = Pipeline([
        ('tfidf', TfidfVectorizer(stop_words='english', max_features=5000)),
        ('clf', LogisticRegression(max_iter=1000, class_weight='balanced'))
    ])

    model.fit(X_train, Y_train)

    y_pred = model.predict(X_test)
    print(classification_report(Y_test, y_pred))

    new_article = "Banks cutting money of employees"
    # print("Predicted category:", model.predict([new_article])[0])
    
    
    
###### Remove De-duplicate articles ######
def deduplicate_articles(df):
    
    texts = df['Title and text of article'].tolist()
    # print(texts[:2])
    vector_embeddings = model_embed.encode(texts,convert_to_tensor=True)
    
    keep_indexes = []
    seen = set()
    
    for i in range(len(texts)):
       if i in seen:
           continue
       
       # Calculate the sim. score of respective article with the rest of the articles
       sim_score= util.cos_sim(vector_embeddings[i], vector_embeddings)[0]
    #    print('dddd',sim_score.shape)
       
       list_of_duplicate_indexes = []
       for j in range(len(texts)):
            if sim_score[j] > 0.8 and j != i:  #80 %
                list_of_duplicate_indexes.append(j)
            
       # keep storing duplicate indexes.
       for j in list_of_duplicate_indexes:
            seen.add(j)
        
       # keep storing non-duplicate indexes
       keep_indexes.append(i)
            
    return df.iloc[keep_indexes].reset_index(drop=True)



def summarize(batch):
    prompt = (
        "You are given several news articles. Summarize each one in 2–3 sentences.\n"
        "Return the summaries in this exact format:\n"
        "Article 1: <summary>\n"
        "Article 2: <summary>\n"
        "...\n"
        "Do NOT add blank lines or extra text. Each article must have exactly one summary line.\n\n"
    )

    
    
    for i in range(len(batch)):
        prompt= prompt + f'Article {i+1}: {batch[i]}\n\n'
        # print(i,'--',batch[i][:20])
        # print(i,'--'*30,prompt)
        
    response = client.chat.completions.create(
            model="gpt-4o-mini",  
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
            max_tokens=800
        )
        
    
    return response.choices[0].message.content.strip()
    
RAW_DIR = Path('data/raw')
PROCESSED_DIR = Path('data/processed')
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
filename = RAW_DIR / "news_raw.json"

# Load the Json File, the keys it has :['Title','Authors','Published','News_channel','category','url','text']
with open(filename,'r', encoding="utf-8") as file:
    articles = json.load(file)
# print('done')

# print(json.dumps(articles[:3], indent=2, ensure_ascii=False))

rows = []

# Create df rows For training
for e in articles:
    
    row = { 'Title and text of article' : e['Title'] + ' ' + e['Text'],
            'Category': e['category']
        }
    rows.append(row)
    
df_training = pd.DataFrame(rows)
print('training_df=',df_training.head(3))

# print(df['Category'].value_counts())

# Train the csv file
training_model(df_training)


#create df for UI
rows = []

# Create df rows
for e in articles:
    
    row = { 
            'Title and text of article' : e['Title'] + ' ' + e['Text'],
            'Title':e['Title'],
            'Category': e['category'],
            'Authors':", ".join(e['Authors']) if e['Authors'] else "N/A",
            'News_channel':e['News_channel'],
            'url': e['url'],
            'Published': e['Published']
            
        }
    rows.append(row)
    
df_UI = pd.DataFrame(rows)
print('training_df=',df_UI.head(3))


#Remove the duplicates
unique_df_without_duplicates = deduplicate_articles(df_UI)
print('shape = ',unique_df_without_duplicates.shape)
print(unique_df_without_duplicates.head(6))


# Create batches for summarizes
batch_size = 5
all_summaries = []
clean_summaries = []
unique_df_without_duplicates = unique_df_without_duplicates[:200].reset_index(drop=True)  # use 200 articles only

for i in range(0, len(unique_df_without_duplicates), batch_size):
    batch_of_articles = unique_df_without_duplicates['Title and text of article'].iloc[i:i+batch_size].tolist()
    summarized_batch = summarize(batch_of_articles)
    all_summaries.append(summarized_batch)
    print(f"✅ Batch {i//batch_size} summarized")
    

# for e in range(len(all_summaries)):
#     print(f'BATCH NO:  {e}',all_summaries[e])

# ---- Parse summaries safely ----
for batch_summary in all_summaries:
    article_in_each_batch = batch_summary.split('\n')
    for i in article_in_each_batch:
        if not i.strip():  # skip blanks
            continue
            
        if ':' in i:
            i = i.split(':', 1)[1].strip()
        
        clean_summaries.append(i)

# print(clean_summaries)
print(len(clean_summaries), "summaries for", len(unique_df_without_duplicates), "articles")


# ---- Add summaries ----
unique_df_without_duplicates['Summary'] = clean_summaries
print(unique_df_without_duplicates[["Title and text of article", "Summary"]].head(5))

# batch_of_articles = unique_df_without_duplicates['Title and text of article'].iloc[0:5].tolist()
# summarized_batch = summarize(batch_of_articles)
# print(summarized_batch)


# Save csv
unique_df_without_duplicates.to_csv(PROCESSED_DIR / "articles_with_summaries.csv", index=False, encoding="utf-8")

