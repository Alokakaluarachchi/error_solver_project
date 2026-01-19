from sentence_transformers import SentenceTransformer

# Load the model once when this module is imported
print("Loading AI Model (this may take a moment)...")
model = SentenceTransformer('all-MiniLM-L6-v2')
print("Model Loaded.")

def get_embedding(text):
    """Generates an embedding for a single text string."""
    return model.encode(text)

def get_query_embedding(text):
    """Generates a reshaped embedding for searching."""
    return model.encode(text).reshape(1, -1)