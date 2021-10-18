# Letters
A small data science project I just started to work on for fun, analysing the letters between two famous German poets -- J. W. v. Goethe and J. C. F. v. Schiller :).

# Contents
- scrape.py downloads 14 HTML files from Projekt Gutenberg (www.projekt-gutenberg.org) containing ~1000 letters exchanged between between Goethe and Schiller.
- preprocess.py extracts all letter numbers, letter writers and letter contents from the raw HTML files, and writes them to one single CSV file. This will be used for further analysis
- all_letters.csv is this CSV file
- Hypothesis1.ipynb contains some exploratory data analysis on this CSV file. We want to check whether the letters become "more similar" over time, since the two writers might find a "common style." We note that depending on whether word counts are normalised across letters or not, results vary drastically. This needs to be chosen/interpreted linguistically (weighting more common words more strongly vs. weighting all words equally).
