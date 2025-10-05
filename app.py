from flask import Flask, render_template, request, jsonify
import datetime
import random
import urllib.parse
import wikipedia
import requests
import os

app = Flask(__name__)

# Basic personality responses
GREETINGS = [
    "Hey there! How are you doing today?",
    "Hello! Nice to see you again.",
    "Hi! How can I assist you?"
]

HOW_ARE_YOU = [
    "I'm great, thanks for asking! How about you?",
    "Feeling awesome! What about you?",
    "Doing well — ready to help you anytime!"
]

GENERIC_RESPONSES = [
    "That's interesting! Tell me more.",
    "Hmm, I get what you mean.",
    "Can you explain a bit more?",
    "Oh, I see! What do you think about it?"
]

JOKES = [
    "Why did the programmer quit his job? Because he didn’t get arrays.",
    "I told my computer I needed a break — it said ‘No problem, I’ll go to sleep.’",
    "Why do Java developers wear glasses? Because they don’t C#!"
]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/assistant', methods=['POST'])
def assistant():
    data = request.get_json() or {}
    text = (data.get('text') or '').strip().lower()

    if not text:
        return jsonify({'text': "I didn't catch that. Could you say that again?"})

    if any(word in text for word in ['hello', 'hi', 'hey']):
        return jsonify({'text': random.choice(GREETINGS)})

    if 'how are you' in text:
        return jsonify({'text': random.choice(HOW_ARE_YOU)})

    if 'time' in text:
        now = datetime.datetime.now()
        return jsonify({'text': now.strftime("The time is %I:%M %p")})

    if 'date' in text:
        today = datetime.datetime.now()
        return jsonify({'text': today.strftime("Today is %A, %B %d, %Y")})

    if 'joke' in text:
        return jsonify({'text': random.choice(JOKES)})

    if 'play' in text or 'song' in text:
        query = text.replace('play', '').replace('song', '').strip()
        q = urllib.parse.quote_plus(query)
        yt_url = f"https://www.youtube.com/results?search_query={q}"
        return jsonify({'text': f"Here’s something you might enjoy from YouTube: {query}", 'url': yt_url})

    if 'search' in text or 'find' in text:
        query = text.replace('search', '').replace('find', '').strip()
        if query:
            q = urllib.parse.quote_plus(query)
            url = f'https://www.google.com/search?q={q}'
            return jsonify({'text': f"I found some results for '{query}' on Google.", 'url': url})

    if 'who is' in text or 'what is' in text or 'tell me about' in text:
        subject = text.replace('who is', '').replace('what is', '').replace('tell me about', '').strip()
        if subject:
            try:
                summary = wikipedia.summary(subject, sentences=2)
                return jsonify({'text': summary})
            except Exception:
                return jsonify({'text': f"I couldn’t find much about {subject}, but you can check Google.", 'url': f'https://www.google.com/search?q={urllib.parse.quote_plus(subject)}'})

    return jsonify({'text': random.choice(GENERIC_RESPONSES)})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
