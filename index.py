import collections
import getopt
import codecs
import struct
import pickle
import math
import nltk
import sys
import os
import re
from math import log
from nltk import PorterStemmer


LIMIT = None                # (for testing) to limit the number of documents indexed
IGNORE_STOPWORDS = True     # toggling the option for ignoring stopwords
IGNORE_NUMBERS = True       # toggling the option for ignoring numbers
IGNORE_SINGLES = True       # toggling the option for ignoring single character tokens




k1 = 1.2

b = 0.75


def score_BM25(n, f, N, dl, avdl):
    K = compute_K(dl, avdl)
    first = log( (N - n  + 0.5) / (n + 0.5) )
    second = ((k1 + 1) * f) / (K + f)
    return first * second


def compute_K(dl, avdl):
    return k1 * ((1-b) + b * (float(dl)/float(avdl)) )

def index(document_directory, dictionary_file):
    # preprocess docID list
    docID_list = []
    i=1
    for doc in os.listdir(document_directory):
        docID_list.append([doc,i])
        i+=1
    f1 = open("output","wb")
    pickle.dump(docID_list,f1)
    f1.close()
    stopwords = nltk.corpus.stopwords.words('english')
    docs_indexed = 0    # counter for the number of docs indexed
    dictionary = {}     # key: term, value: docIDs containing term (incudes repeats)
    l_no = {}
    length = []
    count = 0
    cnt = 0
    c1 = 0
    word_positions = 0
    # for each document in corpus
    for docID in docID_list:
        if (LIMIT and docs_indexed == LIMIT): break
        file_path = os.path.join(document_directory, str(docID[0]))

        # if valid document
        cnt += 1
        line_no = 1
        if (os.path.isfile(file_path)):
            file = codecs.open(file_path, encoding='utf-8', errors='ignore')
            line = file.readline()
            c = 0
            # for line in document
            while line != '':                # read entire document
                tokens = nltk.word_tokenize(line)   # list of word tokens from document
                # for each term in document
                for word in tokens:
                    word_positions += 1
                    word = PorterStemmer().stem(word)
                    c += 1
                    count += 1
                    term = word.lower()         # casefolding
                    if (IGNORE_STOPWORDS and term in stopwords):    continue    # if ignoring stopwords
                    if (IGNORE_NUMBERS and term.isnumeric()):        continue    # if ignoring numbers
                    if (term[-1] == "'"):
                        term = term[:-1]        # remove apostrophe
                    if (IGNORE_SINGLES and len(term) == 1):         continue    # if ignoring single terms
                    if (len(term) == 0):                            continue    # ignore empty terms
                    
                    # if term not already in dictionary
                    if (term not in dictionary):
                        dictionary[term] = [int(docID[1])]   # define new term in in dictionary
                        po = [line_no,word_positions]
                        l_no[term] = [po]
                        c1 += 1
                    # else if term is already in dictionary, append docID
                    else:
                        dictionary[term].append(docID[1])
                        po = [line_no,word_positions]
                        l_no[term].append(po)
                line_no += 1
                line = file.readline()
                
            docs_indexed += 1
            length.append(c)
            file.close()

    f3 = open("len","wb")
    pickle.dump(l_no,f3)
    f3.close()
    dict_file = codecs.open(dictionary_file, 'w', encoding='utf-8')
    dict_file.write(str(cnt) + '\n')
    ct = count / cnt
    fre = {}
    pr = 0
    score = {}
    for term, docs in dictionary.items():
        for x in range(cnt):
            freq = 0
            n = 0
            for t in dictionary[term]:
                if (x+1 == t):
                    freq += 1
                if (pr != t and pr!=0):
                    n += 1
                pr = t
            sc = score_BM25(n,freq,cnt,length[x-1],ct)
            if (term not in score):
                score[term] = [sc]   # define new term in in dictionary
            else:
                score[term].append(sc)
            if (term not in fre):
                fre[term] = [freq]   # define new term in in dictionary
            else:
                fre[term].append(freq)
        dict_file.write(term + " " + str(dictionary[term]) + " " + str(l_no[term]) + "\n")
    # close files
    dict_file.close()
    f2 = open("dict","wb")
    pickle.dump(score,f2)
    f2.close()
    f4 = open("freq","wb")
    pickle.dump(fre,f4)
    f4.close()

f = open("dictionary.txt","a+")
index("/home/sparsh/english/","dictionary.txt")