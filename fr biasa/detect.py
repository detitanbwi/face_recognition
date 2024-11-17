import cv2
import face_recognition
import numpy as np
import sys
import os

# Ambil nama orang yang akan diuji dari argumen input
if len(sys.argv) != 3:
    print("Usage: python recognize.py <nama> <path_gambar_test>")
    sys.exit(1)

nama_orang = sys.argv[1]
test_image_path = sys.argv[2]

train_dir = "train"
person_dir = os.path.join(train_dir, nama_orang)
encoding_file_path = os.path.join(person_dir, f"{nama_orang}_encoding.npy")

# Mengecek apakah encoding sudah ada
if not os.path.isfile(encoding_file_path):
    print(f"Encoding untuk {nama_orang} belum dibuat. Jalankan train.py terlebih dahulu.")
    sys.exit(1)

# Load encoding yang sudah disimpan
known_face_encoding = np.load(encoding_file_path)
known_face_name = nama_orang

# Membaca gambar testing
test_image = cv2.imread(test_image_path)
if test_image is None:
    print("Error loading test image.")
    sys.exit(1)

rgb_test_image = cv2.cvtColor(test_image, cv2.COLOR_BGR2RGB)

# Mencari lokasi dan encoding wajah pada gambar testing
face_encodings = face_recognition.face_encodings(rgb_test_image)

# Jika lebih dari 1 wajah terdeteksi, return error
if len(face_encodings) != 1:
    print("Error: Lebih dari satu wajah terdeteksi pada gambar testing.")
    sys.exit(1)

# Menghitung tingkat kemiripan
face_encoding = face_encodings[0]
face_distance = face_recognition.face_distance([known_face_encoding], face_encoding)[0]
similarity = 1 - face_distance

# Mengembalikan angka akurasi
print(f"Akurasi: {similarity:.2f}")
