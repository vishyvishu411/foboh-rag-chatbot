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


## 📝 Notes

- The scripts should be run **in sequence**:  
  `day_1_scrapping.py → day_2_Preprocessing.py → day_3_Highlights.py → app.py`

- `ignore.py` is optional and only used for word frequency exploration.

- If you don’t have time to run all scripts, you can run **app.py** directly since  
  `data/highlights.json` is already included in the repo.

- Without an OpenAI API key, the app will still work, but the chatbot will return  
  **retrieved highlights only**. With a key, it will generate **natural answers** using GPT.


## ▶️ How to Run
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. run in order:
    ```bash
    python day_1_scrapping.py
    python day_2_Preprocessing.py
    python day_3_Highlights.py
    streamlit run app.py
    ```
