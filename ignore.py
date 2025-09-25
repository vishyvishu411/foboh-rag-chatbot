import pandas as pd
from collections import Counter
import re
from pathlib import Path
import json

RAW_DIR = Path('data/raw')
PROCESSED_DIR = Path('data/processed')

# Load your CSV
df = pd.read_csv(PROCESSED_DIR/f"articles_with_summaries.csv")  # replace with your file

# Combine all titles (or you can use 'Title and text of article')
all_text = " ".join(df["Title and text of article"].astype(str))

# Clean text → remove punctuation, lowercase
words = re.findall(r"\b\w+\b", all_text.lower())

# Count frequency
word_counts = Counter(words)

# Get 20 most common words
for e in word_counts.most_common(400):
    print(e)
    if e[0]=='man':
        print(e)
        print()
    