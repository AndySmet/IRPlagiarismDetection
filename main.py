
import csv
import time
import random
from functools import reduce

import math



def isPrime(n):

    if(n<=1):
        return False


    for i in range(2, int(math.sqrt(n) + 1), 6):
        if (n % i == 0 or n % (i + 2) == 0):
            return False

    return True


def nextPrime(N):
    # calculate next prime for
    if (N <= 1):
        return 2
    prime = N
    while True:
        prime = prime + 1
        if isPrime(prime):
            return prime






#calculate the jacard index (lists and sets are allowed)
def jaccard(A, B):
    union = set(A).union(set(B))
    intersection = set(A).intersection(set(B))
    return len(intersection)/len(union)

#get shingles from a string
def getShingles(string, n):
    #filter these chars first and make the string lower cases
    badchars = ",.?!;\n\"'"
    for c in badchars:
        string = string.replace(c,"")
    words = string.lower().split()
    shingles = []

    for i in range(len(words)-n+1):
        shingle = reduce(lambda x,y: x+y+" ", words[i:i+n],"")

        shingles.append(shingle[:-1])

    return shingles

#apply the hashfunction to all articles and return the minimal hash value
def hashArticles(a, b, c, articles):
    result={}
    for article in articles:
        hashValues={}
        for shingle in articles[article]:
            hashValues[shingle]=(a*shingle+b)%c

        result[article]=[min(hashValues, key=hashValues.get)]

    return result

#compute the k minhashes so u get the signatures of all articles
def minhash(articles, numberOfHash):
    m = max(i for v in articles.values() for i in v)
    c = nextPrime(m*2) #lengte van de hash is gekozen als het priemgetal groter dan het hoogste getal dat toegewezen is aan de shingles
    result={}

    for i in range(numberOfHash): #make for each article a column with 'numberOfHash' rows
        a = int(random.uniform(1,m**5)%m)
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

#calculate the candidates based on the lsh algorithm
def LSH(b, signatures):
    # calculate the bandwith
    r = int(len(list(signatures.values())[0])/b)
    candidates=[]
    #iterate over the bands, hash the band and if there is a band with 2 articles add these as a pair to the candidates
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
    #initialize parameters
    LSH_Bands=20
    minHashingHashes=60
    shingleLength=4
    similarityThreshold=0.8
    filename='news_articles_small.csv'
    minHashEnabled=True
    LSHEnabled=True



    #start time for program
    timestart = time.time()
    #read from file
    with open(filename, mode='r') as infile:
        reader = csv.reader(infile)
        next(reader)
        articles = {rows[0]:rows[1] for rows in reader}



        shinglesDict={}
        articlesDict={}
        # transform all words in to shingles of chosen length, shingles are then mapped on to integers
        for article in articles:
            articlesDict[article]=list()
            shingles = getShingles(articles[article],shingleLength)
            for s in shingles:
                if s not in shinglesDict:
                    shinglesDict[s] = len(shinglesDict)
                articlesDict[article].append(shinglesDict[s]) #articlesDict contains the numbers per shingle per article
        #perform minhashing and lsh to get candidates
        counter = 0

        if minHashEnabled:
            articlesDict = minhash(articlesDict, minHashingHashes)
        if LSHEnabled:
            candidates = LSH(LSH_Bands, articlesDict)
            # for the candidates check if their jaccard score is bigger then threshold
            for pair in candidates:
                score = jaccard(articlesDict[pair[0]], articlesDict[pair[1]])
                if score > similarityThreshold:
                    print(pair[0], pair[1], score)
                    counter += 1
        else:
            #iterate over all articles and  compute the jaccard score, print if its over 0.8
            for a in articlesDict:
                for b in articlesDict:
                    if int(b) > int(a):
                        score=jaccard(articlesDict[a], articlesDict[b])
                        if score > 0.8:
                            print(a,b,score)
                            counter += 1

        print(counter)
        print(time.time()-timestart)


