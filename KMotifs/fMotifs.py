# -*- coding: UTF-8 -*-
import numpy as np
import pandas as pd
from scipy import stats
import itertools
import random
import pysax
import collections
import time
import tsutils



def getCombinations(l,k):
    return list(itertools.combinations(l,k))

def applyMask(word,mask):
    return [word[i] for i in mask]

def keyExists(hash_map,key):
    return not (hash_map.get(key) is None)

def randomMask(possible_combinations,previous_idx):
    idx = random.choice(possible_combinations)
    while(idx == previous_idx):
        idx = random.choice(possible_combinations)
    previous_idx = idx
    return idx,previous_idx

def readjustKMotifs(kMotifs,motif,index,k):
    length = len(kMotifs)
    if length:
        kMotifs.insert(index, motif)
        if length == k:
            kMotifs.pop()
    else: 
        kMotifs.append(motif)
    return kMotifs

"""
#Obtem os candidatos a motifs na matriz e refina a matriz
def getCandidates(collision_matrix,r):
    #new_collision_matrix = collections.defaultdict(dict)
    candidates = collections.defaultdict(dict)
    for keys,values in collision_matrix.iteritems():
        for k,v in values.iteritems():
            if v >= r:
                #new_collision_matrix[keys] = values
                candidates[keys][k] = False
    return candidates
"""

def getCandidates(collision_matrix,r):
    new_collision_matrix = collections.defaultdict(dict)
    candidates = collections.defaultdict(dict)
    for keys,values in collision_matrix.iteritems():
        for k,v in values.iteritems():
            if v >= r:
                new_collision_matrix[keys] = collision_matrix[keys]#values
                #new_collision_matrix[k] = collision_matrix[k]
                candidates[keys][k] = False
    return new_collision_matrix,candidates

def checkKMotif(time_series_data,current_motif,kMotifs,k,window_length,R):
    num_motifs = len(kMotifs)
    i = 0
    while(i < num_motifs):
        #Verficar se o numero de ocorrencias atual maior que as dos k-motifs encontrados
        if(current_motif[1] > kMotifs[i][1]):
            break
        i+=1
    if i < k:
        current_subsequence_id = current_motif[0][0]
        for j in range(num_motifs):
            k_subsequence_id = kMotifs[j][0][0]
            if distance(time_series_data,current_subsequence_id,k_subsequence_id,window_length) <= 2*R:
                return -1
        return i
    return -1


def distance(time_series_data,pos_1,pos_2,window_length):
    
    ts1 = time_series_data[pos_1[0]]
    ts2 = time_series_data[pos_2[0]]
    #Obter as subsequencias p e q 
    subsequence_p = ts1[pos_1[1]:pos_1[1]+window_length]
    subsequence_q = ts2[pos_2[1]:pos_2[1]+window_length]
    #Normalizar para o intervalo [0,1]
    subsequence_p = (subsequence_p-np.min(subsequence_p))/(np.max(subsequence_p)-np.min(subsequence_p))
    subsequence_q = (subsequence_q-np.min(subsequence_q))/(np.max(subsequence_q)-np.min(subsequence_q))
    
    similarity = np.linalg.norm(subsequence_p-subsequence_q)
    
    return similarity

def trivialMatch(time_series_data,pos_1,pos_2,window_length,r):
    # -------Caso 1: series diferentes--------#
    # Nao ha casamento trivial
    if pos_1[0] != pos_2[0]: 
        return False

    # -------Caso 2: mesma serie--------#
    # Verificar se existir um subsequencia entre p e q
    # que nao case com 'p'.
    if pos_1[1] != pos_2[1]: 
        time_serie = time_series_data[pos_1[0]]
        p,q = min(pos_1[1],pos_2[1]),max(pos_1[1],pos_2[1])

        #Obter subsequencia p e normalizar para o intervalo [0,1]
        subsequence_p = time_serie[p:p+window_length]
        subsequence_p = (subsequence_p-np.min(subsequence_p))/(np.max(subsequence_p)-np.min(subsequence_p))

        for k in range(p+1,q):
            #Obter subsequencia k e normalizar para o intervalo [0,1]
            subsequence_k = time_serie[k:k+window_length]
            subsequence_k = (subsequence_k-np.min(subsequence_k))/(np.max(subsequence_k)-np.min(subsequence_k))

            similarity = np.linalg.norm(subsequence_p-subsequence_k)
            if(similarity > r):
                return False
    return True
    
