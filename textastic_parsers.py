import json
from collections import Counter
import string

def custom_parser(self, filename):
        """
        Custom parser for handling text-based JSON files.
        Extracts mission statements, computes word counts.
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
        
        # Number of companies per file
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

        num_words = len(words)

        return {
            'wordcount': wordcount,
            'num_words': num_words,
            'num_elements': size
        }