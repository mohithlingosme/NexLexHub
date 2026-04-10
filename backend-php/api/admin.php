<?php
require_once __DIR__ . '/../config/database.php';
require_once __DIR__ . '/../utils/helpers.php';

ensure_auth(['Admin']);

if ($_SERVER['REQUEST_METHOD'] !== 'GET') {
    send_json(['error' => 'Method not allowed'], 405);
}

$stats = [
    'posts' => (int)$pdo->query("SELECT COUNT(*) FROM Posts")->fetchColumn(),
    'pending_posts' => (int)$pdo->query("SELECT COUNT(*) FROM Posts WHERE status = 'pending'")->fetchColumn(),
    'applications' => (int)$pdo->query("SELECT COUNT(*) FROM Applications WHERE status = 'pending'")->fetchColumn(),
    'users' => (int)$pdo->query("SELECT COUNT(*) FROM Users")->fetchColumn(),
    'acts' => (int)$pdo->query("SELECT COUNT(*) FROM Acts")->fetchColumn(),
];

send_json($stats);
