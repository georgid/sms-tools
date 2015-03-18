'''
Created on Mar 17, 2015
 see V. Rao and P. Rao - Vocal melody extraction in the presence of pitched accompaniment in polyphonic music, II.B

@author: joro
'''

from scipy.signal import get_window
import os
import sys
import math
import numpy as np
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), '../software/models/'))
import utilFunctions as UF
import sineModel as SM
import harmonicModel as HM
import dftModel as DFT
import matplotlib.pyplot as plt

parentParentDir = os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(sys.argv[0]) ), os.path.pardir,  os.path.pardir)) 
pathUtils = os.path.join(parentParentDir, 'utilsLyrics')
if pathUtils not in sys.path:
    sys.path.append(pathUtils )

inputFile = '../sounds/vignesh.wav'
melodiaInput = '../sounds/vignesh.melodia'

from Utilz import readListOfListTextFile_gen


def doit():
    M=2047
    N=2048
     
    # read input sound
    (fs, x) = UF.wavread(inputFile)
    t = 0.0003162

#     readf0 from Melodia 
    f0FreqsRaw = readListOfListTextFile_gen(melodiaInput)
    hopSizeMelodia = int( round( (float(f0FreqsRaw[1][0])  - float(f0FreqsRaw[0][0]) ) * fs ) )
    
    firstTs = float(f0FreqsRaw[0][0])
    pinFirst  = round (firstTs * fs)
    
    # discard ts-s
    f0Series = []
    for foFreqRaw in f0FreqsRaw:
        f0Series.append(float(foFreqRaw[1])) 
    

    window='blackmanharris'
    # compute analysis window
    w = get_window(window, M)
    
    # 2freq domain
    time2Freq(x, fs, w, N, pinFirst,hopSizeMelodia, t)

def time2Freq(x, fs, w, N, pinFirst, hopSizeMelodia, t):
    '''
    fourier transform for window
       '''
    
    ###################
    ## prepare params    
    hM1 = int(math.floor((w.size+1)/2))                     # half analysis window size by rounding
    hM2 = int(math.floor(w.size/2))                         # half analysis window size by floor
    x = np.append(np.zeros(hM2),x)                          # add zeros at beginning to center first window at sample 0
    x = np.append(x,np.zeros(hM2))                          # add zeros at the end to analyze last sample
    #     pin = hM1                                               # init sound pointer in middle of anal window          
    pin = pinFirst + 300 * hopSizeMelodia
    pend = x.size - hM1                                     # last sample to start a frame
    
    ########################
    # process one window     
    print "at time {}".format(pin/fs)

    x1 = x[pin-hM1:pin+hM2]                               # select frame
    mX, pX = DFT.dftAnal(x1, w, N)                        # compute dft   
    
    ploc = UF.peakDetection(mX, t)                        # detect peak locations   
    
    iploc, ipmag, ipphase = UF.peakInterp(mX, pX, ploc)   # refine peak values
    ipfreq = fs * iploc/N
    
    X = UF.genSpecSines_p(ipfreq, ipmag, ipphase, N, fs)     # generate spec sines

    hN = N/2 + 1                                               # size of positive spectrum
    absX = abs(X[:hN])                                      # compute ansolute value of positive side
    absX[absX<np.finfo(float).eps] = np.finfo(float).eps    # if zeros add epsilon to handle log
    generatedX = absX
#     generatedX = 20 * np.log10(absX) 
    
    ########################
    visualizeSpectum(mX,pin/fs, ploc, iploc, ipmag, generatedX)
        

def visualizeSpectum(spectrum, timestamp, ploc,  iploc, ipmag, generatedX):
    # create figure to show plots
    plt.figure(figsize=(12, 9))
    freqBinNums = np.arange(len(spectrum))
    # plot

#     plot original spectrum
    plt.vlines(freqBinNums, [0], spectrum,  linewidth=1)
    

    # plot picked peaks
    plt.vlines(ploc, [0], spectrum[ploc], linewidth=2, color='b')
    
    # plot peak interp peaks
    plt.vlines(iploc, [0], ipmag, linewidth=2, color='r')
    
    # plot main-lobes
    
    plt.vlines(freqBinNums, [0], generatedX, linewidth=2, color='g')
    
    plt.title('at time ' + str(timestamp) )
    plt.show()
    
    
if __name__ == "__main__":
    doit()