from dataclasses import asdict

import ir_datasets
import numpy as np
from nltk import SnowballStemmer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pickle
import os
from rank_bm25 import BM25Okapi

STOPWORDS = ['the', 'and', 'to', 'of', 'a', 'in', 'is', 'that', 'it', 'for']

def get_corpus() -> list:
    """"
    Obtiene el corpus usando la API de ir_datasets.
    """
    return list(ir_datasets.load("sara").docs_iter())

def stem_doc(document: str) -> list:
    """
    Aplica stemming a un documento dado y retorna una lista de palabras despues de aplicar stemming

    :param document: Documento.
    """
    return list(SnowballStemmer("english").stem(word) for word in document.split())

def preprocess_corpus(corpus: list) -> list:
    docs = []
    for doc in corpus:
        docs.append(", ".join(str(word) for word in stem_doc(doc.text)))
    return docs

def get_count_vectorizer() -> CountVectorizer:
    """
    Create una instancia de CountVectorizer. Funciona como un preprocesamiento ya que
    removera caracteres que no sean palabras y numeros. Tambien usa una lista de
    stopwords que seran removidas del corpus.
    """
    return CountVectorizer(token_pattern=r'(?u)\b[a-zA-Z]{2,}\b', stop_words=STOPWORDS)

def vectorize_query(query: str, vectorizer: CountVectorizer):
    return vectorizer.transform([query])

def get_documents_by_similitud_cosine (corpus: list, vectorizer_vector, vectorized_query) -> list:
    cosine_similarities = cosine_similarity(vectorized_query, vectorizer_vector).flatten()
    top_5_indexes = np.argsort(cosine_similarities)[-5:][::-1]
    documents = []
    for index in top_5_indexes:
        documents.append(corpus[index])
    return documents

def get_documents_by_bm25(corpus: list, query: str) -> list:
    """
    Recupera los documentos más relevantes usando BM25.
    :param corpus: Lista de documentos (objetos con atributo .text).
    :param query: Consulta de búsqueda (string).
    :return: Lista de documentos relevantes.
    """
    # Preprocesar los textos del corpus
    tokenized_corpus = [doc.text.lower().split() for doc in corpus]
    bm25 = BM25Okapi(tokenized_corpus)
    tokenized_query = query.lower().split()
    scores = bm25.get_scores(tokenized_query)
    top_k_indexes = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)[:5]
    documents = []
    for index in top_k_indexes:
        documents.append(corpus[index])
    return documents


def preprocess():
    """
    Preprocesa el corpus y lo vectoriza.

    :param corpus: Corpus a preprocesar.
    :return: Lista de documentos preprocesados.
    """
    if os.path.exists("preprocessed.pkl"):
        print("\r⚠️  El corpus ya ha sido preprocesado. Si quieres volver a preprocesarlo, elimina el archivo 'preprocessed.pkl'.")
        return
    
    corpus = get_corpus()
    processed_corpus = preprocess_corpus(corpus)
    vectorizer = get_count_vectorizer()
    vectorizer_vector = vectorizer.fit_transform(processed_corpus)
    # Guardar todo en un archivo
    with open("preprocessed.pkl", "wb") as f:
        pickle.dump({
            "corpus": corpus,
            "vectorizer": vectorizer,
            "vectorizer_vector": vectorizer_vector
        }, f)

def documents_presentation(docs: list) -> None:
    print()
    print("\r✅ Top 5 documentos: ")
    for index, doc in enumerate(docs):
        print("***************************************************")
        print(f"------------------- Documento {index} -------------------")
        print(doc.text)

def seeker(query: str, method: str = "TF-IDF"):
    """
    Busca un documento en el corpus que sea mas relevante a la consulta.

    :param query: Consulta de busqueda.
    :return: Documento mas relevante.
    """
    if not os.path.exists("preprocessed.pkl"):
        print("\r⚠️  Primero debes preprocesar el corpus.")
        return
    
    with open("preprocessed.pkl", "rb") as f:
        data = pickle.load(f)
        corpus = data["corpus"]
        vectorizer = data["vectorizer"]
        vectorizer_vector = data["vectorizer_vector"]

    if method == "BM25":
        documents = get_documents_by_bm25(corpus, query)
    else:
        vectorized_query = vectorize_query(query, vectorizer)
        documents = get_documents_by_similitud_cosine(corpus, vectorizer_vector, vectorized_query)
    documents_presentation(documents)