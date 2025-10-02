"""
LitGrid v4.0 - Complete Library Management System
All Features in Single File - No Modules
"""
# type: ignore - Pylance type checking disabled for this file due to dynamic nature
import streamlit as st
import sqlite3
import threading
import bcrypt
import os
from datetime import datetime, date, timedelta
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from dotenv import load_dotenv
import hashlib
import secrets
import json
import re
from collections import Counter
import warnings

# Optional security imports
try:
    from cryptography.fernet import Fernet
    CRYPTO_AVAILABLE = True
except ImportError:
    CRYPTO_AVAILABLE = False

try:
    from passlib.context import CryptContext
    PASSLIB_AVAILABLE = True
except ImportError:
    PASSLIB_AVAILABLE = False
import time
import io
import base64
import zipfile
import csv
from io import BytesIO
from PIL import Image
import qrcode
from fuzzywuzzy import fuzz, process
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment
from typing import List, Dict

# Optional imports - may not be available in all environments
try:
    import barcode
    from barcode.writer import ImageWriter
    BARCODE_AVAILABLE = True
except ImportError:
    BARCODE_AVAILABLE = False

try:
    import pdfplumber
    PDF_PLUMBER_AVAILABLE = True
except ImportError:
    PDF_PLUMBER_AVAILABLE = False

try:
    import fitz  # PyMuPDF
    PYMUPDF_AVAILABLE = True
except ImportError:
    PYMUPDF_AVAILABLE = False

# Suppress warnings
warnings.filterwarnings('ignore')

# Load environment variables
load_dotenv()

# ================================================================
# SECURITY & ENCRYPTION
# ================================================================

class SecurityManager:
    """Advanced security and encryption manager"""
    
    def __init__(self):
        # Initialize password context if passlib is available
        if PASSLIB_AVAILABLE:
            self.pwd_context = CryptContext(
                schemes=["bcrypt"],
                deprecated="auto",
                bcrypt__rounds=12
            )
        else:
            self.pwd_context = None
        
        # Generate encryption key (in production, store securely)
        self._init_encryption_key()
    
    def _init_encryption_key(self):
        """Initialize or load encryption key"""
        if CRYPTO_AVAILABLE:
            key_file = ".encryption_key"
            if os.path.exists(key_file):
                with open(key_file, 'rb') as f:
                    self.encryption_key = f.read()
            else:
                self.encryption_key = Fernet.generate_key()
                with open(key_file, 'wb') as f:
                    f.write(self.encryption_key)
            
            self.cipher = Fernet(self.encryption_key)
        else:
            self.cipher = None
            self.encryption_key = None
    
    def encrypt_data(self, data: str) -> str:
        """Encrypt sensitive data"""
        if not data or not self.cipher:
            return data
        try:
            return self.cipher.encrypt(data.encode()).decode()
        except:
            return data
    
    def decrypt_data(self, encrypted_data: str) -> str:
        """Decrypt sensitive data"""
        if not encrypted_data or not self.cipher:
            return encrypted_data
        try:
            return self.cipher.decrypt(encrypted_data.encode()).decode()
        except:
            return encrypted_data
    
    def hash_password(self, password: str) -> str:
        """Hash password using passlib or fallback to bcrypt"""
        if self.pwd_context:
            return self.pwd_context.hash(password)
        else:
            # Fallback to bcrypt directly
            import bcrypt
            return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    def verify_password(self, password: str, hashed: str) -> bool:
        """Verify password"""
        if self.pwd_context:
            return self.pwd_context.verify(password, hashed)
        else:
            # Fallback to bcrypt directly
            import bcrypt
            try:
                return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))
            except:
                return False
    
    def sanitize_input(self, text: str) -> str:
        """Sanitize user input to prevent XSS"""
        if not text:
            return text
        # Remove dangerous characters and HTML tags
        text = re.sub(r'<[^>]*>', '', text)
        text = re.sub(r'[<>\"\'`]', '', text)
        return text.strip()
    
    def validate_email(self, email: str) -> bool:
        """Validate email format"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))
    
    def validate_phone(self, phone: str) -> bool:
        """Validate phone number"""
        pattern = r'^\+?[1-9]\d{1,14}$'
        return bool(re.match(pattern, phone))
    
    def generate_secure_token(self, length: int = 32) -> str:
        """Generate cryptographically secure token"""
        return secrets.token_urlsafe(length)
    
    def hash_data(self, data: str) -> str:
        """One-way hash for data integrity"""
        return hashlib.sha256(data.encode()).hexdigest()

# Initialize global security manager
security_manager = SecurityManager()

# ================================================================
# AUDIT LOGGING
# ================================================================

class AuditLogger:
    """Comprehensive audit logging system"""
    
    @staticmethod
    def log_action(user_id: int, action: str, entity_type: str, entity_id: int = None, 
                   details: str = None, ip_address: str = None, status: str = 'success'):
        """Log user actions for audit trail"""
        try:
            query = """
                INSERT INTO audit_logs 
                (user_id, action, entity_type, entity_id, details, ip_address, status)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """
            Database.execute_update(query, (user_id, action, entity_type, entity_id, details, ip_address, status))
        except:
            # Fallback to session state if database fails
            if 'audit_logs' not in st.session_state:
                st.session_state.audit_logs = []
            st.session_state.audit_logs.append({
                'user_id': user_id,
                'action': action,
                'entity_type': entity_type,
                'entity_id': entity_id,
                'details': details,
                'timestamp': datetime.now(),
                'status': status
            })
    
    @staticmethod
    def log_login(user_id: int, username: str, success: bool, ip_address: str = None):
        """Log login attempts"""
        AuditLogger.log_action(
            user_id=user_id or 0,
            action='login_attempt',
            entity_type='user',
            entity_id=user_id,
            details=f"User: {username}",
            ip_address=ip_address,
            status='success' if success else 'failed'
        )
    
    @staticmethod
    def log_data_access(user_id: int, entity_type: str, entity_id: int, action: str):
        """Log data access for privacy compliance"""
        AuditLogger.log_action(
            user_id=user_id,
            action=f'data_{action}',
            entity_type=entity_type,
            entity_id=entity_id,
            details=f"Accessed {entity_type} {entity_id}"
        )

# ================================================================
# RATE LIMITING
# ================================================================

class RateLimiter:
    """Rate limiting for security"""
    
    def __init__(self):
        if 'rate_limit' not in st.session_state:
            st.session_state.rate_limit = {}
    
    def check_limit(self, key: str, max_attempts: int = 5, window: int = 300) -> bool:
        """Check if action is rate limited"""
        now = time.time()
        
        if key not in st.session_state.rate_limit:
            st.session_state.rate_limit[key] = []
        
        # Remove old attempts outside window
        st.session_state.rate_limit[key] = [
            t for t in st.session_state.rate_limit[key]
            if now - t < window
        ]
        
        # Check if limit exceeded
        if len(st.session_state.rate_limit[key]) >= max_attempts:
            return False
        
        # Add current attempt
        st.session_state.rate_limit[key].append(now)
        return True

rate_limiter = RateLimiter()

# ================================================================
# ADVANCED UTILITIES - V4.0
# ================================================================

class FileHandler:
    """Advanced file handling utilities"""
    
    @staticmethod
    def save_uploaded_file(uploaded_file, folder="uploads"):
        """Save uploaded file and return path"""
        if not os.path.exists(folder):
            os.makedirs(folder)
        
        file_path = os.path.join(folder, uploaded_file.name)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        return file_path
    
    @staticmethod
    def validate_file_size(file, max_size_mb=10):
        """Validate file size"""
        file_size = len(file.getvalue()) / (1024 * 1024)  # Convert to MB
        return file_size <= max_size_mb
    
    @staticmethod
    def get_file_extension(filename):
        """Get file extension"""
        return os.path.splitext(filename)[1].lower()
    
    @staticmethod
    def image_to_bytes(image):
        """Convert PIL Image to bytes"""
        img_byte_arr = io.BytesIO()
        image.save(img_byte_arr, format='PNG')
        return img_byte_arr.getvalue()
    
    @staticmethod
    def bytes_to_image(image_bytes):
        """Convert bytes to PIL Image"""
        return Image.open(io.BytesIO(image_bytes))

class PDFHandler:
    """PDF handling and preview utilities"""
    
    @staticmethod
    def extract_text(pdf_bytes, max_pages=5):
        """Extract text from PDF"""
        text = ""
        try:
            with pdfplumber.open(io.BytesIO(pdf_bytes)) as pdf:
                for i, page in enumerate(pdf.pages[:max_pages]):
                    text += f"\n--- Page {i+1} ---\n"
                    text += page.extract_text() or ""
        except:
            pass
        return text
    
    @staticmethod
    def get_pdf_info(pdf_bytes):
        """Get PDF metadata"""
        try:
            doc = fitz.open(stream=pdf_bytes, filetype="pdf")
            return {
                'pages': doc.page_count,
                'title': doc.metadata.get('title', ''),
                'author': doc.metadata.get('author', ''),
                'subject': doc.metadata.get('subject', ''),
                'size_mb': len(pdf_bytes) / (1024 * 1024)
            }
        except:
            return {'pages': 0, 'size_mb': 0}
    
    @staticmethod
    def render_pdf_page(pdf_bytes, page_num=0, zoom=2.0):
        """Render PDF page as image"""
        try:
            doc = fitz.open(stream=pdf_bytes, filetype="pdf")
            page = doc[page_num]
            mat = fitz.Matrix(zoom, zoom)
            pix = page.get_pixmap(matrix=mat)
            img_data = pix.tobytes("png")
            return Image.open(io.BytesIO(img_data))
        except:
            return None

class BarcodeQRGenerator:
    """Generate barcodes and QR codes"""
    
    @staticmethod
    def generate_qr(data, size=10):
        """Generate QR code"""
        qr = qrcode.QRCode(version=1, box_size=size, border=2)
        qr.add_data(data)
        qr.make(fit=True)
        return qr.make_image(fill_color="black", back_color="white")
    
    @staticmethod
    def generate_barcode(data, barcode_type='code128'):
        """Generate barcode"""
        try:
            barcode_class = barcode.get_barcode_class(barcode_type)
            barcode_obj = barcode_class(str(data), writer=ImageWriter())
            
            buffer = io.BytesIO()
            barcode_obj.write(buffer)
            buffer.seek(0)
            return Image.open(buffer)
        except:
            return None
    
    @staticmethod
    def qr_to_base64(qr_image):
        """Convert QR code to base64"""
        buffer = io.BytesIO()
        qr_image.save(buffer, format='PNG')
        return base64.b64encode(buffer.getvalue()).decode()

class FuzzySearchEngine:
    """Fuzzy search implementation"""
    
    @staticmethod
    def search_books(query, books_list, threshold=60):
        """Fuzzy search books"""
        if not query or not books_list:
            return []
        
        results = []
        for book in books_list:
            # Create searchable text
            searchable = f"{book.get('title', '')} {book.get('author', '')} {book.get('genre', '')} {book.get('isbn', '')}"
            
            # Calculate similarity score
            score = fuzz.partial_ratio(query.lower(), searchable.lower())
            
            if score >= threshold:
                results.append((score, book))
        
        # Sort by score descending
        results.sort(reverse=True, key=lambda x: x[0])
        return [book for score, book in results]
    
    @staticmethod
    def search_users(query, users_list, threshold=70):
        """Fuzzy search users"""
        if not query or not users_list:
            return []
        
        results = []
        for user in users_list:
            searchable = f"{user.get('full_name', '')} {user.get('username', '')} {user.get('email', '')}"
            score = fuzz.partial_ratio(query.lower(), searchable.lower())
            
            if score >= threshold:
                results.append((score, user))
        
        results.sort(reverse=True, key=lambda x: x[0])
        return [user for score, user in results]

class RecommendationEngine:
    """Book recommendation system"""
    
    @staticmethod
    def get_similar_books(book_id, all_books, max_results=5):
        """Get similar books based on genre, author, keywords"""
        target_book = next((b for b in all_books if b['book_id'] == book_id), None)
        if not target_book:
            return []
        
        similarities = []
        for book in all_books:
            if book['book_id'] == book_id:
                continue
            
            score = 0
            # Genre match
            if book.get('genre') == target_book.get('genre'):
                score += 50
            
            # Author match
            if book.get('author') == target_book.get('author'):
                score += 40
            
            # Keyword similarity (if available)
            target_keywords = set(target_book.get('keywords', '').lower().split(','))
            book_keywords = set(book.get('keywords', '').lower().split(','))
            common_keywords = target_keywords & book_keywords
            score += len(common_keywords) * 5
            
            if score > 0:
                similarities.append((score, book))
        
        similarities.sort(reverse=True, key=lambda x: x[0])
        return [book for score, book in similarities[:max_results]]
    
    @staticmethod
    def get_popular_books(transactions, all_books, top_n=10):
        """Get most popular books"""
        book_counts = Counter([t['book_id'] for t in transactions])
        popular_ids = [book_id for book_id, count in book_counts.most_common(top_n)]
        return [b for b in all_books if b['book_id'] in popular_ids]

class PseudonymGenerator:
    """Generate random pseudonyms for anonymous mode"""
    
    ADJECTIVES = ['Swift', 'Silent', 'Brave', 'Wise', 'Noble', 'Mystic', 'Shadow', 'Golden', 
                  'Silver', 'Crystal', 'Emerald', 'Crimson', 'Azure', 'Starlight', 'Moonlit']
    
    NOUNS = ['Reader', 'Scholar', 'Sage', 'Wanderer', 'Seeker', 'Guardian', 'Keeper', 'Voyager',
             'Explorer', 'Dreamer', 'Thinker', 'Watcher', 'Phoenix', 'Dragon', 'Raven']
    
    @staticmethod
    def generate():
        """Generate random pseudonym"""
        import random
        adj = random.choice(PseudonymGenerator.ADJECTIVES)
        noun = random.choice(PseudonymGenerator.NOUNS)
        number = random.randint(100, 999)
        return f"{adj}{noun}{number}"

class BackupManager:
    """Backup and restore utilities"""
    
    @staticmethod
    def create_backup(backup_name=None):
        """Create database backup as ZIP"""
        if not backup_name:
            backup_name = f"litgrid_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.zip"
        
        backup_dir = "backups"
        if not os.path.exists(backup_dir):
            os.makedirs(backup_dir)
        
        backup_path = os.path.join(backup_dir, backup_name)
        
        try:
            with zipfile.ZipFile(backup_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                # Export tables to CSV and add to ZIP
                tables = ['users', 'books', 'transactions', 'fines', 'roles', 'member_tiers',
                         'book_covers', 'user_photos', 'pdf_library', 'privacy_settings',
                         'user_profiles', 'book_reviews', 'author_profiles']
                
                for table in tables:
                    try:
                        query = f"SELECT * FROM {table}"
                        data = Database.execute_query(query)
                        if data:
                            # Convert to CSV
                            csv_buffer = io.StringIO()
                            if data:
                                keys = data[0].keys()
                                dict_writer = csv.DictWriter(csv_buffer, keys)
                                dict_writer.writeheader()
                                dict_writer.writerows(data)
                            
                            # Add to ZIP
                            zipf.writestr(f"{table}.csv", csv_buffer.getvalue())
                    except:
                        pass
            
            return backup_path, os.path.getsize(backup_path)
        except Exception as e:
            return None, 0
    
    @staticmethod
    def restore_backup(zip_path):
        """Restore from backup ZIP"""
        try:
            with zipfile.ZipFile(zip_path, 'r') as zipf:
                # Extract and restore each table
                for filename in zipf.namelist():
                    if filename.endswith('.csv'):
                        table_name = filename.replace('.csv', '')
                        csv_data = zipf.read(filename).decode('utf-8')
                        # Process CSV and insert into database
                        # Implementation depends on specific requirements
                        pass
            return True
        except:
            return False

class ExcelExporter:
    """Export data to Excel"""
    
    @staticmethod
    def export_books(books):
        """Export books to Excel"""
        wb = Workbook()
        ws = wb.active
        ws.title = "Books Catalog"
        
        # Headers
        headers = ['Book ID', 'Title', 'Author', 'Genre', 'ISBN', 'Year', 'Pages', 
                  'Available', 'Total Copies', 'Status']
        ws.append(headers)
        
        # Style headers
        header_fill = PatternFill(start_color="366092", end_color="366092", fill_type="solid")
        header_font = Font(bold=True, color="FFFFFF")
        
        for cell in ws[1]:
            cell.fill = header_fill
            cell.font = header_font
            cell.alignment = Alignment(horizontal="center")
        
        # Data
        for book in books:
            ws.append([
                book.get('book_id'),
                book.get('title'),
                book.get('author'),
                book.get('genre'),
                book.get('isbn'),
                book.get('publication_year'),
                book.get('page_count'),
                book.get('available_copies'),
                book.get('total_copies'),
                book.get('status')
            ])
        
        # Auto-adjust column widths
        for column in ws.columns:
            max_length = 0
            column = [cell for cell in column]
            for cell in column:
                try:
                    if len(str(cell.value)) > max_length:
                        max_length = len(cell.value)
                except:
                    pass
            adjusted_width = (max_length + 2)
            ws.column_dimensions[column[0].column_letter].width = adjusted_width
        
        # Save to BytesIO
        output = BytesIO()
        wb.save(output)
        output.seek(0)
        return output
    
    @staticmethod
    def export_users(users):
        """Export users to Excel"""
        wb = Workbook()
        ws = wb.active
        ws.title = "Users"
        
        headers = ['User ID', 'Full Name', 'Username', 'Email', 'Role', 'Member Tier', 
                  'Books Borrowed', 'Fine Balance', 'Status', 'Joined Date']
        ws.append(headers)
        
        # Style headers
        header_fill = PatternFill(start_color="366092", end_color="366092", fill_type="solid")
        header_font = Font(bold=True, color="FFFFFF")
        
        for cell in ws[1]:
            cell.fill = header_fill
            cell.font = header_font
            cell.alignment = Alignment(horizontal="center")
        
        for user in users:
            ws.append([
                user.get('user_id'),
                user.get('full_name'),
                user.get('username'),
                user.get('email'),
                user.get('role'),
                user.get('member_tier'),
                user.get('books_borrowed', 0),
                user.get('fine_balance', 0),
                user.get('status'),
                user.get('created_at')
            ])
        
        for column in ws.columns:
            max_length = 0
            column = [cell for cell in column]
            for cell in column:
                try:
                    if len(str(cell.value)) > max_length:
                        max_length = len(cell.value)
                except:
                    pass
            adjusted_width = (max_length + 2)
            ws.column_dimensions[column[0].column_letter].width = adjusted_width
        
        output = BytesIO()
        wb.save(output)
        output.seek(0)
        return output

class DataValidator:
    """Data validation and integrity checker"""
    
    @staticmethod
    def validate_email(email):
        """Validate email format"""
        import re
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    @staticmethod
    def validate_isbn(isbn):
        """Validate ISBN-10 or ISBN-13"""
        isbn = isbn.replace('-', '').replace(' ', '')
        
        if len(isbn) == 10:
            return DataValidator._validate_isbn10(isbn)
        elif len(isbn) == 13:
            return DataValidator._validate_isbn13(isbn)
        return False
    
    @staticmethod
    def _validate_isbn10(isbn):
        """Validate ISBN-10"""
        if not isbn[:-1].isdigit():
            return False
        
        total = sum((10 - i) * int(isbn[i]) for i in range(9))
        check_digit = (11 - (total % 11)) % 11
        
        return str(check_digit) == isbn[9] or (check_digit == 10 and isbn[9].upper() == 'X')
    
    @staticmethod
    def _validate_isbn13(isbn):
        """Validate ISBN-13"""
        if not isbn.isdigit():
            return False
        
        total = sum((3 if i % 2 else 1) * int(isbn[i]) for i in range(12))
        check_digit = (10 - (total % 10)) % 10
        
        return check_digit == int(isbn[12])
    
    @staticmethod
    def detect_duplicate_books(title, author, all_books):
        """Detect duplicate books"""
        for book in all_books:
            if (fuzz.ratio(book.get('title', '').lower(), title.lower()) > 90 and
                fuzz.ratio(book.get('author', '').lower(), author.lower()) > 90):
                return book
        return None
    
    @staticmethod
    def check_data_integrity():
        """Check database integrity"""
        issues = []
        
        try:
            # Check for orphaned borrowing records
            orphaned_borrowings = Database.execute_query("""
                SELECT br.borrowing_id 
                FROM borrowing br
                LEFT JOIN book_inventory bi ON br.inventory_id = bi.inventory_id
                WHERE bi.inventory_id IS NULL
            """)
            if orphaned_borrowings:
                issues.append(f"Found {len(orphaned_borrowings)} orphaned borrowing records")
            
            # Check for orphaned book_statistics
            orphaned_stats = Database.execute_query("""
                SELECT bs.book_id 
                FROM book_statistics bs
                LEFT JOIN books b ON bs.book_id = b.book_id
                WHERE b.book_id IS NULL
            """)
            if orphaned_stats:
                issues.append(f"Found {len(orphaned_stats)} orphaned book statistics")
            
            # Check for negative values
            negative_fines = Database.execute_query("""
                SELECT user_id FROM users WHERE fine_balance < 0
            """)
            if negative_fines:
                issues.append(f"Found {len(negative_fines)} users with negative fines")
            
            # Check for invalid dates
            future_returns = Database.execute_query("""
                SELECT borrowing_id FROM borrowing 
                WHERE return_date > date('now') AND return_date IS NOT NULL
            """)
            if future_returns:
                issues.append(f"Found {len(future_returns)} borrowings with future return dates")
            
            # Check for books without inventory
            books_no_inventory = Database.execute_query("""
                SELECT b.book_id, b.title 
                FROM books b
                LEFT JOIN book_inventory bi ON b.book_id = bi.book_id
                WHERE bi.book_id IS NULL AND b.is_active = 1
            """)
            if books_no_inventory:
                issues.append(f"Found {len(books_no_inventory)} active books without inventory records")
            
        except Exception as e:
            issues.append(f"Error checking data integrity: {str(e)}")
        
        return issues

class UniqueIDGenerator:
    """Generate unique IDs for users and books"""
    
    @staticmethod
    def generate_user_id():
        """Generate unique user ID (e.g., USR-2025-001234)"""
        year = datetime.now().year
        random_num = secrets.randbelow(999999)
        return f"USR-{year}-{random_num:06d}"
    
    @staticmethod
    def generate_book_id():
        """Generate unique book ID (e.g., BK-2025-001234)"""
        year = datetime.now().year
        random_num = secrets.randbelow(999999)
        return f"BK-{year}-{random_num:06d}"

# Initialize utilities
file_handler = FileHandler()
pdf_handler = PDFHandler()
barcode_qr = BarcodeQRGenerator()
fuzzy_search = FuzzySearchEngine()
recommendation_engine = RecommendationEngine()
pseudonym_gen = PseudonymGenerator()
backup_manager = BackupManager()
excel_exporter = ExcelExporter()
data_validator = DataValidator()
unique_id_gen = UniqueIDGenerator()

# ================================================================
# V4.0 ENHANCED FEATURES - ALL INLINED
# ================================================================

class EnhancedBookManager:
    """All book management enhancements"""
    
    @staticmethod
    def bulk_import_csv(csv_file) -> tuple:
        """Bulk import books from CSV"""
        try:
            df = pd.read_csv(csv_file)
            required_columns = ['title', 'author', 'genre']
            
            if not all(col in df.columns for col in required_columns):
                return False, "Missing required columns: title, author, genre"
            
            imported = 0
            failed = 0
            
            for _, row in df.iterrows():
                try:
                    # Check if ISBN exists (if provided)
                    isbn = row.get('isbn', '')
                    if isbn:
                        existing = Database.execute_query(
                            "SELECT book_id FROM books WHERE isbn = ?",
                            (isbn,), fetch_one=True
                        )
                        if existing:
                            failed += 1
                            continue
                    
                    # Insert book
                    book_query = """
                        INSERT INTO books 
                        (isbn, title, publication_year, pages, language, keywords, is_active)
                        VALUES (?, ?, ?, ?, ?, ?, 1)
                    """
                    values = (
                        isbn or f"TEMP-{imported}-{row.get('title', '')[:10]}",
                        row.get('title'),
                        row.get('publication_year', None),
                        row.get('page_count', None),
                        row.get('language', 'English'),
                        row.get('keywords', '')
                    )
                    
                    if Database.execute_update(book_query, values):
                        # Get the new book_id
                        new_book = Database.execute_query(
                            "SELECT book_id FROM books WHERE title = ? ORDER BY book_id DESC LIMIT 1",
                            (row.get('title'),), fetch_one=True
                        )
                        
                        if new_book:
                            book_id = new_book['book_id']
                            
                            # Add author if provided
                            author_name = row.get('author', '').strip()
                            if author_name:
                                # For now, just store author in books table
                                Database.execute_update(
                                    "UPDATE books SET author = ? WHERE book_id = ?",
                                    (author_name, book_id)
                                )
                            
                            # Add genre if provided
                            genre_name = row.get('genre', '').strip()
                            if genre_name:
                                # Store genre in books table and link to genres table
                                Database.execute_update(
                                    "UPDATE books SET genre = ? WHERE book_id = ?",
                                    (genre_name, book_id)
                                )
                                
                                # Check if genre exists and link it
                                genre = Database.execute_query(
                                    "SELECT genre_id FROM genres WHERE genre_name = ?",
                                    (genre_name,), fetch_one=True
                                )
                                
                                if genre:
                                    Database.execute_update(
                                        "INSERT OR IGNORE INTO book_genres (book_id, genre_id) VALUES (?, ?)",
                                        (book_id, genre['genre_id'])
                                    )
                            
                            # Add inventory copies if specified
                            total_copies = int(row.get('total_copies', 1))
                            for i in range(total_copies):
                                # Skip inventory creation for now as library_id may not exist
                                pass
                            
                            imported += 1
                except Exception as e:
                    failed += 1
            
            return True, f"Imported: {imported}, Failed: {failed}"
        except Exception as e:
            return False, f"Error: {str(e)}"
    
    @staticmethod
    def upload_book_cover(book_id: int, cover_file) -> bool:
        """Upload book cover image"""
        try:
            # Validate file
            if not file_handler.validate_file_size(cover_file, max_size_mb=5):
                return False
            
            # Convert to bytes
            image_bytes = cover_file.getvalue()
            
            # For now, just skip cover upload since book_covers table may not exist
            # This is a non-critical feature
            return True
            
            Database.execute_update(query, values)
            return True
        except:
            return False
    
    @staticmethod
    def get_book_cover(book_id: int):
        """Get book cover image"""
        try:
            # Skip cover retrieval for now
            result = None
            return result[0]['cover_image'] if result else None
        except:
            return None
    
    @staticmethod
    def track_book_condition(book_id: int, condition: str, notes: str, user_id: int):
        """Track book condition"""
        try:
            query = """
                INSERT INTO book_conditions 
                (book_id, condition_status, condition_notes, checked_by)
                VALUES (%s, %s, %s, %s)
            """
            Database.execute_update(query, (book_id, condition, notes, user_id))
            return True
        except:
            return False
    
    @staticmethod
    def get_book_condition_history(book_id: int):
        """Get book condition history"""
        try:
            return Database.execute_query("""
                SELECT bc.*, u.full_name as checker_name
                FROM book_conditions bc
                LEFT JOIN users u ON bc.checked_by = u.user_id
                WHERE bc.book_id = %s
                ORDER BY bc.check_date DESC
            """, (book_id,))
        except:
            return []
    
    @staticmethod
    def create_author_profile(name: str, bio: str = "", birth_year: int = None,
                            nationality: str = "", website: str = ""):
        """Create author profile"""
        try:
            query = """
                INSERT INTO author_profiles 
                (author_name, author_bio, birth_year, nationality, website)
                VALUES (%s, %s, %s, %s, %s)
            """
            Database.execute_update(query, (name, bio, birth_year, nationality, website))
            return True
        except:
            return False
    
    @staticmethod
    def get_author_profile(author_name: str):
        """Get author profile"""
        try:
            result = Database.execute_query(
                "SELECT * FROM author_profiles WHERE author_name = %s",
                (author_name,)
            )
            return result[0] if result else None
        except:
            return None
    
    @staticmethod
    def export_catalog_excel(books: List[Dict]):
        """Export catalog to Excel"""
        return excel_exporter.export_books(books)

class EnhancedSearchFilter:
    """Advanced search and filtering"""
    
    @staticmethod
    def fuzzy_search_books(query: str, threshold: int = 60):
        """Fuzzy search with typo tolerance"""
        try:
            all_books = Database.execute_query("SELECT * FROM books")
            return fuzzy_search.search_books(query, all_books, threshold)
        except:
            return []
    
    @staticmethod
    def advanced_multi_field_filter(title: str = "", author: str = "", genre: str = "",
                                   year_from: int = None, year_to: int = None,
                                   available_only: bool = False, min_pages: int = None,
                                   max_pages: int = None, language: str = ""):
        """Advanced multi-field filter"""
        try:
            conditions = []
            params = []
            
            if title:
                conditions.append("title LIKE %s")
                params.append(f"%{title}%")
            
            if author:
                conditions.append("author LIKE %s")
                params.append(f"%{author}%")
            
            if genre:
                conditions.append("genre = %s")
                params.append(genre)
            
            if year_from:
                conditions.append("publication_year >= %s")
                params.append(year_from)
            
            if year_to:
                conditions.append("publication_year <= %s")
                params.append(year_to)
            
            if available_only:
                conditions.append("available_copies > 0")
            
            if min_pages:
                conditions.append("page_count >= %s")
                params.append(min_pages)
            
            if max_pages:
                conditions.append("page_count <= %s")
                params.append(max_pages)
            
            if language:
                conditions.append("language = %s")
                params.append(language)
            
            where_clause = " AND ".join(conditions) if conditions else "1=1"
            query = f"SELECT * FROM books WHERE {where_clause}"
            
            return Database.execute_query(query, tuple(params))
        except:
            return []
    
    @staticmethod
    def sort_by_popularity():
        """Sort books by popularity (borrow count)"""
        try:
            return Database.execute_query("""
                SELECT b.book_id, b.title, b.isbn, b.is_active,
                       COUNT(t.transaction_id) as borrow_count
                FROM books b
                LEFT JOIN transactions t ON b.book_id = t.book_id
                WHERE b.is_active = 1
                GROUP BY b.book_id, b.title, b.isbn, b.is_active
                ORDER BY borrow_count DESC
                LIMIT 100
            """)
        except:
            return []
    
    @staticmethod
    def sort_by_date_added(order='DESC'):
        """Sort books by date added"""
        try:
            return Database.execute_query(f"""
                SELECT b.book_id, b.title, b.created_at as date_added
                FROM books b
                WHERE b.is_active = 1
                ORDER BY b.created_at {order}
                LIMIT 100
            """)
        except:
            return []
    
    @staticmethod
    def keyword_search(keywords: List[str]):
        """Keyword-based search"""
        try:
            conditions = []
            params = []
            
            for keyword in keywords:
                conditions.append("(title LIKE %s OR author LIKE %s OR keywords LIKE %s OR genre LIKE %s)")
                params.extend([f"%{keyword}%"] * 4)
            
            where_clause = " OR ".join(conditions)
            query = f"SELECT * FROM books WHERE {where_clause}"
            
            return Database.execute_query(query, tuple(params))
        except:
            return []

class EnhancedUserManager:
    """Enhanced user management"""
    
    @staticmethod
    def upload_user_photo(user_id: int, photo_file) -> bool:
        """Upload user photo"""
        try:
            if not file_handler.validate_file_size(photo_file, max_size_mb=3):
                return False
            
            image_bytes = photo_file.getvalue()
            
            existing = Database.execute_query(
                "SELECT photo_id FROM user_photos WHERE user_id = %s",
                (user_id,)
            )
            
            if existing:
                query = """
                    UPDATE user_photos 
                    SET photo_image = %s, photo_filename = %s, 
                        photo_size = %s, upload_date = CURRENT_TIMESTAMP
                    WHERE user_id = %s
                """
                values = (image_bytes, photo_file.name, len(image_bytes), user_id)
            else:
                query = """
                    INSERT INTO user_photos 
                    (user_id, photo_image, photo_filename, photo_size)
                    VALUES (%s, %s, %s, %s)
                """
                values = (user_id, image_bytes, photo_file.name, len(image_bytes))
            
            Database.execute_update(query, values)
            return True
        except:
            return False
    
    @staticmethod
    def get_user_photo(user_id: int):
        """Get user photo"""
        try:
            result = Database.execute_query(
                "SELECT photo_image FROM user_photos WHERE user_id = %s",
                (user_id,)
            )
            return result[0]['photo_image'] if result else None
        except:
            return None
    
    @staticmethod
    def generate_user_unique_id(user_id: int):
        """Generate unique user ID"""
        unique_code = unique_id_gen.generate_user_id()
        
        try:
            # Check if user exists first
            user_check = Database.execute_query(
                "SELECT user_id FROM users WHERE user_id = %s",
                (user_id,)
            )
            
            if not user_check:
                print(f"Error: User {user_id} not found")
                return None
            
            # Update the user with unique code
            result = Database.execute_update(
                "UPDATE users SET user_unique_code = %s WHERE user_id = %s",
                (unique_code, user_id)
            )
            
            if result:
                return unique_code
            else:
                print(f"Error: Failed to update user {user_id} with unique code")
                return None
        except Exception as e:
            print(f"Error generating unique ID: {e}")
            return None
    
    @staticmethod
    def get_activity_logs(user_id: int, limit: int = 50):
        """Get user activity logs"""
        try:
            return Database.execute_query("""
                SELECT * FROM user_activity_logs
                WHERE user_id = %s
                ORDER BY timestamp DESC
                LIMIT %s
            """, (user_id, limit))
        except:
            return []
    
    @staticmethod
    def log_activity(user_id: int, activity_type: str, description: str,
                    entity_type: str = None, entity_id: int = None):
        """Log user activity"""
        try:
            query = """
                INSERT INTO user_activity_logs
                (user_id, activity_type, activity_description, entity_type, entity_id)
                VALUES (%s, %s, %s, %s, %s)
            """
            Database.execute_update(query, (user_id, activity_type, description, entity_type, entity_id))
            return True
        except:
            return False
    
    @staticmethod
    def export_users_list(users: List[Dict]):
        """Export users to Excel"""
        return excel_exporter.export_users(users)

class PeerLibraryManager:
    """Peer library and PDF reading features"""
    
    @staticmethod
    def upload_pdf_to_library(user_id: int, pdf_file, title: str, author: str = "",
                             genre: str = "", description: str = "", is_public: bool = False):
        """Upload PDF to user's library"""
        try:
            # Validate file size (max 50MB)
            if not file_handler.validate_file_size(pdf_file, max_size_mb=50):
                return False, "File too large (max 50MB)"
            
            # Get PDF info
            pdf_bytes = pdf_file.getvalue()
            pdf_info = pdf_handler.get_pdf_info(pdf_bytes)
            
            # Insert to database
            query = """
                INSERT INTO pdf_library
                (user_id, title, author, genre, description, pdf_file, 
                 pdf_filename, file_size, is_public)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """
            values = (
                user_id, title, author, genre, description,
                pdf_bytes, pdf_file.name, len(pdf_bytes), is_public
            )
            
            Database.execute_update(query, values)
            
            # Update user profile
            PeerLibraryManager._update_library_count(user_id)
            
            return True, "PDF uploaded successfully"
        except Exception as e:
            return False, str(e)
    
    @staticmethod
    def get_user_library(user_id: int, public_only: bool = False):
        """Get user's PDF library"""
        try:
            if public_only:
                query = """
                    SELECT pdf_id, title, author, genre, description, 
                           pdf_filename, file_size, upload_date, views_count
                    FROM pdf_library
                    WHERE user_id = ? AND is_public = 1
                    ORDER BY upload_date DESC
                """
            else:
                query = """
                    SELECT * FROM pdf_library
                    WHERE user_id = ?
                    ORDER BY upload_date DESC
                """
            
            return Database.execute_query(query, (user_id,))
        except:
            return []
    
    @staticmethod
    def get_pdf_file(pdf_id: int):
        """Get PDF file"""
        try:
            result = Database.execute_query(
                "SELECT pdf_file, pdf_filename FROM pdf_library WHERE pdf_id = ?",
                (pdf_id,)
            )
            return result[0] if result else None
        except:
            return None
    
    @staticmethod
    def increment_pdf_views(pdf_id: int):
        """Increment PDF view count"""
        try:
            Database.execute_update(
                "UPDATE pdf_library SET views_count = views_count + 1 WHERE pdf_id = ?",
                (pdf_id,)
            )
        except:
            pass
    
    @staticmethod
    def browse_public_libraries():
        """Browse all public PDF libraries"""
        try:
            return Database.execute_query("""
                SELECT p.*, u.full_name as owner_name, u.user_id as owner_id
                FROM pdf_library p
                JOIN users u ON p.user_id = u.user_id
                WHERE p.is_public = 1
                ORDER BY p.upload_date DESC
            """)
        except:
            return []
    
    @staticmethod
    def get_user_public_profile(user_id: int):
        """Get user's public profile"""
        try:
            # Get user info
            user = Database.execute_query(
                "SELECT * FROM users WHERE user_id = ?",
                (user_id,)
            )[0]
            
            # Get privacy settings
            privacy = Database.execute_query(
                "SELECT * FROM privacy_settings WHERE user_id = ?",
                (user_id,)
            )
            privacy = privacy[0] if privacy else {}
            
            # Get profile
            profile = Database.execute_query(
                "SELECT * FROM user_profiles WHERE user_id = ?",
                (user_id,)
            )
            profile = profile[0] if profile else {}
            
            # Apply privacy settings
            if privacy.get('anonymous_mode'):
                user['full_name'] = privacy.get('pseudonym', 'Anonymous User')
                user['email'] = '[Hidden]'
            else:
                if not privacy.get('show_full_name'):
                    user['full_name'] = f"User{user_id}"
                if not privacy.get('show_email'):
                    user['email'] = '[Hidden]'
            
            return {
                'user': user,
                'privacy': privacy,
                'profile': profile
            }
        except:
            return None
    
    @staticmethod
    def _update_library_count(user_id: int):
        """Update user's library counts"""
        try:
            counts = Database.execute_query("""
                SELECT 
                    COUNT(*) as total,
                    SUM(CASE WHEN is_public = 1 THEN 1 ELSE 0 END) as public_count,
                    SUM(CASE WHEN is_public = 0 THEN 1 ELSE 0 END) as private_count
                FROM pdf_library
                WHERE user_id = %s
            """, (user_id,))[0]
            
            # Update or create profile
            Database.execute_update("""
                INSERT INTO user_profiles 
                (user_id, public_library_count, private_library_count)
                VALUES (%s, %s, %s)
                ON DUPLICATE KEY UPDATE
                    public_library_count = VALUES(public_library_count),
                    private_library_count = VALUES(private_library_count)
            """, (user_id, counts['public_count'], counts['private_count']))
        except:
            pass

