
import csv
import time
from functools import reduce
def jaccard(A, B):
    union = A.union(B)
    intersection = A.intersection(B)
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



if __name__ == '__main__':

    timestart = time.time()
    with open('news_articles_small.csv', mode='r') as infile:
        reader = csv.reader(infile)
        next(reader)
        articles = {rows[0]:rows[1] for rows in reader}

        jaccardMatrix=[]

        shinglesDict={}
        articlesDict={}
        for article in articles:
            articlesDict[article]=set()
            shingles = set(getShingles(articles[article],2))
            for s in shingles:
                if s not in shinglesDict:
                    shinglesDict[s] = len(shinglesDict)
                articlesDict[article].add(shinglesDict[s])
        for a in articlesDict:
            row = []

            for b in articlesDict:
                if a > b:
                    score=jaccard(articlesDict[a], articlesDict[b])
                    if score > 0.8:
                        print(a,b,score)
                    row.append(score)
            jaccardMatrix.append(row)

        print(time.time()-timestart)


