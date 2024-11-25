<?php

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
$id = $_POST['user_id'];
$imageBase64 = base64_urlsafe_to_standard($_POST['image']);
$tempDir = "temporary";

// Validasi input image
if (empty($imageBase64)) {
    http_response_code(400); // Bad Request
    echo json_encode([
        "status" => "error",
        "message" => "Image data is missing."
    ]);
    exit;
}

// Buat folder temporary jika belum ada
if (!file_exists($tempDir)) {
    mkdir($tempDir, 0777, true);
}

// Decode base64 dan simpan sebagai file sementara
$tempImagePath = $tempDir . "/temp.jpg";
$imageData = base64_decode($imageBase64);
if ($imageData === false) {
    http_response_code(422); // Unprocessable Entity
    echo json_encode([
        "status" => "error",
        "message" => "Failed to decode base64 image data."
    ]);
    exit;
}
file_put_contents($tempImagePath, $imageData);

// Path untuk encoding wajah yang sudah disimpan
$encodingFilePath = "faces/" . $id . "/" . $id . "_encoding.npy";

// Cek apakah file encoding ada
if (!file_exists($encodingFilePath)) {
    http_response_code(404); // Not Found
    echo json_encode([
        "status" => "error",
        "message" => "Encoding file for user '$id' not found."
    ]);
    exit;
}

// Panggil Python script untuk deteksi wajah dan perbandingan
$output = [];
$resultCode = 0;
$pythonPath = "venv\\Scripts\\python.exe"; // Ganti dengan jalur ke Python venv Anda
$command = $pythonPath . " detect_face.py " . escapeshellarg($id) . " " . escapeshellarg($tempImagePath) . " " . escapeshellarg($encodingFilePath) . " 2>&1";
exec($command, $output, $resultCode);

// Hapus file sementara
unlink($tempImagePath);

// Kirim respons ke pengguna
if ($resultCode === 0) {
    // Periksa apakah output mengandung hasil yang valid
    $match = (trim($output[0]) == "True");
    $similarity = isset($output[1]) ? $output[1] : null;

    if ($match) {
        http_response_code(200); // OK
        echo json_encode([
            "status" => "success",
            "message" => "Login berhasil!",
            "match" => $match,
            "similarity" => $similarity
        ]);
    } else {
        http_response_code(401); // Unauthorized
        echo json_encode([
            "status" => "error",
            "message" => "Face recognition failed. No match found."
        ]);
    }
} else {
    http_response_code(500); // Internal Server Error
    echo json_encode([
        "status" => "error",
        "message" => "Face detection failed. Error: " . implode("\n", $output)
    ]);
}

