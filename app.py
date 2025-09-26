import streamlit as st
import json
from sentence_transformers import SentenceTransformer
import numpy as np
from openai import OpenAI
from dotenv import load_dotenv
import os
from pathlib import Path


load_dotenv()

# Use API key
client = OpenAI(api_key= st.secrets.get("OPENAI_API_KEY") or os.getenv("OPENAI_API_KEY"))

# Load highlights
with open("data/highlights.json", "r", encoding="utf-8") as f:
    highlights = json.load(f)  # top 5 articles of each category



########## Create Embeddings ##########
def create_embedding_for_each_articles(highlights):
    
    All_articles_combined = []
    metadata_of_articles_combined=[]
    
    for category, values in highlights.items():
        for i in values:
            Title = i['Title']
            Category = i['Category']
            
            if i['Authors']:
                Authors = i['Authors']
            else:
                Authors = 'N/A'
                
            source = i['News_channel']
            url = i['url']
            summary = i['Summary']
            
            text = "{} {} {} {} {} {}".format(Title, Category, Authors, source, summary, url)
            print(text)
            print('+'*50)
            
            metadata_of_articles_combined.append({**i, 'long_text':text})
            All_articles_combined.append(text)
            
    # print(len(All_articles_combined))
            
    # Create embeddings (downloads the model once on first run)
    embedder = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
    vecs = embedder.encode(All_articles_combined, normalize_embeddings=True).astype(np.float32)
    print(vecs.shape, len(All_articles_combined))
    
    return metadata_of_articles_combined, vecs, embedder



####### Retrive top k closest details as per cosine similarity #######
def retrieve_items(metadata_of_articles_combined, query, vecs, embedder):
    
    query = [query]
    query_vector = embedder.encode(query, normalize_embeddings=True).astype(np.float32)
    print('Its a straight !',query_vector.shape)
    
    # Dot product b/w two vectors
    dot_product = (query_vector @ vecs.T) [0]
    print('dot_product_shape=',dot_product.shape)
    print(dot_product)
    
    # get the indices of the highest values of the dot product vector in descending order
    indices = np.argsort(-dot_product)[:3]
    print('indices = ',indices)
    
    results = []
    for i in indices:
        element = metadata_of_articles_combined[i]
            
        Title = element['Title']
        Category = element['Category']
        Authors = element['Authors']
        source = element['News_channel']
        url = element['url']
        summary = element['Summary']
        
        results.append({'Title':Title,
                        'Category':Category,
                        'Authors':Authors,
                        'source':source,
                        'url':url,
                        'summary':summary
                        })

    return results

####### ChatGPT Response ######
def open_API(top_k_matches, question):
    
    context = []
    print('open_API------')
    for i in top_k_matches:
        # print(i)
        # print()
        text = "- {} {} --> {} {} \n".format(i['Title'], i['source'], i['summary'], i['url'])
        print(text)
        context.append(text)
        
    context_str = ''.join(context)
        
    prompt =  (
            "You are a helpful assistant. Answer the user’s question using ONLY these highlights.\n"
            "If the info is not present, respond only with the exact text: 'No relevant highlights found.'\n\n"
            f"{context_str}\n\n"
            f"Question: {question}\n"
        )
    
    response = client.chat.completions.create(
            model="gpt-4o-mini",  
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
            max_tokens=500
        )
    
    print("open_API------")
    print(prompt)  # <-- Debug: see full prompt sent
    
    return response.choices[0].message.content




metadata_of_articles_combined, vecs, embedder = create_embedding_for_each_articles(highlights)
# print()
# print()
print(vecs)
# for k in metadata_of_articles_combined:
#     for key,_ in k.items():
#         print(key)
#     print()

results = retrieve_items(metadata_of_articles_combined,'AFL News is good ',vecs,embedder)
print(results)
        
############## UI ############
st.title("Daily News Highlights")

# Dropdown to pick category
category = st.selectbox("Choose a category:", list(highlights.keys()))

st.subheader(f"Top 5 articles in {category}")

for article in highlights[category]:
    st.markdown(f"### {article['Title']}")
    st.write(article.get("Summary", "No summary available"))
    st.caption(f"Source: {article['News_channel']} | Score: {article['Total_Score']} | Authors :{article['Authors']}")
    st.markdown(f"[Read more]({article['url']})")
    st.divider()

st.subheader("Chatbot")

user_query = st.text_input("Ask about today’s highlights:")

if user_query:
    with st.spinner('Please Wait .....'):
        top_k_matches = retrieve_items(metadata_of_articles_combined, user_query, vecs, embedder)
        response = open_API(top_k_matches, user_query)
        # print('Response = ',response)
        
    if response.strip()== "No relevant highlights found.":
        st.warning("The highlights don’t contain enough information to answer your question.")
    
    elif response:
        st.markdown(response)

        with st.expander("Closest Sources"):
            for i in top_k_matches:
                st.markdown(f"- **{i['Title']}** ({i['source']}) — [Read more]({i['url']})")
         