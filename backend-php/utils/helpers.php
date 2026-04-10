<?php
function send_json($data, int $status = 200): void {
    http_response_code($status);
    header('Content-Type: application/json');
    echo json_encode($data);
    exit;
}

function get_json_body(): array {
    $raw = file_get_contents('php://input');
    return $raw ? (json_decode($raw, true) ?: []) : [];
}

function ensure_auth(array $allowedRoles = ['Admin', 'Editor']): void {
    // Placeholder token-based auth. Replace with JWT/session in production.
    $role = $_SERVER['HTTP_X_ROLE'] ?? '';
    if (!in_array($role, $allowedRoles, true)) {
        send_json(['error' => 'Unauthorized'], 401);
    }
}

function save_pdf_upload(string $fieldName): array {
    if (!isset($_FILES[$fieldName])) {
        throw new RuntimeException('No file uploaded.');
    }

    $file = $_FILES[$fieldName];
    $ext = strtolower(pathinfo($file['name'], PATHINFO_EXTENSION));
    if ($ext !== 'pdf' || $file['type'] !== 'application/pdf') {
        throw new RuntimeException('Only PDF files are allowed.');
    }

    $uploadsDir = realpath(__DIR__ . '/../../uploads') ?: (__DIR__ . '/../../uploads');
    if (!is_dir($uploadsDir)) {
        mkdir($uploadsDir, 0775, true);
    }

    $safeName = uniqid('pdf_', true) . '.pdf';
    $target = $uploadsDir . DIRECTORY_SEPARATOR . $safeName;
    if (!move_uploaded_file($file['tmp_name'], $target)) {
        throw new RuntimeException('Failed to save uploaded file.');
    }

    return [
        'original_name' => $file['name'],
        'stored_name' => $safeName,
        'path' => '/uploads/' . $safeName,
        'mime_type' => 'application/pdf',
        'size' => $file['size'],
    ];
}
