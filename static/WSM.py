import numpy as np
import math

def initiation (matrix, weight):
    if type(matrix) != np.ndarray:  
        matrix = np.array(matrix)
    else:
        matrix = matrix
            
    if type(weight) != np.ndarray:  
        weight = np.array(weight)
    else:
        weight = weight
    print(matrix,weight)
    return 

def horizontalSum(matrix):
    return np.sum(matrix, axis=1)

def criteriaBenefitNormalisation(matriks):
    baris = len(matriks)
    kolom = len(matriks[0])
    normalized = np.zeros((baris, kolom))
    maxValuesVertical = np.max(matriks, axis=0)
    print(maxValuesVertical)

    for row in range (baris):
        for column in range (kolom):
            normalized[row][column]= matriks[row][column] / maxValuesVertical[column]

    return normalized



def criteriaCostNormalisation(matriks):
    baris = len(matriks)
    kolom = len(matriks[0])
    normalized = np.zeros((baris, kolom))
    minValuesVertical = np.min(matriks, axis=0)
    print(minValuesVertical)
    for row in range (baris):
        for column in range (kolom):
            normalized[row][column]= minValuesVertical[column]/matriks[row][column] 
    
    return normalized

def combine(matrix1,matrix2):
    return np.concatenate((matrix1, matrix2), axis=0)

def wsm(matrix,weight):
    baris = len(matrix)
    kolom = len(matrix[0])

    result = np.zeros((baris, kolom))
    for row in range (baris):
        for column in range (kolom):
            result[row][column]= matrix[column]*result[row][column] 

    return result

def wpm(matrix,weight):
    baris = len(matrix)
    kolom = len(matrix[0])

    result = np.zeros((baris, kolom))
    for row in range (baris):
        for column in range (kolom):
            result[row][column]= matrix[column]^result[row][column] 

    return result

benefit = np.array([[2, 2, 3],
                [2, 3, 3],
                [3, 2, 4]])

cost = np.array([[2, 7],
                 [1, 2],
                 [2, 4]])

print (criteriaBenefitNormalisation(benefit))
print(criteriaCostNormalisation(cost))