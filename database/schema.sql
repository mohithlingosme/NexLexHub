<<<<<<< HEAD
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
=======
-- Main Users Table
CREATE TABLE Users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255) NOT NULL UNIQUE,
    email VARCHAR(255) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    role ENUM('admin', 'editor', 'contributor') NOT NULL DEFAULT 'contributor',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Contributor Applications
CREATE TABLE Applications (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    education TEXT,
    background TEXT,
    legal_questions_answers TEXT,
    writing_sample_path VARCHAR(255),
    status ENUM('pending', 'approved', 'rejected') DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Invitation tokens for approved applicants
CREATE TABLE Invites (
    id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(255) NOT NULL,
    token VARCHAR(255) NOT NULL UNIQUE,
    is_used BOOLEAN DEFAULT FALSE,
    expires_at TIMESTAMP NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- For storing uploaded files meta-information
CREATE TABLE Files (
    id INT AUTO_INCREMENT PRIMARY KEY,
    filename VARCHAR(255) NOT NULL,
    filepath VARCHAR(255) NOT NULL,
    mimetype VARCHAR(100) NOT NULL,
    filesize INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Legal Categories
CREATE TABLE LegalCategories (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL UNIQUE,
    slug VARCHAR(255) NOT NULL UNIQUE,
    description TEXT
);

-- Tags for content
CREATE TABLE Tags (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL UNIQUE,
    slug VARCHAR(255) NOT NULL UNIQUE
);

-- Unified Content Table
CREATE TABLE Posts (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    post_type ENUM('article', 'case_law', 'whitepaper', 'news', 'law_review') NOT NULL,
    title VARCHAR(255) NOT NULL,
    content LONGTEXT,
    status ENUM('draft', 'pending', 'published') DEFAULT 'draft',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES Users(id) ON DELETE SET NULL
);

-- Junction table for Posts and LegalCategories (many-to-many)
CREATE TABLE PostCategories (
    post_id INT,
    category_id INT,
    PRIMARY KEY (post_id, category_id),
    FOREIGN KEY (post_id) REFERENCES Posts(id) ON DELETE CASCADE,
    FOREIGN KEY (category_id) REFERENCES LegalCategories(id) ON DELETE CASCADE
);

-- Junction table for Posts and Tags (many-to-many)
CREATE TABLE PostTags (
    post_id INT,
    tag_id INT,
    PRIMARY KEY (post_id, tag_id),
    FOREIGN KEY (post_id) REFERENCES Posts(id) ON DELETE CASCADE,
    FOREIGN KEY (tag_id) REFERENCES Tags(id) ON DELETE CASCADE
);

-- Bare Acts Structure
CREATE TABLE Acts (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    file_id INT,
    FOREIGN KEY (file_id) REFERENCES Files(id) ON DELETE SET NULL
>>>>>>> 6a0c154 (Agent_J)
);

CREATE TABLE Chapters (
    id INT AUTO_INCREMENT PRIMARY KEY,
<<<<<<< HEAD
    act_id INT NOT NULL,
    chapter_number VARCHAR(30) NOT NULL,
    title VARCHAR(255) NOT NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
=======
    act_id INT,
    chapter_number VARCHAR(50),
    title VARCHAR(255) NOT NULL,
>>>>>>> 6a0c154 (Agent_J)
    FOREIGN KEY (act_id) REFERENCES Acts(id) ON DELETE CASCADE
);

CREATE TABLE Sections (
    id INT AUTO_INCREMENT PRIMARY KEY,
<<<<<<< HEAD
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
=======
    chapter_id INT,
    section_number VARCHAR(50) NOT NULL,
    title VARCHAR(255) NOT NULL,
    content TEXT NOT NULL,
    FOREIGN KEY (chapter_id) REFERENCES Chapters(id) ON DELETE CASCADE
);

-- Law Review / Section Analysis
CREATE TABLE SectionAnalysis (
    id INT AUTO_INCREMENT PRIMARY KEY,
    section_id INT,
    explanation TEXT,
    FOREIGN KEY (section_id) REFERENCES Sections(id) ON DELETE CASCADE
);

-- Linking other content (posts) to a specific section
CREATE TABLE SectionRelations (
    id INT AUTO_INCREMENT PRIMARY KEY,
    section_id INT,
    post_id INT,
    FOREIGN KEY (section_id) REFERENCES Sections(id) ON DELETE CASCADE,
    FOREIGN KEY (post_id) REFERENCES Posts(id) ON DELETE CASCADE
);

-- Metadata for Case Laws
CREATE TABLE CaseLawMeta (
    id INT AUTO_INCREMENT PRIMARY KEY,
    post_id INT NOT NULL,
    court VARCHAR(255),
    case_date DATE,
    summary_facts TEXT,
    summary_issues TEXT,
    summary_held TEXT,
    summary_principles TEXT,
    file_id INT,
    FOREIGN KEY (post_id) REFERENCES Posts(id) ON DELETE CASCADE,
    FOREIGN KEY (file_id) REFERENCES Files(id) ON DELETE SET NULL
);

-- Metadata for Whitepapers
CREATE TABLE WhitepaperMeta (
    id INT AUTO_INCREMENT PRIMARY KEY,
    post_id INT NOT NULL,
    file_id INT,
    FOREIGN KEY (post_id) REFERENCES Posts(id) ON DELETE CASCADE,
    FOREIGN KEY (file_id) REFERENCES Files(id) ON DELETE SET NULL
);

-- Metadata for News
CREATE TABLE NewsMeta (
    id INT AUTO_INCREMENT PRIMARY KEY,
    post_id INT NOT NULL,
    summary TEXT,
    source VARCHAR(255),
    news_date DATE,
    FOREIGN KEY (post_id) REFERENCES Posts(id) ON DELETE CASCADE
);

-- Initial Data for Categories
INSERT INTO LegalCategories (name, slug, description) VALUES
('Criminal Law', 'criminal-law', 'Deals with crime and the punishment of criminal offenses.'),
('Corporate Law', 'corporate-law', 'The body of laws, rules, regulations and practices that govern the formation and operation of corporations.'),
('Constitutional Law', 'constitutional-law', 'Deals with the fundamental principles by which the government exercises its authority.'),
('Technology Law', 'technology-law', 'Covers legal issues related to the use of technology, including intellectual property, privacy, and data security.'),
('Finance Law', 'finance-law', 'Governs the regulation of the financial industry, including banks, investment firms, and insurance companies.'),
('Taxation Law', 'taxation-law', 'Concerns the rules and regulations that govern the levying and collection of taxes.');
>>>>>>> 6a0c154 (Agent_J)
