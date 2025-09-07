from flask import Flask, render_template, request, jsonify
import pandas as pd
from difflib import SequenceMatcher
import os

app = Flask(__name__)

# Load anime data once at startup
anime_names = []
try:
    # Use the correct processed dataframe
    df = pd.read_csv("artifacts/processed/df.csv")
    anime_names = df['eng_version'].dropna().unique().tolist()
    print(f"Loaded {len(anime_names)} anime names")
        
except Exception as e:
    print(f"Error loading data: {e}")
    anime_names = []

@app.route('/api/suggestions')
def get_suggestions():
    query = request.args.get('q', '').strip().lower()
    if len(query) < 2:
        return jsonify([])
    
    suggestions = []
    
    # Exact matches first
    for name in anime_names:
        if name and query in name.lower():
            suggestions.append(name)
            if len(suggestions) >= 10:  # Limit to 10 for performance
                break
    
    # If no exact matches, use fuzzy matching
    if not suggestions:
        for name in anime_names:
            if name:
                similarity = SequenceMatcher(None, query, name.lower()).ratio()
                if similarity > 0.4:
                    suggestions.append((name, similarity))
        
        # Sort by similarity and take top 10
        suggestions.sort(key=lambda x: x[1], reverse=True)
        suggestions = [name for name, _ in suggestions[:10]]
    
    return jsonify(suggestions[:10])

@app.route('/', methods=['GET','POST'])
def home():
    recommendations = None
    input_value = None
    error_message = None
    
    if request.method == 'POST':
        input_value = request.form.get("query", "").strip()
        try:
            from pipeline.prediction_pipeline import recommend
            recommendations = recommend(input_value)
            if not recommendations:
                error_message = "No recommendations found. Please try a different input."
        except Exception as e:
            print(f"Error occurred: {e}")
            error_message = f"Error: {str(e)}"
            recommendations = []
            
    return render_template('index.html', 
                         recommendations=recommendations, 
                         query=input_value,
                         error_message=error_message)

if __name__=="__main__":
    app.run(debug=True,host='0.0.0.0',port=5000)