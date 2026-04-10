<?php
require_once __DIR__ . '/../config/database.php';
require_once __DIR__ . '/../utils/helpers.php';

$method = $_SERVER['REQUEST_METHOD'];

if ($method === 'GET') {
    $acts = $pdo->query("SELECT * FROM Acts ORDER BY title")->fetchAll();

    foreach ($acts as &$act) {
        $chaptersStmt = $pdo->prepare("SELECT * FROM Chapters WHERE act_id = ? ORDER BY chapter_number");
        $chaptersStmt->execute([$act['id']]);
        $chapters = $chaptersStmt->fetchAll();

        foreach ($chapters as &$chapter) {
            $sectionsStmt = $pdo->prepare("SELECT id, section_number, title FROM Sections WHERE chapter_id = ? ORDER BY section_number");
            $sectionsStmt->execute([$chapter['id']]);
            $chapter['sections'] = $sectionsStmt->fetchAll();
        }

        $act['chapters'] = $chapters;
    }

    send_json($acts);
}

if ($method === 'POST') {
    ensure_auth(['Admin']);
    $body = get_json_body();
    $stmt = $pdo->prepare("INSERT INTO Acts (title, description, pdf_path, created_at) VALUES (?, ?, ?, NOW())");
    $stmt->execute([
        $body['title'] ?? '',
        $body['description'] ?? '',
        $body['pdf_path'] ?? null,
    ]);
    send_json(['message' => 'Act created', 'id' => $pdo->lastInsertId()], 201);
}

send_json(['error' => 'Method not allowed'], 405);
