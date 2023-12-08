# -*- coding: utf-8 -*-
"""
Created on Wed Dec  6 15:38:00 2023

@author: alebu
"""

import numpy as np
import pandas as pd
import random

def sum_cifre(n):
    if n < 10:
        return n
    
    return sum_cifre(sum([int(x) for x in list(str(n))]))

def generate_pool():
    pool = [list(range(x0, x0 + 10)) for x0 in range(0, 90, 10)]
    pool[0].pop(0)
    pool[-1].append(90)
    for _l in pool:
        random.shuffle(_l)
    #random.shuffle(pool)
    return pool

def flat_list(l):
    return [item for sublist in l for item in sublist]


def numeri_usati(cartelle):
    _x = np.array(flat_list(cartelle)).copy()
    _x.sort()
    return _x[_x>0]

def check_cartelle(cartelle):
    # check that there are 5 numbers per row:
    for index, cartella in enumerate(cartelle):
        for row in cartella:
            assert row[row > 0].size == 5, f"Cartella {index + 1} ha una riga non con 5 elementi"
    
    # Check that all 90 numbers have been used
    numeri_usati = np.array(flat_list(cartelle)).flatten()
    numeri_usati = numeri_usati[numeri_usati > 0]
    numeri_usati.sort()
    assert np.array_equal(numeri_usati, np.arange(1, 91).astype(np.int_)) 
           
    

def gestisci_resti(cartelle):
    global pool
    
    if not pool:
        return cartelle
    
    def parse_numero_rimasto(cartelle):
        global pool
        
        numero_rimasto = pool[0]
        decina_rimasta = numero_rimasto // 10 if numero_rimasto < 90 else 8
        
        # cartella_source: verrà prelevato un numero da passare a cartella_dest- 
        #                  numero_rimasto verrà inserito qui
        # cartella_dest: ha una riga con <5 elementi: un numero da cartella_source
        #                riempirà la riga
                
        for index_cartella_source, cartella_source in enumerate(cartelle):
            for row_source in cartella_source:
                if row_source[row_source>0].size < 5:
                    continue
                
                # Non posso inserire qui il numero rimasto (la colonna è piena)
                if row_source[decina_rimasta] > 0:
                    continue
                
            
                for index_cartella_dest, cartella_dest in enumerate(cartelle):
                    for row_dest in cartella_dest:
                        # Qui non posso copiare nulla
                        if (row_dest[row_dest > 0].size == 5):
                            continue
                                                            
                        # Devo cercare dove posso copiare il numero della cartella_source         
                        for col_dest in [col_dest for col_dest in range(9) if not col_dest==decina_rimasta]:
                            
                            # Deve esserci un numero in cartella_source da copiare in cartella_dest
                            if row_source[col_dest] == 0:
                                continue
                            
                            if row_dest[col_dest] > 0:
                                continue
                            
                            row_dest[col_dest] = row_source.copy()[col_dest]
                            row_source[col_dest] = 0
                            row_source[decina_rimasta] = numero_rimasto
                            pool.pop(0)
                            return    
    
    
    while pool:
        parse_numero_rimasto(cartelle)
                                
    return gestisci_resti(cartelle)
    

def generate_cartelle():
    global pool
    
    cartelle = []
    pool = generate_pool()
    for i in range(6):
        arr = np.zeros((3, 9), dtype=np.int_)
        
        for row in range(3):
            cinquina = random.sample(range(9), 5)
            
            for decina in cinquina:
                # Se ci sono ancora numeri disponibili per quella decina,
                # altrimenti lasciali lì che verranno gestiti dai resti
                if pool[decina]:
                    sample = random.choice(pool[decina])
                    pool[decina].remove(sample)
                    
                    arr[row, decina] = sample      
                
        cartelle.append(arr)

            
    pool = flat_list(pool)
    
    assert numeri_usati(cartelle).size + len(pool) == 90
    
    cartelle = gestisci_resti(cartelle)
    
    # Order the arrays
    for arr in cartelle:
        for col in range(9):
            x = arr[:,col].copy()
            x = x[x>0]
            x.sort()
            arr[:,col][arr[:,col]>0]=x.copy()

    check_cartelle(cartelle)
    return cartelle

cartelle = generate_cartelle()
