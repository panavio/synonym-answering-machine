
'''Semantic Similarity: starter code

Author: Michael Guerzhoy. Last modified: Nov. 18, 2022.
'''

import math
def norm(vec):
    '''Return the norm of a vector stored as a dictionary, as 
    described in the handout for Project 3.
    '''
    
    sum_of_squares = 0.0  
    for x in vec:
        sum_of_squares += vec[x] * vec[x]
    
    return math.sqrt(sum_of_squares)


def cosine_similarity(vec1, vec2):
    sum=0
    deno1=0
    deno2=0
    v1=list(vec1)
    v2=list(vec2)
    for k,v in vec1.items():
        if k in vec2:
            sum+=vec1[k]*vec2[k]
    
    for i in range(len(vec1.keys())):
        deno1+=(vec1[v1[i]])**2

    for i in range(len(vec2.keys())):
        deno2+=(vec2[v2[i]])**2

    deno=deno1*deno2
    deno=deno**(1/2)
    return sum/deno
    

def build_semantic_descriptors(sentences):
    dictionary={}
    for L in sentences:
        
        for w in L:
            if w not in dictionary:
                if w!='':
                    dicin={}
                    for word in L:
                        dicin[word]=1
                    dicin.pop(w)
                    dictionary[w]=dicin
                
            else:
                for word in L:
                    if word not in dictionary[w] and word!=w:
                        dictionary[w][word]=1
                    elif word!=w:
                        dictionary[w][word]+=1
                        
    return dictionary

#print(build_semantic_descriptors([["i", "am", "a", "sick", "man"],["i", "am", "a", "spiteful", "man"],["i", "am", "an", "unattractive", "man"],["i", "believe", "my", "liver", "is", "diseased"]]))

def build_semantic_descriptors_from_files(filenames):
    res=[]
    for files in range(len(filenames)):
        file=open(filenames[files], "r", encoding="latin1")
    
        text=file.read()
        text=text.lower()
        text=text.replace("\n", " ")
        #print(text)
        text=text.replace("!", ".")
        text=text.replace("?", ".")
        text=text.replace(",", "")
        text=text.replace("--", " ")#punctuation splits words?
        text=text.replace("-", " ")#the split includes the space?
        text=text.replace(":", " ")
        text=text.replace(";", " ")
        #text=text.replace("\"", "")#should I include?
        words=text.split(". ")
    
        for i in range(len(words)):
            words1=words[i].split(" ")
            words[i]=words1
        res.extend(words)
    return build_semantic_descriptors(res)

#build_semantic_descriptors_from_files(["tester.txt"])


def most_similar_word(word, choices, semantic_descriptors, similarity_fn):
    max=-1000
    out=None
    if (word in semantic_descriptors):
        for choice in choices:
            if choice in semantic_descriptors:
                res=similarity_fn(semantic_descriptors[word], semantic_descriptors[choice])
                if res==None:
                    res=-1
                if res>max:
                    max=similarity_fn(semantic_descriptors[word], semantic_descriptors[choice])
                    out=choice 
        
    if out!=None:
        return out
    else:
        return choices[0]
'''
desc=build_semantic_descriptors([["i", "am", "a", "sick", "man"],
["i", "am", "a", "spiteful", "man"],
["i", "am", "an", "unattractive", "man"],
["i", "believe", "my", "liver", "is", "diseased"],
["however", "i", "know", "nothing", "at", "all", "about", "my",
"disease", "and", "do", "not", "know", "for", "certain", "what", "ails", "me"]])
print(cosine_similarity(desc["i"], desc["am"]))
print(cosine_similarity(desc["i"], desc["a"]))
print(cosine_similarity(desc["i"], desc["sick"]))
print(desc)
print(most_similar_word("i", ["am", "a","sick"], desc, cosine_similarity))

'''

def run_similarity_test(filename, semantic_descriptors, similarity_fn):
    file=open(filename, "r", encoding="latin1")
    counter=0
    total=0
    
    for line in file:
        line=line.replace("\n","")
        words=line.split(" ")
        choices=words[2:len(words)]
        ans=most_similar_word(words[0], choices, semantic_descriptors, similarity_fn)
        if ans==words[1]:
            counter+=1
        total+=1
    return (counter/total)*100


sem_descriptors = build_semantic_descriptors_from_files(["wp.txt","sw.txt"])
res = run_similarity_test("test.txt", sem_descriptors, cosine_similarity)
print(res, "of the guesses were correct")
