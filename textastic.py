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
import json
import re
import string
import os
from collections import defaultdict, Counter
from nltk.corpus import stopwords
from matplotlib.sankey import Sankey
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
            results = parser(filename)

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
        Default parser for handling text-based JSON files.
        Extracts mission statements and computes word counts.
        """
        try:
            with open(filename, 'r', encoding='utf-8') as file:
                content = json.load(file)
        except FileNotFoundError:
            print(f"Error: File {filename} not found.")
            return {}
        except json.JSONDecodeError:
            print(f"Error: File {filename} is not a valid JSON file.")
            return {}
        
        # Size of file

        size = content.get("num_companies", 0)

        # Extract mission statements
        mission_statements = [entry["mission_statement"] for entry in content.get("companies", [])]
        if not mission_statements:
            print(f"Warning: No mission statements found in {filename}.")
            return {}

        full_text = " ".join(mission_statements)

        # Process text
        cleaned_text = full_text.translate(str.maketrans('', '', string.punctuation)).lower()
        words = cleaned_text.split()

        self.load_stop_words('nltk')

        filtered_words = [word for word in words if word not in self.stopwords]

        wordcount = Counter(filtered_words)

        sentences = re.split(r'[.!?]+', full_text)
        sentences = [sentence.strip() for sentence in sentences if sentence.strip()]

        # Statistics
        num_words = len(words)
        num_sentences = len(sentences)
        avg_word_length = sum(len(word) for word in words) / num_words if num_words else 0
        avg_sentence_length = num_words / num_sentences if num_sentences else 0

        return {
            'wordcount': wordcount,
            'num_words': num_words,
            'num_sentences': num_sentences,
            'avg_word_length': avg_word_length,
            'avg_sentence_length': avg_sentence_length,
            'num_elements': size
        }


    def compare_num_words(self):
        """ This is a very simplistic visualization that creates
        a bar chart comparing number of words (Not intended for
        project)."""

        num_words_normalized = [
            num_words / size
            for num_words, size in zip(self.data['num_words'].values(), self.data['num_elements'].values())
        ]
        
        plt.bar(self.data['num_words'].keys(), num_words_normalized)
        plt.title("Number of Words per Text")
        plt.xlabel("Text")
        plt.ylabel("Number of Words")
        plt.xticks(rotation=45)
        plt.tight_layout()

        plt.show()
    
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

        fig, axes = plt.subplots(rows, cols, figsize=(cols * 5, rows * 5))
        axes = axes.flatten()

        for i, (label, wc) in enumerate(wordcounts.items()):
            wordcloud = WordCloud(width=200, height=150, background_color="white").generate_from_frequencies(wc)
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