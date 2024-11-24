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
        num_words = len(filtered_words)
        num_sentences = len(sentences)
        avg_word_length = sum(len(word) for word in filtered_words) / num_words if num_words else 0
        avg_sentence_length = num_words / num_sentences if num_sentences else 0

        return {
            'wordcount': wordcount,
            'num_words': num_words,
            'num_sentences': num_sentences,
            'avg_word_length': avg_word_length,
            'avg_sentence_length': avg_sentence_length,
        }


    def compare_num_words(self):
        """ This is a very simplistic visualization that creates
        a bar chart comparing number of words (Not intended for
        project)."""

        num_words = self.data['num_words']
        
        plt.bar(num_words.keys(), num_words.values())
        plt.title("Number of Words per Text")
        plt.xlabel("Text")
        plt.ylabel("Number of Words")
        plt.xticks(rotation=45)
        plt.tight_layout()

        plt.show()
    
    def text_to_word_sankey(self, k=10, user_defined_words=None):
        """
        Generate a Sankey diagram linking texts to their k most common words
        or a user-defined set of words.
        """
        wordcounts = self.data['wordcount']
        if not wordcounts:
            print("No word count data available for visualization.")
            return

        flows = []

        for text, wc in wordcounts.items():
            if user_defined_words:
                words = {word: wc[word] for word in user_defined_words if word in wc}
            else:
                words = dict(wc.most_common(k))

            for word, count in words.items():
                flows.append((text, word, count))

        texts = list({text for text, _, _ in flows})
        words = list({word for _, word, _ in flows})
        labels = texts + words
        label_map = {label: i for i, label in enumerate(labels)}

        sources = [label_map[text] for text, _, _ in flows]
        targets = [label_map[word] for _, word, _ in flows]
        weights = [count for _, _, count in flows]

        sankey = Sankey(unit=None)
        for source, target, weight in zip(sources, targets, weights):
            sankey.add(flows=[weight, -weight], labels=[labels[source], labels[target]])
        sankey.finish()
        plt.title("Text-to-Word Sankey Diagram")
        plt.show()