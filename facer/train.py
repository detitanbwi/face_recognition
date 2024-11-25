# import sys
# import os
# import face_recognition
# import numpy as np
# import pickle

# # Mendapatkan user_id dari argument
# user_id = sys.argv[1]

# # Direktori data wajah
# face_dir = f"faces/{user_id}"
# if not os.path.exists(face_dir):
#     print("Error: User folder not found")
#     sys.exit(1)

# # Memproses semua gambar di folder user
# encodings = []
# for image_file in os.listdir(face_dir):
#     image_path = os.path.join(face_dir, image_file)
#     image = face_recognition.load_image_file(image_path)
#     try:
#         # Mendapatkan encoding wajah
#         face_encoding = face_recognition.face_encodings(image)[0]
#         encodings.append(face_encoding)
#     except IndexError:
#         print(f"Warning: No face found in {image_file}")

# # Simpan encoding ke file .np
# if encodings:
#     output_file = os.path.join(face_dir, "encodings.np")
#     with open(output_file, "wb") as f:
#         pickle.dump(encodings, f)
#     print("Training completed")
# else:
#     print("Error: No encodings found")
#     sys.exit(1)

import cv2
import face_recognition
import numpy as np
import os
import sys

# Mendapatkan ID pengguna dari argumen command-line
if len(sys.argv) < 2:
    print("Usage: python train.py <user_id>")
    sys.exit(1)

user_id = sys.argv[1]
train_dir = f"faces/{user_id}"  # Direktori gambar training
output_dir = f"faces/{user_id}"        # Direktori penyimpanan encoding
encoding_file_path = os.path.join(output_dir, f"{user_id}_encoding.npy")

# Membuat folder untuk encoding jika belum ada
os.makedirs(output_dir, exist_ok=True)

# Fungsi untuk menghitung rata-rata encoding wajah
def get_average_encoding(encodings):
    if len(encodings) == 0:
        return []
    return np.mean(encodings, axis=0)

# Pastikan direktori pengguna ada
if not os.path.exists(train_dir):
    print(f"Direktori {train_dir} tidak ditemukan. Pastikan gambar telah diunggah.")
    sys.exit(1)

# Mulai proses pelatihan
user_encodings = []

# Cek apakah encoding sudah ada
if os.path.exists(encoding_file_path):
    print(f"Encoding untuk {user_id} sudah ada. Lewati training.")
    sys.exit(0)

# Iterasi untuk setiap gambar dalam direktori
for image_name in os.listdir(train_dir):
    image_path = os.path.join(train_dir, image_name)
    print(f"Processing {image_path}...")

    # Muat dan konversi gambar
    image = cv2.imread(image_path)
    if image is None:
        print(f"Error loading image {image_path}")
        continue
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    if image.shape[-1] == 4:  # Menghilangkan saluran Alpha jika ada
        image = cv2.cvtColor(image, cv2.COLOR_BGRA2BGR)

    # Ekstraksi encoding wajah
    encodings = face_recognition.face_encodings(image)

    if len(encodings) > 0:
        user_encodings.append(encodings[0])
    else:
        print(f"Tidak ada wajah yang terdeteksi pada {image_path}.")

# Simpan rata-rata encoding ke file `.npy`
if len(user_encodings) > 0:
    average_encoding = get_average_encoding(user_encodings)
    np.save(encoding_file_path, average_encoding)
    print(f"Encoding untuk user {user_id} berhasil disimpan di {encoding_file_path}.")
else:
    print(f"Tidak ada encoding yang ditemukan untuk user {user_id}. Pelatihan gagal.")
    sys.exit(1)