def updateCollisionMatrix(collision_matrix,hash_value,subsequence_position,max_entry_so_far):
    # Se essa chave ja foi encontrada anteriormente, entao incrementa a matriz de colisao
    if (hash_value in collision_matrix and subsequence_position in collision_matrix[hash_value]):
        collision_matrix[hash_value][subsequence_position] += 1
    else:
        collision_matrix[hash_value][subsequence_position] = 1
        #Guardar o maior numero de colisoes
    if(collision_matrix[hash_value][subsequence_position] >  max_entry_so_far):
        max_entry_so_far = collision_matrix[hash_value][subsequence_position]

    return collision_matrix,max_entry_so_far



#Aplica o SAX sobre uma série temporal
def symbolize(time_serie,word_length,alphabet_size,breakpoints,eps = 1e-6):
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
    return np.asarray(word)


def buildSubsequenceMatrix(time_serie,window_length,word_length,alphabet_size,breakpoints,eps = 1e-6):
        ts_length = len(time_serie)
        previous_subsequence = ""
        indices = []
        subsequence_matrix = []
        num_subsequences = 0

        for i in xrange(ts_length-window_length + 1):
            current_subsequence = symbolize(time_serie[i:i+window_length],word_length,alphabet_size,breakpoints,eps)
            if(np.array_equal(current_subsequence,previous_subsequence)):
                continue
            subsequence_matrix.append(current_subsequence)
            indices.append(i)
            num_subsequences += 1
            previous_subsequence = current_subsequence

        return ({"window_length": window_length, "word_length": word_length, "alphabet_size": alphabet_size},subsequence_matrix,indices,num_subsequences)



def buildCollisionMatrix(sm,mask_size, iteration_number,time_serie_id = None,backup = False):

    word_length = sm[0][0]['word_length']

    #Preparar o conjunto de combinacoes possiveis de mascara
    all_positions = np.arange(0,word_length,1)
    possible_combinations = getCombinations(all_positions,mask_size)
    previous_idx = (-1,-1)

    collision_matrix = collections.defaultdict(dict)
    max_value,num_series = 0, len(sm)
    mask_comb = []

    for it in range(iteration_number):
        hash_table = {}
        # Obter indices da mascara diferentes da iteracao anterior
        idx, previous_idx = randomMask(possible_combinations,previous_idx)
        mask_comb.append(idx)
        # Percorrer sobre todas as series temporais
        for i in xrange(num_series):

            current_subsequences = sm[i][1]
            subsequences_positions =sm[i][2]
            num_subsequences = sm[i][3]

            # Percorre sobre todas as subsequencias da i-esima serie
            for k in range(num_subsequences):
                subsequence = current_subsequences[k]
                key = str(applyMask(subsequence,idx))
                if time_serie_id is None:
                    subsequence_position = (i,subsequences_positions[k])
                else:
                    subsequence_position = (time_serie_id,subsequences_positions[k])
                if keyExists(hash_table,key):
                    collision_matrix,max_value = updateCollisionMatrix(collision_matrix,hash_table[key],subsequence_position,max_value)
                else:
                    hash_table[key] = subsequence_position#(i,subsequences_positions[k])
    if backup:
        timestr = time.strftime("%Y%m%d-%H%M%S")
        filename ="temp/idxserie_%s__%s.fmotif"%(time_serie_id,timestr)
        tsutils.saveData(mask_comb,filename)

    return (collision_matrix, max_value)

def findKMotifs(data,candidates,window_length,K,R,KMotifs = [], backup = False):
    num_time_series = len(data)
    for c1 in candidates:
        for c2,motif_occurrence in candidates[c1].iteritems():
            if not motif_occurrence and distance(data,c1,c2,window_length) <= R and not trivialMatch(data,c1,c2,window_length,R):
                #Guardar membros do motif e ocorrencias de motifs
                members = [[],0]

                candidates[c1][c2] = True
                members[0].append(c1)
                members[0].append(c2)
                members[1] = 2

                for time_serie_id in range(num_time_series):
                    subsequence_length = len(data[time_serie_id])
                    for subsequence_id in range(subsequence_length-window_length):
                        ck = (time_serie_id,subsequence_id)
                        if ck != c1 and ck != c2:
                            if distance(data,c1,ck,window_length) <= R and not trivialMatch(data,c1,ck,window_length,R):
                                members[0].append(ck)
                                members[1] += 1
                                if keyExists(candidates[c1],ck):
                                    candidates[c1][ck] = True
                #Verificar K-Motifs
                idx = checkKMotif(data,members,KMotifs,K,window_length,R)
                if idx >= 0:
                    KMotifs =  readjustKMotifs(KMotifs,members,idx,K)
                    #Salvar variaveis atuais de Motifs
                    if(backup):
                        tsutils.saveData(KMotifs,"temp/KMotifs.fmotif")
                        tsutils.saveData(candidates,"temp/candidates.fmotif")
    return KMotifs
