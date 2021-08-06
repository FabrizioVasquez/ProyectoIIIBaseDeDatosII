import face_recognition
from flask import Flask, jsonify, request, redirect
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

# You can change this to any folder on your system
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET', 'POST'])
def upload_image():
    # Check if a valid image file was uploaded
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)

        file = request.files['file']
        if file.filename == '':
            return redirect(request.url)

        if file and allowed_file(file.filename):
            # The image file seems valid! Detect faces and return the result.
            return detect_faces_in_image(file, 5)

    # If no valid image file was uploaded, show the file upload form:
    return '''
    <!doctype html>
    <title>Busca tu Doppelganger</title>
    <h1>Busca tu doppelganger</h1>
    <form method="POST" enctype="multipart/form-data">
      <input type="file" name="file">
      <p>Ingresa valor K
      <input type="text" name = "kvalue">
      <input type="submit" value="Cargar">
    </form>
    '''


def detect_faces_in_image(name, N):
    arbolitos = []
    for i in range(TREES):
        arbolitos.append(index.Index())

    
    imagen = read_faces(5720)

    for i in range(len(imagen)):
        for j in range(64):
            arbolitos[j].insert(i, list(imagen[i][j]))

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
        Ans_generator.append(arbolitos[i].nearest(final_query[i], N))

    real_answers = []
    for i in Ans_generator:
        for j in range(N):
            real_answers.append(next(i))

    real_answers_names = []

    for i in real_answers:
        real_answers_names.append(general_index[i])

    result = sorted(real_answers, key=real_answers.count, reverse = True)
    result_count = 0
    true_result = []
    for i in result:
        if i not in true_result:
            true_result.append(i)
    resultaditos = {}
    for i in range (N):
        resultaditos[i] = str(true_result[i]) + " " + general_index[true_result[i]]

    return resultaditos

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
            answer[count] = []
            general_index[count] = i
            counter_low = 0
            counter_top = 2
            for j in range(64):
                answer[count].append(temp_array[k][counter_low : counter_top])
                counter_top+=2
                counter_low+=2
            count +=1
        #print(i, all_face_encodings[i])
    return answer

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001, debug=True)
