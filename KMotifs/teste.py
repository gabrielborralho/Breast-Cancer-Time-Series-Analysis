# -*- coding: UTF-8 -*-
import pysax
import numpy as np
import pandas as pd
from scipy import stats
from math import sqrt
import tsutils
import fMotifs

#Parametros para discretizacao
window_length = 20#int(0.1*min(map(len,time_series_data)))#20 #Tamanho do Motif
word_length = window_length#int(0.1*window_length)#10% do tamanho da janela
alphabet_size = 6 #corroborando com o artigo
breakpoints = pysax.getBreakpoints(alphabet_size)

#Parametros para encontrar os Motifs
percent = 0.20 #5%10% #corroborando com o artigo
K = 10 #Numero de K-Motifs #chute inicial
R = sqrt(word_length)*percent

#Parametros para a random projection 
mask_size = 2 #corroborando com o artigo
num_iter = int (0.5 * tsutils.binomialCoefficient(word_length, mask_size)) #corroborando com o artigo

#Aplica o SAX sobre uma série temporal
def symbolize(time_serie,word_length = word_length,alphabet_size = alphabet_size,breakpoints = breakpoints,eps = 1e-6):
    if(alphabet_size < 3):
        return None
    stdev = np.std(time_serie)
    if(stdev < eps):
        letter = chr(97+(alphabet_size/2))
        word = np.repeat(letter,[word_length])
        return word
    normalized = stats.zscore(time_serie)
    paa = pysax.convertToPAA(normalized,word_length)
    word = pd.cut(paa, bins = breakpoints, labels= map(chr, range(97, (97+alphabet_size))))
    return word



time_series = np.load("E:/K-Motifs2/DADOS/Series/2.Com Anomalia/Max_13x13_ID_192.npy")
time_series = stats.zscore(time_series, axis = 1) 
subsequence_matrix = np.asarray(map(symbolize,time_series))
num_subsequences = len(time_series)
indices = np.linspace(0, num_subsequences-1, num=num_subsequences)
indices = indices.astype(np.int)
subsequences = {"window_length": window_length, "word_length": word_length, "alphabet_size": alphabet_size},subsequence_matrix,indices,num_subsequences


collision_matrix,max_value = fMotifs.buildCollisionMatrix([subsequences],mask_size,num_iter,0)

collision_matrix,candidates = fMotifs.getCandidates(collision_matrix,max_value)


KMotifs = fMotifs.findKMotifs([time_series],candidates,window_length,K,R)

print KMotifs