"""

file: textastic.py

Description: A reusable library for text analysis and comparison
In theory, the framework should support any collection
of texts of interest (though this might require the implementation
of some custom parsers.)

Possible sources for mini-project

- gutenburg texts
- political speech
- tweet compilations
- corporate filines
- philosophy treatises
- letters, journals, diaries
- blogs
- news articles

The core data structure:

Input: "A" --> raw text, "B" --> another text

Extract wordcounts:
         "A" --> wordcounts_A, "B" --> wordcounts_B, .....

What gets stored:

        "wordcounts" ---> {"A" --> wordcount_A,
                           "B" --> wordcounts_B, etc.}

        e.g., dict[wordcounts][A] --> wordcounts_A

"""

from collections import defaultdict, Counter
import random as rnd
import matplotlib.pyplot as plt
import os
import re
import string
from nltk.corpus import stopwords
from wordcloud import WordCloud
import pandas as pd
from sankey import show_sankey
import seaborn as sns

class Textastic:

    def __init__(self):
        """ Constructor

        datakey
        """
        self.data = defaultdict(dict)
        self.stopwords = set()
        self.text_files = []

    def load_text(self, filename, label=None, parser=None):
        """ Register a document with the framework.
        Extract and store data to be used later by
        the visualization """

        if not os.path.isfile(filename):
            print(f"Error: File {filename} not found.")
            return

        if parser is None:
            results = self.default_parser(filename)
        else:
            results = parser(self, filename)

        if label is None:
            label = filename

        for k, v in results.items():
            self.data[k][label] = v
        
        self.text_files.append(label)
        
    def load_stop_words(self, stopfile):
        """Load stopwords from a file or NLTK's list."""
        if stopfile.lower() == "nltk":
            self.stopwords = set(stopwords.words('english'))
        else:
            with open(stopfile, 'r', encoding='utf-8') as file:
                self.stopwords = set(file.read().splitlines())

    
    def default_parser(self, filename):
        """
        Parse a standard text file and extract word count,
        number of words, sentences, and other statistics.
        """

        try:
            with open(filename, 'r', encoding='utf-8') as file:
                text = file.read()
        except FileNotFoundError:
            print(f"Error: File {filename} not found.")
            return {}
        except Exception as e:
            print(f"Error reading file {filename}: {e}")
            return {}

        size = len(self.text_files)
        # Clean text
        cleaned_text = text.translate(str.maketrans('', '', string.punctuation)).lower()
        words = cleaned_text.split()

        # Remove stopwords if they are loaded
        filtered_words = [word for word in words if word not in self.stopwords]

        # Word and sentence counts
        wordcount = Counter(filtered_words)
        num_words = len(filtered_words)

        # Results dictionary
        results = {
            'wordcount': wordcount,
            'numwords': num_words,
            'num_elements': size
        }

        return results

    
    def wordcount_sankey(self, word_list=None, k=5):
        """
        Generate a Sankey diagram linking texts to their k most common words
        or a user-defined set of words.
        """

        wordcounts = self.data['wordcount']
        if not wordcounts:
            print("No word count data available.")
            return

        # Prepare data for Sankey diagram
        rows = []
        for text_label, wc in wordcounts.items():
            if word_list:
                selected_words = {word: wc[word] for word in word_list if word in wc}
            else:
                selected_words = dict(wc.most_common(k))

            for word, count in selected_words.items():
                rows.append({"src": text_label, "targ": word, "vals": count})

        # Convert rows to DataFrame
        df = pd.DataFrame(rows)

        if df.empty:
            print("No data to visualize in the Sankey diagram.")
            return

        # Use the Plotly wrapper to generate the Sankey diagram
        show_sankey(df, src='src', targ='targ', vals='vals', width=1000, height=600)
    
    def wordcloud_subplots(self, cols=2):
        """Generate a subplot of word clouds, one for each text."""
        wordcounts = self.data['wordcount']
        num_files = len(wordcounts)
        rows = (num_files + cols - 1) // cols

        fig, axes = plt.subplots(rows, cols, figsize=(cols * 3, rows * 3))
        axes = axes.flatten()

        for i, (label, wc) in enumerate(wordcounts.items()):
            wordcloud = WordCloud(width=400, height=300, background_color="white").generate_from_frequencies(wc)
            axes[i].imshow(wordcloud, interpolation="bilinear")
            axes[i].set_title(label)
            axes[i].axis('off')

        for j in range(i + 1, len(axes)):
            axes[j].axis('off')

        plt.tight_layout()
        plt.show()
    
    def heatmap_word_frequencies(self, words):
        """
        Generate a heatmap of word frequencies across industries.
        """
        labels = list(self.data['wordcount'].keys())
        wordcounts = self.data['wordcount']

        # Prepare data
        heatmap_data = {word: [wordcounts[label].get(word, 0) for label in labels] for word in words}
        heatmap_df = pd.DataFrame(heatmap_data, index=labels)

        # Plot heatmap
        plt.figure(figsize=(10, 6))
        sns.heatmap(heatmap_df, annot=True, cmap="YlGnBu", fmt="d", linewidths=0.5)
        plt.title("Word Frequencies Across Industries")
        plt.xlabel("Words")
        plt.ylabel("Industries")
        plt.show()