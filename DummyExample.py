from nltk.sentiment.vader import SentimentIntensityAnalyzer

sid = SentimentIntensityAnalyzer()
sentence = "Hello World! I love Georgia Tech!"
sentence2 = "Goodbye World! I HATE Georgia Tech!"
ss1 = sid.polarity_scores(sentence)
ss2 = sid.polarity_scores(sentence2)
print "compound: ", ss1['compound'], " negative: ", ss1['neg'], " positive: ", ss1['pos']
print "compound: ", ss2['compound'], " negative: ", ss2['neg'], " positive: ", ss2['pos']
print "_________________________________________________________________________________"