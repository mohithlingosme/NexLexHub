<?php
require_once __DIR__ . '/../config/database.php';
require_once __DIR__ . '/../utils/helpers.php';

if ($_SERVER['REQUEST_METHOD'] !== 'GET') {
    send_json(['error' => 'Method not allowed'], 405);
}

$id = (int)($_GET['id'] ?? 0);
if (!$id) {
    send_json(['error' => 'Section id required'], 400);
}

$sectionStmt = $pdo->prepare("SELECT * FROM Sections WHERE id = ?");
$sectionStmt->execute([$id]);
$section = $sectionStmt->fetch();
if (!$section) {
    send_json(['error' => 'Section not found'], 404);
}

$analysisStmt = $pdo->prepare("SELECT * FROM SectionAnalysis WHERE section_id = ? LIMIT 1");
$analysisStmt->execute([$id]);
$analysis = $analysisStmt->fetch();

$relatedCaseLaws = $pdo->prepare("SELECT p.id, p.title FROM SectionRelations sr JOIN Posts p ON sr.post_id = p.id WHERE sr.section_id = ? AND p.type = 'case_law'");
$relatedCaseLaws->execute([$id]);

$relatedArticles = $pdo->prepare("SELECT p.id, p.title FROM SectionRelations sr JOIN Posts p ON sr.post_id = p.id WHERE sr.section_id = ? AND p.type = 'article'");
$relatedArticles->execute([$id]);

send_json([
    'section' => $section,
    'analysis' => $analysis,
    'related' => [
        'case_laws' => $relatedCaseLaws->fetchAll(),
        'articles' => $relatedArticles->fetchAll(),
    ],
]);
