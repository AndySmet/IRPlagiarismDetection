
import csv
import time
import random
from functools import reduce

import math



def isPrime(n):

    if (n <= 1):
        return False
    if (n <= 3):
        return True

    if (n % 2 == 0 or n % 3 == 0):
        return False

    for i in range(5, int(math.sqrt(n) + 1), 6):
        if (n % i == 0 or n % (i + 2) == 0):
            return False

    return True


def nextPrime(N):
    # Base case
    if (N <= 1):
        return 2
    prime = N
    while True:
        prime = prime + 1
        if isPrime(prime):
            return prime






def jaccard(A, B):
    union = set(A).union(set(B))
    intersection = set(A).intersection(set(B))
    return len(intersection)/len(union)

def getShingles(string, n):
    badchars = ",.?!;\n\"'"
    for c in badchars:
        string = string.replace(c,"")
    words = string.lower().split()
    shingles = []

    for i in range(len(words)-n+1):
        shingle = ""
        shingle = reduce(lambda x,y: x+y+" ", words[i:i+n],"")

        shingles.append(shingle[:-1])

    return shingles

def hashArticles(a, b, c, articles):
    result={}
    for article in articles:
        hashValues={}
        for shingle in articles[article]:
            hashValues[shingle]=(a*shingle+b)%c

        result[article]=[min(hashValues, key=hashValues.get)]

    return result

def minhash(articles, numberOfHash):
    m = max(i for v in articles.values() for i in v)
    c = nextPrime(m*2) #lengte van de hash is gekozen als het priemgetal groter dan het hoogste getal dat toegewezen is aan de shingles
    result={}

    for i in range(numberOfHash): #make for each article a column with 'numberOfHash' rows
        random.seed(time.time())
        a = int(random.uniform(1,m**5)%m)
        random.seed(time.time())
        b = int(random.uniform(1,m**5)%m)

        ithMinHash=hashArticles(a, b, c, articles) #Hash function maps the 'numbers/shingles' to a new number from length 'c'
        if i == 0:
            result = ithMinHash
        else:
            for article in ithMinHash:
                result[article] = result[article]+(ithMinHash[article])
    return result

def makeOnesMatrix(n):
    matrix = []
    for i in range(n):
        row=[]
        for j in range(n):
            row.append(1.0)
        matrix.append(row)
    return matrix

def LSH(b, signatures):
    r = int(len(list(signatures.values())[0])/b)
    candidates=[]
    for i in range(b):
        hashBand={}
        for article in signatures:
            band = list(signatures[article][i * r:i * r + r])
            h = hash(tuple(band)) % 1000000
            if h in hashBand:
                hashBand[h].append(article)
            else:
                hashBand[h]=[article]
        c = [signatures for signatures in hashBand.values() if len(signatures) > 1]
        for pairs in c:
            for k in range(len(pairs)-1):
                for l in range(k+1,len(pairs)):
                    if not((pairs[k], pairs[l]) in candidates or (pairs[l], pairs[k]) in candidates):
                        candidates.append((pairs[k], pairs[l]))


    return candidates


if __name__ == '__main__':

    timestart = time.time()
    with open('news_articles_small.csv', mode='r') as infile:
        reader = csv.reader(infile)
        next(reader)
        articles = {rows[0]:rows[1] for rows in reader}



        shinglesDict={}
        articlesDict={}
        for article in articles:
            articlesDict[article]=list()
            shingles = getShingles(articles[article],4)
            for s in shingles:
                if s not in shinglesDict:
                    shinglesDict[s] = len(shinglesDict)
                articlesDict[article].append(shinglesDict[s]) #articlesDict contains the numbers per shingle per article
        articlesDict = minhash(articlesDict, 20)
        candidates = LSH(10, articlesDict)
        print(len(candidates))
        counter=0
        print(articlesDict['311'])
        print(articlesDict['312'])
        for pair in candidates:
            score = jaccard(articlesDict[pair[0]], articlesDict[pair[1]])
            if score > 0.8:
                print(pair[0], pair[1], score)

                counter += 1
        # jaccardMatrix = makeOnesMatrix(len(articlesDict))
        # signatureMatrix = []
        # aIndex = 0
        # counter=0
        # for a in articlesDict:
            # signatureMatrix.append(list(articlesDict[a]))
            # bIndex = 0
            # for b in articlesDict:
            #     if bIndex > aIndex:
            #         score=jaccard(articlesDict[a], articlesDict[b])
            #         if score > 0.8:
            #             print(a,b,score)
            #             counter += 1
                    # jaccardMatrix[aIndex][bIndex] = score
                    # jaccardMatrix[bIndex][aIndex] = score
                # bIndex += 1
            # aIndex += 1
        #
        print(counter)
        print(time.time()-timestart)


