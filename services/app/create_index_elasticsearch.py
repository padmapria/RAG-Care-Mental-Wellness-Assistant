import os,re,openai
from dotenv import load_dotenv
import pandas as pd
from elasticsearch import Elasticsearch
from tqdm.auto import tqdm
from sentence_transformers import SentenceTransformer
import numpy as np
import minsearch
from minsearch import Index
import json
import time

# Load environment variables from .env file
load_dotenv()
model = SentenceTransformer("multi-qa-MiniLM-L6-cos-v1")

# Prepare data
def prepare_data():
    df = pd.read_csv('Mental_wellness_data.csv')
    documents = df.to_dict(orient='records')
    return documents

es_client = None  # Initialize it to None or you can leave it undefined.
def connect_to_es():
    global es_client  # Declare es_client as global
    for _ in range(10):  # Retry up to 10 times
        try:
            es_client = Elasticsearch("http://elasticsearch:9200", basic_auth=('elastic', 'DkIedPPSCb'))  # Use service name
            if es_client.ping():
                print("Successfully connected to Elasticsearch")
                return es_client
        except Exception as e:
            print(f"Connection failed, retrying... ({e})")
            time.sleep(10)  # Wait 10 seconds before retrying
    raise Exception("Failed to connect to Elasticsearch after several retries")



index_settings = {
    "settings": {
        "number_of_shards": 1,
        "number_of_replicas": 0
    },
    "mappings": {
        "properties": {
            "answer": {"type": "text"},
            "question": {"type": "text"},
            "question_title": {"type": "text"},
            "therapist_info": {"type": "text"},
            "question_id": {"type": "keyword"},
            "question_title_vector": {
                "type": "dense_vector",
                "dims": 384,
                "index": True,
                "similarity": "cosine"
            },
            "question_vector": {
                "type": "dense_vector",
                "dims": 384,
                "index": True,
                "similarity": "cosine"
            },
            "answer_vector": {
                "type": "dense_vector",
                "dims": 384,
                "index": True,
                "similarity": "cosine"
            },
            "question_answer_vector": {
                "type": "dense_vector",
                "dims": 384,
                "index": True,
                "similarity": "cosine"
            },
        }
    }
}


def create_embeddings_index(es_client,index_name, filtered_documents):
    for doc in tqdm(documents):
        question_title = doc['question_title']
        question = doc['question']
        answer =  doc['answer']
        qa = question_title + '    ' + question + '    ' + answer
        
        doc['question_title_vector'] = model.encode(question_title)
        doc['question_vector'] = model.encode(question)
        doc['answer_vector'] = model.encode(answer)
        doc['question_answer_vector'] = model.encode(qa)

    for doc in tqdm(documents):
        es_client.index(index=index_name, document=doc)
        

# Main entry point for the assistant
if __name__ == '__main__':
    es_client = connect_to_es()

    # Verify the connection before proceeding
    if es_client is None:
        raise Exception("Elasticsearch client not initialized. Exiting.")

    print("Elasticsearch connection is ready, proceed with next step")
   
    ## Read the dataframe and create index in elasticsearch
    documents = prepare_data()


    ## Create index in elasticsearch
    es_client = connect_to_es()
    es_client.info()

    index_name = "mental_wellness_therapist"

    ## Delete index if exists
    es_client.indices.delete(index=index_name, ignore_unavailable=True)
    es_client.indices.create(index=index_name, body=index_settings)
    create_embeddings_index(es_client,index_name, documents)
    print("Elastic search embeddings created")
    
    ## create index in minsearch
    index = Index(
        text_fields=["question_title","question", "answer"],
        keyword_fields=["question_id"]
    )
    index.fit(documents)