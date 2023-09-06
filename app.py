from flask import Flask, render_template, request
import requests
import spacy
import config

nlp = spacy.load('en_core_web_sm')

# API endpoint and key
api_key = config.API_KEY

app = Flask(__name__)

def get_verse(book, chapter, verse):
    url = "https://ajith-holy-bible.p.rapidapi.com/GetVerseOfaChapter"
    params = {
        "Book": book,
        "chapter": chapter,
        "Verse": verse
    }
    headers = {
        "X-RapidAPI-Key": api_key,
        "X-RapidAPI-Host": "ajith-holy-bible.p.rapidapi.com"
    }
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        data = response.json()["Verse"]
        return data
    else:
        return None

def get_keywords(text):
    doc = nlp(text)
    keywords = [token.lemma_ for token in doc if not token.is_stop]
    return keywords

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        user_input = request.form['keyword']
        keywords = get_keywords(user_input)
        keyword_str = " ".join(keywords)

        # Get verse
        verse = get_verse("John", "3", "16")
        if verse:
            return render_template('results.html', verse=verse)
        else:
            return render_template('error.html', message="Failed to retrieve Bible verse")

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
