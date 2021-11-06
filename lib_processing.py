from sklearn.feature_extraction.text import CountVectorizer
import sklearn.metrics.pairwise

def cosinesim(X):
    ''' Compute cosine similarity matrix on the individual letters (i.e. bag-of-words vectors in X) '''
    cosinesim = sklearn.metrics.pairwise.cosine_similarity(X)
    return cosinesim


def bag_of_words(df, n_gram_n = 1, min_word_length = 3, normalise_counts = False, binary = False):
    ''' Fit a bag of words model with n_gram_n-grams, consisting of min_word_length+ letters only. '''
    # normalise_counts: Norm word counts across the letters?
    # binary: Binary presence-absence data instead of frequencies?

    # Model fitting
    token_pattern = "[a-zA-Z]{" + str(min_word_length) + ",100000}"
    model = CountVectorizer(ngram_range=(n_gram_n,n_gram_n), token_pattern=token_pattern, binary=binary)
    X = model.fit_transform(df.Content)
    X = X.toarray()
    feature_names = model.get_feature_names()

    # Norming words if desired
    if normalise_counts:
        X = (X - X.mean(axis=0)) / X.std(axis=0)

    return feature_names, X
