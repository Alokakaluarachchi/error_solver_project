# Error Solver Project

A Flask-based web application that helps solve coding errors by leveraging semantic search through embeddings. The application stores error messages and their solutions, then uses AI-powered similarity search to find relevant solutions for new errors.

## Features

- **Add Error Solutions**: Store error messages along with their solutions in a database
- **Semantic Search**: Find similar errors using AI-powered embeddings and cosine similarity
- **Interactive Web Interface**: User-friendly web UI for adding and searching errors
- **Feedback System**: Validate search results to improve the system
- **Persistent Storage**: SQLite database for error log storage

## Technology Stack

- **Backend**: Flask (Python web framework)
- **Database**: SQLite with NumPy array storage for embeddings
- **AI/ML**: Sentence Transformers (`all-MiniLM-L6-v2`) for generating text embeddings
- **Similarity Search**: scikit-learn cosine similarity
- **Frontend**: HTML/CSS/JavaScript (in `templates/index.html`)

## Installation

1. **Clone the repository** (or navigate to the project directory)

2. **Create a virtual environment** (recommended):
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment**:
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

4. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. **Start the Flask application**:
   ```bash
   python app.py
   ```

2. **Open your web browser** and navigate to:
   ```
   http://localhost:5000
   ```

3. **Add Error Solutions**:
   - Enter an error message in the "Error Text" field
   - Enter the corresponding solution in the "Solution Text" field
   - Click "Add Entry" to save it to the database

4. **Search for Solutions**:
   - Enter an error message you're experiencing
   - Click "Search" to find similar errors and their solutions
   - The system will return the most similar error if the similarity score is above 0.3

5. **Provide Feedback**:
   - After a search, provide feedback on whether the solution was helpful
   - This helps track which solutions are validated by users

## Project Structure

```
error_solver_project/
├── app.py              # Main Flask application with routes
├── db.py               # Database connection and helper functions
├── ai_engine.py        # AI model loading and embedding generation
├── requirements.txt    # Python dependencies
├── templates/
│   └── index.html      # Web interface
└── company_errors.db   # SQLite database (created automatically)
```

## API Endpoints

- `GET /` - Serves the main web interface
- `POST /add` - Add a new error-solution pair
  - Request body: `{"error": "...", "solution": "..."}`
- `POST /search` - Search for similar errors
  - Request body: `{"query": "..."}`
  - Returns: `{"id": int, "solution": "...", "score": float}` or `{"solution": null}`
- `POST /feedback` - Submit feedback on a search result
  - Request body: `{"id": int, "status": "helpful" | "not_helpful"}`

## Database Schema

The `error_logs` table contains:
- `id`: Primary key (auto-increment)
- `error_text`: The error message text
- `solution_text`: The solution text
- `embedding`: BLOB storing the NumPy embedding array
- `user_validated`: Integer flag (0/1) for user validation
- `created_at`: Timestamp of creation

## How It Works

1. **Embedding Generation**: When an error is added, the AI engine generates a vector embedding using the Sentence Transformers model
2. **Storage**: The embedding is stored as a BLOB in SQLite along with the error and solution text
3. **Search**: When searching, the query is converted to an embedding and compared against all stored embeddings using cosine similarity
4. **Results**: The most similar error (if above threshold) is returned with its solution

## Notes

- The AI model (`all-MiniLM-L6-v2`) is loaded once when the application starts, which may take a moment on first run
- The similarity threshold is set to 0.3 - results below this threshold are considered not similar enough
- The database file (`company_errors.db`) is created automatically on first run

## Requirements

- Python 3.7+
- See `requirements.txt` for full dependency list

## License

This project is open source and available for use.
