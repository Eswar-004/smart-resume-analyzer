-- Database Schema for Smart Resume Analyzer

-- Ensure users table has NOT NULL constraints
ALTER TABLE users 
    MODIFY COLUMN name VARCHAR(100) NOT NULL,
    MODIFY COLUMN email VARCHAR(100) NOT NULL,
    MODIFY COLUMN password VARCHAR(255) NOT NULL;

-- Create feedback history table
CREATE TABLE IF NOT EXISTS feedback_history (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    resume_filename VARCHAR(255) NOT NULL,
    job_description TEXT NOT NULL,
    ats_score INT NOT NULL,
    strengths JSON NOT NULL,
    weaknesses JSON NOT NULL,
    missing_keywords JSON NOT NULL,
    improvement_plan JSON NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_user_id (user_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
