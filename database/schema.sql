CREATE DATABASE IF NOT EXISTS nexlexhub CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE nexlexhub;

CREATE TABLE Users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(120) NOT NULL,
    email VARCHAR(190) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    role ENUM('Admin', 'Editor') NOT NULL DEFAULT 'Editor',
    created_at DATETIME NOT NULL
);

CREATE TABLE Applications (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(120) NOT NULL,
    email VARCHAR(190) NOT NULL,
    education VARCHAR(255) NOT NULL,
    background TEXT NOT NULL,
    legal_questions TEXT NOT NULL,
    writing_sample TEXT NOT NULL,
    status ENUM('pending', 'approved', 'rejected') NOT NULL DEFAULT 'pending',
    created_at DATETIME NOT NULL
);

CREATE TABLE Invites (
    id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(190) NOT NULL,
    token VARCHAR(100) NOT NULL UNIQUE,
    role ENUM('Admin', 'Editor') NOT NULL DEFAULT 'Editor',
    expires_at DATETIME NOT NULL,
    is_used TINYINT(1) NOT NULL DEFAULT 0,
    created_at DATETIME NOT NULL
);

CREATE TABLE Posts (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    content LONGTEXT NOT NULL,
    type ENUM('article', 'case_law', 'bare_act', 'whitepaper', 'news', 'law_review') NOT NULL,
    tags VARCHAR(500) NULL,
    author VARCHAR(120) NOT NULL,
    status ENUM('draft', 'pending', 'published') NOT NULL DEFAULT 'draft',
    file_path VARCHAR(255) NULL,
    created_at DATETIME NOT NULL
);

CREATE TABLE Acts (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT NULL,
    pdf_path VARCHAR(255) NULL,
    created_at DATETIME NOT NULL
);

CREATE TABLE Chapters (
    id INT AUTO_INCREMENT PRIMARY KEY,
    act_id INT NOT NULL,
    chapter_number VARCHAR(30) NOT NULL,
    title VARCHAR(255) NOT NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (act_id) REFERENCES Acts(id) ON DELETE CASCADE
);

CREATE TABLE Sections (
    id INT AUTO_INCREMENT PRIMARY KEY,
    chapter_id INT NOT NULL,
    section_number VARCHAR(30) NOT NULL,
    title VARCHAR(255) NOT NULL,
    bare_text LONGTEXT NOT NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (chapter_id) REFERENCES Chapters(id) ON DELETE CASCADE
);

CREATE TABLE SectionAnalysis (
    id INT AUTO_INCREMENT PRIMARY KEY,
    section_id INT NOT NULL,
    explanation LONGTEXT NOT NULL,
    created_by INT NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (section_id) REFERENCES Sections(id) ON DELETE CASCADE,
    FOREIGN KEY (created_by) REFERENCES Users(id) ON DELETE SET NULL
);

CREATE TABLE SectionRelations (
    id INT AUTO_INCREMENT PRIMARY KEY,
    section_id INT NOT NULL,
    post_id INT NOT NULL,
    relation_type ENUM('case_law', 'article', 'whitepaper') NOT NULL,
    FOREIGN KEY (section_id) REFERENCES Sections(id) ON DELETE CASCADE,
    FOREIGN KEY (post_id) REFERENCES Posts(id) ON DELETE CASCADE,
    UNIQUE(section_id, post_id, relation_type)
);

CREATE TABLE CaseLawMeta (
    id INT AUTO_INCREMENT PRIMARY KEY,
    post_id INT NOT NULL UNIQUE,
    case_name VARCHAR(255) NOT NULL,
    court VARCHAR(255) NOT NULL,
    judgment_date DATE NOT NULL,
    facts LONGTEXT NOT NULL,
    issues LONGTEXT NOT NULL,
    held LONGTEXT NOT NULL,
    principles LONGTEXT NOT NULL,
    FOREIGN KEY (post_id) REFERENCES Posts(id) ON DELETE CASCADE
);

CREATE TABLE WhitepaperMeta (
    id INT AUTO_INCREMENT PRIMARY KEY,
    post_id INT NOT NULL UNIQUE,
    abstract_text LONGTEXT NULL,
    publication_date DATE NULL,
    FOREIGN KEY (post_id) REFERENCES Posts(id) ON DELETE CASCADE
);

CREATE TABLE NewsMeta (
    id INT AUTO_INCREMENT PRIMARY KEY,
    post_id INT NOT NULL UNIQUE,
    source VARCHAR(255) NULL,
    news_category VARCHAR(120) NULL,
    news_date DATE NULL,
    FOREIGN KEY (post_id) REFERENCES Posts(id) ON DELETE CASCADE
);

CREATE TABLE LegalCategories (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(120) NOT NULL UNIQUE
);

CREATE TABLE PostCategories (
    id INT AUTO_INCREMENT PRIMARY KEY,
    post_id INT NOT NULL,
    category_id INT NOT NULL,
    UNIQUE(post_id, category_id),
    FOREIGN KEY (post_id) REFERENCES Posts(id) ON DELETE CASCADE,
    FOREIGN KEY (category_id) REFERENCES LegalCategories(id) ON DELETE CASCADE
);

CREATE TABLE Tags (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(80) NOT NULL UNIQUE
);

CREATE TABLE Files (
    id INT AUTO_INCREMENT PRIMARY KEY,
    original_name VARCHAR(255) NOT NULL,
    stored_name VARCHAR(255) NOT NULL,
    path VARCHAR(255) NOT NULL,
    mime_type VARCHAR(80) NOT NULL,
    size BIGINT NOT NULL,
    created_at DATETIME NOT NULL
);

INSERT INTO LegalCategories (name) VALUES
('Criminal Law'), ('Corporate Law'), ('Constitutional Law'),
('Technology Law'), ('Finance Law'), ('Taxation Law');
