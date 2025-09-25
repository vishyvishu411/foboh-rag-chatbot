📰 FOBOH News Aggregation & Chatbot

This project scrapes Australian news articles from news sources such SBS,Guardian,ABC, processes them, and provides a Streamlit UI with a chatbot powered by Retrieval-Augmented Generation (RAG). Files:

1. day_1_scrapping.py - Involves Scrapes articles from news sources such as ABC, SBS, Guardian. The final output file is saved as 'data/raw/news_raw.json'/
2. day_2_Preprocessing.py - Removes duplicates, summarizes articles, prepares clean dataset. The final output file is saved as 'data/processed/articles_with_summaries.csv'
3. day_3_Highlights.py - Scores and ranks articles using:
Frequency score → how many times the article is published across sources
Priority score → counts important keywords in the title (e.g. breaking, live, exclusive)
The final output file is saved as 'data/highlights.json'
4. ignore.py - Exploring the important words occuring in the titles of articles from different news sources.
5. app.py - Displays highlights and provides a chatbot where users can ask questions using prompt engineering and RAG.
19,48