# -*- coding: UTF-8 -*-
from scipy import stats
import numpy as np
import pandas as pd
import math

"""

Implementação do SAX, algoritmo proposto por:

[1] Lin, J., Keogh, E., Lonardi, S. & Chiu, B. 
    "A Symbolic Representation of Time Series, with Implications for Streaming Algorithms." 
    In proceedings of the 8th ACM SIGMOD Workshop on Research Issues in Data Mining and 
     Knowledge Discovery. San Diego, CA. June 13, 2003.

"""


#Dada uma série tempora T, essa série temporal é convertida em uma versão reduzida de tamanho N
def convertToPAA(time_serie,paa_length):
    length = len(time_serie)
    if(length == paa_length):
        return time_serie
    paa = np.zeros(paa_length)
    if(length%paa_length == 0):
        segments = np.array_split(time_serie, paa_length)
        paa = map(lambda seg: seg.mean(axis = 0), segments)
    else:
        for i in range(length*paa_length):
            paa[i/length] += time_serie[i/paa_length]
        for i in range(paa_length):
            paa[i] /= float(length)
    return np.asarray(paa)



def compareLetters(letter1,letter2,breakpoints):
        indices = [ord(letter1) - 97, ord(letter2) - 97]
        indices = sorted(indices)
        if(abs(indices[0] - indices[1]) <= 1):
            return 0.0
        return breakpoints[indices[1]] - breakpoints[indices[0]+1]
   
#Encontra a distância entre duas palavras geradas pelo SAX 
def mindist(word1,word2,serie_length,breakpoints):
        word_size = len(word1)
        if(word_size != len(word2)):
            return None
        my_sum  = 0.0
        for w1, w2 in zip(word1, word2):
            my_sum += (compareLetters(w1, w2,breakpoints))**2
        return math.sqrt((my_sum*serie_length)/float(word_size))



def getBreakpoints(num_breakpoints):
    breakpoints = stats.norm.ppf(np.linspace(1./num_breakpoints,1-1./num_breakpoints,num_breakpoints-1))
    breakpoints = np.insert(breakpoints,0,-np.inf)
    breakpoints = np.append(breakpoints, np.inf)
    return breakpoints


def applySAX(time_serie,word_length,alphabet_size,eps):
    if(alphabet_size < 3 or alphabet_size > 20):
        return None
    stdev = np.std(time_serie)
    if(stdev < eps):
        letter = chr(97+(alphabet_size/2))
        word = np.repeat(letter,[word_length])
        return word
    normalized = stats.zscore(time_serie)
    paa = convertToPAA(normalized,word_length)
    beta = getBreakpoints(alphabet_size)
    word = pd.cut(paa, bins = beta, labels= map(chr, range(97, (97+alphabet_size))))
    return np.asarray(word)


