<?php
$uri = parse_url($_SERVER['REQUEST_URI'], PHP_URL_PATH);
$base = '/api/';

if (strpos($uri, $base) === 0) {
    $file = __DIR__ . $uri;
    if (file_exists($file)) {
        require $file;
        exit;
    }
}

header('Content-Type: application/json');
http_response_code(404);
echo json_encode(['error' => 'Endpoint not found']);
