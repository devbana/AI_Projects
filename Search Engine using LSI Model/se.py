import pandas as pd
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
stop_nltk = stopwords.words("english")
from sklearn.feature_extraction.text import TfidfVectorizer
vectorizer = TfidfVectorizer(max_features=3000)
from sklearn.metrics.pairwise import cosine_similarity


def del_stop(inp_tokens):
    res = [term for term in inp_tokens if term not in stop_nltk]
    return res


def get_top5_query(qry):
    target_vector = vectorizer.transform([qry])
    sim_scores = []
    for ind, vector in enumerate(tfidf_dense):
        sim = cosine_similarity(target_vector, tfidf_dense[ind, :])[0][0]
        sim_scores.append(sim)
    similarity = pd.Series(sim_scores)
    top5_scores = similarity.sort_values(ascending=False).head(5)
    top5_index = top5_scores.index.values
    print("Search query: " + qry + "\n")
    for ind in top5_index:
        print("Similarity score:" + str(round(top5_scores[ind], 2)) + "\n" + "Article text: " + articles_string[ind] + "\n")


inp_docs = pd.read_table("r8-all-terms.txt", sep="\t", names=['label', 'text'])
articles0 = inp_docs.text.values
articles_lower = [art.lower() for art in articles0]
article_tokens = [word_tokenize(art) for art in articles_lower]
articles_nostop = [del_stop(art) for art in article_tokens]
articles_string = [" ".join(art) for art in articles_nostop]
articles_tfidf = vectorizer.fit_transform(articles_string)
tfidf_dense = articles_tfidf.todense()
get_top5_query('computer system')
