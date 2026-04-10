<?php
require_once __DIR__ . '/../config/database.php';
require_once __DIR__ . '/../utils/helpers.php';

$method = $_SERVER['REQUEST_METHOD'];

if ($method === 'POST') {
    $body = get_json_body();
    $stmt = $pdo->prepare("INSERT INTO Applications (name, email, education, background, legal_questions, writing_sample, status, created_at)
                           VALUES (?, ?, ?, ?, ?, ?, 'pending', NOW())");
    $stmt->execute([
        $body['name'] ?? '',
        $body['email'] ?? '',
        $body['education'] ?? '',
        $body['background'] ?? '',
        $body['legal_questions'] ?? '',
        $body['writing_sample'] ?? '',
    ]);
    send_json(['message' => 'Application submitted'], 201);
}

if ($method === 'GET') {
    ensure_auth(['Admin']);
    $stmt = $pdo->query("SELECT * FROM Applications ORDER BY created_at DESC");
    send_json($stmt->fetchAll());
}

send_json(['error' => 'Method not allowed'], 405);
