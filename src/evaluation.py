import pickle
import ir_datasets
import os
from ir import get_documents_by_similitud_cosine, get_documents_by_bm25, vectorize_query

def precision_recall(query_id, retrieved_docs, dataset_name="sara"):
    """
    Calcula precision y recall para una consulta usando qrels.
    """
    dataset = ir_datasets.load(dataset_name)
    relevantes = set()
    for qrel in dataset.qrels_iter():
        if qrel.query_id == query_id and qrel.relevance > 0:
            relevantes.add(qrel.doc_id)
    if not relevantes:
        return 0.0, 0.0
    recuperados = set(getattr(doc, "doc_id", None) for doc in retrieved_docs)
    recuperados_relevantes = len(relevantes & recuperados)
    precision = recuperados_relevantes / len(recuperados) if recuperados else 0.0
    recall = recuperados_relevantes / len(relevantes)
    return precision, recall

def average_precision(query_id, retrieved_docs, dataset_name="sara"):
    """
    Calcula Average Precision para una consulta.
    """
    dataset = ir_datasets.load(dataset_name)
    relevantes = set()
    for qrel in dataset.qrels_iter():
        if qrel.query_id == query_id and qrel.relevance > 0:
            relevantes.add(qrel.doc_id)
    if not relevantes:
        return 0.0
    hits = 0
    sum_precisions = 0.0
    for i, doc in enumerate(retrieved_docs, 1):
        if getattr(doc, "doc_id", None) in relevantes:
            hits += 1
            sum_precisions += hits / i
    return sum_precisions / len(relevantes) if relevantes else 0.0

def evaluar_sistema(dataset_name="sara", metodo="TF-IDF"):
    """
    Evalúa el sistema en todas las queries del dataset.
    """
    if not os.path.exists("preprocessed.pkl"):
        print("\r⚠️  Primero debes preprocesar el corpus.")
        return
    
    dataset = ir_datasets.load(dataset_name)
    with open("preprocessed.pkl", "rb") as f:
        data = pickle.load(f)
        corpus = data["corpus"]
        vectorizer = data["vectorizer"]
        vectorizer_vector = data["vectorizer_vector"]

    precisiones = []
    recalls = []
    average_precisions = []

    for query in dataset.queries_iter():
        query_text = query.text
        if metodo == "BM25":
            retrieved_docs = get_documents_by_bm25(corpus, query_text)
        else:
            vectorized_query = vectorize_query(query_text, vectorizer)
            retrieved_docs = get_documents_by_similitud_cosine(corpus, vectorizer_vector, vectorized_query)
        p, r = precision_recall(query.query_id, retrieved_docs, dataset_name)
        ap = average_precision(query.query_id, retrieved_docs, dataset_name)
        precisiones.append(p)
        recalls.append(r)
        average_precisions.append(ap)

    mean_precision = sum(precisiones) / len(precisiones) if precisiones else 0.0
    mean_recall = sum(recalls) / len(recalls) if recalls else 0.0
    MAP = sum(average_precisions) / len(average_precisions) if average_precisions else 0.0
    print("\n=== Resultados globales ===")
    print(f"Mean Precision: {mean_precision:.3f}")
    print(f"Mean Recall: {mean_recall:.3f}")
    print(f"MAP: {MAP:.3f}")
