<?php
require_once __DIR__ . '/../config/database.php';
require_once __DIR__ . '/../utils/helpers.php';

$method = $_SERVER['REQUEST_METHOD'];

if ($method === 'POST') {
    ensure_auth(['Admin']);
    $body = get_json_body();
    $token = bin2hex(random_bytes(16));

    $stmt = $pdo->prepare("INSERT INTO Invites (email, token, role, expires_at, is_used, created_at)
                           VALUES (?, ?, ?, DATE_ADD(NOW(), INTERVAL 7 DAY), 0, NOW())");
    $stmt->execute([$body['email'] ?? '', $token, $body['role'] ?? 'Editor']);

    send_json(['invite_token' => $token, 'signup_link' => '/signup?token=' . $token], 201);
}

if ($method === 'GET') {
    $token = $_GET['token'] ?? '';
    $stmt = $pdo->prepare("SELECT * FROM Invites WHERE token = ? AND is_used = 0 AND expires_at > NOW() LIMIT 1");
    $stmt->execute([$token]);
    $invite = $stmt->fetch();
    if (!$invite) {
        send_json(['error' => 'Invalid or expired token'], 404);
    }
    send_json(['valid' => true, 'email' => $invite['email'], 'role' => $invite['role']]);
}

send_json(['error' => 'Method not allowed'], 405);
