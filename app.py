from flask import Flask, render_template, request, jsonify
import re
from datetime import datetime

app = Flask(__name__)

# Enhanced knowledge base
knowledge_base = {
    'greetings': {
        'patterns': ['hello', 'hi', 'hey', 'greetings', 'good morning', 'good afternoon', 'good evening'],
        'responses': [
            "Hello! How can I assist you today? 😊",
            "Hi there! What can I help you with?",
            "Hey! Great to see you! How may I help?"
        ]
    },
    'farewells': {
        'patterns': ['bye', 'goodbye', 'see you', 'farewell', 'later'],
        'responses': [
            "Goodbye! Have a wonderful day! 👋",
            "See you later! Feel free to return anytime!",
            "Take care! Come back whenever you need help!"
        ]
    },
    'thanks': {
        'patterns': ['thank', 'thanks', 'appreciate'],
        'responses': [
            "You're welcome! Happy to help! 😊",
            "My pleasure! Anything else I can assist with?"
        ]
    },
    'how_are_you': {
        'patterns': ['how are you', 'how do you do', 'hows it going'],
        'responses': [
            "I'm doing great, thank you for asking! How can I help you today?",
            "I'm functioning perfectly and ready to assist!"
        ]
    },
    'ai': {
        'patterns': ['artificial intelligence', 'machine learning', 'what is ai', 'tell me about ai'],
        'responses': [
            "Artificial Intelligence (AI) is the simulation of human intelligence by machines. It includes:\n\n• Machine Learning - Learning from data\n• Deep Learning - Neural networks\n• NLP - Understanding language\n• Computer Vision - Understanding images\n\nAI powers everything from voice assistants to self-driving cars! 🤖"
        ]
    },
    'nlp': {
        'patterns': ['natural language processing', 'nlp', 'what is nlp'],
        'responses': [
            "Natural Language Processing (NLP) enables computers to understand and generate human language! 💬\n\nKey techniques:\n• Tokenization\n• Named Entity Recognition\n• Sentiment Analysis\n• Text Generation\n\nI use NLP to understand you!"
        ]
    },
    'programming': {
        'patterns': ['programming', 'coding', 'python', 'java', 'javascript'],
        'responses': [
            "Popular Programming Languages:\n\n• Python - Versatile, great for AI/ML\n• Java - Enterprise applications\n• JavaScript - Web development\n• C++ - Performance-critical apps\n\nEach has unique strengths! 💻"
        ]
    },
    'database': {
        'patterns': ['database', 'sql', 'nosql', 'mysql', 'mongodb', 'dbms'],
        'responses': [
            "Databases store and manage data! 🗄️\n\nSQL Databases: MySQL, PostgreSQL, Oracle\nNoSQL Databases: MongoDB, Cassandra, Redis\n\nSQL uses structured tables, NoSQL offers flexibility!"
        ]
    },
    'testing': {
        'patterns': ['testing', 'software testing', 'qa', 'selenium'],
        'responses': [
            "Software Testing ensures quality! ✅\n\nTest Types:\n• Unit Testing\n• Integration Testing\n• System Testing\n• Acceptance Testing\n\nTools: Selenium, JUnit, PyTest, Jest"
        ]
    },
    'cse': {
        'patterns': ['computer science', 'cse', 'computer engineering'],
        'responses': [
            "Computer Science Engineering covers:\n\n• Programming\n• Data Structures & Algorithms\n• Operating Systems\n• Computer Networks\n• Database Management\n• AI/ML\n• Cybersecurity 💻"
        ]
    },
    'math': {
        'patterns': ['mathematics', 'calculus', 'algebra', 'statistics'],
        'responses': [
            "Mathematics Topics:\n\n• Calculus - Derivatives, Integrals\n• Algebra - Equations, Matrices\n• Statistics - Probability, Analysis\n• Geometry - Shapes, Areas\n\nMath is the language of science! 📐"
        ]
    },
    'grammar': {
        'patterns': ['grammar', 'english grammar', 'tenses'],
        'responses': [
            "English Grammar Basics:\n\n• Nouns - Person/place/thing\n• Verbs - Actions\n• Adjectives - Describe nouns\n• Adverbs - Describe verbs\n• 12 Tenses (Present, Past, Future) 📝"
        ]
    },
    'time': {
        'patterns': ['time', 'what time', 'current time'],
        'responses': lambda: f"The current time is {datetime.now().strftime('%I:%M:%S %p')} ⏰"
    },
    'date': {
        'patterns': ['date', 'today', 'what day'],
        'responses': lambda: f"Today is {datetime.now().strftime('%A, %B %d, %Y')} 📅"
    }
}

def find_best_match(user_message):
    """Find the best matching category for user message"""
    lower_msg = user_message.lower()
    best_match = None
    highest_score = 0
    
    for category, data in knowledge_base.items():
        for pattern in data['patterns']:
            if pattern in lower_msg:
                score = len(pattern)
                if score > highest_score:
                    highest_score = score
                    best_match = category
    
    return best_match

def calculate_math(text):
    """Calculate basic math operations"""
    math_match = re.search(r'(\d+\.?\d*)\s*([\+\-\*\/])\s*(\d+\.?\d*)', text)
    if math_match:
        num1 = float(math_match.group(1))
        operator = math_match.group(2)
        num2 = float(math_match.group(3))
        
        operations = {
            '+': num1 + num2,
            '-': num1 - num2,
            '*': num1 * num2,
            '/': num1 / num2 if num2 != 0 else "Cannot divide by zero"
        }
        
        result = operations.get(operator)
        return f"The answer is: {result} 🔢"
    
    return None

def get_bot_response(user_message):
    """Generate bot response based on user message"""
    # Check for math calculation
    math_result = calculate_math(user_message)
    if math_result:
        return math_result
    
    # Find matching category
    category = find_best_match(user_message)
    
    if category and category in knowledge_base:
        responses = knowledge_base[category]['responses']
        
        # Handle callable responses (like time/date)
        if callable(responses):
            return responses()
        
        # Return random response from list
        import random
        return random.choice(responses) if isinstance(responses, list) else responses
    
    return "I'm here to help! I can answer questions about AI/ML, programming, databases, testing, CSE, mathematics, grammar, and more. What would you like to know? 🤔"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/get", methods=["POST"])
def get_response():
    user_input = request.form.get("msg", "")
    if not user_input:
        return jsonify({"response": "Please enter a message!"})
    
    response = get_bot_response(user_input)
    return jsonify({"response": response})

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
