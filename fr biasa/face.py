import cv2
import face_recognition
import numpy as np
import os

# Folder untuk data training
train_dir = "train"
# Gambar testing
test_image_path = "test/titan.jpg"

def get_average_encoding(encodings):
    if len(encodings) == 0:
        return []
    return np.mean(encodings, axis=0)

# List untuk menyimpan encoding dan nama yang dikenal
known_face_encodings = []
known_face_names = []

# Melakukan iterasi untuk setiap folder di dalam folder train/
for person_name in os.listdir(train_dir):
    person_dir = os.path.join(train_dir, person_name)
    if os.path.isdir(person_dir):
        person_encodings = []
        # Melakukan iterasi untuk setiap file gambar dalam folder tersebut
        for image_name in os.listdir(person_dir):
            image_path = os.path.join(person_dir, image_name)
            print(f"Processing {image_path}...")
            # Memuat gambar menggunakan OpenCV dan mengubah ke RGB
            image = cv2.imread(image_path)
            if image is None:
                print(f"Error loading image {image_path}")
                continue
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

            # Memastikan gambar tidak memiliki saluran Alpha
            if image.shape[-1] == 4:
                image = cv2.cvtColor(image, cv2.COLOR_BGRA2BGR)

            encodings = face_recognition.face_encodings(image)

            # Jika ada encoding, tambahkan ke daftar person_encodings
            if len(encodings) > 0:
                person_encodings.append(encodings[0])
        
        # Jika terdapat encoding untuk orang ini, tambahkan rata-rata encoding ke data training
        if len(person_encodings) > 0:
            average_encoding = get_average_encoding(person_encodings)
            known_face_encodings.append(average_encoding)
            known_face_names.append(person_name)

# Membaca gambar testing
test_image = cv2.imread(test_image_path)
if test_image is None:
    print("Error loading test image.")
else:
    # Konversi gambar testing ke RGB
    rgb_test_image = cv2.cvtColor(test_image, cv2.COLOR_BGR2RGB)

    # Mencari lokasi dan encoding wajah pada gambar testing
    face_encodings = face_recognition.face_encodings(rgb_test_image)

    # Daftar untuk menyimpan tingkat kemiripan
    similarity_results = []

    # Membandingkan encoding wajah pada gambar testing dengan data training
    for face_encoding in face_encodings:
        # Menghitung jarak dari setiap wajah yang dikenali
        face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)

        # Menyimpan hasil kemiripan sebagai (nama, jarak)
        for i, distance in enumerate(face_distances):
            name = known_face_names[i]
            similarity = 1 - distance  # Akurasi kemiripan, semakin mendekati 1, semakin mirip
            similarity_results.append((name, similarity))

    # Menampilkan hasil akurasi kemiripan
    if similarity_results:
        print("Tingkat Kemiripan:")
        for name, similarity in similarity_results:
            print(f"{name}: {similarity:.2f}")
    else:
        print("Tidak ada wajah yang terdeteksi pada gambar testing.")