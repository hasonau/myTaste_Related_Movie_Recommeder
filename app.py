import pandas as pd
from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

app = Flask(__name__)
CORS(app)   # ⭐ THIS LINE FIXES FAILED TO FETCH

watched_df = pd.read_csv("watched.csv")
ratings_df = pd.read_csv("ratings.csv")

watched_list = []
for _, row in watched_df.iterrows():
    watched_list.append({
        "name": row["Name"],
        "year": row["Year"],
        "rating": None
    })

for _, row in ratings_df.iterrows():
    for movie in watched_list:
        if movie["name"] == row["Name"]:
            movie["rating"] = row.get("Rating", None)
            break

@app.route("/ping")
def ping():
    return jsonify({"status": "ok"})

@app.route("/recommend", methods=["POST"])
def recommend():
    user_query = request.json.get("message", "")

    watched_names = [m["name"] for m in watched_list[:20]]

    prompt = f"""
    I have already watched these movies:
    {watched_names}

    Recommend 5 NEW movies I might like.
    User preference: {user_query}
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=200
    )

    return jsonify({
        "recommendation": response.choices[0].message.content
    })

if __name__ == "__main__":
    app.run(debug=True)
