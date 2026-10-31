import csv
import os
import spacy
import torch
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import pickle
from transformers import BertTokenizer, BertModel

# Determine the directory of the current script
CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))
MODEL_FILES_DIR = os.path.join(CURRENT_DIR, 'model_files')

tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
model = BertModel.from_pretrained('bert-base-uncased')

def load_data_from_pickle(filename):
    file_path = os.path.join(MODEL_FILES_DIR, filename)
    with open(file_path, 'rb') as f:
        data = pickle.load(f)
    return data

# Load preprocessed titles and computed embeddings
preprocessed_titles = load_data_from_pickle("preprocessed_titles.pkl")
computed_embeddings = load_data_from_pickle("product_embeddings.pkl")

# Load your e-commerce product dataset
product_data_path = os.path.join(MODEL_FILES_DIR, "scrapdata_productrecord.csv")
product_data = pd.read_csv(product_data_path)


def compute_embeddings(tokens):
    inputs = torch.tensor([tokens])
    with torch.no_grad():
        outputs = model(inputs)
    embeddings = outputs[0][:, 0, :].numpy()  # Extract embeddings for [CLS] token
    return embeddings

def preprocess_title(title):
    tokens = tokenizer.encode(title, add_special_tokens=True)
    return tokens

def recommend_products(query, product_data):
    query_tokens = preprocess_title(query)
    query_embedding = compute_embeddings(query_tokens)

    product_embeddings = np.array(computed_embeddings)

    # Reshape query embedding to 2D array if necessary
    query_embedding = query_embedding.reshape(1, -1)

    # Reshape product embeddings to 2D array if necessary
    product_embeddings = product_embeddings.reshape(product_embeddings.shape[0], -1)

    # Calculate cosine similarity between query embedding and product embeddings
    similarity_scores = cosine_similarity(query_embedding, product_embeddings)

    # Get indices of top recommended products
    top_indices = similarity_scores.argsort(axis=1)[:, ::-1][:, :20]  # Top 20 recommendations

    # Get top recommended product titles
    recommended_products = [product_data['title'][i] for i in top_indices[0]]
    return recommended_products

def filter_and_sort_products(products, product_data):
    filtered_products = product_data[product_data['title'].isin(products)]
    sorted_products = filtered_products.sort_values(by=['rating', 'sold_count', 'review_count'], ascending=False).head(20)
    return sorted_products



# ____________________________________formal search________________________________

nlp = spacy.load("en_core_web_lg")

# Function to search for products
def search_products(query):
    # Get the path to the CSV file
    csv_file_path = os.path.join(os.path.dirname(__file__), 'model_files', 'scrapdata_productrecord.csv')
    
    # Read CSV file and load data
    with open(csv_file_path, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        data = list(reader)
    
#     # Perform entity recognition on the input query
#     doc = nlp(query)
#     product_keywords = [token.text.lower() for token in doc if not token.is_stop and not token.is_punct]

#     # Search for products matching any of the recognized keywords
#     matching_products = []
#     for row in data:
#         title_keywords = row['title'].lower().split()
#         if any(keyword in title_keywords for keyword in product_keywords):
#             matching_products.append({
#                 'title': row['title'],
#                 'rating': row['rating'],
#                 'price': row['price'],
#                 'img_src': row['image_src'],
#                 'addtocart_href': row['addtocart_href']
#             })
#             if len(matching_products) >= 50:
#                 break   
#     return matching_products
    doc = nlp(query)
    product_keywords = [token.text.lower() for token in doc if not token.is_stop and not token.is_punct]

    # Search for products matching any of the recognized keywords
    matching_products = []
    for row in data:
        title_keywords = row['title'].lower().split()
        keyword_matches = sum(keyword in title_keywords for keyword in product_keywords)
        if keyword_matches > 0:
            matching_products.append({
                'title': row['title'],
                'rating': row['rating'],
                'price': row['price'],
                'img_src': row['image_src'],
                'addtocart_href': row['addtocart_href'],
                'keyword_matches': keyword_matches
            })
    
    # Sort matching products based on the number of keyword matches (descending order)
    matching_products.sort(key=lambda x: x['keyword_matches'], reverse=True)
    
    # Return the first 30 matching products or less if there are fewer matching products
    return matching_products[:30]