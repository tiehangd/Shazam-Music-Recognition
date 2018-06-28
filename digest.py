
import numpy as np
from scipy.integrate import ode
from numpy import array
import matplotlib.pyplot as pl
from math import exp

import math;
from pylab import *;
import matplotlib.pyplot as plt
from numpy import *
import sys
from operator import itemgetter
import hashlib

import pickle
from scipy.io import wavfile
import matplotlib.pyplot as plt
from scipy.fftpack import fft
import matplotlib.mlab as mlab
from scipy.ndimage.filters import maximum_filter
from scipy.ndimage.morphology import generate_binary_structure, iterate_structure, binary_erosion
from collections import Counter

rate1,data1=wavfile.read('F:/music/the_love_like_flood.wav')
rate2,data2=wavfile.read('F:/music/one_game_one_dream.wav')
rate3,data3=wavfile.read('F:/music/shape_of_my_heart.wav')


rate_test,data_test=wavfile.read('F:/music/test/test2.wav')

def digest(rate,data):
#print data.shape
    n=data.shape[0]
    #print data.shape
    d=n/float(rate)
    
    window=2048
    
    overlap=0.5
    
    pair_number=10
    
    min_max=5
    
    neig_number=10
    
    region_t=200
    region_f=200
    
    hash_keep=24
    
    spectrum=mlab.specgram(data[:,1],NFFT=window,Fs=rate,window=mlab.window_hanning,noverlap=int(window*overlap))
    
    
    #spec=asarray(spec_1,spec_2,spec_3)
    
    spec_data=asarray(spectrum[0])
    #print spec_data.shape    
    
    struct = generate_binary_structure(2, 1)
    #print struct
    neighborhood = iterate_structure(struct,neig_number)
    #print neighborhood
    local_max = maximum_filter(spec_data, footprint=neighborhood) == spec_data
    #print maximum_filter(spec_data, footprint=neighborhood)
    background = (spec_data==0)
    eroded_background = binary_erosion(background, structure=neighborhood, border_value=1)
    #print eroded_background
    detected_peaks = local_max - eroded_background # this is because previously the eroded background is also true in the peaks;    
    
    the_peaks=spec_data[detected_peaks]
    
    #print detected_peaks.shape
    p_row, p_col=where(detected_peaks)
    
    peaks = vstack((p_row,p_col,the_peaks))
    
    real_peaks=peaks[:,peaks[2,:]>min_max]

    f_index=real_peaks[0,:]
    t_index=real_peaks[1,:]
    
    star=zip(f_index,t_index)
    star.sort(key=itemgetter(1))
    star=asarray(star).T
    #print star
    
    star_leng=star.shape[1]
    store=list()
    for i in range(star_leng):
        for j in range(1,neig_number):
            if (i+j)<star_leng and (star[1,(i+j)]-star[1,i])<region_t and abs((star[0,(i+j)]-star[0,i]))<region_f:
                f1=star[0,i]
                f2=star[0,(i+j)]
                t=star[1,i]
                t_diff=star[1,(i+j)]-star[1,i]
                
                hass = hashlib.sha1("%s|%s|%s" % (str(f1), str(f2), str(t_diff)))            
                
                this_hash=[hass.hexdigest()[0:hash_keep],t]
                store.append(this_hash)
                
                
        
    
    return store
    
  
store1=digest(rate1,data1)

store2=digest(rate2,data2)

store3=digest(rate3,data3)


store_test=digest(rate_test,data_test)

store1=asarray(store1).T

#print "store1"
#print store1

store2=asarray(store2).T

store3=asarray(store3).T

pickled = pickle.dumps([store1,store2,store3])


store_test=asarray(store_test).T


test_leng=store_test.shape[1]
#print test_leng
leng_1=store1.shape[1]
#print leng_1
leng_2=store2.shape[1]
#2_leng=store2.shape

leng_3=store3.shape[1]




match1=[]
for i in range(leng_1):
    for j in range(test_leng):
        if store1[0,i]==store_test[0,j]:
            match1.append((int(float(store1[1,i])))-int(float((store_test[1,j]))))

#print match1

match2=[]
for i in range(leng_2):
    for j in range(test_leng):
        if store2[0,i]==store_test[0,j]:
            match2.append((int(float(store2[1,i])))-int(float((store_test[1,j]))))


match3=[]
for i in range(leng_3):
    for j in range(test_leng):
        if store3[0,i]==store_test[0,j]:
            match3.append((int(float(store3[1,i])))-int(float((store_test[1,j]))))


#print match2

match1=abs(asarray(match1))
match2=abs(asarray(match2))
match3=abs(asarray(match3))





count1=max(bincount(match1))
count2=max(bincount(match2))
count3=max(bincount(match3))
print count1
print count2
print count3





#print store1.shape







#print spec_data















