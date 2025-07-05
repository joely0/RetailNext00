"""
search_similar_items.py
Contains functions for generating embeddings using OpenAI (text-embedding-3-large) and retrieving top-matching items
based on cosine similarity. Forms the retrieval layer in the GPT-4o mini + RAG pipeline.
"""

# Standard library imports
from typing import List

# 3P Imports
import numpy as np
from openai import OpenAI
from tenacity import retry, wait_random_exponential, stop_after_attempt

# Local application imports
from config import EMBEDDING_MODEL, OPENAI_API_KEY

# Initialize OpenAI client
if OPENAI_API_KEY:
    client = OpenAI(api_key=OPENAI_API_KEY)
else:
    client = None

# Simple function to take in a list of text objects and return them as a list of embeddings

@retry(wait=wait_random_exponential(min=1, max=40), stop=stop_after_attempt(10))

def get_embeddings(input: List):
    if not client:
        return None
        
    response = client.embeddings.create(
        input=input,
        model=EMBEDDING_MODEL
    ).data
    return [data.embedding for data in response]


# Includes matching algorithm. Math - cosine similarity function]

def cosine_similarity_manual(vec1, vec2):
    """
    Calculate the cosine similarity between two vectors.
    """
    vec1 = np.array(vec1, dtype=float)
    vec2 = np.array(vec2, dtype=float)


    dot_product = np.dot(vec1, vec2)
    norm_vec1 = np.linalg.norm(vec1)
    norm_vec2 = np.linalg.norm(vec2)
    return dot_product / (norm_vec1 * norm_vec2)


def find_similar_items(input_embedding, embeddings, threshold=0.5, top_k=2):
    """
    Find the most similar items based on cosine similarity.
    """
    
    # Calculate cosine similarity between the input embedding and all other embeddings
    similarities = [(index, cosine_similarity_manual(input_embedding, vec)) for index, vec in enumerate(embeddings)]
    
    # Filter out any similarities below the threshold
    filtered_similarities = [(index, sim) for index, sim in similarities if sim >= threshold]
    
    # Sort the filtered similarities by similarity score
    sorted_indices = sorted(filtered_similarities, key=lambda x: x[1], reverse=True)[:top_k]

    # Return the top-k most similar items
    return sorted_indices


def find_matching_items_with_rag(df_items, item_descs):
    """
    Take the input item descriptions and find the most similar items based on cosine similarity for each description.
    """

    # Select the embeddings from the DataFrame
    embeddings = df_items['embeddings'].tolist()

    similar_items = []
    for desc in item_descs:
        # Generate the embedding for the input item
        input_embedding = get_embeddings([desc])
        
        if input_embedding is None:
            continue

        # Find the most similar items based on cosine similarity
        similar_indices = find_similar_items(input_embedding, embeddings, threshold=0.6)
    
        similar_items += [df_items.iloc[i].to_dict() for i in similar_indices]
    return similar_items