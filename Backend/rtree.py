import face_recognition
from os import listdir
import rtree

mypath = '/Users/fabriziovasquez/Downloads/DB2/Proyecto03/ProyectoIIIBaseDeDatosII/Resources/lfw'

onlyfiles = [f for f in listdir(mypath)]

def face_vector(file_stream):
    img = face_recognition.load_image_file(file_stream)
    unkown_face_encoding = face_recognition.face_encodings(img)
    return unkown_face_encoding







