<?php
include_once "database.php";

// Fungsi untuk mengubah Base64 URL-safe ke Base64 standar
function base64_urlsafe_to_standard($base64String) {
    $base64String = str_replace(['-', '_'], ['+', '/'], $base64String);
    // Tambahkan padding jika diperlukan
    $padding = strlen($base64String) % 4;
    if ($padding > 0) {
        $base64String .= str_repeat('=', 4 - $padding);
    }
    return $base64String;
}

// Menerima data dari POST
$name = $_POST['name'];
$id = $_POST['id'];
$images = json_decode($_POST['images'], true); // Decode JSON ke array

// Validasi $images harus berupa array
if (!is_array($images)) {
    http_response_code(400); // Bad Request
    echo json_encode([
        "status" => "error",
        "message" => "Invalid images data. Expected an array of base64 strings."
    ]);
    exit;
}

// Cek apakah user sudah ada di tabel `users`
$sqlCheckUser = "SELECT id FROM users WHERE user_id = '$id'";
$result = $conn->query($sqlCheckUser);
if ($result->num_rows > 0) {
    http_response_code(409); // Conflict
    echo json_encode([
        "status" => "error",
        "message" => "User with user_id '$id' already exists."
    ]);
    exit;
}

// Direktori penyimpanan gambar
$imageDir = "faces/" . $id;

// Membuat folder jika belum ada
if (!file_exists($imageDir)) {
    mkdir($imageDir, 0777, true);
}

// Simpan data user ke tabel `users`
$sql = "INSERT INTO users (name, user_id) VALUES ('$name', '$id')";
if ($conn->query($sql) === TRUE) {
    // ID pengguna berhasil disimpan
    $userId = $conn->insert_id;

    // Simpan gambar ke folder dan path-nya ke tabel `faces`
    foreach ($images as $index => $imageBase64) {
        // Konversi Base64 URL-safe ke standar
        $imageBase64 = base64_urlsafe_to_standard($imageBase64);

        $imagePath = $imageDir . "/face_" . ($index + 1) . ".jpg";

        // Decode base64 dan simpan ke file
        $imageData = base64_decode($imageBase64);
        if ($imageData === false) {
            http_response_code(422); // Unprocessable Entity
            echo json_encode([
                "status" => "error",
                "message" => "Failed to decode base64 image data for image " . ($index + 1)
            ]);
            exit;
        }
        file_put_contents($imagePath, $imageData);

        // Simpan path ke tabel `faces` dan link ke user_id yang ada di tabel users
        $sql = "INSERT INTO faces (user_id, face_data) VALUES ($userId, '$imagePath')";
        if (!$conn->query($sql)) {
            http_response_code(500); // Internal Server Error
            echo json_encode([
                "status" => "error",
                "message" => "Failed to save face data to database: " . $conn->error
            ]);
            exit;
        }
    }

    // Panggil train.py untuk melatih model
    $output = [];
    $resultCode = 0;

    // Tangkap juga output dari stderr
    $pythonPath = "venv\\Scripts\\python.exe"; // Ganti dengan jalur ke Python venv Anda
    $command = $pythonPath . " train.py " . escapeshellarg($id) . " 2>&1";
    exec($command, $output, $resultCode);

    if ($resultCode === 0) {
        http_response_code(200); // OK
        echo json_encode([
            "status" => "success",
            "message" => "Account registered and face data trained successfully.",
            "output" => $output // Tambahkan output untuk debugging jika perlu
        ]);
    } else {
        http_response_code(500); // Internal Server Error
        echo json_encode([
            "status" => "error",
            "message" => "Account registered but face training failed.",
            "error" => implode("\n", $output) // Sertakan pesan error dari Python
        ]);
    }

} else {
    http_response_code(500); // Internal Server Error
    echo json_encode([
        "status" => "error",
        "message" => "Database error: " . $conn->error
    ]);
}

$conn->close();
?>
