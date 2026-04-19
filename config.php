<?php
/**
 * NexLexHub Database Configuration
 * Optimized for XAMPP (Localhost)
 */

// Database Credentials
define('DB_HOST', 'localhost');
define('DB_NAME', 'lexnexhub_db'); // Ensure this matches your created database name
define('DB_USER', 'root');
define('DB_PASS', ''); // Default XAMPP password is empty
define('DB_CHARSET', 'utf8mb4');

// API Settings
define('API_BASE_URL', 'http://localhost:8000/api');

// Establish PDO connection
try {
    $dsn = "mysql:host=" . DB_HOST . ";dbname=" . DB_NAME . ";charset=" . DB_CHARSET;
    $options = [
        PDO::ATTR_ERRMODE            => PDO::ERRMODE_EXCEPTION,
        PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC,
        PDO::ATTR_EMULATE_PREPARES   => false,
    ];
    
    $pdo = new PDO($dsn, DB_USER, DB_PASS, $options);
} catch (\PDOException $e) {
    // In production, log the error and show a generic message
    // For local development, we display the error
    header('Content-Type: application/json', true, 500);
    echo json_encode([
        "error" => "Database connection failed",
        "message" => $e->getMessage()
    ]);
    exit;
}

/**
 * Helper: Get Request Headers
 * Used for role-based behavior (X-Role: Admin/Editor)
 */
function getRequestRole() {
    $headers = getallheaders();
    return isset($headers['X-Role']) ? $headers['X-Role'] : 'user';
}

/**
 * Helper: JSON Response Utility
 */
function sendJsonResponse($data, $statusCode = 200) {
    header('Content-Type: application/json');
    http_response_code($statusCode);
    echo json_encode($data);
    exit;
}

// Global PDO instance for use in other API files
$db = $pdo;