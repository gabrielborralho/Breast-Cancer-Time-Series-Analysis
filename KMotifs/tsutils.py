# -*- coding: UTF-8 -*-
import cv2
import numpy as np
import glob,os
import cPickle
import itertools 
import numpy as np


#Normalizações

#Amplitude
def standardScore(x):
    z = ((x.T - np.mean(x,axis = 1))/np.std(x,axis = 1)).T
    return z

#Escala
def featureScaling(x):
    z = ((x.T - np.min(x,1))/(np.max(x,1) - np.min(x,1))).T
    return z

#Escala
def normalizeMax(x):
    z = (x.T/np.max(x,1)).T
    return z


#remover presença de Nans resultantes do registro
def removeNans(arr):
    where_are_NaNs = np.isnan(arr)
    if True in where_are_NaNs:
        aux = arr[np.logical_not(where_are_NaNs)]
        min_value = aux.min()
        arr[where_are_NaNs] = min_value
    return arr

def slidingWindow(image, stepSize, windowSize):
    for y in xrange(0, image.shape[0], stepSize):
        for x in xrange(0, image.shape[1], stepSize):
            yield (x, y, image[y:y+windowSize[1], x:x+windowSize[1]])

'''
Retorna um numpy array 1D contendo, onde cada
posição contém o valor máximo extraído de cada
região quadrada (windowSize x windowSize).

Recebe como argumentos, uma imagem (numpy array) e
uma mascara binaria (numpy array) de mesmo tamanho 
da imagem. Além disso, recebe o tamanho da janela,
e se é janela sobreposta ou não.
'''
def applyMask(image,mask,windowSize = 3, overlap = False):
    values = []
    winH = winW = windowSize
    boolean_mask = mask.astype(np.bool)
    stepSize = 1 if overlap else windowSize
    for (x, y, window) in slidingWindow(image, stepSize, windowSize=(winW, winH)):
        submask = boolean_mask[y:(y+winH),x:(x + winW)]
        region = window[submask]
        if len(region):
            values.append(region.max())
    return np.asarray(values)

'''
A partir uma lista de imagens (numpy array), todas com mesmas proporções,
uma máscara binária (numpy array) de mesma dimensão da imagem, é construída
uma lista de séries temporais, onde cada posição representa uma série temporal
de cada pixel ou região (Dimensão da região dada por windowSize).
'''
def buildTimeSeries(data,mask,windowSize = 13):
    time_series = []
    for mat in data:
        mat = removeNans(mat)
        values = applyMask(mat,mask,windowSize)
        time_series.append(values)
    time_series_data = np.asarray(map(np.array, time_series)).T
    return time_series_data


'''
Carregar arquivo txt como arquivo de imagem em escala/numpy eliminando
presença de NANS resultantes do registro.
'''
def txtToGrayImage(filepath,normalize = True):
    data = np.loadtxt(filepath)
    data = removeNans(data) 
    #escala de cinza
    if normalize:
        data = (data - np.min(data))*(255/(np.max(data) - np.min(data)))
    return data


def binomialCoefficient(n,r):
    return reduce(lambda x, y: x * y[0] / y[1], itertools.izip(xrange(n - r + 1, n+1), xrange(1, r+1)), 1)

def saveData(data,filename):
    with open(filename, "wb") as output_file:
        cPickle.dump(data, output_file)
        output_file.close()

def loadData(filename):
    with open(filename, "rb") as input_file:
        data = cPickle.load(input_file)
        input_file.close()
        return data


"""
rootdir = 'DADOS'
output = 'Series'

for subdir, dirs, files in os.walk(rootdir):
    if 'Mascaras' in subdir:
        continue
     
    output = os.path.join('Series',os.path.basename(subdir))
    print output
    for filename in files:
        maskpath = os.path.join(rootdir, 'Mascaras',os.path.splitext(filename)[0] + '.txt') 
        datapath = os.path.join(subdir, filename)

        mask = np.loadtxt(maskpath)
        data = np.load(datapath)
        output_path = os.path.join(output, 'Max_13x13_' + filename)
        time_series = buildTimeSeries(data,mask)
        np.save(output_path,time_series)

"""