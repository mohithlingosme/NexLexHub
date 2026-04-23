<?php
require_once __DIR__ . '/../config/database.php';
require_once __DIR__ . '/../utils/helpers.php';

if ($_SERVER['REQUEST_METHOD'] !== 'GET') {
    send_json(['error' => 'Method not allowed'], 405);
}

$latest = (int)($_GET['latest'] ?? 0);
if ($latest > 0) {
    $stmt = $pdo->prepare("SELECT p.id, p.title, p.created_at FROM Posts p WHERE p.type = 'news' AND p.status = 'published' ORDER BY p.created_at DESC LIMIT ?");
    $stmt->bindValue(1, $latest, PDO::PARAM_INT);
    $stmt->execute();
    send_json($stmt->fetchAll());
}

$stmt = $pdo->query("SELECT p.*, nm.source, nm.news_category, nm.news_date
                     FROM Posts p LEFT JOIN NewsMeta nm ON p.id = nm.post_id
                     WHERE p.type = 'news' ORDER BY p.created_at DESC");
send_json($stmt->fetchAll());
