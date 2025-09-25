# 📰 FOBOH News Aggregation & Chatbot

This project scrapes Australian news articles from news sources such SBS,Guardian,ABC, processes them, and provides a Streamlit UI with a chatbot powered by Retrieval-Augmented Generation (RAG). Files:

1. **day_1_scrapping.py - Involves Scrapes articles from news sources such as ABC, SBS, Guardian. The final output file is saved as 'data/raw/news_raw.json'/

2. **day_2_Preprocessing.py - Removes duplicates, summarizes articles, prepares clean dataset. The final output file is saved as 'data/processed/articles_with_summaries.csv'

3. **day_3_Highlights.py - Scores and ranks articles using:
    Frequency score → how many times the article is published across sources
    Priority score → counts important keywords in the title (e.g. breaking, live, exclusive)
    The final output file is saved as 'data/highlights.json'

4. ignore.py - Exploring the important words occuring in the titles of articles from different news sources.

5. app.py - Displays highlights and provides a chatbot where users can ask questions using prompt engineering and RAG.
19,48

Note: These .py files should be run setrial wise as they utilize the generated JSON/CSV file from the previous .py file. You can ignore the ignore.py file. If the time does'nt allow you to run all these files, you can directly run **app.py** as it uses **highlight.json** directly file which i have uploaded here on git.

## ▶️ How to Run
1. Install dependencies:
   ```bash
   pip install -r requirements.txt

2. run in order:
python day_1_scrapping.py
python day_2_Preprocessing.py
python day_3_Highlights.py
streamlit run app.py
