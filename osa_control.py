# -*- coding: utf-8 -*-
"""
Created on Mon Nov  2 09:36:10 2020

@author: andrei

v1. 10 Nov 2020
"""

import visa
import numpy as np

rm = visa.ResourceManager()
# print(rm.list_resources())


# ANDO AQ6315A grey old: 'GPIB0::1::INSTR'
ANDO = rm.open_resource('GPIB0::1::INSTR')
# print(ANDO_6315A.query('*IDN?'))

def get_trace(trace):
    # remove the leading and the trailing characters, split values, remove the first value showing number of values in a dataset
    wl = ANDO.query('WDAT'+trace).strip().split(',')[1:]
    intensity = ANDO.query('LDAT'+trace).strip().split(',')[1:]
    # list of strings -> numpy array (vector) of floats
    wl = np.asarray(wl,'f').T
    intensity = np.asarray(intensity,'f').T
    return wl, intensity


def save_trace(wl, intensity, filename):
    wl = np.asarray(wl,'str')
    intensity = np.asarray(intensity,'str')
    data = np.column_stack((wl, intensity))
    
    with open(filename+'.txt', "w") as txt_file:
        for line in data:
            txt_file.write(" ".join(line) + "\n")
    # todo: add exception handler
    return

def print_hint():
    print('COMMANDS:')
    print('    save             Save active trace to file')
    print('    range            Set range in nm')
    print('    ref              Set reference level (-90.0 to 20.0 dBm)')
    print('    res              Set resolution (0.05 to 10 nm)')
    print('    active *         Set active trace A,B or C')
    print('    disp *           Show a trace')
    print('    blank *          Hide a trace')
    print('    write *          Set a trace write mode')
    print('    fix *            Set a trace fixed data mode')
    print('                     Sweep:')
    print('    auto sweep         AUTO')
    print('    single             SINGLE')
    print('    repeat             REPEAT')
    print('    stop               STOP')
    print('                     Sensitivity:')
    print('    hold               HOLD')
    print('    auto               AUTO')
    print('    high1              HIGH 1')
    print('    high2              HIGH 2')
    print('    high3              HIGH 3')
    print('    exit             Close the program')
    print('')
    


print_hint()

while True:
    command = input('>>> ')
    if command == 'hint':
        print_hint()
        
    elif command == 'save':
        trace = input('Trace: ').upper()
        wl, intensity = get_trace(trace)
        filename = input('Filename: ')
        save_trace(wl, intensity, filename)
        print("Done! File saved.")
        
    elif command == 'range':
        start = input('Start wl: ')
        ANDO.query('STAWL'+start+'.00')
        stop = input('Stop wl: ')
        ANDO.query('STPWL'+stop+'.00')
        
    elif command == 'ref':
        ref = input('Ref. level: ')
        ANDO.query('REFL'+ref+'.0')
        
    elif command == 'res':
        res = input('Resolution: ')
        ANDO.query('RESLN'+res)
        
    elif command[:-2] == 'active':
        if command[-1:].upper() == 'A':
            trace = '0'
        elif command[-1:].upper() == 'B':
            trace = '1'
        elif command[-1:].upper() == 'C':
            trace = '2'
        ANDO.query('ACTV'+trace)
        
    elif command[:-2] == 'disp':
        ANDO.query('DSP'+command[-1:].upper())
    
    elif command[:-2] == 'blank':
        ANDO.query('BLK'+command[-1:].upper())
        
    elif command[:-2] == 'write':
        ANDO.query('WRT'+command[-1:].upper())
    
    elif command[:-2] == 'fix':
        ANDO.query('FIX'+command[-1:].upper())
        
    elif command == 'auto':
        ANDO.query('AUTO')
    
    elif command == 'single':
        ANDO.query('SGL')
    
    elif command == 'repeat':
        ANDO.query('RPT')
    
    elif command == 'stop':
        ANDO.query('STP')
    
    elif command == 'hold':
        ANDO.query('SNHD')
    
    elif command == 'auto sens':
        ANDO.query('SNAT')
    
    elif command == 'high1':
        ANDO.query('SHI1')
    
    elif command == 'high2':
        ANDO.query('SHI2')
        
    elif command == 'high3':
        ANDO.query('SHI3')
    
    elif command == 'exit':
        ANDO.close()
        break
    
    else:
        continue
