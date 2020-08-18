import os
import sys
import pickle
import nltk
from nltk import PorterStemmer


stopwords = nltk.corpus.stopwords.words('english')

f1 = open("output","rb")
docID_list = pickle.load(f1)
f2 = open("dict","rb")
score = pickle.load(f2)
f2.close()
f3 = open("len","rb")
l_no = pickle.load(f3)
f3.close()
f4 = open("freq","rb")
fre = pickle.load(f4)
f4.close()

search = 1
while search > 0 :
	b = input("Search keywords? (y/n)\n")

	if (b == 'n') :
		quit()
	b = input("Do you want to search for phrase? (y/n)\n")

	search_str = input("Enter the search string : ")
	snl = ''
	sti = search_str.split(" ")
	for s1 in sti:
		term = s1.lower()
		if(term in stopwords ): continue
		s1 = PorterStemmer().stem(s1)
		snl += " " + s1
	stir = snl.split(" ")
	stir.remove('')
	# print(stir)
	f = open('/home/sparsh/dictionary.txt')
	line = f.readline()
	N = int(line)

	f.close()

	nt = 0
	for st in stir:
		if (st in l_no):
			nt +=1
			break
	if(nt == 0):
		print("No Results Found")
		quit()


	sc = [[0 for x in range(2)] for y in range(N)]
	
	for x in range(N):
		s = 0
		i1=0
		for st in stir:
			s += score[st][x]
		sc[x][0] = s
		sc[x][1] = x+1
	sc = sorted(sc,key = lambda x: x[0], reverse = True)
	counter = [[]  for c in range(N)  ]
	no_of_words = len(stir)
	no_of_docs = int(N)

	if (b == 'y') :
		ind = [[[] for x in range(N)] for y in range(len(stir))]
		i1=0
		for st in stir:
			rd=0
			for x in range(N):
				for r in range(fre[st][x]):
					ind[i1][x].append(l_no[st][r+rd][1])

				rd+=fre[st][x]
			i1 +=1
		p = [[] for i in range(no_of_docs)]

		for i in range(no_of_docs) :
			for j in range(no_of_words):
				ind[j][i] = list(map(lambda x : x - j,ind[j][i]))
		for i in range(no_of_docs) :
			p[i] = ind[0][i]
			for j in range(no_of_words) :
				p[i] = list(set(p[i])&set(ind[j][i]))
		cot = 0
		for i in range(N):
			if(cot>10): break
			if((sc[i][0])!=0):
				j = int(sc[i][1])
				if(p[j-1]!=[]):
					cot+=1
					print(docID_list[j-1][0],"at positions",p[j-1])
		if(cot == 0):
			print("No results found")
		print()
		continue

	for st in stir:
		i = 0
		j = 0
		for fr in fre[st]:
			i+=1
			if(fr != 0):
				for v in range(fr):
					counter[i-1].append(l_no[st][j])
					j+=1

	for z in range(N):
		counter[z] = sorted(counter[z])

	cnt = 1
	for i in range(N):
		if(cnt>10): break
		cn = 1
		if((sc[i][0])!=0):
			cnt+=1
			j = int(sc[i][1])
			x = -1
			flag = 0
			for k in counter[j-1]:
				if (k[0] != 0):
					if(flag==0):
						flag = 1
						print("File: " + (docID_list[j-1][0]) + "    Line no.: " + str(k) ,end="")
					elif(k[0]!= x and flag!=0):
						print("    Matches: ",cn,"")
						cn = 1
						print("File: " + (docID_list[j-1][0]) + "    Line no.: " + str(k) ,end="")
					else:
						cn+=1
				x=k[0]
			print("    Matches: ",cn,"")