from flask import Flask, request, jsonify
from openai import OpenAI
import os

# Initialize OpenAI client
client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

# You can predefine your watched list here or read CSVs if small
watched_list = [
    {"name": "Inception", "year": 2010, "rating": 9},
    {"name": "The Dark Knight", "year": 2008, "rating": 9},
    {"name": "Interstellar", "year": 2014, "rating": 8},
]

# Serverless handler for Vercel
def handler(request):
    try:
        data = request.get_json() or {}
        user_query = data.get("message", "")

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
        recommendation = response.choices[0].message.content

        return jsonify({"recommendation": recommendation})
    except Exception as e:
        return jsonify({"error": str(e)})
