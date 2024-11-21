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

class Textastic:

    def __init__(self):
        """ Constructor

        datakey
        """

        self.data = defaultdict(dict)

    def default_parser(self, filename):
        """ Parse a standard text file and produce
        extract data results in the form of a dictionary. """

        results = {
            'wordcount': Counter("To be or not to be".split(" ")),
            'numwords': rnd.randrange(10,50)
        }

        return results


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