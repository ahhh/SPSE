#!/usr/bin/env python
#Naive Bayes Classifier for phishing

from __future__ import division
from itertools import groupby
from collections import Counter

texts = [('phish', ['malicious', 'update', 'download', 'phishing', 'email']),
        ('phish', ['run', 'click', 'install', 'FREE', '!!!']),
        ('phish', ['wire', 'transfer', 'urgent', 'money']),
		('safe', ['results', 'repository', 'online']),
        ('safe', ['conference', 'online', 'registration', 'conference']),
        ('safe', ['conference', 'results', 'repository'])]

#Compute the prob table for classes
classFreq = Counter(map(lambda (cls, t): cls, texts))

pt = {}
for cls in classFreq.keys():
    pt[cls] = classFreq[cls] / sum(classFreq.values())

classes = pt.keys()
dictionary = sorted(list(set([w for cls, words in texts for w in words])))

#Compute the Common Probability Table (CPT)

#Group texts by classes
textsGroupedByCls = groupby(sorted(texts, key = lambda tpl: tpl[0]), lambda tpl: tpl[0])

#Conditional probability distribution
cpd = {}

#For each class compute the probability distribution
for cls, listOfTexts in textsGroupedByCls:
    cpd[cls] = {}

    #Count the frequency of each word
    wordFreq = Counter([w for cls, ts in listOfTexts for w in ts])

    print cls, wordFreq
    totalCount = sum(wordFreq.values())

    #For each word in the dictionary, calcualte the relative frequency (with smoothing)
    for w in dictionary:
        cpd[cls][w] = (wordFreq[w] + 1) / (totalCount + len(dictionary))
        #cpd[cls][w] = "%d + 1 / (%d + %d)" %(wordFreq[w], totalCount, len (dictionary))
print cpd

#Tabular display of probability distributions
for cls, table in cpd.items():
    print cls
    words = sorted(table.keys())
    print ' '.join(words)

    print ' & '.join(map(lambda w: "%.4f" %table[w], words))

    print


#Calc the posterior probability of the training samples (aka the probability these are phish based on old phish)
def posterior(texts, cpd, pt):
    result = []
    for t in texts:
        probs = {}
        total = 0
        for cls in classes:
            probs[cls] = reduce(lambda acc, word: acc * cpd[cls][word], t, pt[cls])
            total += probs[cls]
        #Normalization
        for cls in classes:
            probs[cls] /= total
        result.append(probs)
    return result

pos =  posterior(map(lambda (cls, t): t, texts), cpd, pt)

print 'safe \t phish'
for t in pos:
    print ' & '.join(map(lambda n: '%.3f' % n, t.values()))

#Some classification task
testText = [['FREE', 'online', 'install', '!!!'], ['registration', 'click', 'conference', 'online']]

print posterior(testText, cpd, pt)
