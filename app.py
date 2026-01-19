from flask import Flask, request, jsonify, render_template
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import db
import ai_engine

app = Flask(__name__)

# Initialize Database on Startup
db.init_db()

@app.route('/')
def home():
    # Flask looks for this file in the 'templates' folder automatically
    return render_template('index.html')

@app.route('/add', methods=['POST'])
def add_entry():
    data = request.json
    error_text = data['error']
    solution_text = data['solution']
    
    # 1. Generate Embedding using our AI module
    embedding = ai_engine.get_embedding(error_text)
    
    # 2. Save to SQLite using our DB module
    conn = db.get_db_connection()
    conn.execute('INSERT INTO error_logs (error_text, solution_text, embedding) VALUES (?, ?, ?)',
                 (error_text, solution_text, db.adapt_array(embedding)))
    conn.commit()
    conn.close()
    return jsonify({"status": "success"})

@app.route('/search', methods=['POST'])
def search_error():
    data = request.json
    query_text = data['query']
    
    # 1. Get embedding from AI module
    query_embedding = ai_engine.get_query_embedding(query_text)
    
    # 2. Fetch all data from DB
    conn = db.get_db_connection()
    rows = conn.execute('SELECT id, error_text, solution_text, embedding FROM error_logs').fetchall()
    conn.close()
    
    if not rows:
        return jsonify({"solution": None})

    # 3. Prepare DB embeddings
    db_embeddings = []
    ids = []
    solutions = []
    
    for row in rows:
        ids.append(row['id'])
        solutions.append(row['solution_text'])
        db_embeddings.append(db.convert_array(row['embedding']))
        
    db_embeddings_np = np.array(db_embeddings)
    
    # 4. Calculate Cosine Similarity
    similarities = cosine_similarity(query_embedding, db_embeddings_np)
    
    best_idx = np.argmax(similarities)
    best_score = float(similarities[0][best_idx])
    
    if best_score < 0.3: 
        return jsonify({"solution": "No similar error found in database.", "score": best_score, "id": -1})

    return jsonify({
        "id": ids[best_idx],
        "solution": solutions[best_idx],
        "score": best_score
    })

@app.route('/feedback', methods=['POST'])
def feedback():
    data = request.json
    row_id = data['id']
    status = data['status']
    
    if row_id != -1:
        conn = db.get_db_connection()
        conn.execute('UPDATE error_logs SET user_validated = ? WHERE id = ?', (status, row_id))
        conn.commit()
        conn.close()
        
    return jsonify({"status": "updated"})

if __name__ == '__main__':
    app.run(debug=True, port=5000)