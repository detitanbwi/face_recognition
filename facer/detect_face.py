import face_recognition
import cv2
import numpy as np
import sys
import os

# Mendapatkan parameter dari command line
user_id = sys.argv[1]
test_image_path = sys.argv[2]
encoding_file_path = sys.argv[3]

# Memuat encoding wajah yang sudah disimpan
if not os.path.exists(encoding_file_path):
    print("Encoding wajah tidak ditemukan untuk user_id:", user_id)
    sys.exit(1)

known_face_encoding = np.load(encoding_file_path)

# Membaca gambar testing
test_image = cv2.imread(test_image_path)
if test_image is None:
    print("Error loading test image.")
    sys.exit(1)

rgb_test_image = cv2.cvtColor(test_image, cv2.COLOR_BGR2RGB)

# Mencari lokasi dan encoding wajah pada gambar testing
face_encodings = face_recognition.face_encodings(rgb_test_image)

# Jika tidak ada wajah terdeteksi
if len(face_encodings) == 0:
    print("Error: Tidak ada wajah yang terdeteksi.")
    sys.exit(1)

# Jika lebih dari 1 wajah terdeteksi, return error
if len(face_encodings) != 1:
    print("Error: Lebih dari satu wajah terdeteksi pada gambar testing.")
    sys.exit(1)

# Menghitung tingkat kemiripan
face_encoding = face_encodings[0]
face_distance = face_recognition.face_distance([known_face_encoding], face_encoding)[0]
similarity = 1 - face_distance

# Tentukan threshold similarity (misalnya 50% atau 0.5)
threshold = 0.5

# Menampilkan hasil kecocokan jika similarity lebih besar dari threshold
if similarity >= threshold:
    print("True")
    print(similarity)  # Menyertakan nilai kemiripan
else:
    print("False")

sys.exit(0)
