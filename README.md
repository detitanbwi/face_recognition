# Face Recognition API

versi Python 3.10.6

### Instalasi Python Environment

1. **Clone Repositori**:
   ```bash
   git clone https://github.com/detitanbwi/face_recognition.git
   cd face_recognition
   ```
   letakkan file tersebut ke dalam direktori lokal server Xampp(htdocs)/Laragon(www) dan beri nama untuk proyek anda seperti contoh berikut
   
   ![{0E258A86-C011-4598-AF55-B38A490D844B}](https://github.com/user-attachments/assets/dfddef4a-8888-4676-9662-6f771e32b521)

3. **Buat virtual environment python**:
   ```bash
   python -m venv venv
4. **Aktifkan virtual environment**:
   ```bash
   venv\Scripts\activate
5. **Install module yang diperlukan**:
   ```bash
   pip install -r requirements.txt

Jika terjadi error saat install dlib maka instalasi dlib wheel dilakukan secara manual dengan mendownload file .whl nya sesuai versi python anda
contoh:
```bash
pip install dlib-19.22.99-cp310-cp310-win_amd64.whl
```

### Migrasi Database
Database yang digunakan adalah database MySQL

1. **Sesuaikan kredensial Database anda pada migrate.py**
   ```bash
   hostdb = "localhost"
   usernamedb = "root"
   passwordDb = ""
   db_name = "fr_app"
   ```
2. **Sesuaikan kredensial Database anda pada database.php**
   ```bash
   $servername = "localhost";
   $username = "root";
   $password = "";
   $dbname = "fr_app";
   ```
3. **Jalankan migrate.py**
   ```bash
   python migrate.py
   ```
