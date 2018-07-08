# -*- coding: UTF-8 -*-
import time
import math
import glob,os
import numpy as np
from scipy import stats
from timeit import default_timer as timer


import pysax
import fMotifs
import tsutils


#Parametros para discretizacao
window_length = 10#int(0.1*min(map(len,time_series_data)))#20 #Tamanho do Motif
word_length = window_length#int(0.1*window_length)#10% do tamanho da janela
alphabet_size = 6 #corroborando com o artigo
breakpoints = pysax.getBreakpoints(alphabet_size)

#Parametros para encontrar os Motifs
percent = 0.1 #5%10% #corroborando com o artigo
K = 5 #Numero de K-Motifs #chute inicial
R = math.sqrt(word_length)*percent

#Parametros para a random projection 
mask_size = 2 #corroborando com o artigo
num_iter = int (0.5 * tsutils.binomialCoefficient(word_length, mask_size)) #corroborando com o artigo



rootdir = 'DADOS/Series/'
time_series = []
for subdir, dirs, files in os.walk(rootdir):
    for filename in files:
        fullpath = os.path.join(subdir, filename)
        data = np.load(fullpath)
        data = stats.zscore(data, axis = 1)
        super_serie = data.ravel()
        time_series.append(super_serie)
time_series_data = np.asarray(time_series)


num_series = len(time_series_data)
print "Quantidade de series: %s"%num_series

N = 1000

for k in range(27,N):

	text_file = open("temp/progress_%s.txt"%k, "w")
	KMotifs = []
	i = 0
	start = timer()
	for serie in time_series_data:
		if i%10 == 0:
			end = timer()
			print("Construindo matriz de subsequencias para o dado %s, tempo decorrido %s" %(i,end - start))
		subsequences = fMotifs.buildSubsequenceMatrix(serie,window_length,word_length,alphabet_size,breakpoints)
	    
		if i%10 == 0:
			end = timer()
			print ("Construindo matriz de colisao para o dado %s, tempo decorrido %s" %(i,end - start))
		collision_matrix,max_value = fMotifs.buildCollisionMatrix([subsequences],mask_size,num_iter,i,True)
		subsequences = None
		if i%10 == 0:
			end = timer()
			print ("Buscando k-motifs para o dado %s, tempo decorrido %s" %(i,end - start))

		collision_matrix,candidates = fMotifs.getCandidates(collision_matrix,max_value)
		KMotifs = fMotifs.findKMotifs(time_series_data,candidates,window_length,K,R,KMotifs,True)

	    #Salva um backup a cada 10 series (sao 180)
		if i%10 == 0:
			end = timer()
			print ("Fim busca k-motifs para o dado %s, tempo decorrido %s\n" %(i,end - start))
			text_file.write("serie atual: %s, tempo decorrido: %s\n" % (i,end - start))
			filename ="temp/KMotifs.fmotif"
			tsutils.saveData(KMotifs,filename)
		i += 1
	#Salvar resultado final
	#timestr = time.strftime("%Y%m%d-%H%M%S")
	filename ="resultado/KMotifs01_v%s.fmotif"%k
	tsutils.saveData(KMotifs,filename)
	text_file.close()


