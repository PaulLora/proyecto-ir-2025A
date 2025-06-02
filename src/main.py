from sklearn.datasets import fetch_20newsgroups
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

STOPWORDS = ['the', 'and', 'to', 'of', 'a', 'in', 'is', 'that', 'it', 'for']

def get_corpus():
    newsgroups = fetch_20newsgroups(subset='all', remove=('headers', 'footers', 'quotes'))
    return newsgroups.data


# def

if __name__ == "__main__":
    corpus = get_corpus()
    vectorizer = CountVectorizer(token_pattern=r'(?u)\b[a-zA-Z]{2,}\b', stop_words=STOPWORDS, lowercase=True)
    vectorizer_vector = vectorizer.fit_transform(corpus)
    query = "zzzzzzt"
    vectorized_query=vectorizer.transform([query])
    # print(vectorizer.get_feature_names_out())

    cosine_similarities = cosine_similarity(vectorized_query, vectorizer_vector).flatten()

    # print(cosine_similarities.argmax())
    # print(cosine_similarities[cosine_similarities.argmax()])

    print(corpus[cosine_similarities.argmax()])


