from nltk.stem import WordNetLemmatizer
import re
from nltk.corpus import stopwords
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
lemaoi = WordNetLemmatizer()

def pre_processing(x):
    x = x.lower()
    x = re.sub('[^a-z0-9 ]','',x)
    result = []
    for i in x.split():
        if i in stopwords.words('english'):
            pass
        else:
            if len(i) <3:
                pass
            else:
                result.append(lemaoi.lemmatize(i))
    res = ' '.join(result)
    res = re.sub('\d{2,}\w+','',res)
    return res

def word_sequence(n_most_words, x, max_len):
    tokeniz = Tokenizer(num_words=n_most_words)
    tokeniz.fit_on_texts(x.values)
    sequen = tokeniz.texts_to_sequences(x.values)
    word_index = tokeniz.word_index
    X = pad_sequences(sequen, maxlen=max_len)
    return X, word_index

