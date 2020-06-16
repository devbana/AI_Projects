from nltk.corpus import stopwords

STOPWORDS = set(stopwords.words('english'))

INSUREDNAME_PATTERN = [{'POS': 'PROPN'}, {'POS': 'PROPN'}]

BROKERNAME_PATTERN = [{'POS': 'PROPN'}]
