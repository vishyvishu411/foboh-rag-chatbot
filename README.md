# 📰 FOBOH News Aggregation & Chatbot

This project scrapes Australian news articles from news sources such SBS,Guardian,ABC, processes them, and provides a Streamlit UI with a chatbot powered by Retrieval-Augmented Generation (RAG). Files:

1. **day_1_scrapping.py** - Involves Scrapes articles from news sources such as ABC, SBS, Guardian. The final output file is saved as `'data/raw/news_raw.json'/`

2. **day_2_Preprocessing.py** - Removes duplicates, summarizes articles, prepares clean dataset. The final output file is saved as `'data/processed/articles_with_summaries.csv'`

3. **day_3_Highlights.py** - Scores and ranks articles using:
    Frequency score → how many times the article is published across sources
    Priority score → counts important keywords in the title (e.g. breaking, live, exclusive)
    The final output file is saved as `'data/highlights.json'`

4. ignore.py - Exploring the important words occuring in the titles of articles from different news sources.

5. **app.py** - Displays highlights and provides a chatbot where users can ask questions using prompt engineering and RAG.
19,48


## 📝 Notes

- The scripts should be run **in sequence**:  
  `day_1_scrapping.py → day_2_Preprocessing.py → day_3_Highlights.py → app.py`

- `ignore.py` is optional and only used for word frequency exploration.

- If you don’t have time to run all scripts, you can run **app.py** directly since  
  `data/highlights.json` is already included in the repo.

- Without an OpenAI API key, the app will not work as the chatBot generates highlights
  /summaries with the help of prompting. 


## ▶️ How to Run
1. Install virtual Environment

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. run in order:
    ```bash
    python day_1_scrapping.py
    python day_2_Preprocessing.py
    python day_3_Highlights.py
    streamlit run app.py
    ```
4. Add your OpenAI API key in a `.env` file:
   ```
   OPENAI_API_KEY=sk-xxxx
   ```
   Without this, the chatbot will not be able to create meaningful
   highlights.

## FOBOH News Aggregation & Chatbot  
```
├── app.py                   # Streamlit app (UI + chatbot)
├── day_1_scrapping.py       # Scrapes news (raw JSON output)
├── day_2_Preprocessing.py   # Deduplicates + summarizes articles
├── day_3_Highlights.py      # Scores & selects top 5 highlights
├── ignore.py                # Word frequency exploration (optional)
├── README.md                
├── requirements.txt         
├── data/
│   ├── raw/                 # Raw scraped JSON (ignored in Git)
│   ├── processed/           # Summarized CSVs (ignored in Git)
│   ├── articles_with_scores/# Scored CSVs (ignored in Git)
│   └── highlights.json      
└── venv/                    # Virtual environment (ignored in Git)
```
