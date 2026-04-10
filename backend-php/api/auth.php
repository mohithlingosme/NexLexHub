<?php
require_once __DIR__ . '/../config/database.php';
require_once __DIR__ . '/../utils/helpers.php';

$method = $_SERVER['REQUEST_METHOD'];
$body = get_json_body();

if ($method === 'POST' && ($_GET['action'] ?? '') === 'login') {
    $stmt = $pdo->prepare("SELECT id, name, email, password_hash, role FROM Users WHERE email = ? LIMIT 1");
    $stmt->execute([$body['email'] ?? '']);
    $user = $stmt->fetch();

    if (!$user || !password_verify($body['password'] ?? '', $user['password_hash'])) {
        send_json(['error' => 'Invalid credentials'], 401);
    }

    // Placeholder token response.
    send_json(['token' => base64_encode($user['email'] . '|role:' . $user['role']), 'role' => $user['role']]);
}

if ($method === 'POST' && ($_GET['action'] ?? '') === 'signup-invite') {
    $token = $body['token'] ?? '';
    $inviteStmt = $pdo->prepare("SELECT * FROM Invites WHERE token = ? AND is_used = 0 AND expires_at > NOW() LIMIT 1");
    $inviteStmt->execute([$token]);
    $invite = $inviteStmt->fetch();

    if (!$invite) {
        send_json(['error' => 'Invalid invite token'], 400);
    }

    $insert = $pdo->prepare("INSERT INTO Users (name, email, password_hash, role, created_at)
                             VALUES (?, ?, ?, ?, NOW())");
    $insert->execute([
        $body['name'] ?? '',
        $invite['email'],
        password_hash($body['password'] ?? '', PASSWORD_BCRYPT),
        $invite['role'],
    ]);

    $pdo->prepare("UPDATE Invites SET is_used = 1 WHERE id = ?")->execute([$invite['id']]);
    send_json(['message' => 'Signup complete'], 201);
}

send_json(['error' => 'Unsupported route'], 404);