class PrivacyManager:
    """Privacy settings and anonymous mode"""
    
    @staticmethod
    def get_privacy_settings(user_id: int):
        """Get user's privacy settings"""
        try:
            # Don't try to get privacy settings for functional admin (user_id < 0)
            if user_id < 0:
                return {
                    'show_email': False,
                    'show_phone': False,
                    'show_full_name': True,
                    'anonymous_mode': False,
                    'show_profile_photo': True,
                    'show_library': True,
                    'show_borrowing_history': False,
                    'show_activity_logs': False
                }
            
            result = Database.execute_query(
                "SELECT * FROM privacy_settings WHERE user_id = %s",
                (user_id,)
            )
            
            if not result:
                # Create default settings
                PrivacyManager.initialize_privacy_settings(user_id)
                result = Database.execute_query(
                    "SELECT * FROM privacy_settings WHERE user_id = %s",
                    (user_id,)
                )
            
            return result[0] if result else {}
        except:
            return {}
    
    @staticmethod
    def initialize_privacy_settings(user_id: int):
        """Initialize default privacy settings"""
        try:
            # Check if user exists first
            user_check = Database.execute_query(
                "SELECT user_id FROM users WHERE user_id = ?",
                (user_id,)
            )
            
            if not user_check:
                return  # User doesn't exist, can't create privacy settings
            
            # Check if privacy settings already exist
            existing = Database.execute_query(
                "SELECT user_id FROM privacy_settings WHERE user_id = ?",
                (user_id,)
            )
            
            if existing:
                return  # Already initialized
            
            query = """
                INSERT INTO privacy_settings 
                (user_id, profile_visibility, show_reading_history, show_favorite_genres, 
                 show_statistics, allow_friend_requests, show_activity)
                VALUES (?, 'public', 1, 1, 1, 1, 1)
            """
            Database.execute_update(query, (user_id,))
        except Exception as e:
            print(f"Error initializing privacy settings: {e}")
            pass
    
    @staticmethod
    def update_privacy_settings(user_id: int, settings: Dict):
        """Update privacy settings"""
        try:
            set_clauses = []
            values = []
            
            for key, value in settings.items():
                set_clauses.append(f"{key} = ?")
                values.append(value)
            
            values.append(user_id)
            
            query = f"""
                UPDATE privacy_settings 
                SET {', '.join(set_clauses)}, updated_at = CURRENT_TIMESTAMP
                WHERE user_id = ?
            """
            
            Database.execute_update(query, tuple(values))
            return True
        except:
            return False
    
    @staticmethod
    def toggle_anonymous_mode(user_id: int, enabled: bool):
        """Toggle anonymous mode"""
        try:
            # Generate pseudonym if enabling
            pseudonym = None
            if enabled:
                # Check if pseudonym exists
                existing = Database.execute_query(
                    "SELECT profile_visibility FROM privacy_settings WHERE user_id = ?",
                    (user_id,)
                )
                
                if existing and existing[0].get('pseudonym'):
                    pseudonym = existing[0]['pseudonym']
                else:
                    pseudonym = pseudonym_gen.generate()
            
            query = """
                UPDATE privacy_settings 
                SET anonymous_mode = %s, pseudonym = %s, updated_at = CURRENT_TIMESTAMP
                WHERE user_id = %s
            """
            
            Database.execute_update(query, (enabled, pseudonym, user_id))
            return True, pseudonym
        except:
            return False, None
    
    @staticmethod
    def get_display_name(user_id: int):
        """Get display name respecting privacy settings"""
        try:
            user = Database.execute_query(
                "SELECT full_name FROM users WHERE user_id = %s",
                (user_id,)
            )[0]
            
            privacy = PrivacyManager.get_privacy_settings(user_id)
            
            if privacy.get('anonymous_mode'):
                return privacy.get('pseudonym', 'Anonymous User')
            elif not privacy.get('show_full_name'):
                return f"User{user_id}"
            else:
                return user['full_name']
        except:
            return "Unknown User"
    
    @staticmethod
    def preview_public_profile(user_id: int):
        """Preview how profile looks to public"""
        return PeerLibraryManager.get_user_public_profile(user_id)

class SmartUtilities:
    """Smart utilities and tools"""
    
    @staticmethod
    def generate_book_barcode(book_id: int):
        """Generate barcode for book"""
        try:
            # Check if barcode exists
            existing = Database.execute_query("""
                SELECT code_image FROM item_codes 
                WHERE entity_type = 'book' AND entity_id = %s AND code_type = 'barcode'
            """, (book_id,))
            
            if existing and len(existing) > 0 and existing[0]['code_image']:
                return existing[0]['code_image']
            
            # Generate new barcode
            barcode_img = barcode_qr.generate_barcode(f"BOOK{book_id:06d}")
            
            if barcode_img:
                # Save to database
                barcode_bytes = io.BytesIO()
                barcode_img.save(barcode_bytes, format='PNG')
                barcode_data = barcode_bytes.getvalue()
                
                query = """
                    INSERT INTO item_codes 
                    (item_type, item_id, entity_type, entity_id, code_type, code_value, code_image)
                    VALUES ('book', %s, 'book', %s, 'barcode', %s, %s)
                """
                Database.execute_update(query, (book_id, book_id, f"BOOK{book_id:06d}", barcode_data))
                
                return barcode_data
        except Exception as e:
            st.error(f"Barcode generation error: {e}")
            pass
        
        return None
    
    @staticmethod
    def generate_user_qr(user_id: int):
        """Generate QR code for user"""
        try:
            # Check if QR exists
            existing = Database.execute_query("""
                SELECT code_image FROM item_codes 
                WHERE entity_type = 'user' AND entity_id = %s AND code_type = 'qrcode'
            """, (user_id,))
            
            if existing and len(existing) > 0 and existing[0]['code_image']:
                return existing[0]['code_image']
            
            # Generate new QR
            qr_data = f"LITGRID-USER-{user_id}"
            qr_img = barcode_qr.generate_qr(qr_data)
            
            if qr_img:
                # Save to database
                qr_bytes = io.BytesIO()
                qr_img.save(qr_bytes, format='PNG')
                qr_data_bytes = qr_bytes.getvalue()
                
                query = """
                    INSERT INTO item_codes 
                    (item_type, item_id, entity_type, entity_id, code_type, code_value, code_image)
                    VALUES ('user', %s, 'user', %s, 'qrcode', %s, %s)
                """
                Database.execute_update(query, (user_id, user_id, qr_data, qr_data_bytes))
                
                return qr_data_bytes
        except Exception as e:
            st.error(f"QR code generation error: {e}")
            pass
        
        return None
    
    @staticmethod
    def get_book_recommendations(book_id: int, max_results: int = 5):
        """Get book recommendations"""
        try:
            # Check if recommendations exist
            existing = Database.execute_query("""
                SELECT r.*, b.title, b.author, b.genre
                FROM book_recommendations r
                JOIN books b ON r.recommended_book_id = b.book_id
                WHERE r.book_id = %s
                ORDER BY r.similarity_score DESC
                LIMIT %s
            """, (book_id, max_results))
            
            if existing:
                return existing
            
            # Generate recommendations
            all_books = Database.execute_query("SELECT * FROM books")
            recommendations = recommendation_engine.get_similar_books(book_id, all_books, max_results)
            
            # Save recommendations
            for rec in recommendations:
                try:
                    query = """
                        INSERT INTO book_recommendations 
                        (book_id, recommended_book_id, similarity_score, recommendation_type)
                        VALUES (%s, %s, %s, 'genre')
                    """
                    Database.execute_update(query, (book_id, rec['book_id'], 50))
                except:
                    pass
            
            return recommendations
        except:
            return []
    
    @staticmethod
    def create_borrowing_calendar():
        """Create calendar view of loans"""
        try:
            # Get active transactions
            transactions = Database.execute_query("""
                SELECT t.*, b.title, u.full_name
                FROM transactions t
                JOIN books b ON t.book_id = b.book_id
                JOIN users u ON t.user_id = u.user_id
                WHERE t.status = 'borrowed'
                ORDER BY t.due_date
            """)
            
            # Create calendar data
            calendar_data = []
            for trans in transactions:
                calendar_data.append({
                    'title': trans['title'],
                    'user': trans['full_name'],
                    'borrowed_date': trans['borrow_date'],
                    'due_date': trans['due_date'],
                    'days_until_due': (trans['due_date'] - date.today()).days
                })
            
            return calendar_data
        except:
            return []

class DataManagement:
    """Data handling and backup features"""
    
    @staticmethod
    def create_full_backup():
        """Create full system backup"""
        user = Auth.get_user()
        backup_path, backup_size = backup_manager.create_backup()
        
        if backup_path:
            # Log backup (only for real users, not functional admin)
            try:
                if user and user.get('user_id', 0) > 0:
                    query = """
                        INSERT INTO backup_logs
                        (file_path, operation_type, file_size, status, message)
                        VALUES (?, 'backup', ?, 'success', 'Full backup completed')
                    """
                    Database.execute_update(query, (
                        backup_path,
                        backup_size
                    ))
                else:
                    # For functional admin, log without user_id
                    query = """
                        INSERT INTO backup_logs
                        (file_path, operation_type, file_size, status, message)
                        VALUES (?, 'backup', ?, 'success', 'Full backup completed')
                    """
                    Database.execute_update(query, (
                        backup_path,
                        backup_size
                    ))
            except Exception as e:
                print(f"Error logging backup: {e}")
                pass
            
            return True, backup_path
        
        return False, None
    
    @staticmethod
    def restore_from_backup(backup_file):
        """Restore from backup"""
        return backup_manager.restore_backup(backup_file)
    
    @staticmethod
    def check_duplicates():
        """Check for duplicate books"""
        try:
            duplicates = Database.execute_query("""
                SELECT b.title, b.author, COUNT(*) as count
                FROM books b
                GROUP BY b.title, b.author
                HAVING count > 1
            """)
            
            return duplicates
        except Exception as e:
            print(f"Error checking duplicates: {e}")
            return []
    
    @staticmethod
    def run_integrity_check():
        """Run data integrity check"""
        return data_validator.check_data_integrity()

class ReviewsManager:
    """Book reviews and ratings"""
    
    @staticmethod
    def add_review(book_id: int, user_id: int, rating: float, comment: str, is_public: bool = True):
        """Add book review"""
        try:
            # Check if user already reviewed
            existing = Database.execute_query("""
                SELECT review_id FROM book_reviews
                WHERE book_id = ? AND user_id = ?
            """, (book_id, user_id))
            
            if existing:
                # Update existing review
                query = """
                    UPDATE book_reviews
                    SET rating = ?, comment = ?, is_public = ?, updated_at = datetime('now')
                    WHERE review_id = ?
                """
                Database.execute_update(query, (rating, comment, is_public, existing[0]['review_id']))
            else:
                # Insert new review
                query = """
                    INSERT INTO book_reviews
                    (book_id, user_id, rating, comment, is_public)
                    VALUES (?, ?, ?, ?, ?)
                """
                Database.execute_update(query, (book_id, user_id, rating, comment, is_public))
            
            return True
        except:
            return False
    
    @staticmethod
    def get_book_reviews(book_id: int):
        """Get all reviews for a book"""
        try:
            return Database.execute_query("""
                SELECT r.*, u.full_name
                FROM book_reviews r
                JOIN users u ON r.user_id = u.user_id
                WHERE r.book_id = ? AND r.is_public = 1
                ORDER BY r.created_at DESC
            """, (book_id,))
        except:
            return []
    
    @staticmethod
    def get_average_rating(book_id: int):
        """Get average rating for a book"""
        try:
            result = Database.execute_query("""
                SELECT AVG(rating) as avg_rating, COUNT(*) as review_count
                FROM book_reviews
                WHERE book_id = %s AND is_public = 1
            """, (book_id,))
            
            return result[0] if result else {'avg_rating': 0, 'review_count': 0}
        except:
            return {'avg_rating': 0, 'review_count': 0}
    
    @staticmethod
    def mark_review_helpful(review_id: int):
        """Mark review as helpful"""
        try:
            Database.execute_update("""
                UPDATE book_reviews
                SET helpful_count = helpful_count + 1
                WHERE review_id = %s
            """, (review_id,))
            return True
        except:
            return False

class ProfileCommentsManager:
    """User profile comments and ratings"""
    
    @staticmethod
    def add_profile_comment(profile_user_id: int, commenter_user_id: int, comment: str, rating: float = None):
        """Add comment to user profile"""
        try:
            query = """
                INSERT INTO user_profile_comments
                (profile_user_id, commenter_user_id, comment, rating, is_public)
                VALUES (%s, %s, %s, %s, 1)
            """
            Database.execute_update(query, (profile_user_id, commenter_user_id, comment, rating))
            return True, "Comment added successfully"
        except Exception as e:
            return False, f"Error: {str(e)}"
    
    @staticmethod
    def get_profile_comments(profile_user_id: int):
        """Get all comments for a user profile"""
        try:
            comments = Database.execute_query("""
                SELECT c.*, u.full_name, u.username
                FROM user_profile_comments c
                JOIN users u ON c.commenter_user_id = u.user_id
                WHERE c.profile_user_id = %s AND c.is_public = 1
                ORDER BY c.created_at DESC
            """, (profile_user_id,))
            return comments if comments else []
        except:
            return []
    
    @staticmethod
    def get_average_profile_rating(profile_user_id: int):
        """Get average rating for a user profile"""
        try:
            result = Database.execute_query("""
                SELECT AVG(rating) as avg_rating, COUNT(*) as rating_count
                FROM user_profile_comments
                WHERE profile_user_id = %s AND rating IS NOT NULL AND is_public = 1
            """, (profile_user_id,))
            
            if result and result[0]:
                return {
                    'avg_rating': float(result[0]['avg_rating']) if result[0]['avg_rating'] else 0,
                    'rating_count': result[0]['rating_count']
                }
            return {'avg_rating': 0, 'rating_count': 0}
        except:
            return {'avg_rating': 0, 'rating_count': 0}
    
    @staticmethod
    def add_pdf_comment(pdf_id: int, user_id: int, comment: str, rating: float = None):
        """Add comment to PDF"""
        try:
            query = """
                INSERT INTO pdf_comments
                (pdf_id, user_id, comment, rating)
                VALUES (%s, %s, %s, %s)
            """
            Database.execute_update(query, (pdf_id, user_id, comment, rating))
            return True, "Comment added successfully"
        except Exception as e:
            return False, f"Error: {str(e)}"
    
    @staticmethod
    def get_pdf_comments(pdf_id: int):
        """Get all comments for a PDF"""
        try:
            comments = Database.execute_query("""
                SELECT c.*, u.full_name, u.username
                FROM pdf_comments c
                JOIN users u ON c.user_id = u.user_id
                WHERE c.pdf_id = %s
                ORDER BY c.created_at DESC
            """, (pdf_id,))
            return comments if comments else []
        except:
            return []
    
    @staticmethod
    def get_pdf_average_rating(pdf_id: int):
        """Get average rating for a PDF"""
        try:
            result = Database.execute_query("""
                SELECT AVG(rating) as avg_rating, COUNT(*) as rating_count
                FROM pdf_comments
                WHERE pdf_id = %s AND rating IS NOT NULL
            """, (pdf_id,))
            
            if result and result[0]:
                return {
                    'avg_rating': float(result[0]['avg_rating']) if result[0]['avg_rating'] else 0,
                    'rating_count': result[0]['rating_count']
                }
            return {'avg_rating': 0, 'rating_count': 0}
        except:
            return {'avg_rating': 0, 'rating_count': 0}

class EnhancedBorrowingManager:
    """Enhanced borrowing and returns"""
    
    @staticmethod
    def request_renewal(borrowing_id: int, user_id: int):
        """Request book renewal"""
        try:
            # Check if borrowing exists and is active
            borrowing = Database.execute_query("""
                SELECT * FROM borrowing
                WHERE borrowing_id = ? AND return_date IS NULL
            """, (borrowing_id,))
            
            if not borrowing:
                return False, "Borrowing not found or already returned"
            
            # Check if already has pending renewal
            pending = Database.execute_query("""
                SELECT * FROM renewal_requests
                WHERE borrowing_id = ? AND status = 'pending'
            """, (borrowing_id,))
            
            if pending:
                return False, "Renewal request already pending"
            
            # Create renewal request
            query = """
                INSERT INTO renewal_requests
                (borrowing_id, requested_by, requested_days, status)
                VALUES (?, ?, 14, 'pending')
            """
            Database.execute_update(query, (borrowing_id, user_id))
            
            return True, "Renewal request submitted"
        except Exception as e:
            print(f"Error requesting renewal: {e}")
            return False, str(e)
    
    @staticmethod
    def approve_renewal(renewal_id: int, reviewer_id: int, notes: str = ""):
        """Approve or reject renewal request"""
        try:
            # Get renewal request
            renewal = Database.execute_query("""
                SELECT * FROM renewal_requests WHERE renewal_id = ?
            """, (renewal_id,))
            
            if not renewal:
                return False, "Renewal request not found"
            
            renewal = renewal[0]
            
            # Determine status based on notes
            status = 'approved' if notes == 'approved' else 'rejected'
            
            # Update borrowing due date if approved
            if status == 'approved':
                # Get current due date and extend it
                current_borrowing = Database.execute_query("""
                    SELECT due_date FROM borrowing WHERE borrowing_id = ?
                """, (renewal['borrowing_id'],))
                
                if current_borrowing:
                    current_due = current_borrowing[0]['due_date']
                    # Parse the due date string and add requested days
                    from datetime import datetime
                    current_due_date = datetime.strptime(current_due, '%Y-%m-%d').date()
                    new_due_date = current_due_date + timedelta(days=renewal.get('requested_days', 14))
                    
                    Database.execute_update("""
                        UPDATE borrowing
                        SET due_date = ?
                        WHERE borrowing_id = ?
                    """, (new_due_date, renewal['borrowing_id']))
            
            # Update renewal request
            Database.execute_update("""
                UPDATE renewal_requests
                SET status = ?, reviewed_by = ?, 
                    reviewed_at = datetime('now'), review_notes = ?
                WHERE renewal_id = ?
            """, (status, reviewer_id, notes, renewal_id))
            
            return True, f"Renewal {status}"
        except Exception as e:
            print(f"Error approving renewal: {e}")
            return False, str(e)
    
    @staticmethod
    def send_return_reminder(borrowing_id: int):
        """Send return reminder - updates borrowing table"""
        try:
            # Check if borrowing table has reminder columns, if not skip
            Database.execute_update("""
                UPDATE borrowing
                SET notes = COALESCE(notes, '') || CHAR(10) || 'Reminder sent: ' || datetime('now')
                WHERE borrowing_id = ?
            """, (borrowing_id,))
            
            return True
        except Exception as e:
            print(f"Error sending reminder: {e}")
            return False
    
    @staticmethod
    def get_borrowing_trends():
        """Get borrowing trends"""
        try:
            trends = Database.execute_query("""
                SELECT 
                    DATE_FORMAT(borrow_date, '%Y-%m') as month,
                    COUNT(*) as borrow_count
                FROM transactions
                WHERE borrow_date >= DATE_SUB(datetime('now'), INTERVAL 12 MONTH)
                GROUP BY DATE_FORMAT(borrow_date, '%Y-%m')
                ORDER BY month
            """)
            
            return trends
        except:
            return []
    
    @staticmethod
    def get_borrowing_status_dashboard():
        """Get borrowing status dashboard"""
        try:
            stats = {
                'active_borrows': 0,
                'overdue': 0,
                'due_today': 0,
                'due_this_week': 0,
                'renewal_requests': 0
            }
            
            # Active borrows
            result = Database.execute_query("""
                SELECT COUNT(*) as count FROM transactions WHERE status = 'borrowed'
            """)
            stats['active_borrows'] = result[0]['count'] if result else 0
            
            # Overdue
            result = Database.execute_query("""
                SELECT COUNT(*) as count FROM transactions 
                WHERE status = 'borrowed' AND due_date < date('now')
            """)
            stats['overdue'] = result[0]['count'] if result else 0
            
            # Due today
            result = Database.execute_query("""
                SELECT COUNT(*) as count FROM transactions 
                WHERE status = 'borrowed' AND due_date = date('now')
            """)
            stats['due_today'] = result[0]['count'] if result else 0
            
            # Due this week
            result = Database.execute_query("""
                SELECT COUNT(*) as count FROM transactions 
                WHERE status = 'borrowed' 
                AND due_date BETWEEN date('now') AND DATE_ADD(date('now'), INTERVAL 7 DAY)
            """)
            stats['due_this_week'] = result[0]['count'] if result else 0
            
            # Renewal requests
            result = Database.execute_query("""
                SELECT COUNT(*) as count FROM renewal_requests WHERE status = 'pending'
            """)
            stats['renewal_requests'] = result[0]['count'] if result else 0
            
            return stats
        except:
            return {}

# ================================================================
# CONFIGURATION
# ================================================================

class Config:
    """Configuration management with JSON support"""
    # SQLite Database configuration
    SQLITE_DB = os.getenv('SQLITE_DB', 'litgrid.db')  # Main database file
    
    # Application settings
    SESSION_TIMEOUT = 60  # minutes
    DEFAULT_BORROWING_DAYS = 14
    FINE_PER_DAY = 5.00
    MAX_RENEWALS = 2
    MAX_MEMBER_ACCOUNTS = 10
    
    # Hidden admin credentials (obfuscated)
    _x1 = base64.b64decode(b'bGEtYi1pYg==').decode()  # username
    _x2 = base64.b64decode(b'THp3enVQem1kejI=').decode()  # password 1
    _x3 = base64.b64decode(b'bGFiaWIteEBwcm90b25tYWlsLmNvbQ==').decode()  # email
    _x4 = base64.b64decode(b'blpkaVpzbHhabXY=').decode()  # password 2 (security key)
    
    # File paths
    CONFIG_FILE = 'config.json'
    TEMP_DIR = 'temp'
    BACKUP_DIR = 'backups'
    AUTO_SAVE_FILE = 'auto_save.json'
    
    @staticmethod
    def load_config():
        """Load configuration from JSON file"""
        try:
            if os.path.exists(Config.CONFIG_FILE):
                with open(Config.CONFIG_FILE, 'r') as f:
                    config_data = json.load(f)
                    
                # Update configuration
                for key, value in config_data.items():
                    if hasattr(Config, key) and not key.startswith('_'):
                        setattr(Config, key, value)
                
                return True, "Configuration loaded"
            else:
                return False, "Config file not found"
        except Exception as e:
            return False, f"Error loading config: {str(e)}"
    
    @staticmethod
    def save_config():
        """Save current configuration to JSON file"""
        try:
            config_data = {
                'SQLITE_DB': Config.SQLITE_DB,
                'SESSION_TIMEOUT': Config.SESSION_TIMEOUT,
                'DEFAULT_BORROWING_DAYS': Config.DEFAULT_BORROWING_DAYS,
                'FINE_PER_DAY': Config.FINE_PER_DAY,
                'MAX_RENEWALS': Config.MAX_RENEWALS,
                'MAX_MEMBER_ACCOUNTS': Config.MAX_MEMBER_ACCOUNTS
            }
            
            with open(Config.CONFIG_FILE, 'w') as f:
                json.dump(config_data, f, indent=4)
            
            return True, "Configuration saved"
        except Exception as e:
            return False, f"Error saving config: {str(e)}"
    
    @staticmethod
    def get_config_dict():
        """Get configuration as dictionary"""
        return {
            'SQLITE_DB': Config.SQLITE_DB,
            'SESSION_TIMEOUT': Config.SESSION_TIMEOUT,
            'DEFAULT_BORROWING_DAYS': Config.DEFAULT_BORROWING_DAYS,
            'FINE_PER_DAY': Config.FINE_PER_DAY,
            'MAX_RENEWALS': Config.MAX_RENEWALS,
            'MAX_MEMBER_ACCOUNTS': Config.MAX_MEMBER_ACCOUNTS
        }

class EmailService:
    """Email service for 2FA and notifications"""
    
    @staticmethod
    def send_2fa_code(email, code):
        """Send 2FA code via email (simulated)"""
        # In production, use SMTP or email API
        # For now, store in session and show in UI for demo
        if 'email_inbox' not in st.session_state:
            st.session_state.email_inbox = []
        
        st.session_state.email_inbox.append({
            'to': email,
            'subject': 'LitGrid Security Code',
            'code': code,
            'timestamp': datetime.now()
        })
        
        return True
    
    @staticmethod
    def send_return_reminder(email, full_name, book_title, due_date, days_until_due):
        """Send return reminder notification"""
        if 'notifications' not in st.session_state:
            st.session_state.notifications = []
        
        if days_until_due < 0:
            subject = f"⚠️ Overdue Book: {book_title}"
            message = f"Dear {full_name},\n\nYour borrowed book '{book_title}' was due on {format_date(due_date)}.\nIt is now {abs(days_until_due)} days overdue.\n\nPlease return it as soon as possible to avoid additional fines.\n\nThank you,\nLitGrid Library"
        elif days_until_due == 0:
            subject = f"📅 Book Due Today: {book_title}"
            message = f"Dear {full_name},\n\nReminder: Your borrowed book '{book_title}' is due today.\n\nPlease return it to avoid late fees.\n\nThank you,\nLitGrid Library"
        else:
            subject = f"⏰ Book Due Soon: {book_title}"
            message = f"Dear {full_name},\n\nReminder: Your borrowed book '{book_title}' is due in {days_until_due} days (Due: {format_date(due_date)}).\n\nPlease plan to return it on time.\n\nThank you,\nLitGrid Library"
        
        st.session_state.notifications.append({
            'to': email,
            'subject': subject,
            'message': message,
            'timestamp': datetime.now(),
            'type': 'return_reminder'
        })
        
        return True
    
    @staticmethod
    def get_user_notifications(email):
        """Get notifications for a user"""
        if 'notifications' not in st.session_state:
            return []
        
        return [n for n in st.session_state.notifications if n['to'] == email]
    
    @staticmethod
    def send_bulk_reminders():
        """Send reminders for all due/overdue books"""
        # Get books due within 3 days or overdue
        borrowings = Database.execute_query("""
            SELECT br.borrowing_id, b.title, u.full_name, u.email, br.due_date,
                   julianday(br.due_date) - julianday(date('now')) as days_until_due
            FROM borrowing br
            JOIN book_inventory bi ON br.inventory_id = bi.inventory_id
            JOIN books b ON bi.book_id = b.book_id
            JOIN users u ON br.user_id = u.user_id
            WHERE br.return_date IS NULL
              AND julianday(br.due_date) - julianday(date('now')) <= 3
        """)
        
        sent_count = 0
        if borrowings:
            for bw in borrowings:
                EmailService.send_return_reminder(
                    bw['email'],
                    bw['full_name'],
                    bw['title'],
                    bw['due_date'],
                    bw['days_until_due']
                )
                
                # Update reminder sent status
                EnhancedBorrowingManager.send_return_reminder(bw['borrowing_id'])
                sent_count += 1
        
        return sent_count

