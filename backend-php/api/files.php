<?php
require_once __DIR__ . '/../config/database.php';
require_once __DIR__ . '/../utils/helpers.php';

$method = $_SERVER['REQUEST_METHOD'];

if ($method === 'POST') {
    ensure_auth(['Admin', 'Editor']);
    try {
        $file = save_pdf_upload('file');
        $stmt = $pdo->prepare("INSERT INTO Files (original_name, stored_name, path, mime_type, size, created_at)
                               VALUES (?, ?, ?, ?, ?, NOW())");
        $stmt->execute([$file['original_name'], $file['stored_name'], $file['path'], $file['mime_type'], $file['size']]);
        send_json(['message' => 'Uploaded', 'file' => $file], 201);
    } catch (Throwable $e) {
        send_json(['error' => $e->getMessage()], 400);
    }
}

if ($method === 'GET') {
    $path = $_GET['path'] ?? '';
    if (!preg_match('#^/uploads/[a-zA-Z0-9_\-.]+\.pdf$#', $path)) {
        send_json(['error' => 'Invalid path'], 400);
    }

    $fullPath = realpath(__DIR__ . '/../../' . ltrim($path, '/'));
    $uploadsRoot = realpath(__DIR__ . '/../../uploads');
    if (!$fullPath || !$uploadsRoot || strpos($fullPath, $uploadsRoot) !== 0 || !file_exists($fullPath)) {
        send_json(['error' => 'File not found'], 404);
    }

    header('Content-Type: application/pdf');
    header('Content-Disposition: inline; filename="' . basename($fullPath) . '"');
    readfile($fullPath);
    exit;
}

send_json(['error' => 'Method not allowed'], 405);
