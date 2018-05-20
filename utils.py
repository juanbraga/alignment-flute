#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun May 20 16:25:40 2018

@author: jbraga
"""

import matplotlib.pyplot as plt
import numpy as np
import librosa as lr

def alignment_plot(gt_array,gt_t,score_array,path,audio,t):
    
        fig = plt.figure(figsize=(18,6))                                                               
        ax = fig.add_subplot(3,1,(1,2))                                             
        
        yticks_major = [ 59, 60, 62, 64, 65, 67, 69, 71, 72, 74, 76, 77, 79, 81, 83, 84, 86, 88, 89, 91, 93, 95, 96, 98, 100 ]
        yticks_minor = [ 61, 63, 66, 68, 70, 73, 75, 78, 80, 82, 85, 87, 90, 92, 94, 97, 99 ]
        yticks_labels = ['59-B3', '60-C4', '62-D4', '64-E4', '65-F4', '67-G4', '69-A4', '71-B4', '72-C5', '74-D5', '76-E5', '77-F5', '79-G5', '81-A5', '83-B5', '84-C6', '86-D6', '88-E6', '89-F6', '91-G6', '93-A6', '95-B6', '96-C7', '98-D7', '100-E7']                         
                                                 
        ax.set_yticks(yticks_major)                                                   
        ax.set_yticks(yticks_minor, minor=True)
        
        ax.set_yticklabels(yticks_labels, size='small')                                
        
        ax.set_ylim([58, 101]) #flute register in midi   
        ax.set_xlim([0, gt_t[-1]])
        ax.grid(b=True, which='major', color='black', axis='y', linestyle='-', alpha=0.3)
        ax.grid(b=True, which='minor', color='black', axis='y', linestyle='-', alpha=1)    
    
        plt.plot(gt_t, gt_array, color='red', lw=0.8)
        plt.plot(gt_t[path[:,0]], score_array[path[:,1]], color='blue', lw=0.8)
        plt.fill_between(gt_t, gt_array-0.5, gt_array+0.5, facecolor='magenta', label='gt', alpha=0.6)
        plt.fill_between(gt_t[path[:,0]], score_array[path[:,1]]-0.5, score_array[path[:,1]]+0.5, facecolor='cyan', label='aligned score', alpha=0.6)
        plt.legend()
        
        plt.title("Alignment plot")
        plt.ylabel("Notes (American Notation)")
        
        plt.subplot(3,1,3)
        plt.plot(t, audio, color='black', alpha=0.5)
        plt.grid()
        plt.axis('tight')
        plt.ylabel("Amplitude")
        plt.xlabel("Time (s)")    
        plt.xlim([gt_t[0], gt_t[-1:]])
        plt.show()
    
def intermediate_representation_plot(note_fb,Cxx):
    
    plt.figure(figsize=(10,5))
    plt.subplot(1,2,1)
    plt.pcolormesh(note_fb)
    plt.subplot(1,2,2)
    plt.pcolormesh(np.log10(Cxx))
    
def convert2notelist(array,t):
    
    array_diff = np.abs(np.diff(array))
    array_diff[array_diff>0] = 1 
    
    onset = []
    note = []
    duration = []
    
    onset.append(str(t[0]))
    note.append(str(array[0]))
    
    for i in range(0,len(array_diff)):
        if array_diff[i]==1:
            onset.append(str(t[i+1]))
            note.append(str(array[i+1]))
    
    for i in range(0, len(onset)):
        if i == (len(onset)-1):
            duration.append(str(float(t[-1:])-float(onset[i])))
        else:
            duration.append(str(float(onset[i+1])-float(onset[i])))

    onset = np.array(onset, dtype='float')
    note = np.array(note, dtype='float')
    duration = np.array(duration, dtype='float')
    
    return onset, note, duration


def note_filter(f0_array, fmin=lr.note_to_midi('B3'), fmax=lr.note_to_midi('B9'), fs=44100, resolution_octave=1, harmonics=0, beta=0.1):

    faux = np.linspace(fmin, fmax, (fmax-fmin)*resolution_octave)
    filter_aux = np.zeros((len(faux), len(f0_array)))
    for j in range(0, len(f0_array)):
        if f0_array[j] == 0:
            filter_aux[:,j] = beta*np.ones(len(faux))
        else:
            idx=resolution_octave*int(f0_array[j]-fmin)
            filter_aux[idx, j] = 1
            if harmonics > 0: 
                if (idx+12*resolution_octave) < len(faux): #octava
                    filter_aux[idx+12*resolution_octave, j] = 1
                if harmonics > 1:    
                    if (idx+19*resolution_octave) < len(faux): #octava + quinta
                        filter_aux[idx+19*resolution_octave, j] = 1
                        if harmonics > 2:    
                            if (idx+24*resolution_octave) < len(faux): #octava + quinta
                                filter_aux[idx+24*resolution_octave, j] = 1            
                            if harmonics > 3:    
                                if (idx+28*resolution_octave) < len(faux): #octava + quinta
                                    filter_aux[idx+28*resolution_octave, j] = 1
                                if harmonics > 4:    
                                    if (idx+31*resolution_octave) < len(faux): #octava + quinta
                                        filter_aux[idx+31*resolution_octave, j] = 1 
                                    if harmonics > 5:    
                                        if (idx+34*resolution_octave) < len(faux): #octava + quinta
                                            filter_aux[idx+31*resolution_octave, j] = 1   


    return filter_aux