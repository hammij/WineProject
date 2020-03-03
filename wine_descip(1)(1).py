# -*- coding: utf-8 -*-
"""
Group Members: Anthony Deniro, Hamilton Pitlik
Date: 1/23/19
Description: Script that generates descriptions for wine provided a variety, price range, and point range

"""

import pandas as pd
import random as rnd
#quartile values for prices
q0 = 4
q1 = 16
q2 = 24
q3 = 40
q4 = 2300
#quartile values for points
p0 = 80
p1 = 86
p2 = 88
p3 = 90
p4 = 100

def readIn(fileIn):
    df = pd.read_csv(fileIn)
    df = df.dropna()
    return df

def getpointMinMax(point_range):
    mini = 0
    maxi = 0
    if(point_range <= p1):
        mini = p0
        maxi = p1
    elif(point_range > p1 and point_range <= p2):
        mini = p1
        maxi = p2
    elif(point_range > p2 and point_range <= p3):
        mini = p2
        maxi = p3
    else:
        mini = p3
        maxi = p4
    return (mini, maxi)

def getpriceMinMax(price_range):
    mini = 0
    maxi = 0
    if(price_range <= q1):
        mini = q0
        maxi = q1
    elif(price_range > q1 and price_range <= q2):
        mini = q1
        maxi = q2
    elif(price_range > q2 and price_range <= q3):
        mini = q2
        maxi = q3
    else:
        mini = q3
        maxi = q4
    return (mini, maxi)

def getVariety_table(variety):
    variety_list = []
    df = readIn('C:Desktop/Wine/winemag-data_first150k.csv')
    for i in range(len(df)):
        line = df.iloc[i]
        wine_var = line[4]
        if(wine_var == variety):
            variety_list.append(line)
    return variety_list

def getPoint_table(v_table, point_range):
    point_list = []
    extrema = getpointMinMax(point_range)
    for item in v_table:
        if(item[2] >= extrema[0] and item[2] <= extrema[1]):
            point_list.append(item)
    return point_list
    
def getPrice_table(p_table, price_range):
    price_list = []
    try:
        extrema = getpriceMinMax(price_range)
        for item in p_table:
            if(item[3] >= extrema[0] and item[3] <= extrema[1]):
                price_list.append(item)
    except:
        print('Price not within range')
    return price_list

def uniqueWords(clean_data):    #clean data is our list of wines that meet conditions
    em_string = ''
    for i in range(len(clean_data)):
        curr = clean_data[i]
        em_string += curr[1]+' '
    uniq_pd = pd.unique(em_string.split())
    uniq_list = []
    for item in uniq_pd:
        uniq_list.append(item)
    return uniq_list

def firstWords(clean_data):
    em_string = ''
    for i in range(len(clean_data)):
        curr = clean_data[i]
        em_string += curr[1] + ' '
    split_text = em_string.split()
    fWords_list = []
    for i in range(len(split_text)):
        curr_word = split_text[i]
        if (i == 0):
            fWords_list.append(curr_word)
        else:
            if(curr_word.istitle() and '.' in split_text[i-1]):
                fWords_list.append(curr_word)
    return fWords_list

def uniqueFirsts(f_words):
    uniq_first = []
    pd_uniq = pd.unique(f_words)
    for words in pd_uniq:
        uniq_first.append(words)
    return uniq_first

def matrixFWords(uniq_fwords):
    param = len(uniq_fwords)
    matrix = []
    for i in range(param):
        matrix.append(0)
    return matrix

def fillFMatrix(matrix, uniq_fwords, f_words):
    for i in range(len(uniq_fwords)):
        curr_word = uniq_fwords[i]
        for j in range(len(f_words)):
            match = f_words[j]
            if(curr_word == match):
                matrix[uniq_fwords.index(curr_word)] += 1
    return matrix

def firstMatrix(matrix):
    total = 0
    for i in matrix:
        total += i
    for j in range(len(matrix)):
        matrix[j] = round((matrix[j]/total)*100)
    return matrix

def uniqueMatrix(uniq_list):
    param = len(uniq_list)
    matrix = []
    for i in range(param):
        matrix.append({})
        for j in range(param):
            word = uniq_list[j]
            row = matrix[i]
            row[word] = 0
    return matrix

def fillUnique(matrix, unique_words, v_table):
    em_string = ''
    for i in range(len(v_table)):
        curr = v_table[i]
        desc = curr[1]
        em_string += desc + ' '
    split_text = em_string.split()
    for i in range(len(split_text)-1):
        if(i > 0):
            current_word = split_text[i]
            if(current_word in unique_words):
                row_position = matrix[unique_words.index(current_word)]
                if(split_text[i+1] in unique_words):
                    row_position[split_text[i+1]] += 1
    return matrix
    

def transitionMatrix(matrix, unique_words):
    keys = unique_words
    height = len(matrix)
    for i in range(height):
        position = matrix[i]
        total = 0
        for key in keys:
            total += position[key]
        if(total != 0):
            for key in keys:
                position[key] = round(float(position[key]/total)*100)
    return matrix

def writeScentence(f_matrix, t_matrix, uniq_f, uniq_w):
    try:
        scentence = []
        prev_word = ''
        length = rnd.randint(15,20)
        #selecting first word
        f_match = rnd.randint(1,100)
        t_percent = 0
        for i in range(len(f_matrix)):
            c_percent = f_matrix[i]
            t_percent += c_percent
            if(t_percent >= f_match):
                scentence.append(uniq_f[i])
                prev_word = str(uniq_f[i])
                length -= 1
                break
    #selecting subsequent words
        while(length > 0):
            w_match = rnd.randint(1,100)
            row_position = t_matrix[uniq_w.index(prev_word)]
            t_percent = 0
            for word in uniq_w:
                c_percent = row_position[word]
                t_percent += c_percent
                if(t_percent >= w_match):
                    scentence.append(word)
                    prev_word = word
                    length -= 1
                    break
        return scentence
    except:
        print('Something went wrong when writing this scentence.')

def listToScentence(desc_list):
    to_print = ''
    for item in desc_list:
        to_print += item+' '
    return to_print

def exists(variety, price, point):
    nar = getVariety_table(variety)
    nar = getPrice_table(nar, price)
    nar = getPoint_table(nar, point)
    if(len(nar)!=0):
        print('Exists')
    else:
        print('No-entries match')

def results(variety, price, point):
    clean_data = getVariety_table(variety)
    clean_data = getPrice_table(clean_data, price)
    clean_data = getPoint_table(clean_data, point)
    first_words = firstWords(clean_data)
    unique_firsts = uniqueFirsts(first_words)
    unique_words = uniqueWords(clean_data)
    first_word_matrix = firstMatrix(fillFMatrix(matrixFWords(unique_firsts), unique_firsts, first_words))
    transition_matrix = transitionMatrix(fillUnique(uniqueMatrix(unique_words), unique_words, clean_data), unique_words)
    scentence = listToScentence(writeScentence(first_word_matrix, transition_matrix, unique_firsts, unique_words))
    scentence1 = listToScentence(writeScentence(first_word_matrix, transition_matrix, unique_firsts, unique_words))
    return (scentence, scentence1)
    
    
    
    