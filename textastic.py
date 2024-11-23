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
import string
import os
from collections import defaultdict, Counter
from nltk.corpus import stopwords

class Textastic:

    def __init__(self):
        """ Constructor

        datakey
        """

        self.data = defaultdict(dict)
        self.stopwords = set(stopwords.words('english'))

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

        filtered_words = [word for word in words if word not in self.stopwords]

        wordcount = Counter(filtered_words)

        return {
            'wordcount': wordcount,
            'numwords': sum(wordcount.values()),
            'num_companies': len(mission_statements),
        }


    def load_text(self, filename, label=None, parser=None):
        """ Register a document with the framework.
        Extract and store data to be used later by
        the visualization """

        if parser is None:
            results = self.default_parser(filename)
        else:
            results = parser(filename)

        if label is None:
            label = filename

        for k, v in results.items():
            self.data[k][label] = v

    def compare_num_words(self):
        """ This is a very simplistic visualization that creates
        a bar chart comparing number of words (Not intended for
        project)."""

        num_words = self.data['numwords']
        for label, nw in num_words.items():
            plt.bar(label, nw)

        plt.show()