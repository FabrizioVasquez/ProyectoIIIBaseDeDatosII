import face_recognition
from os import listdir, read
import numpy as np
import pickle
from os.path import isfile, join
from numpy.lib.type_check import real
from rtree import index
import math
import operator


mypath = '/home/jpalexander1706/BDII/proyecto/ProyectoIIIBaseDeDatosII/Resources/lfw'

general_index = {}

def read_faces_clean(N):
    with open('/home/jpalexander1706/BDII/proyecto/ProyectoIIIBaseDeDatosII/Resources/dataset_faces.dat', 'rb') as f:
	    all_face_encodings = pickle.load(f)

    face_names = list(all_face_encodings.keys())
    face_encodings = np.array(list(all_face_encodings.values()))
    #print(face_names)
    #print(face_encodings)
    all_sorted_encodings = sorted(all_face_encodings)[:N]
    answer = {}
    for i in all_sorted_encodings:
        answer[i] = all_face_encodings[i]
    return answer

def read_faces(N):
    with open('/home/jpalexander1706/BDII/proyecto/ProyectoIIIBaseDeDatosII/Resources/dataset_faces.dat', 'rb') as f:
	    all_face_encodings = pickle.load(f)
    face_names = list(all_face_encodings.keys())
    face_encodings = np.array(list(all_face_encodings.values()))
    answer = {}
    count = 0
    #print(face_names)
    #print(face_encodings)
    print(len(all_face_encodings))
    all_sorted_encodings = sorted(all_face_encodings)[:N]
    for i in all_sorted_encodings:
        counter_low = 0
        counter_top = 2
        temp_array = all_face_encodings[i].tolist()
        answer[count] = []
        general_index[count] = i
        for j in range(64):
            answer[count].append(temp_array[counter_low : counter_top])
            counter_top+=2
            counter_low+=2
        count +=1
        #print(i, all_face_encodings[i])
    return answer

def face_vector(file_stream):
    img = face_recognition.load_image_file(file_stream)
    unkown_face_encoding = face_recognition.face_encodings(img)
    return unkown_face_encoding

def KNN_Rtree(name):
    arbolitos = []
    for i in range(64):
        arbolitos.append(index.Index())

#for i in range(64):
    
    imagen = read_faces(5720)
    for i in range(5720):
        for j in range(64):
            arbolitos[j].insert(i, imagen[i][j])

    #query = read_faces(1)[0]
    picture = face_recognition.load_image_file(name)
    query = (face_recognition.face_encodings(picture)[0])
    final_query = []
    counter_low = 0
    counter_top = 2
    count = 0
    for j in range(64):
        final_query.append(query[counter_low : counter_top].tolist())
        counter_top+=2
        counter_low+=2


    Ans_generator = []
    for i in range(64):
        Ans_generator.append(arbolitos[i].nearest(final_query[i], 5))

    real_answers = []
    for i in Ans_generator:
        real_answers.append(next(i))
        real_answers.append(next(i))
        real_answers.append(next(i))
        real_answers.append(next(i))
        real_answers.append(next(i))

    newlist = []
    frequency = []
    real_answers.sort()

    result = sorted(real_answers, key=real_answers.count, reverse = True)
    result_count = 0
    true_result = []
    for i in result:
        if i not in true_result:
            true_result.append(i)
    for i in range (10):
        print(general_index[true_result[i]])
    

def KNN_sequential(name):
    answer = {}

    picture = face_recognition.load_image_file(name)
    query = (face_recognition.face_encodings(picture)[0])
    
    #final_query = query
    data = read_faces_clean(5720)
    for i in data.keys():
        partial_sum = 0.0
        for j in range(len(data[i])):
            partial_sum += abs(data[i][j] - query[j])**2
        answer_partial = math.sqrt(partial_sum)
        answer[i] = answer_partial
    answer_sorted = sorted(answer.items(), key=operator.itemgetter(1), reverse=False)
    return answer_sorted[:5]

def Range_sequential(name, range):
    answer = {}

    picture = face_recognition.load_image_file(name)
    query = (face_recognition.face_encodings(picture)[0])
    
    #final_query = query
    data = read_faces_clean(5720)
    for i in data.keys():
        partial_sum = 0.0
        for j in range(len(data[i])):
            partial_sum += abs(data[i][j] - query[j])**2
        answer_partial = math.sqrt(partial_sum)
        if answer_partial < range:
            answer[i] = answer_partial
    return answer[:5]

KNN_Rtree("mateo.jpg")
print(KNN_sequential("mateo.jpg"))