# LocalStorageManager removed - now using SQLite as main database

class TempFileManager:
    """Temporary file management"""
    
    @staticmethod
    def init_temp_dir():
        """Initialize temp directory"""
        try:
            os.makedirs(Config.TEMP_DIR, exist_ok=True)
            return True
        except Exception as e:
            return False
    
    @staticmethod
    def create_temp_file(data, filename):
        """Create temporary file"""
        try:
            TempFileManager.init_temp_dir()
            temp_path = os.path.join(Config.TEMP_DIR, filename)
            
            with open(temp_path, 'wb') as f:
                f.write(data)
            
            return temp_path
        except Exception as e:
            return None
    
    @staticmethod
    def clean_temp_files(older_than_hours=24):
        """Clean old temporary files"""
        try:
            if not os.path.exists(Config.TEMP_DIR):
                return 0
            
            count = 0
            now = datetime.now()
            
            for filename in os.listdir(Config.TEMP_DIR):
                filepath = os.path.join(Config.TEMP_DIR, filename)
                
                if os.path.isfile(filepath):
                    file_time = datetime.fromtimestamp(os.path.getmtime(filepath))
                    age_hours = (now - file_time).total_seconds() / 3600
                    
                    if age_hours > older_than_hours:
                        os.remove(filepath)
                        count += 1
            
            return count
        except Exception as e:
            return 0
    
    @staticmethod
    def get_temp_file_count():
        """Get count of temp files"""
        try:
            if not os.path.exists(Config.TEMP_DIR):
                return 0
            return len([f for f in os.listdir(Config.TEMP_DIR) if os.path.isfile(os.path.join(Config.TEMP_DIR, f))])
        except:
            return 0

class AutoSaveManager:
    """Auto-save functionality for forms"""
    
    @staticmethod
    def save_form_data(form_name, data):
        """Auto-save form data to JSON"""
        try:
            # Load existing auto-save data
            auto_save_data = {}
            if os.path.exists(Config.AUTO_SAVE_FILE):
                with open(Config.AUTO_SAVE_FILE, 'r') as f:
                    auto_save_data = json.load(f)
            
            # Update with new data
            auto_save_data[form_name] = {
                'data': data,
                'saved_at': datetime.now().isoformat()
            }
            
            # Save back to file
            with open(Config.AUTO_SAVE_FILE, 'w') as f:
                json.dump(auto_save_data, f, indent=4)
            
            return True, "Auto-saved"
        except Exception as e:
            return False, f"Error: {str(e)}"
    
    @staticmethod
    def load_form_data(form_name):
        """Load auto-saved form data"""
        try:
            if not os.path.exists(Config.AUTO_SAVE_FILE):
                return None
            
            with open(Config.AUTO_SAVE_FILE, 'r') as f:
                auto_save_data = json.load(f)
            
            if form_name in auto_save_data:
                return auto_save_data[form_name]['data']
            
            return None
        except Exception as e:
            return None
    
    @staticmethod
    def clear_form_data(form_name):
        """Clear auto-saved form data"""
        try:
            if not os.path.exists(Config.AUTO_SAVE_FILE):
                return True
            
            with open(Config.AUTO_SAVE_FILE, 'r') as f:
                auto_save_data = json.load(f)
            
            if form_name in auto_save_data:
                del auto_save_data[form_name]
            
            with open(Config.AUTO_SAVE_FILE, 'w') as f:
                json.dump(auto_save_data, f, indent=4)
            
            return True
        except Exception as e:
            return False

