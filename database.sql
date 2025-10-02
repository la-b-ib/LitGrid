-- Complete Database Setup and Fixes for LitGrid
-- Date: 2025-10-01
-- This file contains all necessary schema fixes and improvements

USE litgrid;

-- Disable foreign key checks temporarily for safe modifications
SET FOREIGN_KEY_CHECKS = 0;

-- ================================================================
-- BOOKS TABLE ENHANCEMENTS
-- ================================================================

-- Add missing columns to books table
ALTER TABLE books
ADD COLUMN IF NOT EXISTS isbn_13 VARCHAR(13) AFTER isbn,
ADD COLUMN IF NOT EXISTS isbn_10 VARCHAR(10) AFTER isbn_13,
ADD COLUMN IF NOT EXISTS page_count INT AFTER pages,
ADD COLUMN IF NOT EXISTS keywords TEXT AFTER description,
ADD COLUMN IF NOT EXISTS popularity_score INT DEFAULT 0 AFTER keywords;

-- ================================================================
-- USERS TABLE ENHANCEMENTS
-- ================================================================

-- Add missing columns to users table
ALTER TABLE users
ADD COLUMN IF NOT EXISTS user_unique_code VARCHAR(50) UNIQUE AFTER user_id,
ADD COLUMN IF NOT EXISTS created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP AFTER registration_date,
ADD COLUMN IF NOT EXISTS borrowing_days INT DEFAULT 14 AFTER borrowing_limit_days;

-- Add indexes for better performance
ALTER TABLE books
ADD INDEX IF NOT EXISTS idx_isbn13 (isbn_13),
ADD INDEX IF NOT EXISTS idx_isbn10 (isbn_10),
ADD INDEX IF NOT EXISTS idx_popularity (popularity_score);

-- Migrate existing ISBN data
UPDATE books 
SET isbn_13 = isbn 
WHERE isbn IS NOT NULL 
  AND LENGTH(isbn) = 13 
  AND isbn_13 IS NULL;

UPDATE books 
SET isbn_10 = isbn 
WHERE isbn IS NOT NULL 
  AND LENGTH(isbn) = 10 
  AND isbn_10 IS NULL;

-- Set page_count from pages if not set
UPDATE books 
SET page_count = pages 
WHERE pages IS NOT NULL 
  AND page_count IS NULL;

-- ================================================================
-- ITEM CODES TABLE FOR BARCODES/QR CODES
-- ================================================================

