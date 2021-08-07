import face_recognition
import time
from os import listdir, read
import numpy as np
import pickle
from os.path import isfile, join
from numpy.lib.type_check import real
from rtree import index
import math
import operator


mypath = '/home/jpalexander1706/BDII/proyecto/ProyectoIIIBaseDeDatosII/Resources/lfw'

TREES = 128
general_index = {}

def read_faces_clean(N):
    with open('/home/jpalexander1706/BDII/proyecto/ProyectoIIIBaseDeDatosII/Resources/dataset_faces1.dat', 'rb') as f:
	    all_face_encodings = pickle.load(f)

    face_names = list(all_face_encodings.keys())
    face_encodings = np.array(list(all_face_encodings.values()))
    #print(all_face_encodings['Abdullah'])
    #print(face_names)
    #print(face_encodings)
    #print(len(all_face_encodings))
    sum=0
    all_sorted_encodings = sorted(all_face_encodings)[:N]
    answer = {}
    count = 0
    for i in all_sorted_encodings:
        temp_array = list(all_face_encodings[i])
        for k in range(len(temp_array)):
            answer[count] = temp_array[k]
            count+=1
    return answer
    

def read_faces(N):
    with open('/home/jpalexander1706/BDII/proyecto/ProyectoIIIBaseDeDatosII/Resources/dataset_faces1.dat', 'rb') as f:
	    all_face_encodings = pickle.load(f)
    
    face_names = list(all_face_encodings.keys())
    face_encodings = np.array(list(all_face_encodings.values()))
    answer = {}
    count = 0
    #print(face_names)
    #print(face_encodings)
    
    all_sorted_encodings = sorted(all_face_encodings)[:N]
    for i in all_sorted_encodings:
        temp_array = list(all_face_encodings[i])
        
        for k in range(len(temp_array)):
            general_index[count] = i
            counter_low = 0
            counter_top = 2
            answer[count] = list(temp_array[k])
            count +=1
        #print(i, all_face_encodings[i])
    return answer

def face_vector(file_stream):
    img = face_recognition.load_image_file(file_stream)
    unkown_face_encoding = face_recognition.face_encodings(img)
    return unkown_face_encoding

def KNN_Rtree(name, N):
    properties = index.Property()
    properties.dimension = 128
    properties.dat_extension = 'data'
    properties.idx_extension = 'index'  
    
    arbol = index.Index("MyIdex", properties = properties)

    imagen = read_faces(5749)

    for i in range(len(imagen)):
        arbol.insert(i, imagen[i])
    

    picture = face_recognition.load_image_file(name)
    query = list(face_recognition.face_encodings(picture)[0])
    answer = arbol.nearest(query, N)
    print(general_index[next(answer)])
    
    

def KNN_sequential(name, N, size):
    answer = {}

    picture = face_recognition.load_image_file(name)
    query = (face_recognition.face_encodings(picture)[0])
    
    #final_query = query
    data = read_faces_clean(size)
    for i in data.keys():
        partial_sum = 0.0
        for j in range(len(data[i])):
            partial_sum += abs(data[i][j] - query[j])**2
        answer_partial = math.sqrt(partial_sum)
        answer[i] = answer_partial
    answer_sorted = sorted(answer.items(), key=operator.itemgetter(1), reverse=False)
    
    return answer_sorted[:N]

def Range_sequential(name, rango):
    answer = {}

    picture = face_recognition.load_image_file(name)
    query = (face_recognition.face_encodings(picture)[0])
    
    #final_query = query
    data = read_faces_clean(5749)
    for i in data.keys():
        partial_sum = 0.0
        for j in range(len(data[i])):
            partial_sum += abs(data[i][j] - query[j])**2
        answer_partial = math.sqrt(partial_sum)
        if answer_partial < rango:
            answer[i] = answer_partial    
    return len(answer)

#KNN_Rtree("mateo.jpg", 10)

#KNN_Rtree("mateo.jpg", 10)




"""
for i in KNN_sequential("mateo.jpg", 10, 5740):
    print(general_index[i[0]] , " ", i)
"""


#print(read_faces(1))
#TEST N = 100
"""
start = time.time()
KNN_sequential("mateo.jpg", 10, 100)
fin = time.time()
print(fin-start)
"""
#TEST N = 200
"""
start = time.time()
KNN_sequential("mateo.jpg", 10, 200)
fin = time.time()
print(fin-start)
"""
#TEST N = 400
"""
start = time.time()
KNN_sequential("mateo.jpg", 10, 400)
fin = time.time()
print(fin-start)
"""
#TEST N = 800
"""
start = time.time()
KNN_sequential("mateo.jpg", 10, 800)
fin = time.time()
print(fin-start)
"""
#TEST N = 1600
"""
start = time.time()
KNN_sequential("mateo.jpg", 10, 1600)
fin = time.time()
print(fin-start)
"""
#TEST N = 3200
"""
start = time.time()
KNN_sequential("mateo.jpg", 10, 3200)
fin = time.time()
print(fin-start)
"""
#TEST N = 6400
"""
start = time.time()
KNN_sequential("mateo.jpg", 10, 5000)
fin = time.time()
print(fin-start)
"""
#TEST N = 12800
"""
start = time.time()
KNN_sequential("mateo.jpg", 10, 5749)
fin = time.time()
print(fin-start)
"""

#print(Range_sequential("mateo.jpg", 0.8))