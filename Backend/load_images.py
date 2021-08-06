import face_recognition
from collections import defaultdict
import os
from os import listdir
import numpy as np
import pickle
from os.path import isfile, join
mypath = '/Users/fabriziovasquez/Downloads/DB2/Proyecto03/ProyectoIIIBaseDeDatosII/Resources/lfw'

# Los vectores característicos luego de cargarse se guardaron en memoria secundaria en ../Resources/dataset_faces.dat
# Si deseas comprobar los mismos solo descomenta la funcion READ_FACES()

all_path_images = []
all_face_encodings = {}
all_sorted_encodings = {}

for path, subdirs, files in os.walk(mypath):
    for name in files:
        all_path_images.append(os.path.join(path, name))

def load_faces():
    for path_image in all_path_images:
        name_picture = os.path.basename(path_image).split('0', 1)[0]
        clean_name = name_picture[:len(name_picture)-1]
        picture = face_recognition.load_image_file(path_image)
        #face_encoding = face_recognition.face_encodings(picture)[0]
        try:
            if clean_name not in all_face_encodings:
                all_face_encodings[clean_name] = []
                all_face_encodings[clean_name].append(face_recognition.face_encodings(picture)[0])
            else:
                all_face_encodings[clean_name].append(face_recognition.face_encodings(picture)[0])
            print(clean_name)
            #print(f'Se cargo correctamente el {face_recognition.face_encodings(picture)[0]}')
        except IndexError as e:
            pass
            #print(f'NO SE CARGO LA {path_image}')
    with open('../Resources/dataset_faces1.dat', 'wb') as f:
        pickle.dump(all_face_encodings, f)
    print(f'Todo se cargo de correctamente')

#load_faces()

def read_faces(N):
    with open('../Resources/dataset_faces1.dat', 'rb') as f:
	    all_face_encodings = pickle.load(f)

    face_names = list(all_face_encodings.keys())
    face_encodings = np.array(list(all_face_encodings.values()))
    #print(all_face_encodings['Abdullah'])
    #print(face_names)
    #print(face_encodings)
    #print(len(all_face_encodings))
    sum=0
    all_sorted_encodings = sorted(all_face_encodings)[:N]
    for i in all_sorted_encodings:
        print(i, all_face_encodings[i])

read_faces(5749)