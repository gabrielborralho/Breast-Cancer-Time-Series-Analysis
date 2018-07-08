import pysax
from scipy import stats
import numpy as np
import math
import matplotlib.pyplot as plt
import pandas as pd


alphabet_size = 4
beta = pysax.getBreakpoints(alphabet_size)

time_series_A =  [0,    0.3146,    0.5972,    0.8192,    0.9580,    0.9996,    0.9396,    0.7843,    
		         0.5494,    0.2586,   -0.0584,   -0.3694,   -0.6430,   -0.8513,   -0.9731,   -0.9962,   
		         -0.9181,   -0.7468,   -0.4996,   -0.2018,    0.1165,    0.4231,    0.6866,    0.8805,    
		         0.9849,    0.9894,    0.8934,    0.7067,    0.4482,    0.1443,   -0.1743,   -0.4752]

time_series_B = [-0.3694,   -0.6430,   -0.8513,   -0.9731,   -0.9962,   -0.9181,   -0.7468,   -0.4996,
				 -0.2018,    0.1165,    0.4231,    0.6866,    0.8805,    0.9849,    0.9894,    0.8934,    
				 0.7067,    0.4482,    0.1443,   -0.1743,   -0.4752,   -0.7279,   -0.9066,   -0.9933,   
				 -0.9792,   -0.8656,   -0.6642,   -0.3953,   -0.0863,    0.2315,    0.5258,    0.7667]


time_series_A = stats.zscore(time_series_A)
time_series_B = stats.zscore(time_series_B)


#plt.plot(t,time_series_A,'b') # plotting t,a separately 
#plt.plot(t,time_series_B,'r') # plotting t,b separately 
#plt.show()

sax_version_of_A = pysax.convertToPAA(time_series_A,8)
sax_version_of_A = pd.cut(sax_version_of_A, bins = beta, labels= map(chr, range(97, (97+alphabet_size))))

sax_version_of_B = pysax.convertToPAA(time_series_B,8)
sax_version_of_B = pd.cut(sax_version_of_B, bins = beta, labels= map(chr, range(97, (97+alphabet_size))))


print sax_version_of_A
print sax_version_of_B


beta =  np.around(beta, decimals=2)

print "distance: %f"%pysax.mindist(sax_version_of_A,sax_version_of_B,32,beta)

