# -*- coding: UTF-8 -*-
import cv2
import numpy as np
import glob,os
import _pickle as cPickle
import itertools 
import numpy as np
import re


'''
Retorna um numpy array 1D contendo, onde cada
posição contém o valor médio extraído de cada
região quadrada (windowSize x windowSize).
Recebe como argumentos, uma imagem (numpy array) e
uma mascara binaria (numpy array) de mesmo tamanho 
da imagem. Além disso, recebe o tamanho da janela,
e se é sobreposta ou não.
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
            values.append(region.mean())
    return np.asarray(values)

'''
A partir uma lista de imagens (numpy array) com mesmas proporções,
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
    #time_series_data = np.asarray(map(np.array, time_series)).T
    time_series_data = np.asarray(time_series).T
    return time_series_data

'''
Carregar arquivo txt como arquivo de imagem/numpy eliminando
presença de NANS resultantes do registro.
'''
def txtToGrayImage(filepath,normalize = True):
    data = np.loadtxt(filepath)
    data = removeNans(data) 
    if normalize:
        data = (data - np.min(data))*(255/(np.max(data) - np.min(data)))
    return data

#remover presença de Nans resultantes do registro
def removeNans(arr):
    where_are_NaNs = np.isnan(arr)
    if True in where_are_NaNs:
        aux = arr[np.logical_not(where_are_NaNs)]
        min_value = aux.min()
        arr[where_are_NaNs] = min_value
    return arr

def slidingWindow(image, stepSize, windowSize):
    # slide a window across the image
    for y in range(0, image.shape[0], stepSize):
        for x in range(0, image.shape[1], stepSize):
            # yield the current window
            yield (x, y, image[y:y + windowSize[1], x:x + windowSize[0]])

def get_number(x):
    return int(re.findall('\d+', x[-6:])[0])


if __name__ == "__main__":

    out_dir = 'Series/'
    mask_path = 'Mascara/'
    directory = 'Matrizes/Sem Anomalia/'
    directories = [os.path.join(directory, f) for f in os.listdir(directory)]

    for path in directories:
        name = os.path.basename(path)
        print("Current dir %s" % name)
        files = sorted(glob.glob(os.path.join(path,'*.txt')), key=get_number)
        imgs = list(map(np.loadtxt,files))
        filename = os.path.join(mask_path,name + ".txt")
        mask = np.loadtxt(filename)

        series = buildTimeSeries(imgs,mask,windowSize = 11)
        np.savetxt(os.path.join(out_dir,'Saudavel_Media_11x11_' + name + '.txt'),series)


    #Aqui começa a extrair das com anomalia
    directory = 'Matrizes/Com Anomalia/'
    directories = [os.path.join(directory, f) for f in os.listdir(directory)]

    for path in directories:
        name = os.path.basename(path)
        print("Current dir %s" % name)
        files = sorted(glob.glob(os.path.join(path,'*.txt')), key=get_number)
        imgs = list(map(np.loadtxt,files))
        filename = os.path.join(mask_path,name + ".txt")
        mask = np.loadtxt(filename)

        series = buildTimeSeries(imgs,mask,windowSize = 11)
        np.savetxt(os.path.join(out_dir,'Anomalia_Media_11x11_' + name + '.txt'),series)