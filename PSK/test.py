#!/usr/bin/env python  
# -*- coding: utf-8 -*-  
__author__ = 'xanxus'  
s1 = "11111111111000000011111100000111111100001111111111000011111111110111111111100000000111111000000000000000000011111111000000000000000111111111100000011111000011111111111111110000011111111111111100000000" 
s2 = "00000000000000000000111111110000000000000000111111111000000001111000011111111111000000111100000001111111100000000000000000111111000000000000000000000000011111111110000000000000000111111111000000000000"
m, n = len(s1), len(s2)  
colsize, matrix = m + 1, []  
for i in range((m + 1) * (n + 1)):  
    matrix.append(0)  
for i in range(colsize):  
    matrix[i] = i  
for i in range(n + 1):  
    matrix[i * colsize] = i  
for i in range(n + 1)[1:n + 1]:  
    for j in range(m + 1)[1:m + 1]:  
        cost = 0  
        if s1[j - 1] == s2[i - 1]:  
            cost = 0  
        else:  
            cost = 1  
        minValue = matrix[(i - 1) * colsize + j] + 1  
        if minValue > matrix[i * colsize + j - 1] + 1:  
            minValue = matrix[i * colsize + j - 1] + 1  
        if minValue > matrix[(i - 1) * colsize + j - 1] + cost:  
            minValue = matrix[(i - 1) * colsize + j - 1] + cost  
        matrix[i * colsize + j] = minValue  
print matrix[n * colsize + m]  
