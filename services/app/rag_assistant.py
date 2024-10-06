#app/rag_assistant.py
import os,re,openai
from dotenv import load_dotenv
import pandas as pd
from elasticsearch import Elasticsearch
from tqdm.auto import tqdm
from sentence_transformers import SentenceTransformer
import numpy as np
import minsearch
from minsearch import Index
import json, time, logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger("assistant")  # Custom logger name for the Flask app

# Load environment variables from .env file
load_dotenv(dotenv_path=".env")
load_dotenv(dotenv_path=".env.dbdetails")

model = SentenceTransformer("multi-qa-MiniLM-L6-cos-v1")
index_name = "mental_wellness_therapist"

# Prepare data
def prepare_data():
    print('preparing_data');
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


def elastic_search_knn(field, vector):
    es_client = connect_to_es()
    knn = {
        "field": field,
        "query_vector": vector,
        "k": 5,
        "num_candidates": 10000
    }
    
    search_query = {
    "knn": knn,
    "_source": ["answer","question", "question_title", "therapist_info", "question_id"]
    }
    
    es_results = es_client.search(
        index=index_name,
        body=search_query
    )
    
    result_docs = []
    
    for hit in es_results['hits']['hits']:
        result_docs.append(hit['_source'])
    return result_docs

def question_answer_vector_knn(question):
    v_q = model.encode(question)
    return elastic_search_knn('question_answer_vector', v_q)


def elastic_search_knn_combined(vector):
    es_client = connect_to_es()
    search_query = {
        "size": 5,
        "query": {
            "bool": {
                "must": [
                    {
                        "script_score": {
                            "query": {
                                "match_all": {}  # No specific term, matching all documents
                            },
                            "script": {
                                "source": """
                                    cosineSimilarity(params.query_vector, 'question_title_vector') + 
                                    cosineSimilarity(params.query_vector, 'question_vector') + 
                                    cosineSimilarity(params.query_vector, 'answer_vector') + 
                                    cosineSimilarity(params.query_vector, 'question_answer_vector') + 
                                    1
                                """,
                                "params": {
                                    "query_vector": vector
                                }
                            }
                        }
                    }
                ]
            }
        },
        "_source": ["answer", "question", "question_title", "therapist_info", "question_id"] 
    }

    es_results = es_client.search(
        index=index_name,
        body=search_query
    )
    
    result_docs = []
    
    for hit in es_results['hits']['hits']:
        result_docs.append(hit['_source'])

    return result_docs

def question_answer_vector_knn_combined(question):
    v_q = model.encode(question)
    return elastic_search_knn_combined(v_q)
    
################################
#####LLM related#
#############################
index = Index(
        text_fields=["question_title","question", "answer"],
        keyword_fields=["question_id"]
    )
def minsearch_search(q, boost):
    if boost is None:
        boost = {}
        
    results = index.search(
        query = q,
        filter_dict = {},
        boost_dict = boost,
        num_results = 5
    )
    return results


def build_prompt(query, search_results):
    prompt_template = """
    You're a therapist AI assistant focusing on responding to depression related user queries.
    Use only the facts from the CONTEXT when answering the QUESTION.

    QUESTION: {question}

    CONTEXT:
    {context}
    """.strip()

    context = ""
    #print(search_results)
    for doc in search_results:
        context += f"""
        Question Title: {doc['question_title']}
        Question: {doc['question']}
        Answer: {doc['answer']}
        Therapist : {doc['therapist_info']}
        """ 

    prompt = prompt_template.format(question=query, context=context).strip()
    return prompt
    
def openai_4o(prompt):
    """
    Send the prompt to OpenAI and get the model's response. This uses detailed context
    to improve the quality of the AI's answer.
    """
    response = openai.chat.completions.create(
        model='gpt-4o-mini',
        messages=[{"role": "user", "content": prompt}]
    )
    
    return response.choices[0].message.content


def openai_3_5(prompt):
    """
    Send the prompt to OpenAI and get the model's response. This uses detailed context
    to improve the quality of the AI's answer.
    """
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content
    
    
def rag(query, retrieval_search_function_name=minsearch_search, llm_name=openai_3_5,boost = {}):
    if(retrieval_search_function_name==minsearch_search):
        search_results = retrieval_search_function_name(query,boost)
    else:
        #For elasticsearch
        search_results = retrieval_search_function_name(query)
    prompt = build_prompt(query, search_results)
    answer = llm_name(prompt)
    return answer
    
Evaluation_template_answer_answer = """
You are an expert evaluator for a Retrieval-Augmented Generation (RAG) system.
Your task is to analyze the relevance of the generated answer compared to the original answer provided.
Based on the relevance and similarity of the generated answer to the original answer, you will classify
it as "NON_RELEVANT", "PARTLY_RELEVANT", or "RELEVANT".

Here is the data for evaluation:

Original Answer: {true_answer}
Generated Question: {question}
Generated Answer: {answer_llm}

Please analyze the content and context of the generated answer in relation to the original
answer and provide your evaluation in parsable JSON without using code blocks:

{{
  "Relevance": "NON_RELEVANT" | "PARTLY_RELEVANT" | "RELEVANT",
  "Explanation": "[Provide a brief explanation for your evaluation]"
}}
""".strip()


Evaluation_template_quest_answer = """
You are an expert evaluator for a Retrieval-Augmented Generation (RAG) system.
Your task is to analyze the relevance of the generated answer to the given question.
Based on the relevance of the generated answer, you will classify it
as "NON_RELEVANT", "PARTLY_RELEVANT", or "RELEVANT".

Here is the data for evaluation:

Question: {question}
Generated Answer: {answer_llm}

Please analyze the content and context of the generated answer in relation to the question
and provide your evaluation in parsable JSON without using code blocks:

{{
  "Relevance": "NON_RELEVANT" | "PARTLY_RELEVANT" | "RELEVANT",
  "Explanation": "[Provide a brief explanation for your evaluation]"
}}
""".strip()

QUERY_REWRITE_TEMPLATE = """
You are an expert query rewriter. Your task is to simplify and rephrase the given query 
to make it concise and clear.

Here is the original query:

{query}

Rewrite the query to minimize ambiguity and maximize clarity, 
while preserving its original intent.


Return the rewritten query.
"""

## Answer Genration and Evaluation with OpenAI for a single text query passeed
def extract_llm_response_relevance_score(org_query):
    ## Generate answer
    prompt = QUERY_REWRITE_TEMPLATE.format(query=org_query)
    query = openai_3_5(prompt)
    
    print("Passed query *** :",org_query)
    print("Rewritten query *** :",query)
    print("###########")
    answer_llm = rag(query,question_answer_vector_knn, openai_3_5)
    print(answer_llm)
    print("********")
    
    ## Evaluate the relevance of generated answer
    prompt = Evaluation_template_quest_answer.format(question=query, answer_llm=answer_llm)
    response_relevance_llm = openai_4o(prompt)
    print(response_relevance_llm)
    print("********")
    
    ## Cleanup and format the response from LLM
    cleaned_temp = response_relevance_llm.replace('```', '').replace('\n', '').replace('json', '').rstrip(',').strip()
    data = json.loads(cleaned_temp)
    relevance = data.get("Relevance")
    relevance_expl =data.get("Explanation")
    
    return query,answer_llm,relevance,relevance_expl


    
    