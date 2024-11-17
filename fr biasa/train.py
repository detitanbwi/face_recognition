import cv2
import face_recognition
import numpy as np
import os

# Folder untuk data training
train_dir = "train"

# Fungsi untuk menghitung rata-rata encoding wajah
def get_average_encoding(encodings):
    if len(encodings) == 0:
        return []
    return np.mean(encodings, axis=0)

# Melatih model dan menyimpan hasil encoding
for person_name in os.listdir(train_dir):
    person_dir = os.path.join(train_dir, person_name)
    encoding_file_path = os.path.join(person_dir, f"{person_name}_encoding.npy")

    if os.path.isdir(person_dir):
        person_encodings = []
        
        # Jika encoding sudah ada, lewati training
        if os.path.exists(encoding_file_path):
            print(f"Encoding untuk {person_name} sudah ada, lewati training.")
            continue

        # Melakukan iterasi untuk setiap file gambar dalam folder tersebut
        for image_name in os.listdir(person_dir):
            image_path = os.path.join(person_dir, image_name)
            print(f"Processing {image_path}...")
            image = cv2.imread(image_path)
            if image is None:
                print(f"Error loading image {image_path}")
                continue
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

            if image.shape[-1] == 4:  # Menghilangkan saluran Alpha jika ada
                image = cv2.cvtColor(image, cv2.COLOR_BGRA2BGR)

            encodings = face_recognition.face_encodings(image)

            if len(encodings) > 0:
                person_encodings.append(encodings[0])
        
        if len(person_encodings) > 0:
            # Mengambil rata-rata encoding
            average_encoding = get_average_encoding(person_encodings)
            # Menyimpan encoding ke file `.npy`
            np.save(encoding_file_path, average_encoding)
            print(f"Encoding untuk {person_name} disimpan di {encoding_file_path}.")