CREATE TABLE IF NOT EXISTS item_codes (
    code_id INT AUTO_INCREMENT PRIMARY KEY,
    item_type ENUM('book', 'user') NOT NULL,
    item_id INT NOT NULL,
    entity_type VARCHAR(50),  -- For compatibility
    entity_id INT,  -- For compatibility
    code_type ENUM('barcode', 'qrcode') NOT NULL,
    code_value VARCHAR(255) NOT NULL,
    code_image LONGBLOB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE KEY unique_item_code (item_type, item_id, code_type),
    INDEX idx_item (item_type, item_id),
    INDEX idx_entity (entity_type, entity_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ================================================================
-- VIEWS FOR COMPATIBILITY
-- ================================================================

-- Transactions view (compatibility layer)
CREATE OR REPLACE VIEW transactions AS
SELECT 
    b.borrowing_id AS transaction_id,
    b.user_id,
    i.book_id,
    b.checkout_date AS transaction_date,
    b.due_date,
    b.return_date,
    b.status,
    b.fine_amount,
    b.renewed_count AS renewal_count,
    b.notes,
    FALSE as reminder_sent,
    0 as reminder_count
FROM borrowing b
INNER JOIN book_inventory i ON b.inventory_id = i.inventory_id;

-- Fines view (derived from borrowing)
CREATE OR REPLACE VIEW fines AS
SELECT 
    b.borrowing_id AS fine_id,
    b.user_id,
    i.book_id,
    b.fine_amount,
    CASE 
        WHEN b.fine_amount > 0 AND b.fine_paid = 0 THEN 'unpaid'
        WHEN b.fine_amount > 0 AND b.fine_paid = 1 THEN 'paid'
        ELSE 'none'
    END AS fine_status,
    b.checkout_date AS fine_date,
    b.fine_paid_date AS paid_date
FROM borrowing b
INNER JOIN book_inventory i ON b.inventory_id = i.inventory_id
WHERE b.fine_amount > 0;

-- Member tiers view (derived from users)
CREATE OR REPLACE VIEW member_tiers AS
SELECT 
    user_id,
    CASE 
        WHEN fine_balance > 100 THEN 'bronze'
        WHEN fine_balance > 50 THEN 'silver'
        WHEN fine_balance > 20 THEN 'gold'
        ELSE 'platinum'
    END AS tier_name,
    fine_balance AS points,
    registration_date AS joined_date
FROM users;

-- ================================================================
-- BACKUP LOGS TABLE FIX
-- ================================================================

-- Make created_by nullable to avoid foreign key issues
ALTER TABLE backup_logs
MODIFY COLUMN created_by INT NULL;

-- ================================================================
-- PRIVACY SETTINGS TABLE FIX
-- ================================================================

-- Ensure privacy_settings handles foreign key properly
-- Drop and recreate with proper ON DELETE CASCADE
ALTER TABLE privacy_settings 
DROP FOREIGN KEY IF EXISTS privacy_settings_ibfk_1;

ALTER TABLE privacy_settings
ADD CONSTRAINT privacy_settings_ibfk_1 
FOREIGN KEY (user_id) REFERENCES users (user_id) 
ON DELETE CASCADE;

-- Initialize privacy settings for existing users without settings
INSERT IGNORE INTO privacy_settings 
(user_id, show_email, show_phone, show_full_name, anonymous_mode,
 show_profile_photo, show_library, show_borrowing_history, show_activity_logs)
SELECT 
    u.user_id, 
    FALSE, FALSE, TRUE, FALSE, TRUE, TRUE, FALSE, FALSE
FROM users u
WHERE NOT EXISTS (
    SELECT 1 FROM privacy_settings ps WHERE ps.user_id = u.user_id
);

-- ================================================================
-- USER_PHOTOS TABLE FIX
-- ================================================================

-- Ensure user_photos table exists with proper structure
CREATE TABLE IF NOT EXISTS user_photos (
    photo_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    photo_image LONGBLOB NOT NULL,
    photo_filename VARCHAR(255),
    photo_size INT,
    uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE KEY unique_user_photo (user_id),
    FOREIGN KEY (user_id) REFERENCES users (user_id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ================================================================
-- USER_ACTIVITY_LOGS TABLE FIX
-- ================================================================

CREATE TABLE IF NOT EXISTS user_activity_logs (
    log_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    activity_type VARCHAR(100) NOT NULL,
    activity_details TEXT,
    ip_address VARCHAR(45),
    user_agent TEXT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_user_activity (user_id, timestamp),
    FOREIGN KEY (user_id) REFERENCES users (user_id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ================================================================
-- RENEWAL_REQUESTS TABLE FIX
-- ================================================================

CREATE TABLE IF NOT EXISTS renewal_requests (
    renewal_id INT AUTO_INCREMENT PRIMARY KEY,
    borrowing_id INT NOT NULL,
    requested_by INT NOT NULL,
    request_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    requested_days INT DEFAULT 14,
    status ENUM('pending', 'approved', 'rejected') DEFAULT 'pending',
    processed_by INT NULL,
    processed_date TIMESTAMP NULL,
    notes TEXT,
    INDEX idx_borrowing (borrowing_id),
    INDEX idx_status (status),
    FOREIGN KEY (borrowing_id) REFERENCES borrowing (borrowing_id) ON DELETE CASCADE,
    FOREIGN KEY (requested_by) REFERENCES users (user_id) ON DELETE CASCADE,
    FOREIGN KEY (processed_by) REFERENCES users (user_id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ================================================================
-- ADDITIONAL INDEXES FOR PERFORMANCE
-- ================================================================

-- Add indexes for frequently queried columns
ALTER TABLE borrowing
ADD INDEX IF NOT EXISTS idx_checkout_date (checkout_date),
ADD INDEX IF NOT EXISTS idx_due_date (due_date),
ADD INDEX IF NOT EXISTS idx_return_date (return_date),
ADD INDEX IF NOT EXISTS idx_status (status);

ALTER TABLE users
ADD INDEX IF NOT EXISTS idx_email (email),
ADD INDEX IF NOT EXISTS idx_username (username),
ADD INDEX IF NOT EXISTS idx_role (role_id),
ADD INDEX IF NOT EXISTS idx_active (is_active);

ALTER TABLE book_inventory
ADD INDEX IF NOT EXISTS idx_available (is_available),
ADD INDEX IF NOT EXISTS idx_book (book_id);

-- ================================================================
-- RE-ENABLE FOREIGN KEY CHECKS
-- ================================================================

SET FOREIGN_KEY_CHECKS = 1;

-- ================================================================
-- VERIFICATION
-- ================================================================

-- Verify all changes
SELECT 'Database schema updates completed successfully!' AS status;

SELECT COUNT(*) as total_users FROM users;
SELECT COUNT(*) as total_books FROM books;
SELECT COUNT(*) as total_borrowings FROM borrowing;
SELECT COUNT(*) as users_with_privacy FROM privacy_settings;

COMMIT;