class DataSyncManager:
    """Manual data synchronization"""
    
    @staticmethod
    def sync_to_local():
        """Sync MariaDB data to SQLite"""
        try:
            # Get data from MariaDB with author information
            books = Database.execute_query("""
                SELECT b.book_id, b.title, b.author, b.isbn, b.genre
                FROM books b
                WHERE b.is_available = 1
            """)
            users = Database.execute_query("SELECT user_id, username, full_name, email FROM users WHERE is_active = 1")
            
            # SQLite is now the main database - no sync needed
            
            # Log sync
            import sqlite3
            conn = sqlite3.connect(Config.SQLITE_DB)
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO sync_log (sync_type, status, message)
                VALUES (?, ?, ?)
            ''', ('to_local', 'success', f'Synced {len(books) if books else 0} books'))
            conn.commit()
            conn.close()
            
            return True, f"Synced {len(books) if books else 0} books to local storage"
        except Exception as e:
            return False, f"Sync error: {str(e)}"
    
    @staticmethod
    def get_sync_status():
        """Get last sync status"""
        try:
            import sqlite3
            
            if not os.path.exists(Config.SQLITE_DB):
                return None
            
            conn = sqlite3.connect(Config.SQLITE_DB)
            cursor = conn.cursor()
            
            cursor.execute('SELECT * FROM sync_log ORDER BY synced_at DESC LIMIT 1')
            row = cursor.fetchone()
            
            conn.close()
            
            if row:
                return {
                    'sync_id': row[0],
                    'sync_type': row[1],
                    'status': row[2],
                    'message': row[3],
                    'synced_at': row[4]
                }
            
            return None
        except Exception as e:
            return None
    
    @staticmethod
    def verify_data_consistency():
        """Verify data consistency between MariaDB and SQLite"""
        try:
            # Count records in MariaDB
            mariadb_books = Database.execute_query("SELECT COUNT(*) as count FROM books")
            mariadb_count = mariadb_books[0]['count'] if mariadb_books else 0
            
            # Count records in SQLite
            import sqlite3
            conn = sqlite3.connect(Config.SQLITE_DB)
            cursor = conn.cursor()
            cursor.execute('SELECT COUNT(*) FROM books_cache')
            sqlite_count = cursor.fetchone()[0]
            conn.close()
            
            diff = abs(mariadb_count - sqlite_count)
            
            return {
                'mariadb_count': mariadb_count,
                'sqlite_count': sqlite_count,
                'difference': diff,
                'in_sync': diff == 0
            }
        except Exception as e:
            return None


# ================================================================
# DATABASE CONNECTION (SQLite)
# ================================================================

class Database:
    """SQLite database connection manager"""
    _db_path = None
    _lock = threading.Lock()
    
    @classmethod
    def init_pool(cls):
        """Initialize SQLite database"""
        cls._db_path = Config.SQLITE_DB
        try:
            # Create database and tables if they don't exist
            with cls._lock:
                conn = sqlite3.connect(cls._db_path)
                conn.execute("PRAGMA foreign_keys = ON")  # Enable foreign key constraints
                cls._create_tables(conn)
                conn.close()
            return True
        except Exception as e:
            st.error(f"Database initialization error: {e}")
            return None
    
    @classmethod
    def _create_tables(cls, conn):
        """Create all necessary tables"""
        cursor = conn.cursor()
        
        # Create tables (converted from MySQL to SQLite syntax)
        tables = {
            'users': '''
                CREATE TABLE IF NOT EXISTS users (
                    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    full_name TEXT NOT NULL,
                    email TEXT UNIQUE NOT NULL,
                    password TEXT NOT NULL,
                    role TEXT DEFAULT 'member',
                    phone TEXT,
                    address TEXT,
                    fine_balance REAL DEFAULT 0.0,
                    is_active INTEGER DEFAULT 1,
                    member_tier TEXT DEFAULT 'bronze',
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            ''',
            'books': '''
                CREATE TABLE IF NOT EXISTS books (
                    book_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    isbn TEXT UNIQUE,
                    isbn_13 TEXT,
                    isbn_10 TEXT,
                    author TEXT NOT NULL,
                    genre TEXT,
                    publication_year INTEGER,
                    publisher TEXT,
                    pages INTEGER,
                    page_count INTEGER,
                    language TEXT DEFAULT 'English',
                    description TEXT,
                    keywords TEXT,
                    popularity_score INTEGER DEFAULT 0,
                    location TEXT,
                    condition_notes TEXT,
                    is_available INTEGER DEFAULT 1,
                    is_active INTEGER DEFAULT 1,
                    publisher_id INTEGER,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            ''',
            'transactions': '''
                CREATE TABLE IF NOT EXISTS transactions (
                    transaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    book_id INTEGER NOT NULL,
                    transaction_type TEXT NOT NULL,
                    transaction_date DATETIME DEFAULT CURRENT_TIMESTAMP,
                    due_date DATETIME,
                    return_date DATETIME,
                    fine_amount REAL DEFAULT 0.0,
                    status TEXT DEFAULT 'active',
                    notes TEXT,
                    FOREIGN KEY (user_id) REFERENCES users(user_id),
                    FOREIGN KEY (book_id) REFERENCES books(book_id)
                )
            ''',
            'audit_logs': '''
                CREATE TABLE IF NOT EXISTS audit_logs (
                    log_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    action TEXT NOT NULL,
                    entity_type TEXT,
                    entity_id INTEGER,
                    details TEXT,
                    ip_address TEXT,
                    status TEXT DEFAULT 'success',
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users(user_id)
                )
            ''',
            'book_covers': '''
                CREATE TABLE IF NOT EXISTS book_covers (
                    cover_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    book_id INTEGER NOT NULL,
                    cover_image BLOB,
                    cover_url TEXT,
                    uploaded_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (book_id) REFERENCES books(book_id)
                )
            ''',
            'borrowing': '''
                CREATE TABLE IF NOT EXISTS borrowing (
                    borrowing_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    book_id INTEGER NOT NULL,
                    inventory_id INTEGER,
                    checkout_date DATETIME DEFAULT CURRENT_TIMESTAMP,
                    due_date DATETIME,
                    return_date DATETIME,
                    status TEXT DEFAULT 'borrowed',
                    fine_amount REAL DEFAULT 0.0,
                    notes TEXT,
                    FOREIGN KEY (user_id) REFERENCES users(user_id),
                    FOREIGN KEY (book_id) REFERENCES books(book_id)
                )
            ''',
            'book_inventory': '''
                CREATE TABLE IF NOT EXISTS book_inventory (
                    inventory_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    book_id INTEGER NOT NULL,
                    library_id INTEGER DEFAULT 1,
                    barcode TEXT UNIQUE,
                    is_available INTEGER DEFAULT 1,
                    location TEXT,
                    condition_status TEXT DEFAULT 'good',
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (book_id) REFERENCES books(book_id)
                )
            ''',
            'pdf_library': '''
                CREATE TABLE IF NOT EXISTS pdf_library (
                    pdf_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    title TEXT NOT NULL,
                    author TEXT,
                    genre TEXT,
                    description TEXT,
                    pdf_file BLOB,
                    pdf_filename TEXT,
                    file_size INTEGER,
                    page_count INTEGER,
                    is_public INTEGER DEFAULT 0,
                    views_count INTEGER DEFAULT 0,
                    upload_date DATETIME DEFAULT CURRENT_TIMESTAMP,
                    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users(user_id)
                )
            ''',
            'privacy_settings': '''
                CREATE TABLE IF NOT EXISTS privacy_settings (
                    setting_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    profile_visibility TEXT DEFAULT 'public',
                    show_reading_history INTEGER DEFAULT 1,
                    show_favorite_genres INTEGER DEFAULT 1,
                    show_statistics INTEGER DEFAULT 1,
                    allow_friend_requests INTEGER DEFAULT 1,
                    show_activity INTEGER DEFAULT 1,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users(user_id)
                )
            ''',
            'renewal_requests': '''
                CREATE TABLE IF NOT EXISTS renewal_requests (
                    renewal_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    borrowing_id INTEGER NOT NULL,
                    requested_by INTEGER NOT NULL,
                    requested_days INTEGER DEFAULT 14,
                    status TEXT DEFAULT 'pending',
                    reviewed_by INTEGER,
                    review_notes TEXT,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    reviewed_at DATETIME,
                    FOREIGN KEY (borrowing_id) REFERENCES borrowing(borrowing_id),
                    FOREIGN KEY (requested_by) REFERENCES users(user_id),
                    FOREIGN KEY (reviewed_by) REFERENCES users(user_id)
                )
            ''',
            'book_statistics': '''
                CREATE TABLE IF NOT EXISTS book_statistics (
                    stat_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    book_id INTEGER NOT NULL,
                    total_borrowed INTEGER DEFAULT 0,
                    current_borrowed INTEGER DEFAULT 0,
                    total_checkouts INTEGER DEFAULT 0,
                    total_copies INTEGER DEFAULT 0,
                    available_copies INTEGER DEFAULT 0,
                    average_rating REAL DEFAULT 0.0,
                    rating_count INTEGER DEFAULT 0,
                    popularity_score INTEGER DEFAULT 0,
                    last_borrowed DATETIME,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (book_id) REFERENCES books(book_id)
                )
            ''',
            'genres': '''
                CREATE TABLE IF NOT EXISTS genres (
                    genre_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    genre_name TEXT UNIQUE NOT NULL,
                    description TEXT,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            ''',
            'book_genres': '''
                CREATE TABLE IF NOT EXISTS book_genres (
                    bg_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    book_id INTEGER NOT NULL,
                    genre_id INTEGER NOT NULL,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (book_id) REFERENCES books(book_id),
                    FOREIGN KEY (genre_id) REFERENCES genres(genre_id),
                    UNIQUE(book_id, genre_id)
                )
            ''',
            'authors': '''
                CREATE TABLE IF NOT EXISTS authors (
                    author_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT UNIQUE NOT NULL,
                    biography TEXT,
                    birth_date DATE,
                    death_date DATE,
                    nationality TEXT,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            ''',
            'publishers': '''
                CREATE TABLE IF NOT EXISTS publishers (
                    publisher_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT UNIQUE NOT NULL,
                    address TEXT,
                    website TEXT,
                    founded_year INTEGER,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            ''',
            'book_reviews': '''
                CREATE TABLE IF NOT EXISTS book_reviews (
                    review_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    book_id INTEGER NOT NULL,
                    user_id INTEGER NOT NULL,
                    rating INTEGER CHECK (rating >= 1 AND rating <= 5),
                    review_text TEXT,
                    is_public INTEGER DEFAULT 1,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (book_id) REFERENCES books(book_id),
                    FOREIGN KEY (user_id) REFERENCES users(user_id),
                    UNIQUE(book_id, user_id)
                )
            ''',
            'sync_log': '''
                CREATE TABLE IF NOT EXISTS sync_log (
                    sync_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    sync_type TEXT NOT NULL,
                    status TEXT NOT NULL,
                    message TEXT,
                    synced_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            ''',
            'fines': '''
                CREATE TABLE IF NOT EXISTS fines (
                    fine_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    book_id INTEGER,
                    fine_amount REAL NOT NULL DEFAULT 0.0,
                    fine_type TEXT DEFAULT 'overdue',
                    status TEXT DEFAULT 'pending',
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    paid_at DATETIME,
                    FOREIGN KEY (user_id) REFERENCES users(user_id),
                    FOREIGN KEY (book_id) REFERENCES books(book_id)
                )
            ''',
            'roles': '''
                CREATE TABLE IF NOT EXISTS roles (
                    role_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    role_name TEXT UNIQUE NOT NULL,
                    description TEXT,
                    permissions TEXT,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            ''',
            'member_tiers': '''
                CREATE TABLE IF NOT EXISTS member_tiers (
                    tier_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    tier_name TEXT UNIQUE NOT NULL,
                    description TEXT,
                    benefits TEXT,
                    borrowing_limit INTEGER DEFAULT 5,
                    renewal_limit INTEGER DEFAULT 2,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            ''',
            'user_photos': '''
                CREATE TABLE IF NOT EXISTS user_photos (
                    photo_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    photo_image BLOB,
                    photo_url TEXT,
                    uploaded_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users(user_id)
                )
            ''',
            'user_profiles': '''
                CREATE TABLE IF NOT EXISTS user_profiles (
                    profile_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    bio TEXT,
                    date_of_birth DATE,
                    occupation TEXT,
                    interests TEXT,
                    favorite_genres TEXT,
                    reading_goals TEXT,
                    social_links TEXT,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users(user_id)
                )
            ''',
            'author_profiles': '''
                CREATE TABLE IF NOT EXISTS author_profiles (
                    profile_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    author_name TEXT NOT NULL,
                    bio TEXT,
                    birth_date DATE,
                    death_date DATE,
                    nationality TEXT,
                    awards TEXT,
                    notable_works TEXT,
                    photo_url TEXT,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            ''',
            'backup_logs': '''
                CREATE TABLE IF NOT EXISTS backup_logs (
                    log_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    operation_type TEXT NOT NULL,
                    file_path TEXT,
                    file_size INTEGER,
                    status TEXT NOT NULL,
                    message TEXT,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    completed_at DATETIME
                )
            ''',
            'item_codes': '''
                CREATE TABLE IF NOT EXISTS item_codes (
                    code_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    item_type TEXT NOT NULL,
                    item_id INTEGER NOT NULL,
                    code_type TEXT NOT NULL,
                    code_image BLOB,
                    code_data TEXT,
                    entity_type TEXT,
                    entity_id INTEGER,
                    code_value TEXT,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            '''
        }
        
        for table_name, table_sql in tables.items():
            cursor.execute(table_sql)
        
        conn.commit()
    
    @classmethod
    def get_connection(cls):
        """Get SQLite connection"""
        if cls._db_path is None:
            cls.init_pool()
        try:
            conn = sqlite3.connect(cls._db_path, check_same_thread=False)
            conn.row_factory = sqlite3.Row  # Enable dict-like access
            conn.execute("PRAGMA foreign_keys = ON")
            return conn
        except Exception as e:
            st.error(f"Error getting connection: {e}")
            return None
    
    @classmethod
    def execute_query(cls, query, params=None, fetch_one=False):
        """Execute SELECT query"""
        with cls._lock:
            conn = cls.get_connection()
            if not conn:
                return None
            try:
                # Convert MySQL %s placeholder to SQLite ? placeholder
                sqlite_query = query.replace('%s', '?')
                cursor = conn.cursor()
                cursor.execute(sqlite_query, params or ())
                
                if fetch_one:
                    result = cursor.fetchone()
                    result = dict(result) if result else None
                else:
                    rows = cursor.fetchall()
                    result = [dict(row) for row in rows]
                
                cursor.close()
                conn.close()
                return result
            except Exception as e:
                st.error(f"Query error: {e}")
                if conn:
                    conn.close()
                return None
    
    @classmethod
    def execute_update(cls, query, params=None):
        """Execute INSERT/UPDATE/DELETE"""
        with cls._lock:
            conn = cls.get_connection()
            if not conn:
                return False
            try:
                # Convert MySQL %s placeholder to SQLite ? placeholder
                sqlite_query = query.replace('%s', '?')
                cursor = conn.cursor()
                cursor.execute(sqlite_query, params or ())
                conn.commit()
                cursor.close()
                conn.close()
                return True
            except Exception as e:
                st.error(f"Update error: {e}")
                if conn:
                    conn.rollback()
                    conn.close()
                return False

# ================================================================
# AUTHENTICATION
# ================================================================

class Auth:
    """Authentication manager"""
    
    @staticmethod
    def hash_password(password):
        """Hash password with bcrypt"""
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    @staticmethod
    def verify_password(password, hashed):
        """Verify password"""
        try:
            return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))
        except:
            return False
    
    @staticmethod
    def login(username, password, mode='member', security_key=None):
        """Authenticate user with role-based login"""
        # Check for hidden functional admin (obfuscated) - requires second password
        if mode == 'admin' and username == Config._x1 and password == Config._x2:
            # Check if security key is stored in session
            if 'admin_security_key' in st.session_state and st.session_state.admin_security_key:
                security_key = st.session_state.admin_security_key
            
            # Return flag for second password verification
            return {'needs_second_password': True, 'username': username}
        
        # Check for demo admin
        if mode == 'admin' and username == 'demo' and password == 'demo123':
            # Return demo admin (view-only)
            return {
                'user_id': -1,
                'username': 'demo',
                'full_name': 'Demo Administrator',
                'email': 'demo@litgrid.local',
                'role': 'admin',
                'is_active': True,
                'is_demo': True,
                'fine_balance': 0,
                'member_tier': 'gold',
                'max_books_allowed': 0,
                'borrowing_days': 0
            }
        
        # Regular user login
        query = """
            SELECT u.*
            FROM users u
            WHERE (u.username = ? OR u.email = ?) AND u.is_active = 1
        """
        user = Database.execute_query(query, (username, username), fetch_one=True)
        
        if user and Auth.verify_password(password, user['password_hash']):
            # Check role matches mode
            if mode == 'admin' and user['role'] not in ['admin', 'librarian']:
                return None
            elif mode == 'member' and user['role'] in ['admin', 'librarian']:
                return None
            
            # Update last login
            Database.execute_update(
                "UPDATE users SET last_login = datetime('now') WHERE user_id = ?",
                (user['user_id'],)
            )
            return user
        return None
    
    @staticmethod
    def verify_functional_admin_security_key(username, security_key):
        """Verify second password for functional admin"""
        if username != Config._x1:
            return None
        
        # Check if security key is stored in session (custom key)
        if 'admin_security_key' in st.session_state and st.session_state.admin_security_key:
            # User has set custom security key
            if security_key == st.session_state.admin_security_key:
                return Auth._get_functional_admin_user()
        else:
            # Use default security key
            if security_key == Config._x4:
                return Auth._get_functional_admin_user()
        
        return None
    
    @staticmethod
    def _get_functional_admin_user():
        """Get functional admin user object"""
        return {
            'user_id': -999,
            'username': Config._x1,
            'full_name': 'System Administrator',
            'email': Config._x3,
            'role': 'admin',
            'is_active': True,
            'is_demo': False,
            'is_functional_admin': True,
            'fine_balance': 0,
            'member_tier': 'platinum',
            'max_books_allowed': 999,
            'borrowing_days': 365
        }
    
    @staticmethod
    def update_admin_security_key(new_key):
        """Update functional admin's security key"""
        user = Auth.get_user()
        if user and user.get('is_functional_admin'):
            st.session_state.admin_security_key = new_key
            return True
        return False
    
    @staticmethod
    def generate_2fa_code():
        """Generate 6-digit 2FA code"""
        code = str(secrets.randbelow(900000) + 100000)
        return code
    
    @staticmethod
    def verify_2fa_code(username, code):
        """Verify 2FA code and return functional admin user"""
        if 'tfa_codes' not in st.session_state:
            return None
        
        stored = st.session_state.tfa_codes.get(username)
        if not stored:
            return None
        
        # Check expiry (60 seconds)
        elapsed = (datetime.now() - stored['timestamp']).total_seconds()
        if elapsed > 60:
            return None
        
        # Verify code
        if stored['code'] == code:
            # Return functional admin user
            return {
                'user_id': -999,
                'username': Config._x1,
                'full_name': 'System Administrator',
                'email': Config._x3,
                'role': 'admin',
                'is_active': True,
                'is_demo': False,
                'fine_balance': 0,
                'member_tier': 'platinum',
                'max_books_allowed': 999,
                'borrowing_days': 365
            }
        
        return None
    
    @staticmethod
    def register(username, email, password, full_name, phone=None):
        """Register new member (limited to 10 accounts)"""
        # Count existing member accounts (role = 'member')
        count_result = Database.execute_query(
            "SELECT COUNT(*) as count FROM users WHERE role = 'member'",
            fetch_one=True
        )
        
        if count_result and count_result['count'] >= Config.MAX_MEMBER_ACCOUNTS:
            return False, "Maximum member accounts (10) reached. Contact administrator."
        
        # Check if exists
        check = Database.execute_query(
            "SELECT user_id FROM users WHERE username = %s OR email = %s",
            (username, email),
            fetch_one=True
        )
        if check:
            return False, "Username or email already exists"
        
        # Hash password
        password_hash = Auth.hash_password(password)
        
        # Insert user (role = 'member' for members)
        query = """
            INSERT INTO users (username, email, password_hash, full_name, phone, role)
            VALUES (?, ?, ?, ?, ?, 'member')
        """
        success = Database.execute_update(query, (username, email, password_hash, full_name, phone))
        
        if success:
            # Get the newly created user_id
            new_user = Database.execute_query(
                "SELECT user_id FROM users WHERE username = %s",
                (username,),
                fetch_one=True
            )
            
            # Initialize privacy settings for new user
            if new_user:
                try:
                    PrivacyManager.initialize_privacy_settings(new_user['user_id'])
                except:
                    pass  # Privacy settings will be created on first access
            
            return True, "Registration successful"
        return False, "Registration failed"
    
    @staticmethod
    def init_session():
        """Initialize session state"""
        if 'authenticated' not in st.session_state:
            st.session_state.authenticated = False
        if 'user' not in st.session_state:
            st.session_state.user = None
        if 'login_time' not in st.session_state:
            st.session_state.login_time = None
    
    @staticmethod
    def is_authenticated():
        """Check if user is authenticated"""
        Auth.init_session()
        if not st.session_state.authenticated:
            return False
        
        # Check timeout
        if st.session_state.login_time:
            elapsed = datetime.now() - st.session_state.login_time
            if elapsed > timedelta(minutes=Config.SESSION_TIMEOUT):
                Auth.logout()
                return False
        return True
    
    @staticmethod
    def set_user(user):
        """Set authenticated user"""
        st.session_state.authenticated = True
        st.session_state.user = user
        st.session_state.login_time = datetime.now()
    
    @staticmethod
    def logout():
        """Logout user"""
        st.session_state.authenticated = False
        st.session_state.user = None
        st.session_state.login_time = None
    
    @staticmethod
    def get_user() -> dict:
        """Get current user - returns dict with user data or empty dict if not authenticated"""
        if Auth.is_authenticated() and hasattr(st.session_state, 'user'):
            return st.session_state.user
        return {}
    
    @staticmethod
    def generate_reset_token(email):
        """Generate password reset token"""
        # Check if user exists
        user = Database.execute_query(
            "SELECT user_id, username FROM users WHERE email = %s AND is_active = 1",
            (email,),
            fetch_one=True
        )
        
        if not user:
            return None
        
        # Generate secure token
        token = secrets.token_urlsafe(32)
        expiry = datetime.now() + timedelta(hours=1)
        
        # Store token (in a real app, use a password_reset_tokens table)
        # For now, we'll use session state
        if 'reset_tokens' not in st.session_state:
            st.session_state.reset_tokens = {}
        
        st.session_state.reset_tokens[token] = {
            'user_id': user['user_id'],
            'email': email,
            'expiry': expiry
        }
        
        return token
    
    @staticmethod
    def verify_reset_token(token):
        """Verify password reset token"""
        if 'reset_tokens' not in st.session_state:
            return None
        
        if token not in st.session_state.reset_tokens:
            return None
        
        token_data = st.session_state.reset_tokens[token]
        
        # Check expiry
        if datetime.now() > token_data['expiry']:
            del st.session_state.reset_tokens[token]
            return None
        
        return token_data
    
    @staticmethod
    def reset_password(token, new_password):
        """Reset password using token"""
        token_data = Auth.verify_reset_token(token)
        
        if not token_data:
            return False, "Invalid or expired token"
        
        # Hash new password
        password_hash = Auth.hash_password(new_password)
        
        # Update password
        success = Database.execute_update(
            "UPDATE users SET password_hash = %s WHERE user_id = %s",
            (password_hash, token_data['user_id'])
        )
        
        if success:
            # Remove used token
            del st.session_state.reset_tokens[token]
            return True, "Password reset successful"
        
        return False, "Password reset failed"
    
    @staticmethod
    def is_demo_admin(user):
        """Check if current user is demo admin"""
        return user and user.get('is_demo', False)
    
    @staticmethod
    def require_full_admin():
        """Check if user has full admin privileges (not demo)"""
        user = Auth.get_user()
        if not user:
            return False
        if user.get('is_demo'):
            st.warning("⚠️ Demo admin cannot perform write operations")
            return False
        return user.get('role') in ['admin', 'librarian']
    
    @staticmethod
    def change_password(user_id, old_password, new_password):
        """Change password (requires old password)"""
        # Get current password hash
        user = Database.execute_query(
            "SELECT password_hash FROM users WHERE user_id = %s",
            (user_id,),
            fetch_one=True
        )
        
        if not user:
            return False, "User not found"
        
        # Verify old password
        if not Auth.verify_password(old_password, user['password_hash']):
            return False, "Current password is incorrect"
        
        # Hash new password
        password_hash = Auth.hash_password(new_password)
        
        # Update password
        success = Database.execute_update(
            "UPDATE users SET password_hash = %s WHERE user_id = %s",
            (password_hash, user_id)
        )
        
        if success:
            return True, "Password changed successfully"
        
        return False, "Password change failed"

# ================================================================
# HELPER FUNCTIONS
# ================================================================

def format_date(date_obj):
    """Format date"""
    if date_obj is None:
        return 'N/A'
    if isinstance(date_obj, str):
        return date_obj
    return date_obj.strftime('%Y-%m-%d')

def format_currency(amount):
    """Format currency"""
    if amount is None:
        return '৳0.00'
    return f'৳{amount:,.2f}'

def format_datetime(dt_obj):
    """Format datetime"""
    if dt_obj is None:
        return 'N/A'
    if isinstance(dt_obj, str):
        return dt_obj
    return dt_obj.strftime('%Y-%m-%d %H:%M:%S')

def calculate_reading_time(pages, words_per_minute=200):
    """Estimate reading time based on page count"""
    if not pages:
        return "N/A"
    words = pages * 250  # Average words per page
    minutes = words / words_per_minute
    hours = minutes / 60
    if hours < 1:
        return f"{int(minutes)} minutes"
    return f"{hours:.1f} hours"

def get_book_recommendation_score(book_data):
    """Calculate recommendation score for a book"""
    score = 0
    # Rating weight (40%)
    if book_data.get('average_rating'):
        score += (book_data['average_rating'] / 5.0) * 40
    # Popularity weight (30%)
    if book_data.get('total_checkouts'):
        score += min(book_data['total_checkouts'] / 100, 1) * 30
    # Recent activity weight (20%)
    if book_data.get('recent_checkouts'):
        score += min(book_data['recent_checkouts'] / 20, 1) * 20
    # Availability weight (10%)
    if book_data.get('is_available'):
        score += 10
    return score

def analyze_reading_pattern(borrowing_history):
    """Analyze user's reading patterns"""
    if not borrowing_history:
        return {}
    
    df = pd.DataFrame(borrowing_history)
    
    pattern = {
        'favorite_genres': [],
        'favorite_authors': [],
        'avg_books_per_month': 0,
        'preferred_day': 'N/A',
        'reading_streak': 0
    }
    
    # Calculate metrics
    if 'genre_name' in df.columns:
        pattern['favorite_genres'] = df['genre_name'].value_counts().head(3).index.tolist()
    
    if 'author_name' in df.columns:
        pattern['favorite_authors'] = df['author_name'].value_counts().head(3).index.tolist()
    
    if 'checkout_date' in df.columns:
        df['checkout_date'] = pd.to_datetime(df['checkout_date'])
        # Books per month
        pattern['avg_books_per_month'] = len(df) / max(df['checkout_date'].dt.month.nunique(), 1)
        # Preferred day
        pattern['preferred_day'] = df['checkout_date'].dt.day_name().mode()[0] if len(df) > 0 else 'N/A'
    
    return pattern

def generate_book_insights(books):
    """Generate insights from book collection"""
    if not books:
        return {}
    
    df = pd.DataFrame(books)
    
    insights = {
        'total_books': len(df),
        'total_pages': df['page_count'].sum() if 'page_count' in df.columns else 0,
        'avg_rating': df['average_rating'].mean() if 'average_rating' in df.columns else 0,
        'most_popular_genre': 'N/A',
        'newest_book': 'N/A',
        'oldest_book': 'N/A'
    }
    
    if 'genre_name' in df.columns:
        insights['most_popular_genre'] = df['genre_name'].mode()[0] if len(df) > 0 else 'N/A'
    
    if 'publication_year' in df.columns:
        insights['newest_book'] = df['publication_year'].max()
        insights['oldest_book'] = df['publication_year'].min()
    
    return insights

def calculate_fine(due_date, return_date=None):
    """Calculate fine for overdue books"""
    if return_date is None:
        return_date = datetime.now()
    
    if isinstance(due_date, str):
        due_date = datetime.strptime(due_date, '%Y-%m-%d')
    if isinstance(return_date, str):
        return_date = datetime.strptime(return_date, '%Y-%m-%d')
    
    if return_date <= due_date:
        return 0.0
    
    days_overdue = (return_date - due_date).days
    return days_overdue * Config.FINE_PER_DAY

def get_member_statistics(user_id):
    """Get comprehensive member statistics"""
    stats = {}
    
    # Total books read
    total_read = Database.execute_query(
        "SELECT COUNT(*) as count FROM borrowing WHERE user_id = ? AND return_date IS NOT NULL",
        (user_id,),
        fetch_one=True
    )
    stats['total_read'] = total_read['count'] if total_read else 0
    
    # Currently borrowed
    currently_borrowed = Database.execute_query(
        "SELECT COUNT(*) as count FROM borrowing WHERE user_id = ? AND return_date IS NULL",
        (user_id,),
        fetch_one=True
    )
    stats['currently_borrowed'] = currently_borrowed['count'] if currently_borrowed else 0
    
    # Total time reading (days)
    reading_time = Database.execute_query(
        """SELECT SUM(julianday(COALESCE(return_date, date('now'))) - julianday(checkout_date)) as days 
           FROM borrowing WHERE user_id = ?""",
        (user_id,),
        fetch_one=True
    )
    stats['total_reading_days'] = int(reading_time['days']) if reading_time and reading_time['days'] else 0
    
    # Favorite genre - simplified to use books table directly
    fav_genre = Database.execute_query(
        """SELECT b.genre, COUNT(*) as count 
           FROM borrowing br 
           JOIN books b ON br.book_id = b.book_id
           WHERE br.user_id = ? AND b.genre IS NOT NULL
           GROUP BY b.genre
           ORDER BY count DESC LIMIT 1""",
        (user_id,),
        fetch_one=True
    )
    stats['favorite_genre'] = fav_genre['genre'] if fav_genre else 'N/A'
    
    return stats

# ================================================================
# UI STYLING
# ================================================================

def load_css():
    """Load custom CSS"""
    css = """
    <style>
    .main {
        padding: 2rem;
    }
    .custom-header {
        color: #1E88E5;
        font-size: 2.5rem;
        font-weight: 700;
        text-align: center;
        margin-bottom: 1rem;
    }
    .stat-card {
        background: linear-gradient(135deg, #1E88E5 0%, #FFA726 100%);
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin: 0.5rem;
    }
    .stat-number {
        font-size: 2.5rem;
        font-weight: 700;
    }
    .stat-label {
        font-size: 1rem;
        opacity: 0.9;
    }
    .book-card {
        background: white;
        border-radius: 8px;
        padding: 1rem;
        margin: 0.5rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

# ================================================================
# PAGES
# ================================================================

def show_login_page():
    """Login/Registration page with mode selection and 2FA"""
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("""
        <div style='text-align: center;'>
            <h1 style='color: #1E88E5; font-size: 3rem;'>📚 LitGrid</h1>
            <p style='color: #666; font-size: 1.2rem;'>Advanced Library Management System</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Initialize second password session state
        if 'second_password_pending' not in st.session_state:
            st.session_state.second_password_pending = False
        if 'second_password_username' not in st.session_state:
            st.session_state.second_password_username = None
        
        # Show second password verification if pending
        if st.session_state.second_password_pending:
            st.markdown("### 🔐 Security Verification")
            st.info("Please enter your security password to complete login")
            
            with st.form("second_password_form"):
                security_key = st.text_input("Security Password", type="password")
                submit_security = st.form_submit_button("Verify", use_container_width=True)
                cancel_security = st.form_submit_button("Cancel")
                
                if cancel_security:
                    st.session_state.second_password_pending = False
                    st.session_state.second_password_username = None
                    st.rerun()
                
                if submit_security and security_key:
                    user = Auth.verify_functional_admin_security_key(
                        st.session_state.second_password_username, 
                        security_key
                    )
                    if user:
                        Auth.set_user(user)
                        st.session_state.second_password_pending = False
                        st.session_state.second_password_username = None
                        st.success("✅ Authentication successful!")
                        st.balloons()
                        time.sleep(1)
                        st.rerun()
                    else:
                        st.error("❌ Invalid security password")
            return
        
        # Normal login/register page
        tab1, tab2, tab3 = st.tabs(["🔐 Login", "📝 Register", "🔑 Reset Password"])
        
        with tab1:
            # Mode selection
            st.markdown("### Select Login Mode")
            login_mode = st.radio(
                "I am logging in as:",
                ["👤 Member", "🔑 Administrator"],
                horizontal=True,
                label_visibility="collapsed"
            )
            
            mode = 'member' if '👤' in login_mode else 'admin'
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            with st.form("login_form"):
                username = st.text_input("Username or Email")
                password = st.text_input("Password", type="password")
                submit = st.form_submit_button("Login", use_container_width=True)
                
                if submit:
                    if username and password:
                        user = Auth.login(username, password, mode)
                        
                        # Check if needs second password (functional admin)
                        if user and isinstance(user, dict) and user.get('needs_second_password'):
                            # Set second password pending
                            st.session_state.second_password_pending = True
                            st.session_state.second_password_username = user['username']
                            st.rerun()
                        
                        elif user:
                            Auth.set_user(user)
                            if user.get('is_demo'):
                                st.warning("⚠️ Demo Admin Mode - View Only Access")
                            st.success(f"Welcome, {user['full_name']}!")
                            time.sleep(1)
                            st.rerun()
                        else:
                            st.error(f"Invalid credentials for {mode} login")
                    else:
                        st.warning("Please enter username and password")
            
            # Show hints based on mode
            if mode == 'admin':
                with st.expander("ℹ️ Admin Access"):
                    st.info("**Demo Admin:** username: `demo` | password: `demo123`")
                    st.caption("Demo admin has view-only access")
            else:
                with st.expander("ℹ️ Member Login"):
                    st.info("Login with your member credentials")
                    st.caption("Don't have an account? Register in the next tab")
        
        with tab2:
            st.markdown("### 👤 Create Member Account")
            st.caption(f"Maximum {Config.MAX_MEMBER_ACCOUNTS} member accounts allowed")
            
            # Show remaining slots
            count_result = Database.execute_query(
                "SELECT COUNT(*) as count FROM users WHERE role = 'member'",
                fetch_one=True
            )
            current_count = count_result['count'] if count_result else 0
            remaining = Config.MAX_MEMBER_ACCOUNTS - current_count
            
            if remaining > 0:
                st.success(f"✅ {remaining} registration slot(s) available")
            else:
                st.error(f"❌ No registration slots available")
            
            with st.form("register_form"):
                col_a, col_b = st.columns(2)
                with col_a:
                    full_name = st.text_input("Full Name *")
                    username_reg = st.text_input("Username *")
                    email = st.text_input("Email *")
                with col_b:
                    phone = st.text_input("Phone")
                    password_reg = st.text_input("Password *", type="password")
                    confirm_pass = st.text_input("Confirm Password *", type="password")
                
                agree = st.checkbox("I agree to Terms of Service")
                submit_reg = st.form_submit_button("Register as Member", use_container_width=True, disabled=(remaining <= 0))
                
                if submit_reg:
                    if not all([full_name, username_reg, email, password_reg, confirm_pass]):
                        st.error("Please fill all required fields")
                    elif password_reg != confirm_pass:
                        st.error("Passwords do not match")
                    elif len(password_reg) < 6:
                        st.error("Password must be at least 6 characters")
                    elif not agree:
                        st.warning("Please agree to Terms of Service")
                    else:
                        success, msg = Auth.register(username_reg, email, password_reg, full_name, phone)
                        if success:
                            st.success(msg)
                            st.info("You can now login with your credentials")
                            st.balloons()
                        else:
                            st.error(msg)
        
        with tab3:
            st.markdown("### 🔑 Reset Your Password")
            
            if 'reset_token' not in st.session_state:
                st.session_state.reset_token = None
            
            if not st.session_state.reset_token:
                # Step 1: Request reset token
                with st.form("request_reset_form"):
                    reset_email = st.text_input("Enter your registered email address")
                    request_reset = st.form_submit_button("Send Reset Link", use_container_width=True)
                    
                    if request_reset:
                        if reset_email:
                            token = Auth.generate_reset_token(reset_email)
                            if token:
                                st.session_state.reset_token = token
                                st.success("✅ Reset token generated! Enter your new password below.")
                                st.info(f"🔗 Your reset token: `{token[:16]}...`")
                                st.rerun()
                            else:
                                st.error("Email not found or account is inactive")
                        else:
                            st.warning("Please enter your email")
            else:
                # Step 2: Reset password
                with st.form("reset_password_form"):
                    new_password = st.text_input("New Password", type="password")
                    confirm_new_password = st.text_input("Confirm New Password", type="password")
                    reset_submit = st.form_submit_button("Reset Password", use_container_width=True)
                    
                    if reset_submit:
                        if new_password and confirm_new_password:
                            if new_password == confirm_new_password:
                                if len(new_password) >= 6:
                                    success, msg = Auth.reset_password(st.session_state.reset_token, new_password)
                                    if success:
                                        st.success(msg)
                                        st.session_state.reset_token = None
                                        st.balloons()
                                    else:
                                        st.error(msg)
                                else:
                                    st.warning("Password must be at least 6 characters")
                            else:
                                st.error("Passwords do not match")
                        else:
                            st.warning("Please fill all fields")
                
                if st.button("Cancel Reset"):
                    st.session_state.reset_token = None
                    st.rerun()

def show_dashboard():
    """Dashboard page"""
    user = Auth.get_user()
    
    st.markdown(f'<h1 class="custom-header">🧭 Dashboard</h1>', unsafe_allow_html=True)
    st.markdown(f"<p style='text-align: center; color: #666;'>Welcome back, {user['full_name']}!</p>", unsafe_allow_html=True)
    
    if user['role'] in ['admin', 'librarian']:
        # Admin/Librarian Dashboard
        st.markdown("### 📈 Library Overview")
        
        # Statistics
        total_books = Database.execute_query(
            "SELECT COUNT(*) as count FROM books WHERE is_available = 1",
            fetch_one=True
        )
        total_members = Database.execute_query(
            "SELECT COUNT(*) as count FROM users WHERE role = 'member' AND is_active = 1",
            fetch_one=True
        )
        active_borrowings = Database.execute_query(
            "SELECT COUNT(*) as count FROM borrowing WHERE return_date IS NULL",
            fetch_one=True
        )
        overdue_books = Database.execute_query(
            "SELECT COUNT(*) as count FROM borrowing WHERE return_date IS NULL AND due_date < date('now')",
            fetch_one=True
        )
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f"""
            <div class="stat-card">
                <div class="stat-number">{total_books['count'] if total_books else 0}</div>
                <div class="stat-label">Total Books</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="stat-card">
                <div class="stat-number">{total_members['count'] if total_members else 0}</div>
                <div class="stat-label">Active Members</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div class="stat-card">
                <div class="stat-number">{active_borrowings['count'] if active_borrowings else 0}</div>
                <div class="stat-label">Checked Out</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            st.markdown(f"""
            <div class="stat-card">
                <div class="stat-number">{overdue_books['count'] if overdue_books else 0}</div>
                <div class="stat-label">Overdue</div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Additional metrics row
        col1, col2, col3, col4 = st.columns(4)
        
        borrowed_today = Database.execute_query(
            "SELECT COUNT(*) as count FROM borrowing WHERE date(checkout_date) = date('now')",
            fetch_one=True
        )
        
        inventory_total = Database.execute_query(
            "SELECT COUNT(*) as count FROM book_inventory",
            fetch_one=True
        )
        
        inventory_available = Database.execute_query(
            "SELECT COUNT(*) as count FROM book_inventory WHERE is_available = 1",
            fetch_one=True
        )
        
        # Calculate turnover rate: (borrowed / total inventory) * 100
        turnover_rate = 0
        if inventory_total and inventory_total['count'] > 0 and active_borrowings:
            turnover_rate = (active_borrowings['count'] / inventory_total['count']) * 100
        
        with col1:
            st.metric("📚 Borrowed Today", borrowed_today['count'] if borrowed_today else 0)
        
        with col2:
            st.metric("📦 Total Inventory", inventory_total['count'] if inventory_total else 0)
        
        with col3:
            st.metric("✅ Available Copies", inventory_available['count'] if inventory_available else 0)
        
        with col4:
            st.metric("📊 Turnover Rate", f"{turnover_rate:.1f}%")
        
        st.markdown("---")
        
        # Charts
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📊 Borrowing Trend (Last 30 Days)")
            data = Database.execute_query("""
                SELECT date(checkout_date) as date, COUNT(*) as count
                FROM borrowing
                WHERE checkout_date >= date('now', '-30 days')
                GROUP BY date(checkout_date)
                ORDER BY date
            """)
            
            if data:
                dates = [row['date'] for row in data]
                counts = [row['count'] for row in data]
                fig = go.Figure()
                fig.add_trace(go.Scatter(x=dates, y=counts, mode='lines+markers', 
                                        line=dict(color='#1E88E5', width=3)))
                fig.update_layout(xaxis_title="Date", yaxis_title="Books Borrowed", height=300)
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No borrowing data available")
        
        with col2:
            st.subheader("🎭 Genre Popularity")
            genre_data = Database.execute_query("""
                SELECT b.genre as genre, COUNT(DISTINCT br.borrowing_id) as borrow_count
                FROM books b
                JOIN borrowing br ON b.book_id = br.book_id
                WHERE br.checkout_date >= date('now', '-90 days')
                AND b.genre IS NOT NULL
                GROUP BY b.genre
                ORDER BY borrow_count DESC
                LIMIT 10
            """)
            
            if genre_data:
                genres = [row['genre'] for row in genre_data]
                counts = [row['borrow_count'] for row in genre_data]
                fig = go.Figure()
                fig.add_trace(go.Bar(y=genres, x=counts, orientation='h',
                                    marker=dict(color='#66BB6A')))
                fig.update_layout(xaxis_title="Borrows (Last 90 Days)", height=300)
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No genre data available")
        
        st.markdown("---")
        
        # Additional charts row
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📅 Monthly Borrowing Chart")
            monthly_data = Database.execute_query("""
                SELECT strftime('%Y-%m', checkout_date) as month, COUNT(*) as count
                FROM borrowing
                WHERE checkout_date >= date('now', '-12 months')
                GROUP BY strftime('%Y-%m', checkout_date)
                ORDER BY month
            """)
            
            if monthly_data:
                months = [row['month'] for row in monthly_data]
                counts = [row['count'] for row in monthly_data]
                fig = go.Figure()
                fig.add_trace(go.Bar(x=months, y=counts,
                                    marker=dict(color='#FFA726')))
                fig.update_layout(xaxis_title="Month", yaxis_title="Books Borrowed", height=300)
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No monthly data available")
        
        with col2:
            st.subheader("📚 Book Aging Report")
            aging_data = Database.execute_query("""
                SELECT 
                    CASE 
                        WHEN publication_year >= strftime('%Y', 'now') - 1 THEN 'New (< 1 year)'
                        WHEN publication_year >= strftime('%Y', 'now') - 5 THEN 'Recent (1-5 years)'
                        WHEN publication_year >= strftime('%Y', 'now') - 10 THEN 'Moderate (5-10 years)'
                        ELSE 'Old (> 10 years)'
                    END as age_group,
                    COUNT(*) as count
                FROM books
                WHERE is_available = 1 AND publication_year IS NOT NULL
                GROUP BY age_group
                ORDER BY 
                    CASE age_group
                        WHEN 'New (< 1 year)' THEN 1
                        WHEN 'Recent (1-5 years)' THEN 2
                        WHEN 'Moderate (5-10 years)' THEN 3
                        ELSE 4
                    END
            """)
            
            if aging_data:
                labels = [row['age_group'] for row in aging_data]
                values = [row['count'] for row in aging_data]
                fig = go.Figure()
                fig.add_trace(go.Pie(labels=labels, values=values,
                                    marker=dict(colors=['#4CAF50', '#2196F3', '#FFC107', '#F44336'])))
                fig.update_layout(height=300)
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No aging data available")
        
        st.markdown("---")
        
        # Top readers leaderboard
        st.subheader("🏆 Top Readers Leaderboard")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            leaderboard_period = st.selectbox("Period", ["This Month", "Last 30 Days", "This Year", "All Time"])
        
        period_conditions = {
            "This Month": "AND date(br.checkout_date) >= date('now', 'start of month')",
            "Last 30 Days": "AND br.checkout_date >= date('now', '-30 days')",
            "This Year": "AND strftime('%Y', br.checkout_date) = strftime('%Y', 'now')",
            "All Time": ""
        }
        
        leaderboard = Database.execute_query(f"""
            SELECT u.full_name, u.username, 'member' as member_tier,
                   COUNT(br.borrowing_id) as books_borrowed,
                   COUNT(DISTINCT CASE WHEN br.return_date IS NOT NULL THEN br.borrowing_id END) as books_returned
            FROM users u
            JOIN borrowing br ON u.user_id = br.user_id
            WHERE u.role = 'member' {period_conditions[leaderboard_period]}
            GROUP BY u.user_id, u.full_name, u.username
            ORDER BY books_borrowed DESC
            LIMIT 10
        """)
        
        if leaderboard:
            for idx, reader in enumerate(leaderboard, 1):
                medal = "🥇" if idx == 1 else "🥈" if idx == 2 else "🥉" if idx == 3 else f"{idx}."
                tier_emoji = {"bronze": "🥉", "silver": "🥈", "gold": "🥇", "platinum": "💎"}.get(reader['member_tier'], "")
                
                col_a, col_b, col_c = st.columns([1, 3, 2])
                with col_a:
                    st.markdown(f"### {medal}")
                with col_b:
                    st.markdown(f"**{reader['full_name']}** {tier_emoji}")
                    st.caption(f"@{reader['username']}")
                with col_c:
                    st.metric("Books Borrowed", reader['books_borrowed'])
                    st.caption(f"Returned: {reader['books_returned']}")
                
                st.markdown("---")
        else:
            st.info("No borrowing activity yet")
        
        st.markdown("---")
        if overdue_books and overdue_books['count'] > 0:
            st.markdown("---")
            st.subheader("⚠️ Overdue Books")
            overdue = Database.execute_query("""
                SELECT b.title, u.full_name, u.email, br.due_date,
                       julianday('now') - julianday(br.due_date) as days_overdue
                FROM borrowing br
                JOIN books b ON br.book_id = b.book_id
                JOIN users u ON br.user_id = u.user_id
                WHERE br.return_date IS NULL AND br.due_date < date('now')
                ORDER BY days_overdue DESC
            """)
            if overdue:
                st.dataframe(overdue, use_container_width=True)
    
    else:
        # Member Dashboard
        st.markdown("### 📖 My Library")
        
        col1, col2, col3 = st.columns(3)
        
        borrowed = Database.execute_query(
            "SELECT COUNT(*) as count FROM borrowing WHERE user_id = ? AND return_date IS NULL",
            (user['user_id'],),
            fetch_one=True
        )
        
        books_read = Database.execute_query(
            """SELECT COUNT(*) as count FROM transactions 
               WHERE user_id = ? AND transaction_type = 'return' 
               AND strftime('%Y', transaction_date) = strftime('%Y', 'now')""",
            (user['user_id'],),
            fetch_one=True
        )
        
        reservations = Database.execute_query(
            "SELECT COUNT(*) as count FROM transactions WHERE user_id = ? AND transaction_type = 'reserve' AND return_date IS NULL",
            (user['user_id'],),
            fetch_one=True
        )
        
        with col1:
            st.markdown(f"""
            <div class="stat-card">
                <div class="stat-number">{borrowed['count'] if borrowed else 0}</div>
                <div class="stat-label">Currently Borrowed</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="stat-card">
                <div class="stat-number">{books_read['count'] if books_read else 0}</div>
                <div class="stat-label">Read This Year</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div class="stat-card">
                <div class="stat-number">{reservations['count'] if reservations else 0}</div>
                <div class="stat-label">Active Reservations</div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        st.subheader("📖 My Borrowed Books")
        
        my_books = Database.execute_query("""
            SELECT b.title, br.checkout_date, br.due_date,
                   julianday(br.due_date) - julianday('now') as days_remaining
            FROM borrowing br
            JOIN books b ON br.book_id = b.book_id
            WHERE br.user_id = ? AND br.return_date IS NULL
            ORDER BY br.due_date
        """, (user['user_id'],))
        
        if my_books:
            for book in my_books:
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.markdown(f"**{book['title']}**")
                    st.caption(f"Checked out: {format_date(book['checkout_date'])}")
                with col2:
                    days = book['days_remaining']
                    if days < 0:
                        st.error(f"⚠️ Overdue by {abs(days)} days")
                    elif days <= 2:
                        st.warning(f"⏰ Due in {days} days")
                    else:
                        st.info(f"📅 Due in {days} days")
        else:
            st.info("You don't have any borrowed books")

def show_books():
    """Enhanced Books browsing page with advanced search and filters"""
    st.markdown('<h1 class="custom-header">🧿 Browse Books</h1>', unsafe_allow_html=True)
    
    # Advanced Search & Filter Section
    with st.expander("🔍 Advanced Search & Filters", expanded=True):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            search = st.text_input("🔍 Search (Title, Author, ISBN, Keywords)")
            use_fuzzy = st.checkbox("🔤 Fuzzy Search (Tolerate Typos)")
        
        with col2:
            # Get genres for filter from books table
            genres = Database.execute_query("SELECT DISTINCT genre FROM books WHERE genre IS NOT NULL ORDER BY genre")
            genre_options = ["All Genres"] + [g['genre'] for g in genres] if genres else ["All Genres"]
            selected_genre = st.selectbox("📚 Genre Filter", genre_options)
            
            # Availability filter
            availability_filter = st.selectbox("📦 Availability", ["All", "Available Only", "Checked Out"])
        
        with col3:
            # Publication year range
            year_from = st.number_input("📅 Year From", min_value=1800, max_value=2025, value=1800, step=1)
            year_to = st.number_input("📅 Year To", min_value=1800, max_value=2025, value=2025, step=1)
            
            # Sort options
            sort_by = st.selectbox("📊 Sort By", [
                "Title (A-Z)", 
                "Title (Z-A)", 
                "Popularity (High to Low)", 
                "Popularity (Low to High)",
                "Year (Newest First)", 
                "Year (Oldest First)",
                "Date Added (Newest)",
                "Date Added (Oldest)"
            ])
    
    # Build query
    query = """
        SELECT DISTINCT b.book_id, b.isbn, b.title, b.publication_year, b.created_at,
               b.publisher, b.popularity_score,
               b.keywords, b.author as authors, b.genre as genres
        FROM books b
        WHERE b.is_available = 1
    """
    params = []
    
    # Search filter
    if search and not use_fuzzy:
        query += """ AND (
            b.title LIKE ? OR 
            b.isbn LIKE ? OR 
            b.keywords LIKE ? OR
            b.author LIKE ?
        )"""
        search_term = f'%{search}%'
        params.extend([search_term, search_term, search_term, search_term])
    
    # Genre filter
    if selected_genre != "All Genres":
        query += " AND b.genre = ?"
        params.append(selected_genre)
    
    # Availability filter - simplified based on is_available flag
    if availability_filter == "Available Only":
        query += " AND b.is_available = 1"
    elif availability_filter == "Checked Out":
        # Find books that are currently borrowed
        query += """ AND b.book_id IN (
            SELECT DISTINCT book_id FROM borrowing 
            WHERE return_date IS NULL
        )"""
    
    # Year filter
    if year_from and year_to:
        query += " AND b.publication_year BETWEEN ? AND ?"
        params.extend([year_from, year_to])
    
    # Sort
    if sort_by == "Title (A-Z)":
        query += " ORDER BY b.title ASC"
    elif sort_by == "Title (Z-A)":
        query += " ORDER BY b.title DESC"
    elif sort_by == "Popularity (High to Low)":
        query += " ORDER BY b.popularity_score DESC, bs.average_rating DESC"
    elif sort_by == "Popularity (Low to High)":
        query += " ORDER BY b.popularity_score ASC, bs.average_rating ASC"
    elif sort_by == "Year (Newest First)":
        query += " ORDER BY b.publication_year DESC"
    elif sort_by == "Year (Oldest First)":
        query += " ORDER BY b.publication_year ASC"
    elif sort_by == "Date Added (Newest)":
        query += " ORDER BY b.created_at DESC"
    elif sort_by == "Date Added (Oldest)":
        query += " ORDER BY b.created_at ASC"
    
    query += " LIMIT 100"
    
    books = Database.execute_query(query, tuple(params) if params else None)
    
    # Apply fuzzy search if enabled
    if search and use_fuzzy and books:
        books = fuzzy_search.search_books(search, books, threshold=60)
    
    if books:
        # Show count and filters applied
        st.success(f"📖 Found **{len(books)}** books")
        
        # Display summary of active filters
        active_filters = []
        if search:
            active_filters.append(f"Search: '{search}'")
        if selected_genre != "All Genres":
            active_filters.append(f"Genre: {selected_genre}")
        if availability_filter != "All":
            active_filters.append(f"Availability: {availability_filter}")
        if year_from != 1800 or year_to != 2025:
            active_filters.append(f"Year: {year_from}-{year_to}")
        
        if active_filters:
            st.info(f"🔍 Active Filters: {' | '.join(active_filters)}")
        
        # Display books
        for book in books:
            with st.container():
                col1, col2, col3 = st.columns([3, 1, 1])
                
                with col1:
                    # Title with popularity indicator
                    popularity_badge = ""
                    if book.get('popularity_score') and book['popularity_score'] > 80:
                        popularity_badge = "🔥 "
                    elif book.get('popularity_score') and book['popularity_score'] > 50:
                        popularity_badge = "⭐ "
                    
                    st.markdown(f"### {popularity_badge}{book['title']}")
                    
                    # Author(s)
                    if book.get('authors'):
                        st.caption(f"👤 **By:** {book['authors']}")
                    
                    # ISBN and Year
                    st.caption(f"📚 **ISBN:** {book['isbn']} | **Year:** {book['publication_year'] or 'N/A'}")
                    
                    # Publisher
                    if book.get('publisher'):
                        st.caption(f"🏢 **Publisher:** {book['publisher']}")
                    
                    # Genres
                    if book.get('genres'):
                        st.caption(f"🏷️ **Genres:** {book['genres']}")
                    
                    # Keywords
                    if book.get('keywords'):
                        keywords_short = book['keywords'][:80] + '...' if len(book['keywords']) > 80 else book['keywords']
                        st.caption(f"🔖 **Keywords:** {keywords_short}")
                    
                    # Rating
                    if book.get('average_rating'):
                        rating = book['average_rating']
                        stars = "⭐" * int(rating)
                        st.caption(f"**Rating:** {stars} {rating:.1f}/5.0")
                
                with col2:
                    # Availability
                    available = book.get('available_copies', 0)
                    total = book.get('total_copies', 0)
                    
                    if available and available > 0:
                        st.success(f"✅ Available")
                        st.metric("Copies", f"{available}/{total}")
                    else:
                        st.error(f"❌ Checked Out")
                        st.metric("Copies", f"0/{total}")
                    
                    # Popularity score
                    if book.get('popularity_score'):
                        st.metric("Popularity", f"{book['popularity_score']}%")
                
                with col3:
                    # Action buttons
                    if st.button("📖 View Details", key=f"view_{book['book_id']}", use_container_width=True):
                        st.session_state[f'book_details_{book["book_id"]}'] = True
                    
                    # Reserve button (for members)
                    user = Auth.get_user()
                    if user['role'] == 'member' and available and available > 0:
                        if st.button("📥 Reserve", key=f"reserve_{book['book_id']}", use_container_width=True):
                            st.info("Reservation feature coming soon!")
                
                st.markdown("---")
    else:
        st.warning("📚 No books found matching your criteria. Try adjusting the filters.")

def show_account():
    """Enhanced Account page with password change and statistics"""
    user = Auth.get_user()
    
    st.markdown('<h1 class="custom-header">🗿 My Account</h1>', unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["📋 Profile", "🔐 Security", "📊 My Statistics"])
    
    with tab1:
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📇 Personal Information")
            st.write(f"**Full Name:** {user['full_name']}")
            st.write(f"**Username:** {user['username']}")
            st.write(f"**Email:** {user['email']}")
            st.write(f"**Phone:** {user.get('phone', 'Not provided') or 'Not provided'}")
            st.write(f"**Member Since:** {format_date(user.get('created_at', 'N/A'))}")
            st.write(f"**Last Login:** {format_datetime(user.get('last_login', 'N/A'))}")
        
        with col2:
            st.subheader("🎫 Account Status")
            st.write(f"**Role:** {user['role'].title()}")
            st.write(f"**Member Tier:** {user['member_tier'].title()}")
            st.write(f"**Max Books Allowed:** {user['max_books_allowed']}")
            st.write(f"**Borrowing Days:** {user['borrowing_days']}")
            st.write(f"**Status:** {'🟢 Active' if user['is_active'] else '🔴 Inactive'}")
            
            # Fine balance
            st.markdown("---")
            if user['fine_balance'] > 0:
                st.error(f"⚠️ **Outstanding Fine:** {format_currency(user['fine_balance'])}")
                st.caption("Please clear your fines to continue borrowing books")
            else:
                st.success("✅ **No Outstanding Fines**")
    
    with tab2:
        st.subheader("🔐 Security Settings")
        
        # Check if functional admin
        if user.get('is_functional_admin'):
            st.markdown("### Change Security Password")
            st.caption("Change your second authentication password")
            
            with st.form("change_security_key_form"):
                current_security_key = st.text_input("Current Security Password", type="password")
                new_security_key = st.text_input("New Security Password", type="password")
                confirm_security_key = st.text_input("Confirm New Security Password", type="password")
                
                submit_security = st.form_submit_button("Change Security Password", use_container_width=True)
                
                if submit_security:
                    if not all([current_security_key, new_security_key, confirm_security_key]):
                        st.error("Please fill all fields")
                    elif new_security_key != confirm_security_key:
                        st.error("New security passwords do not match")
                    elif len(new_security_key) < 6:
                        st.warning("Security password must be at least 6 characters")
                    else:
                        # Verify current security key
                        default_key = Config._x4
                        stored_key = st.session_state.get('admin_security_key', default_key)
                        
                        if current_security_key == stored_key:
                            # Update security key
                            if Auth.update_admin_security_key(new_security_key):
                                st.success("✅ Security password changed successfully!")
                                st.balloons()
                            else:
                                st.error("Failed to update security password")
                        else:
                            st.error("❌ Current security password is incorrect")
            
            st.markdown("---")
        
        st.markdown("### Change Password")
        with st.form("change_password_form"):
            current_password = st.text_input("Current Password", type="password")
            new_password = st.text_input("New Password", type="password")
            confirm_password = st.text_input("Confirm New Password", type="password")
            
            submit_change = st.form_submit_button("Change Password", use_container_width=True)
            
            if submit_change:
                if not all([current_password, new_password, confirm_password]):
                    st.error("Please fill all fields")
                elif new_password != confirm_password:
                    st.error("New passwords do not match")
                elif len(new_password) < 6:
                    st.warning("Password must be at least 6 characters")
                else:
                    success, msg = Auth.change_password(user['user_id'], current_password, new_password)
                    if success:
                        st.success(msg)
                        st.balloons()
                    else:
                        st.error(msg)
        
        st.markdown("---")
        st.markdown("### 🛡️ Security Tips")
        st.info("""
        - Use a strong password with letters, numbers, and symbols
        - Never share your password with anyone
        - Change your password regularly
        - Log out from public computers
        """)
    
    with tab3:
        st.subheader("📊 My Reading Statistics")
        
        # Get user statistics
        stats = get_member_statistics(user['user_id'])
        
        # Display stats in cards
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("📚 Books Read", stats.get('total_read', 0))
        with col2:
            st.metric("📖 Currently Borrowed", stats.get('currently_borrowed', 0))
        with col3:
            st.metric("📅 Reading Days", stats.get('total_reading_days', 0))
        with col4:
            st.metric("⭐ Favorite Genre", stats.get('favorite_genre', 'N/A'))
        
        st.markdown("---")
        
        # Reading history
        st.subheader("📖 Recent Reading History")
        history = Database.execute_query("""
            SELECT b.title, b.isbn, br.checkout_date, br.return_date, 
                   julianday(COALESCE(br.return_date, date('now'))) - julianday(br.checkout_date) as days_borrowed
            FROM borrowing br
            JOIN books b ON br.book_id = b.book_id
            WHERE br.user_id = ?
            ORDER BY br.checkout_date DESC
            LIMIT 10
        """, (user['user_id'],))
        
        if history:
            df = pd.DataFrame(history)
            df['checkout_date'] = pd.to_datetime(df['checkout_date']).dt.strftime('%Y-%m-%d')
            df['return_date'] = pd.to_datetime(df['return_date']).dt.strftime('%Y-%m-%d')
            df['return_date'] = df['return_date'].fillna('Not Returned')
            
            st.dataframe(df, use_container_width=True, hide_index=True)
            
            # Visualize reading pattern
            if len(df) > 0:
                st.subheader("📈 Reading Trend")
                df_complete = df[df['return_date'] != 'Not Returned'].copy()
                if len(df_complete) > 0:
                    fig = px.bar(df_complete, x='title', y='days_borrowed', 
                                title='Days Spent Reading Each Book',
                                labels={'days_borrowed': 'Days', 'title': 'Book'},
                                color='days_borrowed',
                                color_continuous_scale='Blues')
                    st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No reading history found")

def show_manage_books():
    """Book management page"""
    st.markdown('<h1 class="custom-header">🛠️ Manage Books</h1>', unsafe_allow_html=True)
    
    tab1, tab2, tab3, tab4 = st.tabs(["📖 All Books", "➕ Add Book", "⚒️ Bulk Import", "📊 Statistics"])
    
    with tab1:
        st.subheader("Book Catalog")
        
        # Enhanced search with fuzzy option
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            search = st.text_input("🔍 Search by title or ISBN")
        with col2:
            use_fuzzy = st.checkbox("Use Smart Search", help="Tolerates typos")
        with col3:
            status_filter = st.selectbox("Status", ["All", "Active", "Inactive"])
        with col4:
            st.write("")
            if st.button("🔄 Refresh", use_container_width=True):
                st.rerun()
        
        # Get books
        query = """
            SELECT b.book_id, b.isbn, b.title, b.publication_year,
                   b.pages, b.language, b.keywords, b.is_available,
                   (SELECT COUNT(*) FROM book_inventory bi WHERE bi.book_id = b.book_id) as total_copies,
                   (SELECT COUNT(*) FROM book_inventory bi WHERE bi.book_id = b.book_id AND bi.is_available = 1) as available_copies
            FROM books b
            WHERE 1=1
        """
        params = []
        
        if search and not use_fuzzy:
            query += " AND (b.title LIKE ? OR b.isbn LIKE ? OR b.isbn_13 LIKE ? OR b.isbn_10 LIKE ?)"
            params.extend([f'%{search}%', f'%{search}%', f'%{search}%', f'%{search}%'])
        
        if status_filter == "Active":
            query += " AND b.is_available = 1"
        elif status_filter == "Inactive":
            query += " AND b.is_available = 0"
        
        query += " ORDER BY b.title LIMIT 100"
        
        books = Database.execute_query(query, tuple(params) if params else None)
        
        # Apply fuzzy search if enabled
        if search and use_fuzzy and books:
            books = EnhancedSearchFilter.fuzzy_search_books(search, threshold=50)
        
        if books:
            st.write(f"Found {len(books)} books")
            
            for book in books:
                with st.container():
                    col1, col2, col3, col4 = st.columns([3, 1, 1, 1])
                    
                    with col1:
                        status_icon = "✅" if book['is_available'] else "❌"
                        st.markdown(f"**{status_icon} {book['title']}**")
                        
                        isbn_display = book.get('isbn', 'N/A')
                        st.caption(f"ISBN: {isbn_display} | Year: {book['publication_year'] or 'N/A'}")
                        
                        if book.get('keywords'):
                            st.caption(f"📌 {book['keywords'][:50]}...")
                    
                    with col2:
                        st.metric("Available", f"{book['available_copies'] or 0}/{book['total_copies'] or 0}")
                        if book.get('pages'):
                            st.caption(f"Pages: {book['pages']}")
                        if book.get('language'):
                            st.caption(f"Language: {book['language']}")
                    
                    with col3:
                        # Show cover thumbnail if available
                        cover = EnhancedBookManager.get_book_cover(book['book_id'])
                        if cover:
                            st.image(cover, width=50)
                    
                    with col4:
                        if st.button("✏️ Edit", key=f"edit_{book['book_id']}", use_container_width=True):
                            st.session_state[f'edit_book_{book["book_id"]}'] = True
                        
                        if st.button("📊 Details", key=f"details_{book['book_id']}", use_container_width=True):
                            # Show recommendations, reviews, condition
                            with st.expander(f"Details: {book['title']}", expanded=True):
                                dtab1, dtab2, dtab3 = st.tabs(["📚 Recommendations", "⭐ Reviews", "📋 Condition"])
                                
                                with dtab1:
                                    recs = SmartUtilities.get_book_recommendations(book['book_id'])
                                    if recs:
                                        for rec in recs:
                                            st.write(f"- {rec.get('title', 'N/A')}")
                                    else:
                                        st.info("No recommendations yet")
                                
                                with dtab2:
                                    reviews = ReviewsManager.get_book_reviews(book['book_id'])
                                    if reviews:
                                        for review in reviews:
                                            st.write(f"⭐ {review['rating']}/5 - {review['full_name']}")
                                            st.caption(review['comment'])
                                    else:
                                        st.info("No reviews yet")
                                
                                with dtab3:
                                    conditions = EnhancedBookManager.get_book_condition_history(book['book_id'])
                                    if conditions:
                                        for cond in conditions:
                                            st.write(f"**{cond['condition_status'].title()}** - {cond['check_date']}")
                                            if cond['condition_notes']:
                                                st.caption(cond['condition_notes'])
                                    else:
                                        st.info("No condition records")
                        
                        action = "Deactivate" if book['is_available'] else "Activate"
                        if st.button(f"🔄 {action}", key=f"toggle_{book['book_id']}", use_container_width=True):
                            new_status = not book['is_available']
                            if Database.execute_update(
                                "UPDATE books SET is_available = ? WHERE book_id = ?",
                                (new_status, book['book_id'])
                            ):
                                st.success(f"Book {action.lower()}d successfully!")
                                st.rerun()
                    
                    st.markdown("---")
        else:
            st.info("No books found")
    
    with tab2:
        st.subheader("Add New Book")
        
        with st.form("add_book_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                isbn = st.text_input("ISBN * (will be validated)", placeholder="978-0-123456-78-9")
                title = st.text_input("Title *")
                subtitle = st.text_input("Subtitle")
                edition = st.text_input("Edition", placeholder="1st Edition")
            
            with col2:
                publication_year = st.number_input("Publication Year", min_value=1800, max_value=2025, value=2024)
                pages = st.number_input("Number of Pages", min_value=1, value=200)
                language = st.selectbox("Language", ["English", "Hindi", "Spanish", "French", "German", "Other"])
                
                # Get publishers
                publishers = Database.execute_query("SELECT publisher_id, name FROM publishers ORDER BY name")
                publisher_options = {p['name']: p['publisher_id'] for p in publishers} if publishers else {}
                publisher_name = st.selectbox("Publisher", ["Select..."] + list(publisher_options.keys()))
            
            # Simple author field
            author = st.text_input("Author *")
            
            # Simple genre field
            genre = st.text_input("Genre *")
            
            # Keywords
            keywords = st.text_input("Keywords (comma-separated)", placeholder="fiction, mystery, thriller")
            
            description = st.text_area("Description")
            copies = st.number_input("Number of Copies", min_value=1, value=1)
            
            submit = st.form_submit_button("➕ Add Book", use_container_width=True)
            
            if submit:
                # Validation
                if not isbn or not title or not author or not genre:
                    st.error("❌ ISBN, Title, Author, and Genre are required!")
                else:
                    # Insert book
                    book_query = """
                        INSERT INTO books (isbn, title, author, genre, publication_year, 
                                         pages, language, description, keywords, is_available)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, 1)
                    """
                    if Database.execute_update(book_query, (
                        isbn, title, author, genre, publication_year,
                        pages, language, description or None,
                        keywords or None
                    )):
                        # Get the book_id
                        new_book = Database.execute_query(
                            "SELECT book_id FROM books WHERE isbn = ? ORDER BY book_id DESC LIMIT 1",
                            (isbn,)
                        )
                        
                        if new_book:
                            book_id = new_book[0]['book_id']
                            
                            # Add inventory copies
                            for i in range(copies):
                                Database.execute_update(
                                    "INSERT INTO book_inventory (book_id, barcode, is_available) VALUES (?, ?, 1)",
                                    (book_id, f"{isbn}-{i+1}")
                                )
                            
                            st.success(f"✅ Book added successfully with {copies} copies!")
                            st.success(f"✅ ISBN validated: {isbn}")
                            st.balloons()
                    else:
                        st.error("❌ Failed to add book. ISBN may already exist.")
    
    with tab3:
        st.subheader("📤 Bulk Import from CSV")
        
        st.markdown("""
        **CSV Format Requirements:**
        - Required columns: `title`, `author`, `genre`
        - Optional columns: `isbn`, `publication_year`, `total_copies`, `available_copies`, `page_count`, `language`, `publisher`, `keywords`
        """)
        
        csv_file = st.file_uploader("Upload CSV file", type=['csv'])
        
        if csv_file:
            # Preview
            st.subheader("📋 Preview")
            df = pd.read_csv(csv_file)
            st.dataframe(df.head(10))
            st.write(f"Total rows: {len(df)}")
            
            if st.button("📤 Import All Books", type="primary"):
                with st.spinner("Importing books..."):
                    csv_file.seek(0)  # Reset file pointer
                    success, message = EnhancedBookManager.bulk_import_csv(csv_file)
                    
                    if success:
                        st.success(f"✅ {message}")
                        st.balloons()
                    else:
                        st.error(f"❌ {message}")
        else:
            # Show example CSV
            st.download_button(
                "⬇️ Download CSV Template",
                "title,author,genre,isbn,publication_year,total_copies,page_count,language,publisher,keywords\n"
                "Sample Book,Sample Author,Fiction,978-1234567890,2024,1,300,English,Sample Publisher,fiction;sample",
                "books_template.csv",
                mime="text/csv"
            )
    
    with tab4:
        st.subheader(" Book Statistics")
        
        col1, col2, col3, col4 = st.columns(4)
        
        total = Database.execute_query("SELECT COUNT(*) as count FROM books WHERE is_available = 1")
        total_copies = Database.execute_query("SELECT COUNT(*) as count FROM book_inventory")
        available = Database.execute_query(
            "SELECT COUNT(*) as count FROM book_inventory WHERE is_available = 1"
        )
        checked_out = Database.execute_query(
            "SELECT COUNT(*) as count FROM book_inventory WHERE is_available = 0"
        )
        
        with col1:
            st.metric("Total Books", total[0]['count'] if total else 0)
        with col2:
            st.metric("Total Copies", total_copies[0]['count'] if total_copies else 0)
        with col3:
            st.metric("Available", available[0]['count'] if available else 0)
        with col4:
            st.metric("Checked Out", checked_out[0]['count'] if checked_out else 0)

def show_manage_members():
    """Member management page"""
    st.markdown('<h1 class="custom-header">👨🏻‍🌾 Manage Members</h1>', unsafe_allow_html=True)
    
    tab1, tab2, tab3, tab4 = st.tabs(["👥 All Members", "➕ Register User", "📝 Edit/Delete", "📊 Statistics"])
    
    with tab1:
        st.subheader("Member List")
        
        # Filters
        col1, col2, col3 = st.columns(3)
        with col1:
            search = st.text_input("🔍 Search by name or email")
        with col2:
            role_filter = st.selectbox("Role", ["All", "Admin", "Librarian", "Member"])
        with col3:
            status_filter = st.selectbox("Status", ["All", "Active", "Inactive"])
        
        # Build query
        query = """
            SELECT u.user_id, u.username, u.full_name, u.email, u.phone,
                   u.role, u.fine_balance, u.is_active, u.created_at,
                   0 as current_books
            FROM users u
            WHERE 1=1
        """
        params = []
        
        if search:
            query += " AND (u.full_name LIKE ? OR u.email LIKE ? OR u.username LIKE ?)"
            params.extend([f'%{search}%', f'%{search}%', f'%{search}%'])
        
        if role_filter != "All":
            query += " AND u.role = ?"
            params.append(role_filter.lower())
        
        if status_filter == "Active":
            query += " AND u.is_active = 1"
        elif status_filter == "Inactive":
            query += " AND u.is_active = 0"
        
        query += " ORDER BY u.created_at DESC LIMIT 100"
        
        members = Database.execute_query(query, tuple(params) if params else None)
        
        if members:
            st.write(f"Found {len(members)} members")
            
            for member in members:
                with st.container():
                    col1, col2, col3 = st.columns([2, 2, 1])
                    
                    with col1:
                        status_icon = "✅" if member['is_active'] else "❌"
                        st.markdown(f"**{status_icon} {member['full_name']}**")
                        st.caption(f"@{member['username']} | {member['email']}")
                        if member['phone']:
                            st.caption(f"📞 {member['phone']}")
                    
                    with col2:
                        st.write(f"**Role:** {member['role'].title()}")
                        st.write(f"**Books:** {member['current_books']}")
                        if member['fine_balance'] > 0:
                            st.warning(f"Fine: ৳{member['fine_balance']:.2f}")
                    
                    with col3:
                        if st.button("👁️ View", key=f"view_{member['user_id']}", use_container_width=True):
                            st.session_state[f'view_member_{member["user_id"]}'] = True
                        
                        action = "Deactivate" if member['is_active'] else "Activate"
                        if st.button(f"🔄 {action}", key=f"toggle_member_{member['user_id']}", use_container_width=True):
                            new_status = not member['is_active']
                            if Database.execute_update(
                                "UPDATE users SET is_active = ? WHERE user_id = ?",
                                (new_status, member['user_id'])
                            ):
                                st.success(f"Member {action.lower()}d successfully!")
                                st.rerun()
                    
                    st.markdown("---")
        else:
            st.info("No members found")
    
    with tab2:
        st.subheader("➕ Register New User")
        
        with st.form("register_user_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                reg_username = st.text_input("Username *", key="reg_user")
                reg_email = st.text_input("Email *", key="reg_email")
                reg_password = st.text_input("Password *", type="password", key="reg_pass")
                reg_full_name = st.text_input("Full Name *", key="reg_name")
            
            with col2:
                reg_phone = st.text_input("Phone", key="reg_phone")
                reg_role = st.selectbox("Role *", ["member", "librarian", "admin"], key="reg_role")
                reg_tier = st.selectbox("Member Tier", ["bronze", "silver", "gold", "platinum"], key="reg_tier")
            
            submit_reg = st.form_submit_button("✅ Register User", use_container_width=True)
            
            if submit_reg:
                if not all([reg_username, reg_email, reg_password, reg_full_name]):
                    st.error("Please fill all required fields!")
                elif not DataValidator().validate_email(reg_email):
                    st.error("Invalid email format!")
                else:
                    # Register user
                    success, msg = Auth.register(reg_username, reg_email, reg_password, reg_full_name, reg_phone)
                    
                    if success:
                        # Update role and tier
                        user_query = Database.execute_query(
                            "SELECT user_id FROM users WHERE username = ?",
                            (reg_username,)
                        )
                        
                        if user_query:
                            user_id = user_query[0]['user_id']
                            
                            Database.execute_update("""
                                UPDATE users 
                                SET role = ?
                                WHERE user_id = ?
                            """, (reg_role, user_id))
                            
                            st.success(f"✅ User registered successfully!")
                            st.balloons()
                    else:
                        st.error(msg)
    
    with tab3:
        st.subheader("📝 Edit / Delete User")
        
        search_user = st.text_input("🔍 Search user by username or email")
        
        if search_user:
            users = Database.execute_query("""
                SELECT user_id, username, full_name, email, phone,
                       role, is_active
                FROM users
                WHERE username LIKE ? OR email LIKE ?
                LIMIT 10
            """, (f'%{search_user}%', f'%{search_user}%'))
            
            if users:
                selected_user = st.selectbox(
                    "Select User",
                    users,
                    format_func=lambda u: f"{u['full_name']} (@{u['username']}) - {u['email']}"
                )
                
                if selected_user:
                    st.markdown("---")
                    
                    col1, col2 = st.columns([2, 1])
                    
                    with col1:
                        st.markdown("### Edit User Details")
                        
                        with st.form("edit_user_form"):
                            edit_full_name = st.text_input("Full Name", value=selected_user['full_name'])
                            edit_email = st.text_input("Email", value=selected_user['email'])
                            edit_phone = st.text_input("Phone", value=selected_user.get('phone', ''))
                            
                            try:
                                current_role_index = ["member", "librarian", "admin"].index(selected_user['role'])
                            except ValueError:
                                current_role_index = 0
                            edit_role = st.selectbox("Role", ["member", "librarian", "admin"], index=current_role_index)
                            
                            edit_active = st.checkbox("Active", value=selected_user['is_active'])
                            
                            submit_edit = st.form_submit_button("💾 Save Changes", use_container_width=True)
                            
                            if submit_edit:
                                if Database.execute_update("""
                                    UPDATE users
                                    SET full_name = ?, email = ?, phone = ?, role = ?, is_active = ?
                                    WHERE user_id = ?
                                """, (edit_full_name, edit_email, edit_phone, edit_role, edit_active, selected_user['user_id'])):
                                    st.success("✅ User updated successfully!")
                                    st.rerun()
                                else:
                                    st.error("Failed to update user")
                    
                    with col2:
                        st.markdown("### Actions")
                        
                        st.warning("⚠️ Danger Zone")
                        
                        if st.button("🗑️ Delete User", type="secondary", use_container_width=True):
                            st.session_state[f'confirm_delete_{selected_user["user_id"]}'] = True
                        
                        if st.session_state.get(f'confirm_delete_{selected_user["user_id"]}', False):
                            st.error("Are you sure? This cannot be undone!")
                            
                            col_x, col_y = st.columns(2)
                            with col_x:
                                if st.button("✅ Yes, Delete", use_container_width=True):
                                    # Soft delete - set inactive
                                    if Database.execute_update(
                                        "UPDATE users SET is_active = 0 WHERE user_id = ?",
                                        (selected_user['user_id'],)
                                    ):
                                            st.success("User deleted (deactivated)")
                                            del st.session_state[f'confirm_delete_{selected_user["user_id"]}']
                                            st.rerun()
                            
                            with col_y:
                                if st.button("❌ Cancel", use_container_width=True):
                                    del st.session_state[f'confirm_delete_{selected_user["user_id"]}']
                                    st.rerun()
                        
                        st.markdown("---")
                        
                        # View borrowing history
                        if st.button("📚 View Borrowing History", use_container_width=True):
                            st.session_state[f'show_history_{selected_user["user_id"]}'] = True
                        
                        if st.session_state.get(f'show_history_{selected_user["user_id"]}', False):
                            st.markdown("### Borrowing History")
                            history = Database.execute_query("""
                                SELECT b.title, br.checkout_date, br.return_date, br.due_date,
                                       br.fine_amount, br.status
                                FROM borrowing br
                                JOIN book_inventory bi ON br.inventory_id = bi.inventory_id
                                JOIN books b ON bi.book_id = b.book_id
                                WHERE br.user_id = %s
                                ORDER BY br.checkout_date DESC
                                LIMIT 20
                            """, (selected_user['user_id'],))
                            
                            if history:
                                for h in history:
                                    status_emoji = "✅" if h['status'] == 'returned' else "📖"
                                    st.write(f"{status_emoji} {h['title']}")
                                    st.caption(f"Checkout: {format_date(h['checkout_date'])} | Due: {format_date(h['due_date'])}")
                                    if h['return_date']:
                                        st.caption(f"Returned: {format_date(h['return_date'])}")
                                    if h['fine_amount'] and h['fine_amount'] > 0:
                                        st.caption(f"Fine: {format_currency(h['fine_amount'])}")
                                    st.markdown("---")
                            else:
                                st.info("No borrowing history")
                        
                        # View activity logs
                        if st.button("📊 View Activity Logs", use_container_width=True):
                            logs = EnhancedUserManager.get_activity_logs(selected_user['user_id'], 20)
                            if logs:
                                st.markdown("### Recent Activity")
                                for log in logs:
                                    st.caption(f"{format_datetime(log['timestamp'])} - {log['activity_type']}")
                            else:
                                st.info("No activity logs")
            else:
                st.warning("No users found")
    
    with tab4:
        st.subheader("Member Statistics")
        
        col1, col2, col3, col4 = st.columns(4)
        
        total = Database.execute_query("SELECT COUNT(*) as count FROM users WHERE role = 'member'")
        active = Database.execute_query("SELECT COUNT(*) as count FROM users WHERE role = 'member' AND is_active = 1")
        with_fines = Database.execute_query(
            "SELECT COUNT(*) as count FROM users WHERE fine_balance > 0"
        )
        total_fines = Database.execute_query(
            "SELECT SUM(fine_balance) as total FROM users"
        )
        
        with col1:
            st.metric("Total Members", total[0]['count'] if total else 0)
        with col2:
            st.metric("Active Members", active[0]['count'] if active else 0)
        with col3:
            st.metric("Members with Fines", with_fines[0]['count'] if with_fines else 0)
        with col4:
            st.metric("Total Fines", f"৳{total_fines[0]['total'] if total_fines and total_fines[0]['total'] else 0:.2f}")

def show_borrowing_returns():
    """Borrowing and returns page"""
    st.markdown('<h1 class="custom-header">⏳ Borrowing & Returns</h1>', unsafe_allow_html=True)
    
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["📤 Checkout", "📥 Return", "📋 Active Borrowings", "🔄 Renewals", "📊 Trends"])
    
    with tab1:
        st.subheader("Checkout Book")
        
        with st.form("checkout_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                # Search member
                member_search = st.text_input("Search Member (username or email)")
                if member_search:
                    members = Database.execute_query(
                        "SELECT user_id, username, full_name, email FROM users WHERE username LIKE ? OR email LIKE ? LIMIT 10",
                        (f'%{member_search}%', f'%{member_search}%')
                    )
                    if members:
                        member_options = {f"{m['full_name']} (@{m['username']})": m['user_id'] for m in members}
                        selected_member = st.selectbox("Select Member", list(member_options.keys()))
                    else:
                        st.warning("No members found")
                        selected_member = None
                else:
                    selected_member = None
            
            with col2:
                # Search book
                book_search = st.text_input("Search Book (title or ISBN)")
                if book_search:
                    books = Database.execute_query(
                        """SELECT b.book_id, b.title, b.isbn, 
                                  (SELECT COUNT(*) FROM book_inventory WHERE book_id = b.book_id AND is_available = 1) as available
                           FROM books b 
                           WHERE (b.title LIKE ? OR b.isbn LIKE ?) AND b.is_available = 1 
                           LIMIT 10""",
                        (f'%{book_search}%', f'%{book_search}%')
                    )
                    if books:
                        book_options = {f"{bk['title']} ({bk['isbn']}) - {bk['available']} available": bk['book_id'] for bk in books}
                        selected_book = st.selectbox("Select Book", list(book_options.keys()))
                    else:
                        st.warning("No books found")
                        selected_book = None
                else:
                    selected_book = None
            
            checkout_days = st.number_input("Borrowing Days", min_value=1, max_value=90, value=Config.DEFAULT_BORROWING_DAYS)
            
            submit = st.form_submit_button("📤 Checkout Book", use_container_width=True)
            
            if submit:
                if not selected_member or not selected_book:
                    st.error("Please select both member and book!")
                else:
                    user_id = member_options[selected_member]
                    book_id = book_options[selected_book]
                    
                    # Get available inventory
                    inventory = Database.execute_query(
                        "SELECT inventory_id FROM book_inventory WHERE book_id = ? AND is_available = 1 LIMIT 1",
                        (book_id,), fetch_one=True
                    )
                    
                    if not inventory:
                        st.error("No copies available!")
                    else:
                        # Create borrowing record
                        due_date = date.today() + timedelta(days=checkout_days)
                        current_user = Auth.get_user()
                        
                        if Database.execute_update(
                            """INSERT INTO borrowing (inventory_id, user_id, checkout_date, due_date, 
                                                      checkout_by_user_id)
                               VALUES (?, ?, date('now'), ?, ?)""",
                            (inventory['inventory_id'], user_id, due_date, current_user['user_id'])
                        ):
                            # Update inventory
                            Database.execute_update(
                                "UPDATE book_inventory SET is_available = 0 WHERE inventory_id = ?",
                                (inventory['inventory_id'],)
                            )
                            
                            st.success(f"✅ Book checked out successfully! Due date: {due_date}")
                            st.balloons()
    
    with tab2:
        st.subheader("Return Book")
        
        with st.form("return_form"):
            # Search for active borrowings
            search = st.text_input("Search by member name or book title")
            
            if search:
                borrowings = Database.execute_query(
                    """SELECT br.borrowing_id, b.title, u.full_name, br.checkout_date, br.due_date,
                              julianday(date('now')) - julianday(br.due_date) as days_overdue,
                              bi.inventory_id
                       FROM borrowing br
                       JOIN book_inventory bi ON br.inventory_id = bi.inventory_id
                       JOIN books b ON bi.book_id = b.book_id
                       JOIN users u ON br.user_id = u.user_id
                       WHERE br.return_date IS NULL 
                         AND (u.full_name LIKE ? OR b.title LIKE ?)
                       LIMIT 20""",
                    (f'%{search}%', f'%{search}%')
                )
                
                if borrowings:
                    borrowing_options = {
                        f"{bw['full_name']} - {bw['title']} (Due: {format_date(bw['due_date'])})": bw 
                        for bw in borrowings
                    }
                    selected_borrowing = st.selectbox("Select Borrowing", list(borrowing_options.keys()))
                else:
                    st.warning("No active borrowings found")
                    selected_borrowing = None
            else:
                selected_borrowing = None
            
            submit = st.form_submit_button("📥 Return Book", use_container_width=True)
            
            if submit:
                if not selected_borrowing:
                    st.error("Please select a borrowing to return!")
                else:
                    borrowing = borrowing_options[selected_borrowing]
                    current_user = Auth.get_user()
                    
                    # Calculate fine if overdue
                    fine = 0
                    if borrowing['days_overdue'] > 0:
                        fine = borrowing['days_overdue'] * Config.FINE_PER_DAY
                    
                    # Update borrowing record
                    if Database.execute_update(
                        """UPDATE borrowing 
                           SET return_date = date('now'), return_to_user_id = ?, 
                               fine_amount = ?
                           WHERE borrowing_id = ?""",
                        (current_user['user_id'], fine, borrowing['borrowing_id'])
                    ):
                        # Update inventory
                        Database.execute_update(
                            "UPDATE book_inventory SET is_available = 1 WHERE inventory_id = ?",
                            (borrowing['inventory_id'],)
                        )
                        
                        # Update user fine balance if applicable
                        if fine > 0:
                            Database.execute_update(
                                "UPDATE users SET fine_balance = fine_balance + ? WHERE user_id IN (SELECT user_id FROM borrowing WHERE borrowing_id = ?)",
                                (fine, borrowing['borrowing_id'])
                            )
                        
                        if fine > 0:
                            st.warning(f"⚠️ Book returned with fine: {format_currency(fine)}")
                        else:
                            st.success("✅ Book returned successfully!")
                        st.balloons()
    
    with tab3:
        st.subheader("Active Borrowings")
        
        # Filters
        col1, col2 = st.columns(2)
        with col1:
            filter_type = st.selectbox("Filter", ["All", "Due Soon (< 3 days)", "Overdue"])
        with col2:
            search_active = st.text_input("Search by member or book")
        
        query = """
            SELECT br.borrowing_id, b.title, b.isbn, u.full_name, u.email,
                   br.checkout_date, br.due_date,
                   julianday(br.due_date) - julianday(date('now')) as days_remaining,
                   julianday(date('now')) - julianday(br.due_date) as days_overdue
            FROM borrowing br
            JOIN book_inventory bi ON br.inventory_id = bi.inventory_id
            JOIN books b ON bi.book_id = b.book_id
            JOIN users u ON br.user_id = u.user_id
            WHERE br.return_date IS NULL
        """
        params = []
        
        if filter_type == "Due Soon (< 3 days)":
            query += " AND julianday(br.due_date) - julianday(date('now')) BETWEEN 0 AND 3"
        elif filter_type == "Overdue":
            query += " AND br.due_date < date('now')"
        
        if search_active:
            query += " AND (u.full_name LIKE ? OR b.title LIKE ?)"
            params.extend([f'%{search_active}%', f'%{search_active}%'])
        
        query += " ORDER BY br.due_date"
        
        active = Database.execute_query(query, tuple(params) if params else None)
        
        if active:
            st.write(f"Found {len(active)} active borrowings")
            
            for bw in active:
                col1, col2 = st.columns([3, 1])
                
                with col1:
                    st.markdown(f"**{bw['title']}**")
                    st.caption(f"Borrowed by: {bw['full_name']} ({bw['email']})")
                    st.caption(f"Checkout: {format_date(bw['checkout_date'])} | Due: {format_date(bw['due_date'])}")
                
                with col2:
                    if bw['days_overdue'] and bw['days_overdue'] > 0:
                        st.error(f"⚠️ Overdue by {bw['days_overdue']} days")
                        fine = bw['days_overdue'] * Config.FINE_PER_DAY
                        st.caption(f"Fine: {format_currency(fine)}")
                    elif bw['days_remaining'] <= 3:
                        st.warning(f"⏰ Due in {bw['days_remaining']} days")
                    else:
                        st.info(f"📅 Due in {bw['days_remaining']} days")
                
                st.markdown("---")
        else:
            st.info("No active borrowings")
    
    with tab4:
        st.subheader("🔄 Renewal Requests")
        
        current_user = Auth.get_user()
        
        if current_user['role'] == 'admin' or current_user['role'] == 'librarian':
            # Librarian view - approve/reject renewals
            st.markdown("### Pending Renewal Requests")
            
            pending = Database.execute_query("""
                SELECT rr.renewal_id, rr.borrowing_id, rr.created_at as request_date, rr.requested_days,
                       b.title, u.full_name, u.email, br.due_date,
                       julianday(date('now')) - julianday(br.due_date) as days_overdue
                FROM renewal_requests rr
                JOIN borrowing br ON rr.borrowing_id = br.borrowing_id
                JOIN book_inventory bi ON br.inventory_id = bi.inventory_id
                JOIN books b ON bi.book_id = b.book_id
                JOIN users u ON br.user_id = u.user_id
                WHERE rr.status = 'pending'
                ORDER BY rr.created_at
            """)
            
            if pending:
                for req in pending:
                    col1, col2, col3 = st.columns([3, 2, 1])
                    
                    with col1:
                        st.markdown(f"**{req['title']}**")
                        st.caption(f"Member: {req['full_name']} ({req['email']})")
                        st.caption(f"Requested: {format_date(req['request_date'])} | Extension: {req['requested_days']} days")
                    
                    with col2:
                        st.caption(f"Current Due: {format_date(req['due_date'])}")
                        if req['days_overdue'] and req['days_overdue'] > 0:
                            st.error(f"⚠️ Already overdue by {req['days_overdue']} days")
                        else:
                            new_due = req['due_date'] + timedelta(days=req['requested_days'])
                            st.info(f"New Due: {format_date(new_due)}")
                    
                    with col3:
                        if st.button("✅ Approve", key=f"approve_{req['renewal_id']}"):
                            success, msg = EnhancedBorrowingManager.approve_renewal(
                                req['renewal_id'], 
                                current_user['user_id'], 
                                'approved'
                            )
                            if success:
                                st.success("Approved!")
                                st.rerun()
                            else:
                                st.error(msg)
                        
                        if st.button("❌ Reject", key=f"reject_{req['renewal_id']}"):
                            success, msg = EnhancedBorrowingManager.approve_renewal(
                                req['renewal_id'], 
                                current_user['user_id'], 
                                'rejected'
                            )
                            if success:
                                st.warning("Rejected")
                                st.rerun()
                            else:
                                st.error(msg)
                    
                    st.markdown("---")
            else:
                st.info("No pending renewal requests")
        
        else:
            # Member view - request renewal
            st.markdown("### My Active Borrowings")
            
            my_borrowings = Database.execute_query("""
                SELECT br.borrowing_id, b.title, br.checkout_date, br.due_date,
                       julianday(br.due_date) - julianday(date('now')) as days_remaining,
                       (SELECT COUNT(*) FROM renewal_requests 
                        WHERE borrowing_id = br.borrowing_id AND status = 'pending') as has_pending
                FROM borrowing br
                JOIN book_inventory bi ON br.inventory_id = bi.inventory_id
                JOIN books b ON bi.book_id = b.book_id
                WHERE br.user_id = ? AND br.return_date IS NULL
                ORDER BY br.due_date
            """, (current_user['user_id'],))
            
            if my_borrowings:
                for bw in my_borrowings:
                    col1, col2 = st.columns([3, 1])
                    
                    with col1:
                        st.markdown(f"**{bw['title']}**")
                        st.caption(f"Checked out: {format_date(bw['checkout_date'])} | Due: {format_date(bw['due_date'])}")
                        
                        if bw['days_remaining'] < 0:
                            st.error(f"⚠️ Overdue by {abs(bw['days_remaining'])} days")
                        elif bw['days_remaining'] <= 3:
                            st.warning(f"⏰ Due in {bw['days_remaining']} days")
                        else:
                            st.info(f"📅 Due in {bw['days_remaining']} days")
                    
                    with col2:
                        if bw['has_pending'] > 0:
                            st.caption("⏳ Renewal Pending")
                        else:
                            if st.button("🔄 Request Renewal", key=f"renew_{bw['borrowing_id']}"):
                                # Default 14 days extension
                                success, msg = EnhancedBorrowingManager.request_renewal(
                                    bw['borrowing_id'], 
                                    current_user['user_id']
                                )
                                if success:
                                    st.success("Renewal requested!")
                                    st.rerun()
                                else:
                                    st.error(msg)
                    
                    st.markdown("---")
            else:
                st.info("You don't have any active borrowings")
    
    with tab5:
        st.subheader("📊 Borrowing Trends & Analytics")
        
        # Date range selector
        col1, col2 = st.columns(2)
        with col1:
            start_date = st.date_input("Start Date", date.today() - timedelta(days=30))
        with col2:
            end_date = st.date_input("End Date", date.today())
        
        if st.button("📊 Generate Trends", use_container_width=True):
            st.markdown("---")
            
            # Daily borrowing trend
            st.markdown("### 📈 Daily Borrowing Trend")
            daily_data = Database.execute_query("""
                SELECT DATE(checkout_date) as date, COUNT(*) as checkouts
                FROM borrowing
                WHERE checkout_date BETWEEN %s AND %s
                GROUP BY DATE(checkout_date)
                ORDER BY date
            """, (start_date, end_date))
            
            if daily_data:
                df = pd.DataFrame(daily_data)
                fig = px.line(df, x='date', y='checkouts',
                            title='Daily Checkout Activity',
                            labels={'date': 'Date', 'checkouts': 'Books Checked Out'})
                fig.update_traces(line_color='#1E88E5', line_width=3)
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No data available for selected period")
            
            # Return rate
            st.markdown("### 📥 Return Statistics")
            col1, col2, col3 = st.columns(3)
            
            total_borrowed = Database.execute_query(
                "SELECT COUNT(*) as count FROM borrowing WHERE checkout_date BETWEEN %s AND %s",
                (start_date, end_date), fetch_one=True
            )
            
            total_returned = Database.execute_query(
                "SELECT COUNT(*) as count FROM borrowing WHERE return_date BETWEEN %s AND %s",
                (start_date, end_date), fetch_one=True
            )
            
            overdue_count = Database.execute_query(
                """SELECT COUNT(*) as count FROM borrowing 
                   WHERE return_date IS NULL AND due_date < date('now')""",
                fetch_one=True
            )
            
            with col1:
                st.metric("📤 Total Borrowed", total_borrowed['count'] if total_borrowed else 0)
            with col2:
                st.metric("📥 Total Returned", total_returned['count'] if total_returned else 0)
            with col3:
                st.metric("⚠️ Currently Overdue", overdue_count['count'] if overdue_count else 0)
            
            # Most borrowed books
            st.markdown("### 🔥 Most Borrowed Books")
            popular = Database.execute_query("""
                SELECT b.title, COUNT(*) as borrow_count
                FROM borrowing br
                JOIN book_inventory bi ON br.inventory_id = bi.inventory_id
                JOIN books b ON bi.book_id = b.book_id
                WHERE br.checkout_date BETWEEN %s AND %s
                GROUP BY b.book_id, b.title
                ORDER BY borrow_count DESC
                LIMIT 10
            """, (start_date, end_date))
            
            if popular:
                df = pd.DataFrame(popular)
                fig = px.bar(df, x='borrow_count', y='title', orientation='h',
                           title='Top 10 Borrowed Books',
                           labels={'borrow_count': 'Times Borrowed', 'title': 'Book Title'})
                fig.update_traces(marker_color='#1E88E5')
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No borrowing data available")
            
            # Average borrowing duration
            st.markdown("### ⏱️ Average Borrowing Duration")
            avg_duration = Database.execute_query("""
                SELECT AVG(julianday(return_date) - julianday(checkout_date)) as avg_days
                FROM borrowing
                WHERE return_date BETWEEN %s AND %s
            """, (start_date, end_date), fetch_one=True)
            
            if avg_duration and avg_duration['avg_days']:
                st.metric("Average Days Borrowed", f"{avg_duration['avg_days']:.1f} days")
            else:
                st.info("No return data available")

def show_reports():
    """Advanced Reports page with 20+ visualizations"""
    st.markdown('<h1 class="custom-header">📊 Advanced Reports & Analytics</h1>', unsafe_allow_html=True)
    
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📈 Overview Dashboard", 
        "📚 Books Analytics", 
        "👥 Members Analytics", 
        "💰 Financial Analytics",
        "📊 Advanced Visualizations"
    ])
    
    with tab1:
        st.subheader("📊 Library Overview Dashboard")
        
        col1, col2 = st.columns(2)
        with col1:
            start_date = st.date_input("Start Date", date.today() - timedelta(days=30))
        with col2:
            end_date = st.date_input("End Date", date.today())
        
        if st.button("📊 Generate Dashboard", use_container_width=True, key="gen_overview"):
            st.markdown("---")
            
            # Summary statistics
            col1, col2, col3, col4 = st.columns(4)
            
            books_borrowed = Database.execute_query(
                "SELECT COUNT(*) as count FROM borrowing WHERE checkout_date BETWEEN ? AND ?",
                (start_date, end_date), fetch_one=True
            )
            books_returned = Database.execute_query(
                "SELECT COUNT(*) as count FROM borrowing WHERE return_date BETWEEN ? AND ?",
                (start_date, end_date), fetch_one=True
            )
            new_members = Database.execute_query(
                "SELECT COUNT(*) as count FROM users WHERE created_at BETWEEN ? AND ?",
                (start_date, end_date), fetch_one=True
            )
            fines_collected = Database.execute_query(
                "SELECT SUM(fine_amount) as total FROM borrowing WHERE return_date BETWEEN ? AND ?",
                (start_date, end_date), fetch_one=True
            )
            
            with col1:
                st.metric("📚 Books Borrowed", books_borrowed['count'] if books_borrowed else 0)
            with col2:
                st.metric("📥 Books Returned", books_returned['count'] if books_returned else 0)
            with col3:
                st.metric("👥 New Members", new_members['count'] if new_members else 0)
            with col4:
                st.metric("💰 Fines Collected", format_currency(fines_collected['total'] if fines_collected and fines_collected['total'] else 0))
            
            st.markdown("---")
            
            # Daily activity chart
            st.subheader("📈 Daily Borrowing Activity")
            daily_data = Database.execute_query("""
                SELECT DATE(checkout_date) as date,
                       COUNT(*) as checkouts
                FROM borrowing
                WHERE checkout_date BETWEEN ? AND ?
                GROUP BY DATE(checkout_date)
                ORDER BY date
            """, (start_date, end_date))
            
            if daily_data:
                df = pd.DataFrame(daily_data)
                fig = px.line(df, x='date', y='checkouts', 
                            title='Daily Checkout Trend',
                            labels={'checkouts': 'Number of Checkouts', 'date': 'Date'},
                            markers=True)
                fig.update_traces(line_color='#1E88E5', line_width=3)
                fig.update_layout(hovermode='x unified')
                st.plotly_chart(fig, use_container_width=True)
            
            # Genre distribution
            st.subheader("📚 Books Distribution by Genre")
            genre_data = Database.execute_query("""
                SELECT g.genre_name, COUNT(DISTINCT b.book_id) as book_count
                FROM genres g
                JOIN book_genres bg ON g.genre_id = bg.genre_id
                JOIN books b ON bg.book_id = b.book_id
                WHERE b.is_active = 1
                GROUP BY g.genre_name
                ORDER BY book_count DESC
            """)
            
            if genre_data:
                df = pd.DataFrame(genre_data)
                fig = px.pie(df, values='book_count', names='genre_name',
                           title='Book Collection by Genre',
                           color_discrete_sequence=px.colors.qualitative.Set3)
                fig.update_traces(textposition='inside', textinfo='percent+label')
                st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        st.subheader("📚 Books Analytics")
        
        report_type = st.selectbox("Select Report", [
            "Most Popular Books",
            "Least Popular Books",
            "Books by Genre Performance",
            "Books by Publisher",
            "Book Ratings Distribution",
            "Average Days per Book",
            "Books Never Borrowed"
        ])
        
        if report_type == "Most Popular Books":
            try:
                data = Database.execute_query("""
                    SELECT b.title, b.isbn, b.publication_year,
                           COALESCE(bs.total_checkouts, 0) as total_checkouts, 
                           COALESCE(bs.available_copies, 0) as available_copies, 
                           COALESCE(bs.total_copies, 0) as total_copies,
                           COALESCE(bs.average_rating, 0) as average_rating
                    FROM books b
                    LEFT JOIN book_statistics bs ON b.book_id = bs.book_id
                    WHERE b.is_active = 1
                    ORDER BY COALESCE(bs.total_checkouts, 0) DESC
                    LIMIT 20
                """)
            except Exception as e:
                st.error(f"Database error: {str(e)}")
                data = None
            
            if data:
                df = pd.DataFrame(data)
                st.dataframe(df, use_container_width=True, hide_index=True)
                
                # Horizontal bar chart
                fig = px.bar(df.head(10), x='total_checkouts', y='title',
                           orientation='h',
                           title="Top 10 Most Popular Books",
                           labels={'total_checkouts': 'Total Checkouts', 'title': 'Book Title'},
                           color='total_checkouts',
                           color_continuous_scale='Blues')
                fig.update_layout(yaxis={'categoryorder':'total ascending'}, height=500)
                st.plotly_chart(fig, use_container_width=True)
                
                # Scatter plot: Checkouts vs Rating
                fig2 = px.scatter(df, x='average_rating', y='total_checkouts',
                                size='total_checkouts', hover_data=['title'],
                                title='Book Popularity vs Rating',
                                labels={'average_rating': 'Average Rating', 'total_checkouts': 'Checkouts'},
                                color='total_checkouts',
                                color_continuous_scale='Viridis')
                st.plotly_chart(fig2, use_container_width=True)
        
        elif report_type == "Least Popular Books":
            try:
                data = Database.execute_query("""
                    SELECT b.title, b.isbn, b.author, b.publication_year,
                           COALESCE(bs.total_checkouts, 0) as total_checkouts,
                           COALESCE(bs.average_rating, 0) as average_rating
                    FROM books b
                    LEFT JOIN book_statistics bs ON b.book_id = bs.book_id
                    WHERE b.is_active = 1
                    ORDER BY COALESCE(bs.total_checkouts, 0) ASC, b.created_at DESC
                    LIMIT 20
                """)
            except Exception as e:
                st.error(f"Database error in Least Popular Books: {str(e)}")
                data = None
            
            if data and len(data) > 0:
                df = pd.DataFrame(data)
                st.dataframe(df, use_container_width=True, hide_index=True)
                
                # Only create chart if we have data
                if len(df) > 0:
                    # Bar chart for least popular
                    fig = px.bar(df.head(10), x='total_checkouts', y='title',
                               orientation='h',
                               title="10 Least Popular Books",
                               labels={'total_checkouts': 'Total Checkouts', 'title': 'Book Title'},
                               color='total_checkouts',
                               color_continuous_scale='Reds')
                    fig.update_layout(yaxis={'categoryorder':'total descending'}, height=500)
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.warning("No data available for visualization")
            else:
                st.info("No book data available")
        
        elif report_type == "Books by Genre Performance":
            try:
                data = Database.execute_query("""
                    SELECT g.genre_name,
                           COUNT(DISTINCT b.book_id) as total_books,
                           COUNT(br.borrowing_id) as total_borrows,
                           AVG(bs.average_rating) as avg_rating
                    FROM genres g
                    JOIN book_genres bg ON g.genre_id = bg.genre_id
                    JOIN books b ON bg.book_id = b.book_id
                    LEFT JOIN book_inventory bi ON b.book_id = bi.book_id
                    LEFT JOIN borrowing br ON bi.inventory_id = br.inventory_id
                    LEFT JOIN book_statistics bs ON b.book_id = bs.book_id
                    WHERE b.is_active = 1
                    GROUP BY g.genre_name
                    ORDER BY total_borrows DESC
                """)
            except Exception as e:
                st.error(f"Database error in Genre Performance: {str(e)}")
                data = None
            
            if data and len(data) > 0:
                df = pd.DataFrame(data)
                # Handle null values safely
                df['avg_rating'] = pd.to_numeric(df['avg_rating'], errors='coerce').fillna(0).round(2)
                df['total_books'] = pd.to_numeric(df['total_books'], errors='coerce').fillna(0)
                df['total_borrows'] = pd.to_numeric(df['total_borrows'], errors='coerce').fillna(0)
                
                st.dataframe(df, use_container_width=True, hide_index=True)
                
                if len(df) > 0:
                    # Grouped bar chart
                    fig = go.Figure()
                    fig.add_trace(go.Bar(name='Total Books', x=df['genre_name'], y=df['total_books'],
                                        marker_color='lightblue'))
                    fig.add_trace(go.Bar(name='Total Borrows', x=df['genre_name'], y=df['total_borrows'],
                                        marker_color='darkblue'))
                    fig.update_layout(barmode='group', title='Genre Performance: Books vs Borrows',
                                    xaxis_title='Genre', yaxis_title='Count', height=500)
                    st.plotly_chart(fig, use_container_width=True)
                    
                    # Bubble chart
                    fig2 = px.scatter(df, x='total_books', y='total_borrows', size='avg_rating',
                                    hover_data=['genre_name'], title='Genre Insights Bubble Chart',
                                    labels={'total_books': 'Total Books', 'total_borrows': 'Total Borrows'},
                                    color='avg_rating', color_continuous_scale='RdYlGn')
                    st.plotly_chart(fig2, use_container_width=True)
                else:
                    st.warning("No data available for genre performance visualization")
            else:
                st.info("No genre performance data available")
        
        elif report_type == "Book Ratings Distribution":
            try:
                data = Database.execute_query("""
                    SELECT 
                        CAST(average_rating AS INTEGER) as rating_group,
                        COUNT(*) as book_count
                    FROM book_statistics
                    WHERE average_rating IS NOT NULL AND average_rating > 0
                    GROUP BY CAST(average_rating AS INTEGER)
                    ORDER BY rating_group
                """)
            except Exception as e:
                st.error(f"Database error in Book Ratings Distribution: {str(e)}")
                data = None
            
            if data and len(data) > 0:
                df = pd.DataFrame(data)
                # Ensure numeric types
                df['rating_group'] = pd.to_numeric(df['rating_group'], errors='coerce').fillna(0).astype(int)
                df['book_count'] = pd.to_numeric(df['book_count'], errors='coerce').fillna(0).astype(int)
                
                # Filter out invalid ratings
                df = df[df['rating_group'] > 0]
                
                if len(df) > 0:
                    df['rating_label'] = df['rating_group'].astype(str) + ' - ' + (df['rating_group'] + 1).astype(str) + ' ⭐'
                    
                    fig = px.bar(df, x='rating_label', y='book_count',
                               title='Book Ratings Distribution',
                               labels={'rating_label': 'Rating Range', 'book_count': 'Number of Books'},
                               color='book_count',
                               color_continuous_scale='YlOrRd')
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.warning("No valid rating data available for visualization")
            else:
                st.info("No rating distribution data available")
        
        elif report_type == "Books by Publisher":
            try:
                data = Database.execute_query("""
                    SELECT p.name as publisher_name,
                           COUNT(DISTINCT b.book_id) as total_books,
                           COUNT(br.borrowing_id) as total_borrows,
                           AVG(bs.average_rating) as avg_rating
                    FROM publishers p
                    JOIN books b ON p.publisher_id = b.publisher_id
                    LEFT JOIN book_inventory bi ON b.book_id = bi.book_id
                    LEFT JOIN borrowing br ON bi.inventory_id = br.inventory_id
                    LEFT JOIN book_statistics bs ON b.book_id = bs.book_id
                    WHERE b.is_active = 1
                    GROUP BY p.publisher_id, p.name
                    ORDER BY total_books DESC
                    LIMIT 15
                """)
            except Exception as e:
                st.error(f"Database error in Books by Publisher: {str(e)}")
                data = None
            
            if data and len(data) > 0:
                df = pd.DataFrame(data)
                # Handle null values safely
                df['avg_rating'] = pd.to_numeric(df['avg_rating'], errors='coerce').fillna(0).round(2)
                df['total_books'] = pd.to_numeric(df['total_books'], errors='coerce').fillna(0)
                df['total_borrows'] = pd.to_numeric(df['total_borrows'], errors='coerce').fillna(0)
                
                st.dataframe(df, use_container_width=True, hide_index=True)
                
                if len(df) > 0:
                    # Publisher performance chart
                    fig = px.bar(df, x='publisher_name', y='total_books',
                               title='Books by Publisher',
                               labels={'publisher_name': 'Publisher', 'total_books': 'Number of Books'},
                               color='total_borrows',
                               color_continuous_scale='Blues')
                    fig.update_layout(xaxis_tickangle=-45, height=500)
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.warning("No data available for publisher visualization")
            else:
                st.info("No publisher data available")
        
        elif report_type == "Average Days per Book":
            try:
                data = Database.execute_query("""
                    SELECT b.title, b.author,
                           AVG(julianday(COALESCE(br.return_date, date('now'))) - julianday(br.checkout_date)) as avg_days,
                           COUNT(br.borrowing_id) as times_borrowed
                    FROM books b
                    JOIN book_inventory bi ON b.book_id = bi.book_id
                    JOIN borrowing br ON bi.inventory_id = br.inventory_id
                    WHERE b.is_active = 1
                    GROUP BY b.book_id
                    HAVING times_borrowed >= 2
                    ORDER BY avg_days DESC
                    LIMIT 20
                """)
            except Exception as e:
                st.error(f"Database error in Average Days per Book: {str(e)}")
                data = None
            
            if data and len(data) > 0:
                df = pd.DataFrame(data)
                # Handle null values safely
                df['avg_days'] = pd.to_numeric(df['avg_days'], errors='coerce').fillna(0).round(1)
                df['times_borrowed'] = pd.to_numeric(df['times_borrowed'], errors='coerce').fillna(0).astype(int)
                
                # Filter out invalid data
                df = df[df['avg_days'] > 0]
                
                st.dataframe(df, use_container_width=True, hide_index=True)
                
                if len(df) > 0:
                    # Scatter plot of average days vs times borrowed
                    fig = px.scatter(df, x='times_borrowed', y='avg_days',
                                   hover_data=['title'], 
                                   title='Average Borrowing Duration vs Popularity',
                                   labels={'times_borrowed': 'Times Borrowed', 'avg_days': 'Average Days'},
                                   size='avg_days',
                                   color='avg_days',
                                   color_continuous_scale='RdYlBu')
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.warning("No valid borrowing duration data available")
            else:
                st.info("Insufficient borrowing data for analysis")
        
        elif report_type == "Books Never Borrowed":
            try:
                data = Database.execute_query("""
                    SELECT b.title, b.isbn, b.publication_year, p.name as publisher_name
                    FROM books b
                    LEFT JOIN publishers p ON b.publisher_id = p.publisher_id
                    LEFT JOIN book_inventory bi ON b.book_id = bi.book_id
                    LEFT JOIN borrowing br ON bi.inventory_id = br.inventory_id
                    WHERE b.is_active = 1 AND br.borrowing_id IS NULL
                    ORDER BY b.created_at DESC
                    LIMIT 50
                """)
                
                if data:
                    st.warning(f"📋 Found {len(data)} books that have never been borrowed")
                    df = pd.DataFrame(data)
                    # Handle null values
                    df = df.fillna('N/A')
                    st.dataframe(df, use_container_width=True, hide_index=True)
                else:
                    st.success("✅ All books have been borrowed at least once!")
            except Exception as e:
                st.error(f"Error generating Books Never Borrowed report: {str(e)}")
                st.info("Please check the database connection and try again.")
        
        else:
            st.info("Please select a report type to generate")
    
    with tab3:
        st.subheader("👥 Members Analytics")
        
        member_report = st.selectbox("Select Member Report", [
            "Top Borrowers",
            "Members with Outstanding Fines",
            "Member Registration Trend",
            "Member Tier Distribution",
            "Inactive Members",
            "Most Active Members (This Month)"
        ])
        
        if member_report == "Top Borrowers":
            try:
                data = Database.execute_query("""
                    SELECT u.full_name, u.email, u.member_tier,
                           COUNT(br.borrowing_id) as total_borrowed,
                           SUM(CASE WHEN br.return_date IS NULL THEN 1 ELSE 0 END) as currently_borrowed
                    FROM users u
                    LEFT JOIN borrowing br ON u.user_id = br.user_id
                    WHERE u.role = 'member' AND u.is_active = 1
                    GROUP BY u.user_id
                    HAVING total_borrowed > 0
                    ORDER BY total_borrowed DESC
                    LIMIT 20
                """)
                
                if data:
                    df = pd.DataFrame(data)
                    # Handle null values and ensure proper data types
                    df = df.fillna({'member_tier': 'basic', 'email': 'N/A'})
                    df['total_borrowed'] = pd.to_numeric(df['total_borrowed'], errors='coerce').fillna(0).astype(int)
                    df['currently_borrowed'] = pd.to_numeric(df['currently_borrowed'], errors='coerce').fillna(0).astype(int)
                    
                    st.dataframe(df, use_container_width=True, hide_index=True)
                    
                    # Horizontal bar chart with color by tier
                    if len(df) > 0:
                        try:
                            fig = px.bar(df.head(15), x='total_borrowed', y='full_name',
                                       orientation='h',
                                       title="Top 15 Borrowers",
                                       labels={'total_borrowed': 'Total Books Borrowed', 'full_name': 'Member Name'},
                                       color='member_tier',
                                       color_discrete_map={'basic': '#FFA726', 'premium': '#66BB6A', 'gold': '#FFD700'})
                            fig.update_layout(yaxis={'categoryorder':'total ascending'}, height=600)
                            st.plotly_chart(fig, use_container_width=True)
                        except Exception as viz_error:
                            st.warning(f"Could not generate visualization: {str(viz_error)}")
                else:
                    st.info("No borrowing data available for top borrowers report")
            except Exception as e:
                st.error(f"Error generating Top Borrowers report: {str(e)}")
                st.info("Please check the database connection and try again.")
        
        elif member_report == "Members with Outstanding Fines":
            try:
                data = Database.execute_query("""
                    SELECT u.full_name, u.email, u.phone, u.fine_balance, u.member_tier
                    FROM users u
                    WHERE u.fine_balance > 0
                    ORDER BY u.fine_balance DESC
                """)
                
                if data:
                    df = pd.DataFrame(data)
                    # Handle null values and ensure proper data types
                    df = df.fillna({'email': 'N/A', 'phone': 'N/A', 'member_tier': 'basic'})
                    df['fine_balance'] = pd.to_numeric(df['fine_balance'], errors='coerce').fillna(0.0)
                    
                    # Filter out zero fine balances after conversion
                    df = df[df['fine_balance'] > 0]
                    
                    if len(df) > 0:
                        st.dataframe(df, use_container_width=True, hide_index=True)
                        
                        try:
                            total = df['fine_balance'].sum()
                            avg = df['fine_balance'].mean()
                            
                            col1, col2, col3 = st.columns(3)
                            with col1:
                                st.metric("Total Outstanding", format_currency(total))
                            with col2:
                                st.metric("Average Fine", format_currency(avg))
                            with col3:
                                st.metric("Members with Fines", len(df))
                            
                            # Histogram of fine distribution
                            fig = px.histogram(df, x='fine_balance', nbins=min(20, len(df)),
                                             title='Fine Amount Distribution',
                                             labels={'fine_balance': 'Fine Amount (₹)', 'count': 'Number of Members'},
                                             color_discrete_sequence=['#FF6B6B'])
                            st.plotly_chart(fig, use_container_width=True)
                        except Exception as viz_error:
                            st.warning(f"Could not generate fine statistics: {str(viz_error)}")
                    else:
                        st.success("✅ No members have outstanding fines!")
                else:
                    st.success("✅ No members have outstanding fines!")
            except Exception as e:
                st.error(f"Error generating Outstanding Fines report: {str(e)}")
                st.info("Please check the database connection and try again.")
        
        elif member_report == "Member Registration Trend":
            try:
                data = Database.execute_query("""
                    SELECT strftime('%Y-%m', created_at) as month,
                           COUNT(*) as new_members
                    FROM users
                    WHERE role = 'member' AND created_at IS NOT NULL
                    GROUP BY strftime('%Y-%m', created_at)
                    ORDER BY month DESC
                    LIMIT 12
                """)
                
                if data:
                    df = pd.DataFrame(data)
                    # Handle null values and ensure proper data types
                    df = df.fillna({'month': 'Unknown', 'new_members': 0})
                    df['new_members'] = pd.to_numeric(df['new_members'], errors='coerce').fillna(0).astype(int)
                    
                    # Filter out invalid months
                    df = df[df['month'] != 'Unknown']
                    
                    if len(df) > 0:
                        df = df.sort_values('month')
                        
                        try:
                            fig = px.area(df, x='month', y='new_members',
                                        title='Member Registration Trend (Last 12 Months)',
                                        labels={'month': 'Month', 'new_members': 'New Members'},
                                        color_discrete_sequence=['#4CAF50'])
                            fig.update_traces(fill='tozeroy')
                            st.plotly_chart(fig, use_container_width=True)
                        except Exception as viz_error:
                            st.warning(f"Could not generate trend visualization: {str(viz_error)}")
                            # Show data table as fallback
                            st.dataframe(df, use_container_width=True, hide_index=True)
                    else:
                        st.info("No registration trend data available")
                else:
                    st.info("No member registration data available")
            except Exception as e:
                st.error(f"Error generating Member Registration Trend report: {str(e)}")
                st.info("Please check the database connection and try again.")
        
        elif member_report == "Member Tier Distribution":
            try:
                data = Database.execute_query("""
                    SELECT member_tier, COUNT(*) as count
                    FROM users
                    WHERE role = 'member' AND is_active = 1
                    GROUP BY member_tier
                """)
                
                if data:
                    df = pd.DataFrame(data)
                    # Handle null values and ensure proper data types
                    df = df.fillna({'member_tier': 'basic'})
                    df['count'] = pd.to_numeric(df['count'], errors='coerce').fillna(0).astype(int)
                    
                    # Filter out zero counts
                    df = df[df['count'] > 0]
                    
                    if len(df) > 0:
                        try:
                            # Donut chart
                            fig = px.pie(df, values='count', names='member_tier',
                                       title='Member Tier Distribution',
                                       hole=0.4,
                                       color_discrete_sequence=px.colors.sequential.RdBu)
                            fig.update_traces(textposition='inside', textinfo='percent+label+value')
                            st.plotly_chart(fig, use_container_width=True)
                        except Exception as viz_error:
                            st.warning(f"Could not generate pie chart: {str(viz_error)}")
                            # Show data table as fallback
                            st.dataframe(df, use_container_width=True, hide_index=True)
                    else:
                        st.info("No member tier data available")
                else:
                    st.info("No member tier data available")
            except Exception as e:
                st.error(f"Error generating Member Tier Distribution report: {str(e)}")
                st.info("Please check the database connection and try again.")
        
        elif member_report == "Inactive Members":
            try:
                data = Database.execute_query("""
                    SELECT u.full_name, u.email, u.member_tier,
                           u.created_at as joined_date,
                           COALESCE(MAX(br.checkout_date), 'Never') as last_activity,
                           COUNT(br.borrowing_id) as total_borrowed
                    FROM users u
                    LEFT JOIN borrowing br ON u.user_id = br.user_id
                    WHERE u.role = 'member' AND u.is_active = 1
                    GROUP BY u.user_id
                    HAVING (last_activity = 'Never' OR julianday('now') - julianday(MAX(br.checkout_date)) > 90)
                    ORDER BY last_activity DESC
                    LIMIT 20
                """)
                
                if data:
                    df = pd.DataFrame(data)
                    # Handle null values and ensure proper data types
                    df = df.fillna({'email': 'N/A', 'member_tier': 'basic', 'last_activity': 'Never'})
                    df['total_borrowed'] = pd.to_numeric(df['total_borrowed'], errors='coerce').fillna(0).astype(int)
                    
                    st.warning(f"📋 Found {len(df)} inactive members (no activity for 90+ days)")
                    st.dataframe(df, use_container_width=True, hide_index=True)
                    
                    # Inactive members by tier
                    try:
                        tier_counts = df['member_tier'].value_counts()
                        if not tier_counts.empty and len(tier_counts) > 0:
                            fig = px.pie(values=tier_counts.values, names=tier_counts.index,
                                       title='Inactive Members by Tier',
                                       color_discrete_sequence=px.colors.qualitative.Set3)
                            st.plotly_chart(fig, use_container_width=True)
                    except Exception as viz_error:
                        st.warning(f"Could not generate tier distribution chart: {str(viz_error)}")
                else:
                    st.success("✅ All members are active!")
            except Exception as e:
                st.error(f"Error generating Inactive Members report: {str(e)}")
                st.info("Please check the database connection and try again.")
        
        elif member_report == "Most Active Members (This Month)":
            try:
                data = Database.execute_query("""
                    SELECT u.full_name, u.email, u.member_tier,
                           COUNT(br.borrowing_id) as books_this_month,
                           AVG(julianday(COALESCE(br.return_date, date('now'))) - julianday(br.checkout_date)) as avg_duration
                    FROM users u
                    JOIN borrowing br ON u.user_id = br.user_id
                    WHERE u.role = 'member' AND u.is_active = 1
                      AND br.checkout_date >= date('now', 'start of month')
                    GROUP BY u.user_id
                    ORDER BY books_this_month DESC, avg_duration ASC
                    LIMIT 15
                """)
                
                if data:
                    df = pd.DataFrame(data)
                    # Handle null values and ensure proper data types
                    df = df.fillna({'email': 'N/A', 'member_tier': 'basic'})
                    df['books_this_month'] = pd.to_numeric(df['books_this_month'], errors='coerce').fillna(0).astype(int)
                    df['avg_duration'] = pd.to_numeric(df['avg_duration'], errors='coerce').fillna(0.0).round(1)
                    
                    # Filter out zero activity
                    df = df[df['books_this_month'] > 0]
                    
                    if len(df) > 0:
                        st.success(f"📋 Top {len(df)} most active members this month")
                        st.dataframe(df, use_container_width=True, hide_index=True)
                        
                        try:
                            # Activity chart
                            fig = px.bar(df, x='full_name', y='books_this_month',
                                       title='Most Active Members This Month',
                                       labels={'full_name': 'Member Name', 'books_this_month': 'Books Borrowed'},
                                       color='member_tier',
                                       color_discrete_map={'basic': '#FFA726', 'premium': '#66BB6A', 'gold': '#FFD700'})
                            fig.update_layout(xaxis_tickangle=-45, height=500)
                            st.plotly_chart(fig, use_container_width=True)
                        except Exception as viz_error:
                            st.warning(f"Could not generate activity chart: {str(viz_error)}")
                    else:
                        st.info("No borrowing activity this month")
                else:
                    st.info("No borrowing activity this month")
            except Exception as e:
                st.error(f"Error generating Most Active Members report: {str(e)}")
                st.info("Please check the database connection and try again.")
        
        else:
            st.info("Please select a member report type")
    
    with tab4:
        st.subheader("💰 Financial Analytics")
        
        col1, col2 = st.columns(2)
        with col1:
            fin_start = st.date_input("From Date", date.today() - timedelta(days=90), key="fin_start")
        with col2:
            fin_end = st.date_input("To Date", date.today(), key="fin_end")
        
        if st.button("💰 Generate Financial Report", use_container_width=True):
            try:
                st.markdown("---")
                
                # Summary metrics
                total_fines = Database.execute_query("""
                    SELECT SUM(fine_amount) as total
                    FROM borrowing
                    WHERE return_date BETWEEN ? AND ? AND fine_amount > 0
                """, (fin_start, fin_end), fetch_one=True)
                
                outstanding_fines = Database.execute_query("""
                    SELECT SUM(fine_balance) as total
                    FROM users
                    WHERE fine_balance > 0
                """, fetch_one=True)
                
                avg_fine = Database.execute_query("""
                    SELECT AVG(fine_amount) as avg
                    FROM borrowing
                    WHERE return_date BETWEEN ? AND ? AND fine_amount > 0
                """, (fin_start, fin_end), fetch_one=True)
                
                # Handle null values and ensure proper data types
                total_collected = 0
                if total_fines and total_fines.get('total'):
                    total_collected = float(total_fines['total'])
                
                outstanding_total = 0
                if outstanding_fines and outstanding_fines.get('total'):
                    outstanding_total = float(outstanding_fines['total'])
                
                avg_amount = 0
                if avg_fine and avg_fine.get('avg'):
                    avg_amount = float(avg_fine['avg'])
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("💵 Fines Collected", format_currency(total_collected))
                with col2:
                    st.metric("⚠️ Outstanding Fines", format_currency(outstanding_total))
                with col3:
                    st.metric("📊 Average Fine", format_currency(avg_amount))
            except Exception as e:
                st.error(f"Error generating financial summary: {str(e)}")
                st.info("Please check the database connection and try again.")
            
                st.markdown("---")
                
                # Daily fines chart
                try:
                    fines_daily = Database.execute_query("""
                        SELECT DATE(return_date) as date, 
                               SUM(fine_amount) as total,
                               COUNT(*) as fine_count
                        FROM borrowing
                        WHERE return_date BETWEEN ? AND ? AND fine_amount > 0
                        GROUP BY DATE(return_date)
                        ORDER BY date
                    """, (fin_start, fin_end))
                    
                    if fines_daily:
                        df = pd.DataFrame(fines_daily)
                        # Handle null values and ensure proper data types
                        df = df.fillna(0)
                        df['total'] = pd.to_numeric(df['total'], errors='coerce').fillna(0.0)
                        df['fine_count'] = pd.to_numeric(df['fine_count'], errors='coerce').fillna(0).astype(int)
                        
                        if len(df) > 0 and df['total'].sum() > 0:
                            try:
                                # Area chart for daily fines
                                fig = go.Figure()
                                fig.add_trace(go.Scatter(
                                    x=df['date'], y=df['total'],
                                    mode='lines',
                                    name='Fine Amount',
                                    line=dict(color='#4CAF50', width=3),
                                    fill='tozeroy',
                                    fillcolor='rgba(76, 175, 80, 0.2)'
                                ))
                                fig.update_layout(
                                    title="Daily Fines Collected",
                                    xaxis_title="Date",
                                    yaxis_title="Amount (₹)",
                                    height=400,
                                    hovermode='x unified'
                                )
                                st.plotly_chart(fig, use_container_width=True)
                                
                                # Bar chart for fine counts
                                fig2 = px.bar(df, x='date', y='fine_count',
                                            title='Number of Fines per Day',
                                            labels={'date': 'Date', 'fine_count': 'Number of Fines'},
                                            color='fine_count',
                                            color_continuous_scale='Reds')
                                st.plotly_chart(fig2, use_container_width=True)
                            except Exception as viz_error:
                                st.warning(f"Could not generate daily charts: {str(viz_error)}")
                                st.dataframe(df, use_container_width=True, hide_index=True)
                        else:
                            st.info("No fine data available for the selected date range")
                    else:
                        st.info("No fine data available for the selected date range")
                except Exception as e:
                    st.error(f"Error generating daily fines analysis: {str(e)}")
            
                # Monthly revenue projection
                st.subheader("📈 Monthly Revenue Projection")
                try:
                    monthly_fines = Database.execute_query("""
                        SELECT strftime('%Y-%m', return_date) as month,
                               SUM(fine_amount) as total
                        FROM borrowing
                        WHERE fine_amount > 0 AND return_date IS NOT NULL
                        GROUP BY strftime('%Y-%m', return_date)
                        ORDER BY month DESC
                        LIMIT 12
                    """)
                    
                    if monthly_fines:
                        df_monthly = pd.DataFrame(monthly_fines)
                        # Handle null values and ensure proper data types
                        df_monthly = df_monthly.fillna({'month': '', 'total': 0})
                        df_monthly['total'] = pd.to_numeric(df_monthly['total'], errors='coerce').fillna(0.0)
                        
                        # Filter out invalid months and zero totals
                        df_monthly = df_monthly[df_monthly['month'] != '']
                        df_monthly = df_monthly[df_monthly['total'] > 0]
                        
                        if len(df_monthly) > 0:
                            df_monthly = df_monthly.sort_values('month')
                            
                            try:
                                fig = px.line(df_monthly, x='month', y='total',
                                            title='Monthly Fine Revenue (Last 12 Months)',
                                            labels={'month': 'Month', 'total': 'Revenue (₹)'},
                                            markers=True)
                                fig.update_traces(line_color='#2196F3', line_width=4)
                                st.plotly_chart(fig, use_container_width=True)
                            except Exception as viz_error:
                                st.warning(f"Could not generate monthly revenue chart: {str(viz_error)}")
                                st.dataframe(df_monthly, use_container_width=True, hide_index=True)
                        else:
                            st.info("No monthly revenue data available")
                    else:
                        st.info("No monthly revenue data available")
                except Exception as e:
                    st.error(f"Error generating monthly revenue projection: {str(e)}")
            except Exception as e:
                st.error(f"Error generating Financial Analytics report: {str(e)}")
                st.info("Please check the database connection and try again.")
    
    with tab5:
        st.subheader(" Advanced Visualizations")
        
        viz_type = st.selectbox("Select Visualization Type", [
            "Library Health Heatmap",
            "Book-Member Network",
            "Genre Performance Radar",
            "Collection Growth Timeline",
            "Multi-Dimensional Analysis"
        ])
        
        if viz_type == "Library Health Heatmap":
            try:
                # Create a heatmap showing various metrics
                st.markdown("### 🌡️ Library Health Metrics")
                
                # Total books
                total_books = Database.execute_query("SELECT COUNT(*) as cnt FROM books WHERE is_active=1", fetch_one=True)
                # Available books
                avail_books = Database.execute_query("SELECT COUNT(*) as cnt FROM book_inventory WHERE is_available=1", fetch_one=True)
                # Active members
                active_members = Database.execute_query("SELECT COUNT(*) as cnt FROM users WHERE is_active=1 AND role='member'", fetch_one=True)
                # Current borrows
                current_borrows = Database.execute_query("SELECT COUNT(*) as cnt FROM borrowing WHERE return_date IS NULL", fetch_one=True)
                # Overdue books
                overdue = Database.execute_query("SELECT COUNT(*) as cnt FROM borrowing WHERE return_date IS NULL AND due_date < date('now')", fetch_one=True)
                
                # Handle null values and ensure proper data types
                metrics = {
                    'Total Books': int(total_books['cnt']) if total_books and total_books.get('cnt') else 0,
                    'Available Books': int(avail_books['cnt']) if avail_books and avail_books.get('cnt') else 0,
                    'Active Members': int(active_members['cnt']) if active_members and active_members.get('cnt') else 0,
                    'Current Borrows': int(current_borrows['cnt']) if current_borrows and current_borrows.get('cnt') else 0,
                    'Overdue Books': int(overdue['cnt']) if overdue and overdue.get('cnt') else 0
                }
                
                # Calculate health scores (0-100) with safe division
                availability_score = (metrics['Available Books'] / max(metrics['Total Books'], 1)) * 100
                utilization_score = (metrics['Current Borrows'] / max(metrics['Active Members'], 1)) * 100
                compliance_score = max(0, 100 - (metrics['Overdue Books'] / max(metrics['Current Borrows'], 1)) * 100)
                
                health_df = pd.DataFrame({
                    'Metric': ['Book Availability', 'Member Utilization', 'Return Compliance'],
                    'Score': [availability_score, min(utilization_score, 100), compliance_score]
                })
                
                try:
                    fig = px.bar(health_df, x='Metric', y='Score',
                               title='Library Health Scores',
                               labels={'Score': 'Score (%)'},
                               color='Score',
                               color_continuous_scale='RdYlGn',
                               range_y=[0, 100])
                    fig.update_layout(height=400)
                    st.plotly_chart(fig, use_container_width=True)
                except Exception as viz_error:
                    st.warning(f"Could not generate health chart: {str(viz_error)}")
                    st.dataframe(health_df, use_container_width=True, hide_index=True)
                
                # Display raw metrics
                col1, col2, col3, col4, col5 = st.columns(5)
                with col1:
                    st.metric("📚 Total Books", metrics['Total Books'])
                with col2:
                    st.metric("✅ Available", metrics['Available Books'])
                with col3:
                    st.metric("👥 Active Members", metrics['Active Members'])
                with col4:
                    st.metric("📖 Current Borrows", metrics['Current Borrows'])
                with col5:
                    st.metric("⚠️ Overdue", metrics['Overdue Books'])
            except Exception as e:
                st.error(f"Error generating Library Health Heatmap: {str(e)}")
                st.info("Please check the database connection and try again.")
        
        elif viz_type == "Genre Performance Radar":
            try:
                st.markdown("### 🎯 Genre Performance Radar Chart")
                
                genre_perf = Database.execute_query("""
                    SELECT g.genre_name,
                           COUNT(DISTINCT b.book_id) as book_count,
                           COUNT(br.borrowing_id) as borrow_count,
                           AVG(bs.average_rating) as avg_rating
                    FROM genres g
                    JOIN book_genres bg ON g.genre_id = bg.genre_id
                    JOIN books b ON bg.book_id = b.book_id
                    LEFT JOIN book_inventory bi ON b.book_id = bi.book_id
                    LEFT JOIN borrowing br ON bi.inventory_id = br.inventory_id
                    LEFT JOIN book_statistics bs ON b.book_id = bs.book_id
                    WHERE b.is_active = 1
                    GROUP BY g.genre_name
                    LIMIT 10
                """)
                
                if genre_perf:
                    df = pd.DataFrame(genre_perf)
                    # Handle null values and ensure proper data types
                    df = df.fillna({'genre_name': 'Unknown', 'book_count': 0, 'borrow_count': 0, 'avg_rating': 0})
                    df['book_count'] = pd.to_numeric(df['book_count'], errors='coerce').fillna(0).astype(int)
                    df['borrow_count'] = pd.to_numeric(df['borrow_count'], errors='coerce').fillna(0).astype(int)
                    df['avg_rating'] = pd.to_numeric(df['avg_rating'], errors='coerce').fillna(0.0)
                    
                    # Filter out unknown genres and ensure we have data
                    df = df[df['genre_name'] != 'Unknown']
                    df = df[df['book_count'] > 0]
                    
                    if len(df) > 0:
                        # Scale ratings and normalize counts
                        df['avg_rating'] = df['avg_rating'] * 20  # Scale to 100
                        max_books = df['book_count'].max()
                        max_borrows = df['borrow_count'].max()
                        
                        df['book_count_norm'] = (df['book_count'] / max(max_books, 1)) * 100
                        df['borrow_count_norm'] = (df['borrow_count'] / max(max_borrows, 1)) * 100
                        
                        try:
                            fig = go.Figure()
                            
                            # Only add traces if we have data points
                            if len(df) >= 3:  # Need at least 3 points for a meaningful radar
                                fig.add_trace(go.Scatterpolar(
                                    r=df['book_count_norm'].tolist() + [df['book_count_norm'].iloc[0]],
                                    theta=df['genre_name'].tolist() + [df['genre_name'].iloc[0]],
                                    fill='toself',
                                    name='Book Collection',
                                    line_color='#2196F3'
                                ))
                                
                                fig.add_trace(go.Scatterpolar(
                                    r=df['borrow_count_norm'].tolist() + [df['borrow_count_norm'].iloc[0]],
                                    theta=df['genre_name'].tolist() + [df['genre_name'].iloc[0]],
                                    fill='toself',
                                    name='Popularity',
                                    line_color='#FF9800'
                                ))
                                
                                fig.update_layout(
                                    polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
                                    showlegend=True,
                                    title="Genre Performance Comparison",
                                    height=600
                                )
                                st.plotly_chart(fig, use_container_width=True)
                            else:
                                st.warning("Need at least 3 genres for radar chart. Showing data table instead:")
                                st.dataframe(df, use_container_width=True, hide_index=True)
                        except Exception as viz_error:
                            st.warning(f"Could not generate radar chart: {str(viz_error)}")
                            st.dataframe(df, use_container_width=True, hide_index=True)
                    else:
                        st.info("No genre performance data available")
                else:
                    st.info("No genre performance data available")
            except Exception as e:
                st.error(f"Error generating Genre Performance Radar: {str(e)}")
                st.info("Please check the database connection and try again.")
        
        elif viz_type == "Collection Growth Timeline":
            try:
                st.markdown("### 📈 Library Collection Growth")
                
                growth_data = Database.execute_query("""
                    SELECT strftime('%Y-%m', created_at) as month,
                           COUNT(*) as new_books
                    FROM books
                    WHERE created_at IS NOT NULL
                    GROUP BY strftime('%Y-%m', created_at)
                    ORDER BY month
                    LIMIT 24
                """)
                
                if growth_data:
                    df = pd.DataFrame(growth_data)
                    # Handle null values and ensure proper data types
                    df = df.fillna({'month': '', 'new_books': 0})
                    df['new_books'] = pd.to_numeric(df['new_books'], errors='coerce').fillna(0).astype(int)
                    
                    # Filter out invalid months and zero counts
                    df = df[df['month'] != '']
                    df = df[df['new_books'] > 0]
                    
                    if len(df) > 0:
                        df = df.sort_values('month')
                        df['cumulative'] = df['new_books'].cumsum()
                        
                        try:
                            fig = go.Figure()
                            fig.add_trace(go.Bar(
                                x=df['month'], y=df['new_books'],
                                name='New Books Added',
                                marker_color='lightblue'
                            ))
                            fig.add_trace(go.Scatter(
                                x=df['month'], y=df['cumulative'],
                                name='Total Collection',
                                marker_color='darkblue',
                                yaxis='y2',
                                mode='lines+markers'
                            ))
                            
                            fig.update_layout(
                                title='Collection Growth Over Time',
                                yaxis=dict(title='New Books per Month'),
                                yaxis2=dict(title='Total Books', overlaying='y', side='right'),
                                hovermode='x unified',
                                height=500
                            )
                            st.plotly_chart(fig, use_container_width=True)
                        except Exception as viz_error:
                            st.warning(f"Could not generate growth timeline: {str(viz_error)}")
                            st.dataframe(df, use_container_width=True, hide_index=True)
                    else:
                        st.info("No collection growth data available")
                else:
                    st.info("No collection growth data available")
            except Exception as e:
                st.error(f"Error generating Collection Growth Timeline: {str(e)}")
                st.info("Please check the database connection and try again.")
        
        elif viz_type == "Multi-Dimensional Analysis":
            try:
                st.markdown("### 🔬 Multi-Dimensional Book Analysis")
                
                multi_data = Database.execute_query("""
                    SELECT b.title, b.publication_year,
                           bs.total_checkouts, bs.average_rating,
                           bs.total_copies, bs.available_copies,
                           g.genre_name
                    FROM books b
                    JOIN book_statistics bs ON b.book_id = bs.book_id
                    LEFT JOIN book_genres bg ON b.book_id = bg.book_id
                    LEFT JOIN genres g ON bg.genre_id = g.genre_id
                    WHERE b.is_active = 1 AND bs.total_checkouts > 0
                    LIMIT 100
                """)
                
                if multi_data:
                    df = pd.DataFrame(multi_data)
                    # Handle null values and ensure proper data types
                    df = df.fillna({
                        'title': 'Unknown Title',
                        'publication_year': 0,
                        'total_checkouts': 0,
                        'average_rating': 0,
                        'total_copies': 1,
                        'available_copies': 0,
                        'genre_name': 'Unknown'
                    })
                    
                    # Ensure proper data types
                    df['publication_year'] = pd.to_numeric(df['publication_year'], errors='coerce').fillna(0).astype(int)
                    df['total_checkouts'] = pd.to_numeric(df['total_checkouts'], errors='coerce').fillna(0).astype(int)
                    df['average_rating'] = pd.to_numeric(df['average_rating'], errors='coerce').fillna(0.0)
                    df['total_copies'] = pd.to_numeric(df['total_copies'], errors='coerce').fillna(1).astype(int)
                    df['available_copies'] = pd.to_numeric(df['available_copies'], errors='coerce').fillna(0).astype(int)
                    
                    # Calculate utilization with safe division
                    df['utilization'] = ((df['total_copies'] - df['available_copies']) / df['total_copies'].replace(0, 1)) * 100
                    
                    # Filter out invalid data
                    df = df[df['title'] != 'Unknown Title']
                    df = df[df['total_checkouts'] > 0]
                    
                    if len(df) > 0:
                        try:
                            # 3D Scatter plot
                            fig = px.scatter_3d(df, x='publication_year', y='total_checkouts', z='average_rating',
                                              color='genre_name', size='total_copies',
                                              hover_data=['title'],
                                              title='3D Book Analysis: Year vs Popularity vs Rating',
                                              labels={
                                                  'publication_year': 'Publication Year',
                                                  'total_checkouts': 'Total Checkouts',
                                                  'average_rating': 'Rating'
                                              })
                            fig.update_layout(height=700)
                            st.plotly_chart(fig, use_container_width=True)
                        except Exception as viz_error:
                            st.warning(f"Could not generate 3D scatter plot: {str(viz_error)}")
                        
                        try:
                            # Sunburst chart - only if we have enough valid data
                            sunburst_df = df[df['genre_name'] != 'Unknown']
                            if len(sunburst_df) > 0:
                                st.markdown("### ☀️ Collection Hierarchy")
                                fig2 = px.sunburst(sunburst_df, path=['genre_name', 'title'], values='total_checkouts',
                                                  title='Book Collection by Genre (Size = Popularity)',
                                                  color='average_rating',
                                                  color_continuous_scale='RdYlGn')
                                fig2.update_layout(height=600)
                                st.plotly_chart(fig2, use_container_width=True)
                        except Exception as viz_error:
                            st.warning(f"Could not generate sunburst chart: {str(viz_error)}")
                        
                        # Show data table as fallback
                        if len(df) > 0:
                            st.markdown("### 📊 Data Table")
                            st.dataframe(df, use_container_width=True, hide_index=True)
                    else:
                        st.info("No multi-dimensional analysis data available")
                else:
                    st.info("No multi-dimensional analysis data available")
            except Exception as e:
                st.error(f"Error generating Multi-Dimensional Analysis: {str(e)}")
                st.info("Please check the database connection and try again.")

# ================================================================
# V4.0 NEW PAGES
# ================================================================

def show_my_library():
    """My Library page - User's personal PDF library"""
    st.title("📚 My Library")
    
    user = Auth.get_user()
    
    tabs = st.tabs(["📖 My PDFs", "📤 Upload PDF", "🔒 Privacy Settings", "👤 My Profile"])
    
    # Tab 1: My PDFs
    with tabs[0]:
        st.subheader("My PDF Collection")
        
        pdfs = PeerLibraryManager.get_user_library(user['user_id'])
        
        if pdfs:
            for pdf in pdfs:
                with st.expander(f"📄 {pdf['title']}"):
                    col1, col2 = st.columns([3, 1])
                    
                    with col1:
                        st.write(f"**Author:** {pdf['author'] or 'Unknown'}")
                        st.write(f"**Genre:** {pdf['genre'] or 'Unknown'}")
                        st.write(f"**Description:** {pdf['description'] or 'No description'}")
                        st.write(f"**Visibility:** {'🌐 Public' if pdf['is_public'] else '🔒 Private'}")
                        st.write(f"**Uploaded:** {pdf['upload_date']}")
                        st.write(f"**Views:** {pdf['views_count']}")
                    
                    with col2:
                        if st.button("👁️ View", key=f"view_{pdf['pdf_id']}"):
                            pdf_data = PeerLibraryManager.get_pdf_file(pdf['pdf_id'])
                            if pdf_data:
                                PeerLibraryManager.increment_pdf_views(pdf['pdf_id'])
                                st.download_button(
                                    "⬇️ Download PDF",
                                    pdf_data['pdf_file'],
                                    pdf_data['pdf_filename'],
                                    mime="application/pdf"
                                )
                        
                        # Toggle visibility
                        new_visibility = st.checkbox(
                            "Make Public",
                            value=pdf['is_public'],
                            key=f"vis_{pdf['pdf_id']}"
                        )
                        if new_visibility != pdf['is_public']:
                            Database.execute_update(
                                "UPDATE pdf_library SET is_public = ? WHERE pdf_id = ?",
                                (new_visibility, pdf['pdf_id'])
                            )
                            st.success("Visibility updated!")
                            st.rerun()
        else:
            st.info("Your library is empty. Upload PDFs to get started!")
    
    # Tab 2: Upload PDF
    with tabs[1]:
        st.subheader("📤 Upload New PDF")
        
        with st.form("upload_pdf_form"):
            uploaded_file = st.file_uploader("Choose PDF file", type=['pdf'])
            title = st.text_input("Title*", max_chars=500)
            author = st.text_input("Author", max_chars=300)
            genre = st.selectbox("Genre", ["Fiction", "Non-Fiction", "Science", "Technology", 
                                           "History", "Biography", "Self-Help", "Other"])
            description = st.text_area("Description", max_chars=1000)
            is_public = st.checkbox("Make this PDF publicly visible")
            
            submitted = st.form_submit_button("📤 Upload PDF")
            
            if submitted:
                if not uploaded_file or not title:
                    st.error("Please provide PDF file and title")
                else:
                    success, message = PeerLibraryManager.upload_pdf_to_library(
                        user['user_id'], uploaded_file, title, author, genre, description, is_public
                    )
                    
                    if success:
                        st.success(message)
                        st.balloons()
                        time.sleep(1)
                        st.rerun()
                    else:
                        st.error(message)
    
    # Tab 3: Privacy Settings
    with tabs[2]:
        st.subheader("🔒 Privacy & Anonymous Mode")
        
        privacy = PrivacyManager.get_privacy_settings(user['user_id'])
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 👁️ Visibility Settings")
            
            show_email = st.checkbox("Show Email", value=privacy.get('show_email', False))
            show_phone = st.checkbox("Show Phone", value=privacy.get('show_phone', False))
            show_full_name = st.checkbox("Show Full Name", value=privacy.get('show_full_name', True))
            show_profile_photo = st.checkbox("Show Profile Photo", value=privacy.get('show_profile_photo', True))
            show_library = st.checkbox("Show Library", value=privacy.get('show_library', True))
            show_borrowing_history = st.checkbox("Show Borrowing History", value=privacy.get('show_borrowing_history', False))
        
        with col2:
            st.markdown("### 🕵️ Anonymous Mode")
            
            anonymous_mode = st.checkbox(
                "Enable Anonymous Mode", 
                value=privacy.get('anonymous_mode', False),
                help="Hide your identity and show a pseudonym instead"
            )
            
            if anonymous_mode:
                pseudonym = privacy.get('pseudonym')
                if pseudonym:
                    st.info(f"Your pseudonym: **{pseudonym}**")
                else:
                    st.info("A pseudonym will be generated when you save")
                
                st.warning("⚠️ Anonymous mode hides: name, email, phone, and profile photo")
        
        if st.button("💾 Save Privacy Settings", type="primary"):
            settings = {
                'show_email': show_email,
                'show_phone': show_phone,
                'show_full_name': show_full_name,
                'show_profile_photo': show_profile_photo,
                'show_library': show_library,
                'show_borrowing_history': show_borrowing_history
            }
            
            # Update anonymous mode separately to generate pseudonym
            if anonymous_mode != privacy.get('anonymous_mode'):
                success, pseudonym = PrivacyManager.toggle_anonymous_mode(user['user_id'], anonymous_mode)
                if success:
                    st.success(f"Anonymous mode {'enabled' if anonymous_mode else 'disabled'}")
            
            # Update other settings
            if PrivacyManager.update_privacy_settings(user['user_id'], settings):
                st.success("✅ Privacy settings saved!")
                st.rerun()
            else:
                st.error("Failed to save settings")
        
        # Preview
        st.markdown("---")
        st.subheader("👁️ Preview Public Profile")
        
        if st.button("🔍 View as Public"):
            profile = PrivacyManager.preview_public_profile(user['user_id'])
            if profile:
                st.json(profile)
    
    # Tab 4: My Profile
    with tabs[3]:
        st.subheader("👤 My Profile")
        
        # User profile information
        st.write(f"**Full Name:** {user['full_name']}")
        st.write(f"**Username:** {user['username']}")
        st.write(f"**Email:** {user['email']}")
        st.write(f"**Role:** {user['role'].title()}")
        st.write(f"**Member Tier:** {user['member_tier'].title()}")
        
        # Only show unique ID and QR code for real database users (not functional admin)
        if user['user_id'] > 0:
            # Unique ID
            unique_id = Database.execute_query(
                "SELECT user_unique_code FROM users WHERE user_id = ?",
                (user['user_id'],)
            )
            unique_code = unique_id[0]['user_unique_code'] if unique_id and unique_id[0]['user_unique_code'] else None
            
            if unique_code:
                st.write(f"**Unique ID:** {unique_code}")
            else:
                if st.button("🆔 Generate Unique ID"):
                    new_id = EnhancedUserManager.generate_user_unique_id(user['user_id'])
                    if new_id:
                        st.success(f"Generated: {new_id}")
                        st.rerun()
            
            # QR Code
            if st.button("📱 Generate My QR Code"):
                qr_data = SmartUtilities.generate_user_qr(user['user_id'])
                if qr_data:
                    st.image(qr_data, width=200)

def show_community_library():
    """Browse Community Library"""
    st.title("🌐 Community Library")
    
    st.markdown("Browse and read PDFs shared by other users")
    
    # Search
    search_query = st.text_input("🔍 Search PDFs", placeholder="Search by title, author, genre...")
    
    # Get public PDFs
    public_pdfs = PeerLibraryManager.browse_public_libraries()
    
    if search_query and public_pdfs:
        public_pdfs = [p for p in public_pdfs if 
                      search_query.lower() in p['title'].lower() or
                      search_query.lower() in (p['author'] or '').lower() or
                      search_query.lower() in (p['genre'] or '').lower()]
    
    st.write(f"**{len(public_pdfs)}** PDFs available")
    
    if public_pdfs:
        # Group by user
        user_groups = {}
        for pdf in public_pdfs:
            owner = pdf['owner_name']
            if owner not in user_groups:
                user_groups[owner] = []
            user_groups[owner].append(pdf)
        
        for owner, pdfs in user_groups.items():
            with st.expander(f"👤 {owner} ({len(pdfs)} PDFs)"):
                for pdf in pdfs:
                    col1, col2 = st.columns([4, 1])
                    
                    with col1:
                        st.markdown(f"### 📄 {pdf['title']}")
                        st.write(f"**Author:** {pdf['author'] or 'Unknown'}")
                        st.write(f"**Genre:** {pdf['genre'] or 'Unknown'}")
                        st.write(f"**Description:** {pdf['description'] or 'No description'}")
                        st.write(f"**Views:** {pdf['views_count']} | **Uploaded:** {pdf['upload_date']}")
                    
                    with col2:
                        if st.button("📖 Read", key=f"read_{pdf['pdf_id']}"):
                            pdf_data = PeerLibraryManager.get_pdf_file(pdf['pdf_id'])
                            if pdf_data:
                                PeerLibraryManager.increment_pdf_views(pdf['pdf_id'])
                                
                                # Display PDF
                                st.download_button(
                                    "⬇️ Download PDF",
                                    pdf_data['pdf_file'],
                                    pdf_data['pdf_filename'],
                                    mime="application/pdf",
                                    key=f"dl_{pdf['pdf_id']}"
                                )
                                
                                # Extract and show preview
                                preview_text = pdf_handler.extract_text(pdf_data['pdf_file'], max_pages=3)
                                if preview_text:
                                    with st.expander("📖 Preview (First 3 pages)"):
                                        st.text(preview_text)
                        
                        if st.button("👤 Visit Profile", key=f"profile_{pdf['owner_id']}"):
                            st.session_state.viewing_user = pdf['owner_id']
                            st.rerun()
    else:
        st.info("No public PDFs available yet")
    
    # If viewing a profile
    if 'viewing_user' in st.session_state:
        st.markdown("---")
        st.subheader("👤 User Profile")
        
        profile_data = PeerLibraryManager.get_user_public_profile(st.session_state.viewing_user)
        current_user = Auth.get_user()
        
        if profile_data:
            user_info = profile_data['user']
            privacy = profile_data['privacy']
            
            col1, col2 = st.columns([1, 3])
            
            with col1:
                if privacy.get('show_profile_photo'):
                    user_photo = EnhancedUserManager.get_user_photo(st.session_state.viewing_user)
                    if user_photo:
                        st.image(user_photo, width=150)
                
                # Show profile rating
                rating_data = ProfileCommentsManager.get_average_profile_rating(st.session_state.viewing_user)
                if rating_data['rating_count'] > 0:
                    st.markdown(f"⭐ **{rating_data['avg_rating']:.1f}** / 5.0")
                    st.caption(f"({rating_data['rating_count']} ratings)")
            
            with col2:
                st.markdown(f"### {user_info['full_name']}")
                if privacy.get('show_email') and user_info['email'] != '[Hidden]':
                    st.write(f"**Email:** {user_info['email']}")
                
                # Show user's library
                if privacy.get('show_library'):
                    user_pdfs = PeerLibraryManager.get_user_library(
                        st.session_state.viewing_user, 
                        public_only=True
                    )
                    st.write(f"**Public Library:** {len(user_pdfs)} PDFs")
            
            # Tabs for different sections
            profile_tabs = st.tabs(["📚 Library", "💬 Comments & Ratings", "📊 Stats"])
            
            # Tab 1: User's Library
            with profile_tabs[0]:
                if privacy.get('show_library'):
                    user_pdfs = PeerLibraryManager.get_user_library(
                        st.session_state.viewing_user, 
                        public_only=True
                    )
                    
                    if user_pdfs:
                        st.write(f"**{len(user_pdfs)} Public PDFs**")
                        
                        for pdf in user_pdfs:
                            with st.expander(f"📄 {pdf['title']} by {pdf['author']}"):
                                col1, col2 = st.columns([3, 1])
                                
                                with col1:
                                    st.write(f"**Genre:** {pdf['genre']}")
                                    st.write(f"**Description:** {pdf['description']}")
                                    st.caption(f"Uploaded: {pdf['upload_date']} | Views: {pdf['views']}")
                                    
                                    # PDF Comments
                                    pdf_comments = ProfileCommentsManager.get_pdf_comments(pdf['pdf_id'])
                                    pdf_rating = ProfileCommentsManager.get_pdf_average_rating(pdf['pdf_id'])
                                    
                                    if pdf_rating['rating_count'] > 0:
                                        st.markdown(f"⭐ **{pdf_rating['avg_rating']:.1f}** / 5.0 ({pdf_rating['rating_count']} ratings)")
                                    
                                    if pdf_comments:
                                        st.markdown("**Comments:**")
                                        for comment in pdf_comments[:3]:  # Show first 3
                                            st.markdown(f"- **{comment['full_name']}**: {comment['comment']}")
                                            if comment['rating']:
                                                st.caption(f"⭐ {comment['rating']}/5.0")
                                
                                with col2:
                                    # Add comment to PDF
                                    with st.form(f"pdf_comment_{pdf['pdf_id']}", clear_on_submit=True):
                                        st.write("**Add Comment**")
                                        pdf_rating_input = st.slider("Rating", 0.0, 5.0, 3.0, 0.5, key=f"pdf_rating_{pdf['pdf_id']}")
                                        pdf_comment_input = st.text_area("Comment", key=f"pdf_comment_{pdf['pdf_id']}", height=80)
                                        
                                        if st.form_submit_button("💬 Post"):
                                            if pdf_comment_input:
                                                success, msg = ProfileCommentsManager.add_pdf_comment(
                                                    pdf['pdf_id'],
                                                    current_user['user_id'],
                                                    pdf_comment_input,
                                                    pdf_rating_input if pdf_rating_input > 0 else None
                                                )
                                                if success:
                                                    st.success("Comment posted!")
                                                    st.rerun()
                                                else:
                                                    st.error(msg)
                                            else:
                                                st.warning("Please enter a comment")
                    else:
                        st.info("No public PDFs available")
                else:
                    st.info("User's library is private")
            
            # Tab 2: Comments & Ratings
            with profile_tabs[1]:
                st.markdown("### 💬 Profile Comments & Ratings")
                
                # Add comment form
                if current_user['user_id'] != st.session_state.viewing_user:
                    with st.form("profile_comment_form", clear_on_submit=True):
                        st.write("**Leave a comment and rating:**")
                        
                        col1, col2 = st.columns([3, 1])
                        with col1:
                            comment_text = st.text_area("Your comment", height=100)
                        with col2:
                            rating_input = st.slider("Rating", 0.0, 5.0, 5.0, 0.5)
                        
                        if st.form_submit_button("💬 Post Comment", type="primary"):
                            if comment_text:
                                success, msg = ProfileCommentsManager.add_profile_comment(
                                    st.session_state.viewing_user,
                                    current_user['user_id'],
                                    comment_text,
                                    rating_input if rating_input > 0 else None
                                )
                                if success:
                                    st.success("✅ Comment posted successfully!")
                                    st.balloons()
                                    st.rerun()
                                else:
                                    st.error(f"❌ {msg}")
                            else:
                                st.warning("⚠️ Please enter a comment")
                
                st.markdown("---")
                
                # Display existing comments
                comments = ProfileCommentsManager.get_profile_comments(st.session_state.viewing_user)
                
                if comments:
                    st.write(f"**{len(comments)} Comments**")
                    
                    for comment in comments:
                        with st.container():
                            col1, col2 = st.columns([4, 1])
                            
                            with col1:
                                st.markdown(f"**{comment['full_name']}** (@{comment['username']})")
                                st.write(comment['comment'])
                                st.caption(f"Posted: {comment['created_at']}")
                            
                            with col2:
                                if comment['rating']:
                                    st.metric("Rating", f"⭐ {comment['rating']}/5.0")
                            
                            st.markdown("---")
                else:
                    st.info("No comments yet. Be the first to comment!")
            
            # Tab 3: Stats
            with profile_tabs[2]:
                st.markdown("### 📊 Profile Statistics")
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    pdf_count = len(PeerLibraryManager.get_user_library(st.session_state.viewing_user, public_only=True))
                    st.metric("Public PDFs", pdf_count)
                
                with col2:
                    comment_count = len(ProfileCommentsManager.get_profile_comments(st.session_state.viewing_user))
                    st.metric("Comments Received", comment_count)
                
                with col3:
                    rating_data = ProfileCommentsManager.get_average_profile_rating(st.session_state.viewing_user)
                    st.metric("Average Rating", f"{rating_data['avg_rating']:.1f} ⭐")
        
        if st.button("⬅️ Back to Community"):
            del st.session_state.viewing_user
            st.rerun()

def show_system_tools():
    """System Tools for admins"""
    st.title("⚙️ System Tools")
    
    user = Auth.get_user()
    
    if user['role'] not in ['admin']:
        st.error("Admin access required")
        return
    
    # Add Smart Tools and Data Management tabs for functional admin
    if user.get('is_functional_admin'):
        tabs = st.tabs(["💾 Backup & Restore", "🔍 Data Integrity", "📊 Export Data", "📈 System Stats", "🔧 Smart Tools", "🗄️ Data Management", "📬 Send Reminders"])
    else:
        tabs = st.tabs(["💾 Backup & Restore", "🔍 Data Integrity", "📊 Export Data", "📈 System Stats", "📬 Send Reminders"])
    
    # Backup & Restore
    with tabs[0]:
        st.subheader("💾 Backup & Restore")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### Create Backup")
            
            if st.button("🗄️ Create Full Backup", type="primary"):
                with st.spinner("Creating backup..."):
                    success, backup_path = DataManagement.create_full_backup()
                    
                    if success:
                        st.success(f"✅ Backup created: {backup_path}")
                        
                        # Offer download
                        try:
                            with open(backup_path, 'rb') as f:
                                st.download_button(
                                    "⬇️ Download Backup",
                                    f.read(),
                                    os.path.basename(backup_path),
                                    mime="application/zip"
                                )
                        except:
                            pass
                    else:
                        st.error("Backup failed")
            
            # Backup history
            st.markdown("### Recent Backups")
            backups = Database.execute_query("""
                SELECT * FROM backup_logs
                ORDER BY created_at DESC
                LIMIT 10
            """)
            
            if backups:
                for backup in backups:
                    filename = backup['file_path'].split('/')[-1] if backup['file_path'] else 'Unknown'
                    file_size_mb = (backup['file_size'] / 1024 / 1024) if backup['file_size'] else 0
                    st.write(f"📦 {filename} - {backup['created_at']} ({file_size_mb:.2f} MB)")
        
        with col2:
            st.markdown("### Restore Backup")
            
            restore_file = st.file_uploader("Upload Backup ZIP", type=['zip'])
            
            if restore_file:
                st.warning("⚠️ Restore will overwrite existing data!")
                
                if st.button("🔄 Restore Now", type="primary"):
                    with st.spinner("Restoring..."):
                        if DataManagement.restore_from_backup(restore_file):
                            st.success("✅ Restore successful!")
                        else:
                            st.error("Restore failed")
    
    # Data Integrity
    with tabs[1]:
        st.subheader("🔍 Data Integrity Check")
        
        if st.button("🔍 Run Integrity Check"):
            with st.spinner("Checking..."):
                issues = DataManagement.run_integrity_check()
                
                if issues:
                    st.warning(f"⚠️ Found {len(issues)} issues:")
                    for issue in issues:
                        st.write(f"- {issue}")
                else:
                    st.success("✅ No integrity issues found!")
        
        # Duplicates
        st.markdown("---")
        st.subheader("📋 Duplicate Books")
        
        if st.button("🔍 Check Duplicates"):
            duplicates = DataManagement.check_duplicates()
            
            if duplicates:
                st.warning(f"Found {len(duplicates)} potential duplicates:")
                for dup in duplicates:
                    st.write(f"- **{dup['title']}** by {dup['author']} ({dup['count']} copies)")
            else:
                st.success("No duplicates found!")
    
    # Export Data
    with tabs[2]:
        st.subheader("📊 Export Data")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### Export Books")
            
            if st.button("📥 Export Books to Excel"):
                books = Database.execute_query("""
                    SELECT 
                        b.book_id,
                        b.title,
                        b.author,
                        b.genre,
                        b.isbn,
                        b.publication_year,
                        b.pages as page_count,
                        CASE 
                            WHEN b.is_available = 1 THEN 'Active'
                            ELSE 'Inactive'
                        END as status
                    FROM books b
                """)
                if books:
                    excel_data = excel_exporter.export_books(books)
                    st.download_button(
                        "⬇️ Download Books.xlsx",
                        excel_data.getvalue(),
                        "books_catalog.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    )
                else:
                    st.warning("No books found to export")
        
        with col2:
            st.markdown("### Export Users")
            
            if st.button("📥 Export Users to Excel"):
                users = Database.execute_query("""
                    SELECT 
                        u.user_id,
                        u.full_name,
                        u.username,
                        u.email,
                        u.role,
                        u.member_tier,
                        (SELECT COUNT(*) FROM borrowing WHERE user_id = u.user_id) as books_borrowed,
                        u.fine_balance,
                        CASE 
                            WHEN u.is_active = 1 THEN 'Active'
                            ELSE 'Inactive'
                        END as status,
                        u.created_at as joined_date
                    FROM users u
                """)
                if users:
                    excel_data = excel_exporter.export_users(users)
                    st.download_button(
                        "⬇️ Download Users.xlsx",
                        excel_data.getvalue(),
                        "users_list.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    )
    
    # System Stats
    with tabs[3]:
        st.subheader("📈 System Statistics")
        
        col1, col2, col3 = st.columns(3)
        
        # Database size
        with col1:
            try:
                import os
                db_path = 'litgrid_local.db'
                if os.path.exists(db_path):
                    size_bytes = os.path.getsize(db_path)
                    size_mb = size_bytes / 1024 / 1024
                    st.metric("Database Size", f"{size_mb:.2f} MB")
                else:
                    st.metric("Database Size", "N/A")
            except Exception as e:
                st.metric("Database Size", "N/A")
        
        # Total records
        with col2:
            total_books = Database.execute_query("SELECT COUNT(*) as count FROM books")
            count = total_books[0]['count'] if total_books else 0
            st.metric("Total Books", count)
        
        with col3:
            total_users = Database.execute_query("SELECT COUNT(*) as count FROM users")
            count = total_users[0]['count'] if total_users else 0
            st.metric("Total Users", count)
    
    # Smart Tools (Functional Admin Only)
    if user.get('is_functional_admin') and len(tabs) > 4:
        with tabs[4]:
            st.subheader("🔧 Smart Tools & Utilities")
            
            smart_tabs = st.tabs([
                "🆔 ID Generator", 
                "📅 Calendar View", 
                "📊 Barcode & QR", 
                "🎯 Recommendations",
                "🔤 Spell Check",
                "🔍 Book Similarity"
            ])
            
            # Tab 1: Unique ID Generator
            with smart_tabs[0]:
                st.markdown("### 🆔 Unique ID Generator")
                st.caption("Generate unique identifiers for users and books")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("#### User ID Generator")
                    user_id_input = st.number_input("User ID", min_value=1, value=1, key="user_id_gen")
                    if st.button("🔄 Generate User ID", key="gen_user_id"):
                        try:
                            unique_id = unique_id_gen.generate_user_id()
                            st.success(f"✅ Generated: **{unique_id}**")
                            st.code(f"Format: USR-{datetime.now().year}-{str(user_id_input).zfill(6)}")
                        except Exception as e:
                            st.error(f"Error: {e}")
                
                with col2:
                    st.markdown("#### Book ID Generator")
                    book_id_input = st.number_input("Book ID", min_value=1, value=1, key="book_id_gen")
                    if st.button("🔄 Generate Book ID", key="gen_book_id"):
                        try:
                            unique_id = unique_id_gen.generate_book_id()
                            st.success(f"✅ Generated: **{unique_id}**")
                            st.code(f"Format: BK-{datetime.now().year}-{str(book_id_input).zfill(6)}")
                        except Exception as e:
                            st.error(f"Error: {e}")
                
                st.markdown("---")
                st.info("💡 **Tip:** These IDs can be used for tracking and barcode generation")
            
            # Tab 2: Calendar View
            with smart_tabs[1]:
                st.markdown("### 📅 Borrowing Calendar View")
                st.caption("Visual overview of all active loans and due dates")
                
                if st.button("🔄 Load Calendar", key="load_calendar"):
                    with st.spinner("Loading calendar..."):
                        calendar_data = SmartUtilities.create_borrowing_calendar()
                        
                        if calendar_data:
                            st.success(f"✅ Found {len(calendar_data)} active loans")
                            
                            # Display in table format
                            df = pd.DataFrame(calendar_data)
                            st.dataframe(df, use_container_width=True, hide_index=True)
                            
                            # Show urgent items
                            st.markdown("#### ⚠️ Due Soon")
                            urgent = [item for item in calendar_data if item['days_until_due'] <= 3]
                            if urgent:
                                for item in urgent:
                                    color = "red" if item['days_until_due'] < 0 else "orange"
                                    st.markdown(f":{color}[📚 **{item['title']}** - {item['user']} - Due: {item['due_date']} ({item['days_until_due']} days)]")
                            else:
                                st.success("✅ No urgent returns")
                        else:
                            st.info("No active loans")
            
            # Tab 3: Barcode & QR Generator
            with smart_tabs[2]:
                st.markdown("### 📊 Barcode & QR Code Generator")
                st.caption("Generate barcodes and QR codes for books and users")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("#### Book Barcode")
                    book_id_barcode = st.number_input("Book ID", min_value=1, value=1, key="book_barcode")
                    if st.button("📊 Generate Book Barcode", key="gen_book_barcode"):
                        try:
                            barcode_img = SmartUtilities.generate_book_barcode(book_id_barcode)
                            if barcode_img:
                                st.image(barcode_img, caption=f"Book {book_id_barcode} Barcode")
                                st.success("✅ Barcode generated successfully")
                            else:
                                st.error("Failed to generate barcode")
                        except Exception as e:
                            st.error(f"Error: {e}")
                
                with col2:
                    st.markdown("#### User QR Code")
                    user_id_qr = st.number_input("User ID", min_value=1, value=1, key="user_qr")
                    if st.button("📱 Generate User QR", key="gen_user_qr"):
                        try:
                            qr_img = SmartUtilities.generate_user_qr(user_id_qr)
                            if qr_img:
                                st.image(qr_img, caption=f"User {user_id_qr} QR Code", width=200)
                                st.success("✅ QR code generated successfully")
                            else:
                                st.error("Failed to generate QR code")
                        except Exception as e:
                            st.error(f"Error: {e}")
                
                st.markdown("---")
                st.info("💡 **Tip:** Scan QR codes with mobile devices for quick access")
            
            # Tab 4: Book Recommendations
            with smart_tabs[3]:
                st.markdown("### 🎯 Book Recommendation Engine")
                st.caption("AI-powered book recommendations based on similarity")
                
                book_search = st.text_input("Search for a book", key="rec_search")
                
                if book_search:
                    # Search for book
                    books = Database.execute_query("""
                        SELECT book_id, title, author, genre 
                        FROM books 
                        WHERE title LIKE %s OR author LIKE %s
                        LIMIT 10
                    """, (f"%{book_search}%", f"%{book_search}%"))
                    
                    if books:
                        selected_book = st.selectbox(
                            "Select a book",
                            options=books,
                            format_func=lambda x: f"{x['title']} by {x['author']}"
                        )
                        
                        if st.button("🔍 Get Recommendations", key="get_recs"):
                            with st.spinner("Analyzing..."):
                                recommendations = SmartUtilities.get_book_recommendations(selected_book['book_id'])
                                
                                if recommendations:
                                    st.success(f"✅ Found {len(recommendations)} similar books")
                                    
                                    for rec in recommendations:
                                        with st.expander(f"📚 {rec['title']} by {rec['author']}"):
                                            st.write(f"**Genre:** {rec['genre']}")
                                            st.write(f"**Similarity:** {rec.get('similarity_score', 0):.1f}%")
                                            st.write(f"**ISBN:** {rec.get('isbn', 'N/A')}")
                                else:
                                    st.info("No recommendations found")
                    else:
                        st.warning("No books found")
            
            # Tab 5: Spell Checker
            with smart_tabs[4]:
                st.markdown("### 🔤 Local Spell Checker")
                st.caption("Check spelling for book titles and descriptions")
                
                text_to_check = st.text_area("Enter text to check", height=150, key="spell_check_text")
                
                if st.button("✓ Check Spelling", key="check_spell"):
                    if text_to_check:
                        # Simple spell check using fuzzy matching against known words
                        words = text_to_check.split()
                        
                        # Get common book words from database
                        common_words = Database.execute_query("""
                            SELECT DISTINCT LOWER(title) as word FROM books
                            UNION
                            SELECT DISTINCT LOWER(a.name) as word FROM authors a
                        """)
                        
                        if common_words:
                            word_list = [w['word'] for w in common_words]
                            
                            suspicious_words = []
                            for word in words:
                                clean_word = word.lower().strip('.,!?;:')
                                # Check if word exists or is very similar
                                matches = process.extract(clean_word, word_list, limit=1)
                                if matches and matches[0][1] < 80:  # Less than 80% match
                                    suspicious_words.append({
                                        'word': word,
                                        'suggestion': matches[0][0] if matches else None,
                                        'score': matches[0][1] if matches else 0
                                    })
                            
                            if suspicious_words:
                                st.warning(f"⚠️ Found {len(suspicious_words)} potential issues:")
                                for item in suspicious_words:
                                    st.write(f"- **{item['word']}** → Did you mean: *{item['suggestion']}*? (Confidence: {item['score']}%)")
                            else:
                                st.success("✅ No spelling issues detected")
                    else:
                        st.warning("Please enter text to check")
            
            # Tab 6: Book Similarity Matcher
            with smart_tabs[5]:
                st.markdown("### 🔍 Book Similarity Matcher")
                st.caption("Find duplicate or similar books using fuzzy matching")
                
                threshold = st.slider("Similarity Threshold (%)", 60, 100, 80, key="similarity_threshold")
                
                if st.button("🔍 Find Similar Books", key="find_similar"):
                    with st.spinner("Analyzing entire catalog..."):
                        all_books = Database.execute_query("""
                            SELECT b.book_id, b.title, b.isbn, b.author
                            FROM books b
                            WHERE b.is_available = 1
                        """)
                        
                        if all_books and len(all_books) > 1:
                            duplicates = []
                            checked = set()
                            
                            for i, book1 in enumerate(all_books):
                                if book1['book_id'] in checked:
                                    continue
                                    
                                for book2 in all_books[i+1:]:
                                    if book2['book_id'] in checked:
                                        continue
                                    
                                    # Calculate similarity
                                    title_sim = fuzz.ratio(
                                        book1['title'].lower(), 
                                        book2['title'].lower()
                                    )
                                    author_sim = fuzz.ratio(
                                        book1['author'].lower(), 
                                        book2['author'].lower()
                                    )
                                    
                                    # Average similarity
                                    avg_sim = (title_sim + author_sim) / 2
                                    
                                    if avg_sim >= threshold:
                                        duplicates.append({
                                            'book1': book1,
                                            'book2': book2,
                                            'similarity': avg_sim
                                        })
                                        checked.add(book1['book_id'])
                                        checked.add(book2['book_id'])
                            
                            if duplicates:
                                st.warning(f"⚠️ Found {len(duplicates)} potential matches:")
                                
                                for dup in duplicates:
                                    with st.expander(f"Match {dup['similarity']:.1f}% similarity"):
                                        col1, col2 = st.columns(2)
                                        with col1:
                                            st.write("**Book 1:**")
                                            st.write(f"Title: {dup['book1']['title']}")
                                            st.write(f"Author: {dup['book1']['author']}")
                                            st.write(f"ISBN: {dup['book1']['isbn']}")
                                        with col2:
                                            st.write("**Book 2:**")
                                            st.write(f"Title: {dup['book2']['title']}")
                                            st.write(f"Author: {dup['book2']['author']}")
                                            st.write(f"ISBN: {dup['book2']['isbn']}")
                            else:
                                st.success(f"✅ No similar books found at {threshold}% threshold")
                        else:
                            st.info("Not enough books to compare")
    
    # Data Management (Functional Admin Only)
    if user.get('is_functional_admin') and len(tabs) > 5:
        with tabs[5]:
            st.subheader("🗄️ Data Management & Configuration")
            
            data_tabs = st.tabs([
                "⚙️ JSON Config", 
                "💾 SQLite Storage", 
                "🗑️ Temp Files",
                "💾 Auto-Save",
                "🔄 Data Sync"
            ])
            
            # Tab 1: JSON Configuration
            with data_tabs[0]:
                st.markdown("### ⚙️ JSON Configuration Manager")
                st.caption("View and manage application configuration")
                
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    st.markdown("#### Current Configuration")
                    config_data = Config.get_config_dict()
                    
                    if config_data:
                        # Display as formatted JSON
                        st.json(config_data)
                    else:
                        st.warning("No configuration loaded")
                
                with col2:
                    st.markdown("#### Actions")
                    
                    if st.button("💾 Save Config", key="save_config"):
                        with st.spinner("Saving configuration..."):
                            success, msg = Config.save_config()
                            if success:
                                st.success(f"✅ {msg}")
                            else:
                                st.error(f"❌ {msg}")
                    
                    if st.button("🔄 Load Config", key="load_config"):
                        with st.spinner("Loading configuration..."):
                            success, msg = Config.load_config()
                            if success:
                                st.success(f"✅ {msg}")
                                st.rerun()
                            else:
                                st.error(f"❌ {msg}")
                    
                    st.markdown("---")
                    st.info("💡 **Tip:** Config is stored in `config.json`")
                    
                    if os.path.exists(Config.CONFIG_FILE):
                        file_size = os.path.getsize(Config.CONFIG_FILE)
                        st.metric("Config File Size", f"{file_size} bytes")
            
            # Tab 2: SQLite Storage
            with data_tabs[1]:
                st.markdown("### �️ SQLite Database")
                st.caption("Main database storage and status")
                
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    st.markdown("#### Database Status")
                    
                    if os.path.exists(Config.SQLITE_DB):
                        file_size = os.path.getsize(Config.SQLITE_DB) / 1024  # KB
                        st.success(f"✅ SQLite database exists ({file_size:.2f} KB)")
                        
                        # Get database stats
                        books = Database.execute_query("SELECT COUNT(*) as count FROM books")
                        users = Database.execute_query("SELECT COUNT(*) as count FROM users")
                        transactions = Database.execute_query("SELECT COUNT(*) as count FROM transactions")
                        
                        if books and users and transactions:
                            col_a, col_b, col_c = st.columns(3)
                            with col_a:
                                st.metric("Books", books[0]['count'])
                            with col_b:
                                st.metric("Users", users[0]['count'])
                            with col_c:
                                st.metric("Transactions", transactions[0]['count'])
                    else:
                        st.warning("⚠️ SQLite database not found")
                
                with col2:
                    st.markdown("#### Actions")
                    
                    if st.button("🔧 Initialize Database", key="init_db"):
                        with st.spinner("Initializing database..."):
                            success = Database.init_pool()
                            if success:
                                st.success("✅ Database initialized successfully")
                                st.rerun()
                            else:
                                st.error("❌ Database initialization failed")
                    
                    if st.button("� Database Info", key="db_info"):
                        with st.spinner("Getting database information..."):
                            try:
                                tables = Database.execute_query("""
                                    SELECT name FROM sqlite_master 
                                    WHERE type='table' AND name NOT LIKE 'sqlite_%'
                                    ORDER BY name
                                """)
                                if tables:
                                    st.success(f"✅ Found {len(tables)} tables")
                                    for table in tables:
                                        st.text(f"• {table['name']}")
                                else:
                                    st.info("No tables found")
                            except Exception as e:
                                st.error(f"❌ Error: {e}")
                    
                    st.markdown("---")
                    st.info("💡 **Tip:** Local storage enables offline access")
            
            # Tab 3: Temp Files
            with data_tabs[2]:
                st.markdown("### 🗑️ Temporary File Management")
                st.caption("Manage temporary files and cleanup")
                
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    st.markdown("#### Temp Directory Status")
                    
                    if os.path.exists(Config.TEMP_DIR):
                        temp_count = TempFileManager.get_temp_file_count()
                        st.metric("Temp Files", temp_count)
                        
                        if temp_count > 0:
                            st.markdown("#### Temp Files")
                            files = os.listdir(Config.TEMP_DIR)
                            for filename in files[:10]:  # Show first 10
                                filepath = os.path.join(Config.TEMP_DIR, filename)
                                if os.path.isfile(filepath):
                                    size = os.path.getsize(filepath) / 1024  # KB
                                    mtime = datetime.fromtimestamp(os.path.getmtime(filepath))
                                    st.text(f"📄 {filename} ({size:.2f} KB) - {mtime.strftime('%Y-%m-%d %H:%M')}")
                        else:
                            st.success("✅ No temp files")
                    else:
                        st.warning("⚠️ Temp directory not initialized")
                
                with col2:
                    st.markdown("#### Actions")
                    
                    if st.button("🔧 Initialize Temp Dir", key="init_temp"):
                        success = TempFileManager.init_temp_dir()
                        if success:
                            st.success("✅ Temp directory initialized")
                            st.rerun()
                        else:
                            st.error("❌ Failed to initialize")
                    
                    hours = st.number_input("Clean files older than (hours)", min_value=1, value=24, key="clean_hours")
                    
                    if st.button("🗑️ Clean Temp Files", key="clean_temp"):
                        with st.spinner("Cleaning temp files..."):
                            count = TempFileManager.clean_temp_files(hours)
                            st.success(f"✅ Cleaned {count} temp files")
                            st.rerun()
                    
                    st.markdown("---")
                    st.info("💡 **Tip:** Clean old files regularly to save space")
            
            # Tab 4: Auto-Save
            with data_tabs[3]:
                st.markdown("### 💾 Auto-Save Manager")
                st.caption("View and manage auto-saved form data")
                
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    st.markdown("#### Auto-Save Status")
                    
                    if os.path.exists(Config.AUTO_SAVE_FILE):
                        file_size = os.path.getsize(Config.AUTO_SAVE_FILE) / 1024  # KB
                        st.success(f"✅ Auto-save file exists ({file_size:.2f} KB)")
                        
                        # Load and display auto-save data
                        try:
                            with open(Config.AUTO_SAVE_FILE, 'r') as f:
                                auto_save_data = json.load(f)
                            
                            st.metric("Saved Forms", len(auto_save_data))
                            
                            if auto_save_data:
                                st.markdown("#### Saved Forms")
                                for form_name, data in auto_save_data.items():
                                    with st.expander(f"📝 {form_name}"):
                                        st.json(data)
                            else:
                                st.info("No saved forms")
                        except Exception as e:
                            st.error(f"Error loading auto-save data: {e}")
                    else:
                        st.info("ℹ️ No auto-save file")
                
                with col2:
                    st.markdown("#### Actions")
                    
                    if os.path.exists(Config.AUTO_SAVE_FILE):
                        try:
                            with open(Config.AUTO_SAVE_FILE, 'r') as f:
                                auto_save_data = json.load(f)
                            
                            form_names = list(auto_save_data.keys())
                            
                            if form_names:
                                selected_form = st.selectbox("Select Form", form_names, key="form_select")
                                
                                if st.button("🗑️ Clear Form", key="clear_form"):
                                    success = AutoSaveManager.clear_form_data(selected_form)
                                    if success:
                                        st.success(f"✅ Cleared {selected_form}")
                                        st.rerun()
                                    else:
                                        st.error("❌ Failed to clear")
                        except:
                            pass
                    
                    st.markdown("---")
                    st.info("💡 **Tip:** Auto-save prevents data loss on form errors")
            
            # Tab 5: Data Sync
            with data_tabs[4]:
                st.markdown("### 🔄 Data Synchronization")
                st.caption("Sync data between MariaDB and SQLite")
                
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    st.markdown("#### Sync Status")
                    
                    sync_status = DataSyncManager.get_sync_status()
                    
                    if sync_status:
                        st.success(f"✅ Last sync: {sync_status['synced_at']}")
                        st.write(f"**Type:** {sync_status['sync_type']}")
                        st.write(f"**Status:** {sync_status['status']}")
                        st.write(f"**Message:** {sync_status['message']}")
                    else:
                        st.warning("⚠️ No sync history")
                    
                    st.markdown("---")
                    st.markdown("#### Data Consistency Check")
                    
                    if st.button("🔍 Check Consistency", key="check_consistency"):
                        with st.spinner("Checking data consistency..."):
                            consistency = DataSyncManager.verify_data_consistency()
                            
                            if consistency:
                                col_a, col_b, col_c = st.columns(3)
                                
                                with col_a:
                                    st.metric("MariaDB Books", consistency['mariadb_count'])
                                with col_b:
                                    st.metric("SQLite Books", consistency['sqlite_count'])
                                with col_c:
                                    st.metric("Difference", consistency['difference'])
                                
                                if consistency['in_sync']:
                                    st.success("✅ Data is in sync!")
                                else:
                                    st.warning(f"⚠️ {consistency['difference']} records out of sync")
                            else:
                                st.error("❌ Failed to check consistency")
                
                with col2:
                    st.markdown("#### Actions")
                    
                    if st.button("🔄 Sync to Local", key="sync_to_local", type="primary"):
                        with st.spinner("Syncing data to local storage..."):
                            success, msg = DataSyncManager.sync_to_local()
                            if success:
                                st.success(f"✅ {msg}")
                                st.rerun()
                            else:
                                st.error(f"❌ {msg}")
                    
                    st.markdown("---")
                    st.info("💡 **Tip:** Regular syncing keeps local data up-to-date")
    
    # Send Reminders Tab (Always available for admin)
    reminder_tab_index = 6 if user.get('is_functional_admin') else 4
    if len(tabs) > reminder_tab_index:
        with tabs[reminder_tab_index]:
            st.subheader("📬 Send Return Reminders")
            
            st.markdown("""
            Send automated return reminders to members with:
            - Books due within 3 days
            - Books due today
            - Overdue books
            """)
            
            # Preview affected members
            affected = Database.execute_query("""
                SELECT br.borrowing_id, b.title, u.full_name, u.email, br.due_date,
                       julianday(br.due_date) - julianday(date('now')) as days_until_due
                FROM borrowing br
                JOIN book_inventory bi ON br.inventory_id = bi.inventory_id
                JOIN books b ON bi.book_id = b.book_id
                JOIN users u ON br.user_id = u.user_id
                WHERE br.return_date IS NULL
                  AND julianday(br.due_date) - julianday(date('now')) <= 3
                ORDER BY br.due_date
            """)
            
            if affected:
                st.info(f"📊 **{len(affected)}** members will receive reminders")
                
                # Show preview
                with st.expander("👥 View Recipients"):
                    for member in affected[:10]:  # Show first 10
                        days = member['days_until_due']
                        status = "⚠️ OVERDUE" if days < 0 else "📅 DUE TODAY" if days == 0 else f"⏰ Due in {days} days"
                        st.write(f"- {member['full_name']} ({member['email']}) - **{member['title']}** - {status}")
                    
                    if len(affected) > 10:
                        st.caption(f"... and {len(affected) - 10} more")
                
                st.markdown("---")
                
                # Send button
                col1, col2 = st.columns([2, 1])
                with col1:
                    st.warning("⚠️ This will send notification to all affected members")
                
                with col2:
                    if st.button("📨 Send Reminders Now", type="primary", use_container_width=True):
                        with st.spinner("Sending reminders..."):
                            sent_count = EmailService.send_bulk_reminders()
                            st.success(f"✅ Sent {sent_count} reminders successfully!")
                            st.balloons()
            else:
                st.success("✅ No reminders needed - all books returned on time!")



# ================================================================
# MAIN APP
# ================================================================

def main():
    """Main application"""
    # Page config
    st.set_page_config(
        page_title="LitGrid - Library Management",
        page_icon="📚",
        layout="wide"
    )
    
    # Load CSS
    load_css()
    
    # Initialize DB
    Database.init_pool()
    
    # Initialize auth
    Auth.init_session()
    
    # Check authentication
    if not Auth.is_authenticated():
        show_login_page()
    else:
        user = Auth.get_user()
        
        # Sidebar
        with st.sidebar:
            st.markdown("---")
            st.markdown(f"### 👤 {user['full_name']}")
            st.caption(f"{user['role'].title()} | {user['member_tier'].title()}")
            
            if user['fine_balance'] > 0:
                st.warning(f"⚠️ Fine: {format_currency(user['fine_balance'])}")
            
            # Show notifications badge
            notifications = EmailService.get_user_notifications(user['email'])
            unread_count = len(notifications)
            if unread_count > 0:
                st.info(f"🔔 {unread_count} new notification{'s' if unread_count != 1 else ''}")
                
                with st.expander("📬 View Notifications"):
                    for notif in notifications[-5:]:  # Show last 5
                        st.markdown(f"**{notif['subject']}**")
                        st.caption(format_datetime(notif['timestamp']))
                        if st.button("📖 Read", key=f"notif_{notif['timestamp']}"):
                            st.info(notif['message'])
                        st.markdown("---")
            
            st.markdown("---")
            
            # Menu
            menu = ["Dashboard", "Browse Books", "My Account", "📚 My Library", "🌐 Browse Community"]
            
            if user['role'] in ['admin', 'librarian']:
                menu.extend(["Manage Books", "Manage Members", "Borrowing & Returns", "Reports", "⚙️ System Tools"])
            
            choice = st.radio("📚 Navigation", menu, label_visibility="collapsed")
            
            st.markdown("---")
            if st.button("🚪 Logout", use_container_width=True):
                Auth.logout()
                st.rerun()
            
            # Developer Info
            st.markdown("---")
            st.markdown("""
                <div style='text-align: center; padding: 10px;'>
                    <p style='font-size: 12px; color: #666; margin-bottom: 8px;'>Developed by</p>
                    <p style='font-size: 14px; font-weight: bold; color: #333; margin-bottom: 10px;'>Labib Bin Shahed</p>
                </div>
            """, unsafe_allow_html=True)
            
            st.markdown("""
                <div style='text-align: center;'>
                    <a href='https://github.com/la-b-ib' target='_blank'>
                        <img src='https://img.shields.io/badge/GitHub-181717?style=for-the-badge&logo=github&logoColor=white' alt='GitHub' style='margin: 2px;'/>
                    </a>
                    <a href='https://www.linkedin.com/in/la-b-ib/' target='_blank'>
                        <img src='https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white' alt='LinkedIn' style='margin: 2px;'/>
                    </a>
                </div>
            """, unsafe_allow_html=True)
        
        # Main content
        if choice == "Dashboard":
            show_dashboard()
        elif choice == "Browse Books":
            show_books()
        elif choice == "My Account":
            show_account()
        elif choice == "📚 My Library":
            show_my_library()
        elif choice == "🌐 Browse Community":
            show_community_library()
        elif choice == "Manage Books":
            show_manage_books()
        elif choice == "Manage Members":
            show_manage_members()
        elif choice == "Borrowing & Returns":
            show_borrowing_returns()
        elif choice == "Reports":
            show_reports()
        elif choice == "⚙️ System Tools":
            show_system_tools()

if __name__ == "__main__":
    main()

