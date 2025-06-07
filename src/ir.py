import ir_datasets
from nltk import SnowballStemmer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity


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


def get_most_accurate_doc(corpus: list, vectorizer_vector, vectorized_query) -> str:
    cosine_similarities = cosine_similarity(vectorized_query, vectorizer_vector).flatten()
    return corpus[cosine_similarities.argmax()].text

if __name__ == "__main__":
    corpus = get_corpus()

    processed_corpus = preprocess_corpus(corpus)
    vectorizer = get_count_vectorizer()

    vectorizer_vector = vectorizer.fit_transform(processed_corpus)

    query = "speakers"

    vectorized_query = vectorize_query(query, vectorizer)

    print(get_most_accurate_doc(corpus, vectorizer_vector, vectorized_query))
