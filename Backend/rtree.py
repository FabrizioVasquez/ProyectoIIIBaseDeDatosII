import face_recognition
from os import listdir
import numpy as np
import pickle
from os.path import isfile, join
from rtree import index



mypath = '/home/jpalexander1706/BDII/proyecto/ProyectoIIIBaseDeDatosII/Resources/lfw'

general_index = {}

faces = []

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

arbolitos = []
for i in range(64):
    arbolitos.append(index.Index())

#for i in range(64):
    
imagen = read_faces(5720)
for i in range(5720):
    for j in range(64):
        arbolitos[j].insert(i, imagen[i][j])

Ans_generator = []
for i in range(64):
    Ans_generator.append(arbolitos[i].nearest([0.20, 0.35], 5))

real_answers = []
for i in Ans_generator:
    real_answers.append(next(i))
    real_answers.append(next(i))
    real_answers.append(next(i))
    real_answers.append(next(i))
    real_answers.append(next(i))






