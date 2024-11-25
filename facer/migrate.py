import mysql.connector

hostdb = "localhost"
usernamedb = "root"
passwordDb = ""
db_name = "fr_app"

def create_database():
    # Koneksi ke server MySQL
    conn = mysql.connector.connect(
        host=hostdb,
        user=usernamedb,
        password=passwordDb,
    )
    cursor = conn.cursor()

    # Membuat database
    cursor.execute("CREATE DATABASE IF NOT EXISTS " + db_name)
    cursor.close()
    conn.close()

def create_tables():
    # Koneksi ke database yang baru dibuat
    conn = mysql.connector.connect(
        host=hostdb,
        user=usernamedb,
        password=passwordDb,
        database=db_name
    )
    cursor = conn.cursor()

    # Membuat tabel users
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            user_id VARCHAR(100) NOT NULL UNIQUE
        )
    """)

    # Membuat tabel faces
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS faces (
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT NOT NULL,
            face_data VARCHAR(255) NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        )
    """)

    cursor.close()
    conn.close()

# Menjalankan migrasi
create_database()
create_tables()

print("Database dan tabel berhasil dibuat.")
