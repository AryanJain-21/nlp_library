import json
from collections import Counter
import re
import string

def custom_parser(self, filename):
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