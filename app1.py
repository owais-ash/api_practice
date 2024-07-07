from flask import Flask, request, render_template, jsonify
from spellchecker import SpellChecker
import spacy
import requests

# Load spaCy English model
nlp = spacy.load("en_core_web_sm")

# Fallback list of profanity words if the URL is not reachable
FALLBACK_PROFANITY_LIST = set([
    "fuck", "shit", "damn", "hell"  # Add more profanity words here
])

# URL to fetch the list of profanity words
PROFANITY_URL = "https://www.cs.cmu.edu/~biglou/resources/bad-words.txt"

app = Flask(__name__)

spell = SpellChecker()

class TextAnalysisError(Exception):
    """Custom exception class for text analysis errors."""
    pass

class TextAnalyzer:
    def __init__(self, text, profanity_list):
        self.text = text
        self.profanity_list = profanity_list

    def check_spelling(self):
        words = self.text.split()
        misspelled = spell.unknown(words)
        return list(misspelled)

    def find_profanity(self):
        words = self.text.split()
        profane_words = [word for word in words if word.lower() in self.profanity_list]
        return profane_words

    def extract_nouns(self):
        doc = nlp(self.text)
        nouns = [token.text for token in doc if token.pos_ == "NOUN"]
        return sorted(nouns, key=len)

    def analyze(self):
        try:
            misspelled_words = self.check_spelling()
            profane_words = self.find_profanity()
            nouns = self.extract_nouns()

            result = {
                "IncorrectSpellings": misspelled_words,
                "ProfanityWords": profane_words,
                "NounsInAscendingOrderOfLength": nouns
            }

            return result
        except Exception as e:
            raise TextAnalysisError(f"An error occurred during text analysis: {e}")

def fetch_profanity_list(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return set(response.text.splitlines())
    except requests.RequestException as e:
        # Use fallback list if the URL is not reachable
        return FALLBACK_PROFANITY_LIST

@app.route('/')
def upload_form():
    return render_template('input.html')

@app.route('/analyze_text', methods=['POST'])
def analyze_text():
    try:
        text = request.form['text']
        if not text:
            raise TextAnalysisError("No text provided")

        profanity_list = fetch_profanity_list(PROFANITY_URL)
        analyzer = TextAnalyzer(text, profanity_list)
        result = analyzer.analyze()
        return render_template('output.html', result=result)
    except TextAnalysisError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": f"An unexpected error occurred: {e}"}), 500

if __name__ == '__main__':
    app.run(debug=True)
