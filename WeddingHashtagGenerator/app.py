# pip install torch transformers flask
# from transformers import pipeline
from flask import Flask, render_template, request, jsonify
import random

app = Flask(__name__)

# Load Open-Source AI Model
# generator = pipeline("text2text-generation", model="google/flan-t5-small")
# def generate_hashtags(name1):
#     """Generates synonyms"""
#     prompt = f"List exactly 10 synonyms for {name1}. Return them in a single line, separated by commas"
#     response = generator(prompt, max_length=50, num_return_sequences=1)
#     hashtags = response[0]["generated_text"].split("\n")
    
#     return hashtags


# Popular wedding suffixes
WEDDING_SUFFIXES = [
    "Weds", "BigDay", "Forever", "TieTheKnot", "SayIDo", "HappilyEverAfter", 
    "LoveStory", "TheWedding", "Hitched", "DownTheAisle", "OnCloud9", "ToHaveAndToHold",
    "DreamWedding", "CheersTo", "MarriedLife", "HappilyMarried", "Officially"
]

# Catchy modifiers
CATCHY_PHRASES = [
    "Lovestruck", "MatchMadeInHeaven", "BetterTogether", "Twinning", "PerfectPair",
    "CoupleGoals", "Soulmates", "Destined", "HeartToHeart", "MadlyInLove", "PartnersInCrime"
]

def smart_blend(name1, name2):
    """Dynamically blends names for aesthetic appeal."""
    name1, name2 = name1.capitalize(), name2.capitalize()
    blends = [
        name1[:3] + name2[:3],
        name1 + name2,  
        name1[0] + "&" + name2[0],
    ]
    
    return random.choice(blends)  # Pick a random blend from the list

def generate_hashtags(name1, name2, nickname1=None, nickname2=None):
    """Generates a list of wedding hashtags using first names and nicknames."""
    name_blends=[]
    for _ in range(2):
        name_blends.append(smart_blend(name1, name2))
    
    # Combine name blends with wedding suffixes & catchy phrases
    hashtags = {f"#{b}{random.choice(WEDDING_SUFFIXES)}" for b in name_blends}
    hashtags.update({f"#{b}{random.choice(CATCHY_PHRASES)}" for b in name_blends })
   

    # Generate nickname-based hashtags
    if nickname1 and nickname2:
        hashtags.add(f"#{nickname1}And{nickname2}Forever")
        hashtags.add(f"#{nickname1}{nickname2}InLove")
    
    return list(hashtags)


@app.route('/')
def home():
    return render_template("index.html")

@app.route('/generate', methods=['POST'])
def generate():
    data = request.get_json()
    name1 = data.get("name1")
    name2 = data.get("name2")
    
    hashtags = generate_hashtags(name1, name2)
    return jsonify({"hashtags": random.sample(hashtags,2)})

if __name__ == '__main__':
    app.run(debug=True)


