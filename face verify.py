import os
import cv2
from PIL import Image
from matplotlib import pyplot as plt
import numpy as np
import face_recognition
import keras
from keras.models import load_model
import xlsxwriter 

workbook = xlsxwriter.Workbook('Output.xlsx') 
worksheet = workbook.add_worksheet()
row = 0
column = 0
id_dir= "id/" #folder containing registered ID card photos of all students with ID number as filename
webcam_dir= "webcam/" #folder containing webcam photos of students (5 photos each) captured during examination (filename format - idNo_1,2,...5)

for id in os.listdir(id_dir):
    id_no= id.split('.')[0]
    worksheet.write(row, column, str(id_no)) #write the ID number in the first column of the excel sheet
    column =1
    id_image = face_recognition.load_image_file(id_dir + id)
    print(id_no + ":")
    for i in range(1,6):
        webcam_image = face_recognition.load_image_file(webcam_dir + id_no + "_" + str(i) + ".jpg")
 
        encoding_1 = face_recognition.face_encodings(id_image)[0]

        encoding_2 = face_recognition.face_encodings(webcam_image)[0]

        results = face_recognition.compare_faces([encoding_1], encoding_2,tolerance=0.50) #comparing encodings of id card image and webcam image to verify similarity - returns true if matches, else false
        print(results)
        worksheet.write(row, column, str(results)) #write result of each comparision against the id no 
        column += 1
    row +=1
    column =0
    
workbook.close() 
