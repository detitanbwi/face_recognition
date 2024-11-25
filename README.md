## Cara Menjalankan Proyek

1. **Clone Repositori**:
   ```bash
   git clone https://github.com/detitanbwi/face_recognition.git
   cd face_recognition
2. **Buat virtual environment python**:
   ```bash
   python -m venv venv
3. **Aktifkan virtual environment**:
   ```bash
   venv\Scripts\activate
4. **Install module yang diperlukan**:
   ```bash
   pip install -r requirements.txt

Jika terjadi error saat install dlib maka instalasi dlib wheel dilakukan secara manual dengan mendownload file .whl nya sesuai versi python anda
contoh:
```bash
pip install dlib-19.22.99-cp310-cp310-win_amd64.whl
