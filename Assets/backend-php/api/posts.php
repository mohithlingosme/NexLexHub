<?php
require_once __DIR__ . '/../config/database.php';
require_once __DIR__ . '/../utils/helpers.php';

$method = $_SERVER['REQUEST_METHOD'];

if ($method === 'GET') {
    $q = $_GET['q'] ?? '';
    $type = $_GET['type'] ?? '';
    $category = $_GET['category'] ?? '';

    $sql = "SELECT DISTINCT p.* FROM Posts p
            LEFT JOIN PostCategories pc ON p.id = pc.post_id
            LEFT JOIN LegalCategories lc ON pc.category_id = lc.id
            WHERE p.status = 'published'";
    $params = [];

    if ($q !== '') {
        $sql .= " AND (p.title LIKE :q OR p.content LIKE :q OR p.tags LIKE :q)";
        $params[':q'] = "%$q%";
    }
    if ($type !== '') {
        $sql .= " AND p.type = :type";
        $params[':type'] = $type;
    }
    if ($category !== '') {
        $sql .= " AND lc.name = :category";
        $params[':category'] = $category;
    }
    $sql .= " ORDER BY p.created_at DESC";

    $stmt = $pdo->prepare($sql);
    $stmt->execute($params);
    send_json($stmt->fetchAll());
}

if ($method === 'POST') {
    ensure_auth(['Admin', 'Editor']);
    $body = get_json_body();

    $stmt = $pdo->prepare("INSERT INTO Posts (title, content, type, tags, author, status, created_at) VALUES (?, ?, ?, ?, ?, ?, NOW())");
    $stmt->execute([
        $body['title'] ?? '',
        $body['content'] ?? '',
        $body['type'] ?? 'article',
        $body['tags'] ?? '',
        $body['author'] ?? 'Unknown',
        $body['status'] ?? 'draft',
    ]);

    send_json(['message' => 'Post created', 'id' => $pdo->lastInsertId()], 201);
}

send_json(['error' => 'Method not allowed'], 405);
