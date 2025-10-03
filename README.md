# 📚 LitGrid v4.0 - Advanced Library Management System

<div align="center">

![LitGrid Logo](https://img.shields.io/badge/LitGrid-v4.0-blue?style=for-the-badge&logo=library)

**A Complete, Feature-Rich Library Management System Built with Streamlit & SQLite**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Python-3.13+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io/)
[![SQLite](https://img.shields.io/badge/SQLite-07405E?style=for-the-badge&logo=sqlite&logoColor=white)](https://www.sqlite.org/)

[🚀 Live Demo](#live-demo) • [📖 Documentation](#documentation) • [💻 Installation](#installation) • [🤝 Contributing](#contributing)

</div>

---

## 📋 Table of Contents

- [🌟 Overview](#-overview)
- [✨ Key Features](#-key-features)
- [🏗️ System Architecture](#-system-architecture) 
- [📊 Database Schema](#-database-schema)
- [🚀 Installation & Setup](#-installation--setup)
- [🔧 Configuration](#-configuration)
- [📚 User Guide](#-user-guide)
- [👨‍💻 Developer Guide](#-developer-guide)
- [🎯 API Reference](#-api-reference)
- [🔐 Security Features](#-security-features)
- [📈 Analytics & Reporting](#-analytics--reporting)
- [🌐 Deployment](#-deployment)
- [🧪 Testing](#-testing)
- [📄 License](#-license)
- [🤝 Contributing](#-contributing)
- [📞 Contact](#-contact)

---

## 🌟 Overview

**LitGrid v4.0** is a comprehensive, modern library management system designed for educational institutions, public libraries, and private collections. Built with **Python**, **Streamlit**, and **SQLite**, it offers a complete solution for managing books, users, borrowing activities, and administrative tasks.

### 🎯 Project Goals

- **Complete Library Management**: From book cataloging to user management
- **User-Friendly Interface**: Intuitive web-based dashboard for all user types  
- **Advanced Analytics**: Comprehensive reporting and data visualization
- **Security First**: Multi-layer authentication and data protection
- **Scalable Architecture**: Modular design supporting growth
- **Open Source**: MIT licensed for community collaboration

### 🚀 What Makes LitGrid Special

- **All-in-One Solution**: Single file deployment with 7900+ lines of Python code
- **Advanced PDF Library**: Personal and community PDF sharing system
- **Smart Search**: Fuzzy search with typo tolerance
- **Real-time Analytics**: Live dashboards with 20+ visualization types
- **Privacy Controls**: Anonymous mode and granular privacy settings
- **Multi-role Support**: Member, Librarian, and Administrator roles
- **Offline Capable**: SQLite database for reliable local storage

---

## ✨ Key Features

### 📚 **Core Library Management**
- **Book Catalog Management**: Add, edit, delete, and search books with ISBN validation
- **User Management**: Member registration, role-based access, user profiles
- **Borrowing System**: Check-out/check-in with due date tracking and renewals
- **Fine Management**: Automated fine calculation and payment tracking
- **Inventory Control**: Multiple copies per book with barcode generation

### 🔍 **Advanced Search & Discovery**
- **Fuzzy Search Engine**: Typo-tolerant search across titles, authors, genres
- **Multi-field Filtering**: Genre, year, availability, rating-based filters
- **Smart Recommendations**: AI-powered book suggestions based on user history
- **Advanced Sorting**: Popularity, rating, date added, alphabetical options

### 👥 **User Experience**
- **Role-Based Dashboards**: Customized interfaces for members, librarians, admins
- **Personal Library**: Upload and share PDFs with privacy controls
- **Community Features**: Browse public libraries, rate books, leave reviews
- **Reading Analytics**: Personal statistics, reading patterns, goal tracking

### 📊 **Analytics & Reporting**
- **20+ Visualization Types**: Charts, graphs, heatmaps, 3D scatter plots
- **Financial Reports**: Fine collection, revenue projections, payment tracking
- **Member Analytics**: Top borrowers, inactive members, tier distribution
- **Collection Insights**: Most popular books, genre performance, acquisition trends

### 🔐 **Security & Privacy**
- **Multi-Factor Authentication**: Standard login + admin security keys
- **Anonymous Mode**: Pseudonym-based browsing with privacy protection
- **Data Encryption**: Sensitive information encrypted at rest
- **Audit Logging**: Complete activity tracking for compliance
- **Rate Limiting**: Protection against brute force attacks

### 🛠️ **Administrative Tools**
- **System Management**: Database backup/restore, integrity checks
- **Bulk Operations**: CSV import/export, batch user registration
- **Smart Utilities**: Barcode/QR generation, spell checking, duplicate detection
- **Configuration Manager**: JSON-based settings with runtime updates

---

## 🏗️ System Architecture

LitGrid follows a modular, layered architecture designed for maintainability and scalability:

```mermaid
graph TD
    subgraph "Presentation Layer"
        A[Streamlit Web Interface]
        B[User Authentication]
        C[Role-Based Navigation]
    end
    
    subgraph "Business Logic Layer"
        D[User Management]
        E[Book Management] 
        F[Borrowing System]
        G[Analytics Engine]
        H[Security Manager]
        I[PDF Library Manager]
    end
    
    subgraph "Data Access Layer"
        J[Database Manager]
        K[File Handler]
        L[Cache Manager]
    end
    
    subgraph "Data Storage Layer"
        M[(SQLite Database)]
        N[File System Storage]
        O[Session State]
    end
    
    subgraph "External Services"
        P[Email Service]
        Q[Backup System]
        R[Export Services]
    end
    
    A --> B
    A --> C
    B --> H
    C --> D
    C --> E
    C --> F
    C --> G
    C --> I
    
    D --> J
    E --> J
    F --> J
    G --> J
    I --> J
    I --> K
    H --> J
    
    J --> M
    K --> N
    J --> O
    
    G --> P
    F --> P
    J --> Q
    G --> R
    
    classDef presentation fill:#e1f5fe
    classDef business fill:#f3e5f5
    classDef data fill:#e8f5e8
    classDef storage fill:#fff3e0
    classDef external fill:#fce4ec
    
    class A,B,C presentation
    class D,E,F,G,H,I business
    class J,K,L data
    class M,N,O storage
    class P,Q,R external
```

### 🧩 Core Components

#### 🎨 **Presentation Layer**
- **Streamlit Web Interface**: Modern, responsive UI with custom CSS styling
- **Authentication System**: Secure login with session management
- **Navigation Components**: Dynamic menus based on user roles

#### 🔧 **Business Logic Layer**
- **User Management**: Registration, profiles, privacy settings
- **Book Management**: CRUD operations, search, recommendations
- **Borrowing System**: Check-out/in, renewals, fine calculation
- **Analytics Engine**: Data processing, visualization generation
- **Security Manager**: Encryption, audit logging, access control
- **PDF Library Manager**: File upload, sharing, community features

#### 💾 **Data Layer**
- **Database Manager**: SQLite operations with connection pooling
- **File Handler**: PDF processing, image handling, backup operations
- **Cache Manager**: Session state and temporary data management

---

## 📊 Database Schema

LitGrid uses a comprehensive SQLite database with 25+ tables supporting all features:

```mermaid
erDiagram
    USERS {
        int user_id PK
        string username UK
        string full_name
        string email UK
        string password_hash
        string role
        string phone
        string address
        decimal fine_balance
        boolean is_active
        string member_tier
        datetime created_at
        datetime updated_at
        string user_unique_code
        datetime last_login
    }
    
    BOOKS {
        int book_id PK
        string title
        string isbn UK
        string isbn_13
        string isbn_10
        string author
        string genre
        int publication_year
        string publisher
        int pages
        string language
        text description
        text keywords
        int popularity_score
        string location
        text condition_notes
        boolean is_available
        boolean is_active
        datetime created_at
        datetime updated_at
    }
    
    BOOK_INVENTORY {
        int inventory_id PK
        int book_id FK
        int library_id
        string barcode UK
        boolean is_available
        string location
        string condition_status
        datetime created_at
        datetime updated_at
    }
    
    BORROWING {
        int borrowing_id PK
        int user_id FK
        int inventory_id FK
        datetime checkout_date
        datetime due_date
        datetime return_date
        string status
        decimal fine_amount
        text notes
    }
    
    TRANSACTIONS {
        int transaction_id PK
        int user_id FK
        int book_id FK
        string transaction_type
        datetime transaction_date
        datetime due_date
        datetime return_date
        decimal fine_amount
        string status
        text notes
    }
    
    PDF_LIBRARY {
        int pdf_id PK
        int user_id FK
        string title
        string author
        string genre
        text description
        blob pdf_file
        string pdf_filename
        int file_size
        int page_count
        boolean is_public
        int views_count
        datetime upload_date
        datetime updated_at
    }
    
    BOOK_REVIEWS {
        int review_id PK
        int book_id FK
        int user_id FK
        int rating
        text review_text
        boolean is_public
        datetime created_at
        datetime updated_at
    }
    
    PRIVACY_SETTINGS {
        int setting_id PK
        int user_id FK
        string profile_visibility
        boolean show_reading_history
        boolean show_favorite_genres
        boolean show_statistics
        boolean allow_friend_requests
        boolean show_activity
        datetime created_at
        datetime updated_at
    }
    
    AUDIT_LOGS {
        int log_id PK
        int user_id FK
        string action
        string entity_type
        int entity_id
        text details
        string ip_address
        string status
        datetime timestamp
    }
    
    GENRES {
        int genre_id PK
        string genre_name UK
        text description
        datetime created_at
    }
    
    AUTHORS {
        int author_id PK
        string name UK
        text biography
        date birth_date
        date death_date
        string nationality
        datetime created_at
    }
    
    PUBLISHERS {
        int publisher_id PK
        string name UK
        text address
        string website
        int founded_year
        datetime created_at
    }
    
    RENEWAL_REQUESTS {
        int renewal_id PK
        int borrowing_id FK
        int requested_by FK
        int requested_days
        string status
        int reviewed_by FK
        text review_notes
        datetime created_at
        datetime reviewed_at
    }
    
    USERS ||--o{ BORROWING : "borrows"
    USERS ||--o{ TRANSACTIONS : "makes"
    USERS ||--o{ PDF_LIBRARY : "uploads"
    USERS ||--o{ BOOK_REVIEWS : "writes"
    USERS ||--|| PRIVACY_SETTINGS : "has"
    USERS ||--o{ AUDIT_LOGS : "generates"
    
    BOOKS ||--o{ BOOK_INVENTORY : "has_copies"
    BOOKS ||--o{ TRANSACTIONS : "involved_in"
    BOOKS ||--o{ BOOK_REVIEWS : "receives"
    
    BOOK_INVENTORY ||--o{ BORROWING : "checked_out"
    
    BORROWING ||--o{ RENEWAL_REQUESTS : "can_be_renewed"
```

### 🔑 Key Relationships

- **Users ↔ Books**: Many-to-many through borrowing and transactions
- **Books ↔ Inventory**: One-to-many for multiple copies
- **Users ↔ PDF Library**: One-to-many for personal collections
- **Books ↔ Reviews**: One-to-many for community feedback
- **Users ↔ Privacy**: One-to-one for personal settings

---

## 🚀 Installation & Setup

### 📋 Prerequisites

- **Python 3.13+** (recommended)
- **pip** package manager
- **Git** for version control
- **SQLite3** (included with Python)

### ⚡ Quick Start (5 minutes)

1. **Clone the Repository**
   ```bash
   git clone https://github.com/la-b-ib/LitGrid.git
   cd LitGrid
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Application**
   ```bash
   streamlit run litgrid.py
   ```

4. **Access the System**
   - Open your browser to `http://localhost:8501`
   - Use demo credentials: `demo` / `demo123` (Admin)
   - Register as a new member to explore user features

### 🔧 Advanced Installation

#### Virtual Environment Setup
```bash
# Create virtual environment
python -m venv litgrid_env

# Activate environment
# On Windows:
litgrid_env\Scripts\activate
# On macOS/Linux:
source litgrid_env/bin/activate

# Install dependencies
pip install -r requirements.txt
```

#### Docker Installation (Optional)
```dockerfile
FROM python:3.13-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8501

CMD ["streamlit", "run", "litgrid.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

```bash
# Build and run Docker container
docker build -t litgrid .
docker run -p 8501:8501 litgrid
```

---

## 🔧 Configuration

### ⚙️ Environment Variables

Create a `.env` file in the project root:

```env
# Database Configuration
SQLITE_DB=litgrid_local.db
DB_BACKUP_INTERVAL=24  # hours

# Application Settings
SESSION_TIMEOUT=60  # minutes
DEFAULT_BORROWING_DAYS=14
FINE_PER_DAY=5.00
MAX_RENEWALS=2
MAX_MEMBER_ACCOUNTS=10

# Security Settings
SECRET_KEY=your-super-secret-key-change-this
ENCRYPTION_KEY=your-32-character-encryption-key
ENABLE_2FA=true
RATE_LIMIT_ATTEMPTS=5

# Email Configuration (Optional)
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your-email@gmail.com
SMTP_PASSWORD=your-app-password
SMTP_FROM_EMAIL=noreply@litgrid.com

# Feature Flags
ENABLE_PDF_LIBRARY=true
ENABLE_COMMUNITY_FEATURES=true
ENABLE_ANALYTICS=true
ENABLE_BARCODE_GENERATION=true
```

### 📁 Directory Structure

```
LitGrid/
├── litgrid.py                 # Main application (7900+ lines)
├── requirements.txt           # Python dependencies
├── litgrid_local.db          # SQLite database
├── README.md                 # This documentation
├── LICENSE                   # MIT License
├── DEPLOYMENT_GUIDE.md       # Deployment instructions
├── CONTRIBUTING.md           # Contribution guidelines
├── SECURITY.md               # Security policy
├── CODE_OF_CONDUCT.md        # Community guidelines
├── secrets.example.toml      # Secrets template
├── .streamlit/
│   └── config.toml           # Streamlit configuration
├── backups/                  # Database backups
├── temp/                     # Temporary files
├── uploads/                  # File uploads
└── logs/                     # Application logs
```

### 🎛️ Streamlit Configuration

Create `.streamlit/config.toml`:

```toml
[global]
developmentMode = false

[server]
port = 8501
enableCORS = false
enableXsrfProtection = true
maxUploadSize = 50

[theme]
primaryColor = "#1E88E5"
backgroundColor = "#FFFFFF"
secondaryBackgroundColor = "#F0F2F6"
textColor = "#262730"

[browser]
gatherUsageStats = false
```

---

## 📚 User Guide

### 👤 User Roles & Permissions

#### 🎭 **Member Role**
- Browse and search book catalog
- Request book checkouts and returns
- Manage personal profile and privacy settings
- Upload and share PDFs in personal library
- Rate and review books
- View personal reading statistics

#### 📋 **Librarian Role**  
- All member permissions plus:
- Add, edit, and delete books
- Manage book inventory and copies
- Process checkouts and returns
- Approve renewal requests
- Generate reports and analytics
- Manage fines and payments

#### 👨‍💼 **Administrator Role**
- All librarian permissions plus:
- User management (add, edit, delete users)
- System configuration and settings
- Database backup and restore
- Advanced analytics and reporting
- Security management and audit logs
- System monitoring and maintenance

### 🔐 Authentication System

#### Standard Login
```mermaid
sequenceDiagram
    participant U as User
    participant A as Auth System
    participant D as Database
    participant S as Session Manager
    
    U->>A: Enter credentials
    A->>D: Validate username/password
    D-->>A: Return user data
    A->>S: Create session
    S-->>A: Session token
    A-->>U: Login successful
    
    Note over U,S: Session active for 60 minutes
    
    U->>A: Access protected resource
    A->>S: Validate session
    S-->>A: Session valid
    A-->>U: Access granted
```

#### Admin Security
- **Primary Login**: Standard username/password
- **Security Key**: Additional password for sensitive operations
- **Functional Admin**: Hidden admin with special privileges
- **Session Management**: Automatic timeout and renewal

### 📖 Book Management Workflow

```mermaid
flowchart TD
    A[Add Book] --> B{Validate ISBN}
    B -->|Valid| C[Create Book Record]
    B -->|Invalid| D[Show Error]
    C --> E[Add to Inventory]
    E --> F[Generate Barcode]
    F --> G[Update Statistics]
    
    H[Search Books] --> I{Search Type}
    I -->|Title/Author| J[Text Search]
    I -->|ISBN| K[Exact Match]
    I -->|Advanced| L[Multi-field Filter]
    
    J --> M[Fuzzy Matching]
    K --> N[Direct Lookup]
    L --> O[Apply Filters]
    
    M --> P[Display Results]
    N --> P
    O --> P
    
    P --> Q{User Action}
    Q -->|View Details| R[Show Book Info]
    Q -->|Reserve| S[Create Reservation]
    Q -->|Review| T[Add Review/Rating]
    
    classDef process fill:#e3f2fd
    classDef decision fill:#fff3e0
    classDef action fill:#e8f5e8
    
    class A,C,E,F,G,H,J,K,L,M,N,O,P,R,S,T process
    class B,I,Q decision
    class D action
```

### 🔄 Borrowing Process

The borrowing system supports the complete lifecycle from checkout to return:

```mermaid
stateDiagram-v2
    [*] --> Available
    Available --> Reserved : Member reserves
    Reserved --> CheckedOut : Librarian processes
    Available --> CheckedOut : Direct checkout
    
    CheckedOut --> Renewed : Renewal approved
    Renewed --> CheckedOut : Continue borrowing
    
    CheckedOut --> Returned : Returned on time
    CheckedOut --> Overdue : Past due date
    Overdue --> Returned : Returned with fine
    
    Returned --> Available : Book back in system
    
    CheckedOut --> Lost : Reported lost
    Lost --> Replaced : Replacement provided
    Replaced --> Available : Back in circulation
```

---

## 👨‍💻 Developer Guide

### 🏗️ Code Architecture

LitGrid is built as a monolithic application with clear separation of concerns:

#### 📁 **Core Classes Overview**

```python
# Security & Authentication
class Auth:                    # User authentication and session management
class SecurityManager:        # Encryption, validation, and security utilities
class AuditLogger:            # Activity logging and compliance tracking
class RateLimiter:            # Brute force protection

# Data Management  
class Database:               # SQLite connection and query management
class Config:                 # Application configuration management

# Business Logic
class EnhancedBookManager:    # Book CRUD operations and catalog management
class EnhancedUserManager:    # User profile and account management
class EnhancedBorrowingManager: # Checkout, return, and renewal workflows
class PeerLibraryManager:     # PDF library and community features
class PrivacyManager:         # Privacy settings and anonymous mode

# Advanced Features
class SmartUtilities:         # Barcode/QR generation, recommendations
class RecommendationEngine:   # AI-powered book suggestions
class FuzzySearchEngine:      # Typo-tolerant search functionality
class ReviewsManager:         # Book reviews and ratings
class ProfileCommentsManager: # User profile interactions

# Analytics & Reporting
class DataValidator:          # Data integrity and validation
class BackupManager:          # Database backup and restore
class ExcelExporter:          # Data export utilities
class EmailService:           # Notification system

# File Handling
class FileHandler:            # File upload and processing
class PDFHandler:             # PDF text extraction and preview
class BarcodeQRGenerator:     # Code generation utilities
class TempFileManager:        # Temporary file cleanup
```

#### 🔧 **Key Design Patterns**

1. **Singleton Pattern**: Database connection management
2. **Factory Pattern**: Report generation and export formats
3. **Strategy Pattern**: Search algorithms and filtering
4. **Observer Pattern**: Audit logging and event tracking
5. **Command Pattern**: Bulk operations and batch processing

### 🛠️ Development Workflow

#### Adding New Features

1. **Create Feature Branch**
   ```bash
   git checkout -b feature/new-feature-name
   ```

2. **Follow Code Structure**
   ```python
   class NewFeatureManager:
       """Feature description and purpose"""
       
       @staticmethod
       def main_function(params):
           """Main functionality with comprehensive docstring"""
           try:
               # Implementation
               AuditLogger.log_action(user_id, 'feature_used', 'feature', entity_id)
               return True, "Success message"
           except Exception as e:
               st.error(f"Error: {str(e)}")
               return False, str(e)
   ```

3. **Add UI Components**
   ```python
   def show_new_feature():
       """Page function for new feature"""
       st.title("🎯 New Feature")
       
       # Feature implementation
       with st.container():
           # UI elements
           pass
   ```

4. **Update Navigation**
   ```python
   # Add to main menu in main() function
   if user['role'] in ['admin', 'librarian']:
       menu.extend(["New Feature"])
   ```

#### 🧪 Testing Guidelines

```python
# Test structure example
def test_book_management():
    """Test book CRUD operations"""
    # Test data
    test_book = {
        'title': 'Test Book',
        'author': 'Test Author',
        'isbn': '978-0123456789'
    }
    
    # Test creation
    success, book_id = EnhancedBookManager.add_book(test_book)
    assert success, "Book creation failed"
    
    # Test retrieval
    book = Database.execute_query(
        "SELECT * FROM books WHERE book_id = ?", 
        (book_id,), 
        fetch_one=True
    )
    assert book['title'] == test_book['title']
    
    # Cleanup
    Database.execute_update("DELETE FROM books WHERE book_id = ?", (book_id,))
```

### 📊 Performance Optimization

#### Database Query Optimization
```python
# Use indexes for frequent queries
CREATE INDEX idx_books_title ON books(title);
CREATE INDEX idx_borrowing_user_id ON borrowing(user_id);
CREATE INDEX idx_transactions_date ON transactions(transaction_date);

# Batch operations for bulk updates
def bulk_update_books(books_data):
    """Efficient bulk book updates"""
    with Database.get_connection() as conn:
        cursor = conn.cursor()
        cursor.executemany(
            "UPDATE books SET title = ?, author = ? WHERE book_id = ?",
            books_data
        )
        conn.commit()
```

#### Streamlit Performance
```python
# Use caching for expensive operations
@st.cache_data(ttl=300)  # Cache for 5 minutes
def get_analytics_data():
    """Cached analytics data retrieval"""
    return Database.execute_query("SELECT * FROM analytics_view")

# Minimize rerun triggers
if 'data_loaded' not in st.session_state:
    st.session_state.data_loaded = load_initial_data()
```

---

## 🎯 API Reference

### 🗄️ Database Operations

#### Core Database Class
```python
class Database:
    """SQLite database management with connection pooling"""
    
    @classmethod
    def execute_query(cls, query: str, params: tuple = None, fetch_one: bool = False):
        """
        Execute SELECT query and return results
        
        Args:
            query (str): SQL query with ? placeholders
            params (tuple): Query parameters
            fetch_one (bool): Return single record if True
            
        Returns:
            list|dict|None: Query results
        """
        
    @classmethod  
    def execute_update(cls, query: str, params: tuple = None):
        """
        Execute INSERT/UPDATE/DELETE query
        
        Args:
            query (str): SQL query with ? placeholders
            params (tuple): Query parameters
            
        Returns:
            bool: Success status
        """
```

#### Example Database Usage
```python
# Insert new book
success = Database.execute_update(
    "INSERT INTO books (title, author, isbn) VALUES (?, ?, ?)",
    ("Book Title", "Author Name", "978-0123456789")
)

# Fetch user data
user = Database.execute_query(
    "SELECT * FROM users WHERE username = ?",
    ("john_doe",),
    fetch_one=True
)

# Get all active books
books = Database.execute_query(
    "SELECT * FROM books WHERE is_active = 1 ORDER BY title"
)
```

### 🔐 Authentication API

```python
class Auth:
    """Authentication and session management"""
    
    @staticmethod
    def login(username: str, password: str, mode: str = 'member'):
        """
        Authenticate user login
        
        Args:
            username (str): Username or email
            password (str): User password
            mode (str): Login mode ('member', 'admin')
            
        Returns:
            dict|None: User data if successful, None if failed
        """
        
    @staticmethod
    def register(username: str, email: str, password: str, full_name: str, phone: str = None):
        """
        Register new user
        
        Args:
            username (str): Unique username
            email (str): Valid email address
            password (str): Password (min 6 characters)
            full_name (str): User's full name
            phone (str): Optional phone number
            
        Returns:
            tuple: (success: bool, message: str)
        """
```

### 📚 Book Management API

```python
class EnhancedBookManager:
    """Advanced book management operations"""
    
    @staticmethod
    def bulk_import_csv(csv_file) -> tuple:
        """
        Import books from CSV file
        
        Args:
            csv_file: Uploaded CSV file object
            
        Returns:
            tuple: (success: bool, message: str)
        """
        
    @staticmethod
    def upload_book_cover(book_id: int, cover_file) -> bool:
        """
        Upload cover image for book
        
        Args:
            book_id (int): Book identifier
            cover_file: Image file object
            
        Returns:
            bool: Upload success status
        """
```

### 🔍 Search & Filtering API

```python
class EnhancedSearchFilter:
    """Advanced search and filtering capabilities"""
    
    @staticmethod
    def fuzzy_search_books(query: str, threshold: int = 60):
        """
        Perform fuzzy search with typo tolerance
        
        Args:
            query (str): Search term
            threshold (int): Match similarity threshold (0-100)
            
        Returns:
            list: Matching books sorted by relevance
        """
        
    @staticmethod
    def advanced_multi_field_filter(title: str = "", author: str = "", 
                                   genre: str = "", year_from: int = None,
                                   year_to: int = None, available_only: bool = False):
        """
        Advanced multi-field book filtering
        
        Args:
            title (str): Title filter
            author (str): Author filter  
            genre (str): Genre filter
            year_from (int): Start year
            year_to (int): End year
            available_only (bool): Show only available books
            
        Returns:
            list: Filtered book results
        """
```

### 📊 Analytics API

```python
class AnalyticsEngine:
    """Analytics and reporting functionality"""
    
    @staticmethod
    def get_borrowing_trends(start_date: date, end_date: date):
        """
        Generate borrowing trend analysis
        
        Args:
            start_date (date): Analysis start date
            end_date (date): Analysis end date
            
        Returns:
            dict: Trend data with statistics
        """
        
    @staticmethod
    def generate_member_statistics(user_id: int):
        """
        Generate comprehensive member statistics
        
        Args:
            user_id (int): Member identifier
            
        Returns:
            dict: Statistics including books read, favorites, etc.
        """
```

---

## 🔐 Security Features

LitGrid implements multiple layers of security to protect user data and system integrity:

### 🛡️ **Authentication & Authorization**

#### Multi-Factor Authentication Flow
```mermaid
sequenceDiagram
    participant U as User
    participant A as Auth System
    participant S as Security Manager
    participant E as Email Service
    participant D as Database
    
    U->>A: Initial Login
    A->>D: Verify Credentials
    D-->>A: User Verified
    
    alt Admin User
        A->>U: Request Security Key
        U->>A: Provide Security Key
        A->>S: Validate Security Key
        S-->>A: Key Valid
    end
    
    alt 2FA Enabled
        A->>E: Send 2FA Code
        E-->>U: Deliver Code
        U->>A: Enter 2FA Code
        A->>S: Verify Code
        S-->>A: Code Valid
    end
    
    A->>A: Create Session
    A-->>U: Login Successful
    
    Note over U,D: Session expires after 60 minutes
```

#### Role-Based Access Control
```python
# Permission matrix
PERMISSIONS = {
    'member': [
        'view_books', 'search_books', 'borrow_books', 
        'view_profile', 'upload_pdfs', 'rate_books'
    ],
    'librarian': [
        'all_member_permissions', 'manage_books', 'manage_borrowing',
        'view_reports', 'manage_fines', 'approve_renewals'
    ],
    'admin': [
        'all_librarian_permissions', 'manage_users', 'system_config',
        'backup_restore', 'audit_logs', 'security_settings'
    ]
}
```

### 🔒 **Data Protection**

#### Encryption Implementation
```python
class SecurityManager:
    """Advanced security and encryption manager"""
    
    def __init__(self):
        self._init_encryption_key()
        
    def encrypt_data(self, data: str) -> str:
        """Encrypt sensitive data using Fernet encryption"""
        if not data or not self.cipher:
            return data
        return self.cipher.encrypt(data.encode()).decode()
        
    def decrypt_data(self, encrypted_data: str) -> str:
        """Decrypt sensitive data"""
        if not encrypted_data or not self.cipher:
            return encrypted_data
        return self.cipher.decrypt(encrypted_data.encode()).decode()
```

#### Password Security
- **Bcrypt Hashing**: Industry-standard password hashing with salt
- **Password Strength**: Minimum 6 characters with complexity validation
- **Password Reset**: Secure token-based reset mechanism
- **Session Security**: Automatic timeout and secure session tokens

### 🛡️ **Input Validation & Sanitization**

```python
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
```

### 📋 **Audit Logging**

Complete activity tracking for compliance and security monitoring:

```python
class AuditLogger:
    @staticmethod
    def log_action(user_id: int, action: str, entity_type: str, 
                   entity_id: int = None, details: str = None):
        """Log user actions for audit trail"""
        query = """
            INSERT INTO audit_logs 
            (user_id, action, entity_type, entity_id, details, ip_address, status)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """
        Database.execute_update(query, (user_id, action, entity_type, entity_id, details, ip_address, 'success'))
```

### 🚫 **Rate Limiting**

Protection against brute force attacks:

```python
class RateLimiter:
    def check_limit(self, key: str, max_attempts: int = 5, window: int = 300) -> bool:
        """Check if action is rate limited"""
        now = time.time()
        
        # Clean old attempts
        self.attempts[key] = [t for t in self.attempts.get(key, []) if now - t < window]
        
        # Check limit
        if len(self.attempts.get(key, [])) >= max_attempts:
            return False
            
        # Record attempt
        if key not in self.attempts:
            self.attempts[key] = []
        self.attempts[key].append(now)
        return True
```

---

## 📈 Analytics & Reporting

LitGrid provides comprehensive analytics with 20+ visualization types and detailed reporting capabilities:

### 📊 **Dashboard Analytics**

#### Library Overview Metrics
- **Real-time Statistics**: Books, users, transactions, fines
- **Trend Analysis**: Daily, weekly, monthly borrowing patterns
- **Performance Indicators**: Turnover rate, popularity scores
- **Health Metrics**: Overdue books, system status, user activity

#### Visual Components
```python
# Borrowing trend visualization
def generate_borrowing_trend():
    data = Database.execute_query("""
        SELECT date(checkout_date) as date, COUNT(*) as count
        FROM borrowing
        WHERE checkout_date >= date('now', '-30 days')
        GROUP BY date(checkout_date)
        ORDER BY date
    """)
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=[row['date'] for row in data],
        y=[row['count'] for row in data],
        mode='lines+markers',
        name='Daily Checkouts'
    ))
    return fig
```

### 📚 **Book Analytics**

#### Popular Books Analysis
```mermaid
graph LR
    A[Book Data] --> B[Checkout Frequency]
    A --> C[User Ratings]
    A --> D[Review Count]
    
    B --> E[Popularity Score]
    C --> E
    D --> E
    
    E --> F[Top Books List]
    E --> G[Recommendation Engine]
    E --> H[Collection Insights]
    
    F --> I[Dashboard Display]
    G --> J[User Suggestions]
    H --> K[Acquisition Planning]
```

#### Genre Performance Tracking
- **Circulation Statistics**: Borrows per genre over time
- **User Preferences**: Most requested genres by demographics
- **Collection Balance**: Genre distribution analysis
- **Seasonal Trends**: Genre popularity by time periods

### 👥 **Member Analytics**

#### User Behavior Analysis
```python
def analyze_reading_patterns(user_id):
    """Comprehensive user reading pattern analysis"""
    patterns = {
        'favorite_genres': get_top_genres(user_id),
        'reading_frequency': calculate_reading_frequency(user_id),
        'preferred_authors': get_favorite_authors(user_id),
        'seasonal_patterns': analyze_seasonal_reading(user_id),
        'book_length_preference': analyze_page_preferences(user_id)
    }
    return patterns
```

#### Leaderboards & Gamification
- **Top Readers**: Most books borrowed by period
- **Review Champions**: Most helpful reviews
- **Genre Explorers**: Users reading across multiple genres
- **Community Contributors**: PDF sharing and ratings

### 💰 **Financial Analytics**

#### Revenue Tracking
```python
def generate_financial_report(start_date, end_date):
    """Comprehensive financial analysis"""
    return {
        'fine_collection': calculate_fines_collected(start_date, end_date),
        'outstanding_fines': get_outstanding_fines(),
        'payment_trends': analyze_payment_patterns(),
        'revenue_projections': project_future_revenue(),
        'cost_analysis': calculate_operational_costs()
    }
```

### 📋 **Advanced Reports**

#### Multi-Dimensional Analysis
- **3D Scatter Plots**: Book popularity vs. rating vs. age
- **Heatmaps**: Usage patterns by time and location
- **Correlation Analysis**: User behavior relationships
- **Predictive Analytics**: Future demand forecasting

#### Export Capabilities
```python
class ReportExporter:
    """Export reports in multiple formats"""
    
    def export_to_excel(self, data, report_type):
        """Export with advanced formatting"""
        wb = Workbook()
        ws = wb.active
        
        # Apply styling, charts, and calculations
        self.apply_excel_formatting(ws, data)
        self.add_charts(ws, data, report_type)
        
        return wb
        
    def export_to_pdf(self, data, template):
        """Generate professional PDF reports"""
        # PDF generation with charts and formatting
        pass
```

---

## 🌐 Deployment

### ☁️ **Streamlit Cloud Deployment**

#### Quick Deploy to Streamlit Cloud
1. **Push to GitHub**: Ensure all files are in a public repository
2. **Connect to Streamlit Cloud**: Visit [share.streamlit.io](https://share.streamlit.io)
3. **Configure App**: Select repository, branch, and main file (`litgrid.py`)
4. **Set Secrets**: Add environment variables in app settings

```toml
# secrets.toml for Streamlit Cloud
[database]
SQLITE_DB = "litgrid_local.db"

[security]
SECRET_KEY = "your-production-secret-key"
ENCRYPTION_KEY = "your-32-character-encryption-key"

[email]
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SMTP_USERNAME = "your-email@gmail.com"
SMTP_PASSWORD = "your-app-password"
```

### 🐳 **Docker Deployment**

#### Production Docker Setup
```dockerfile
FROM python:3.13-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    sqlite3 \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY . .

# Create necessary directories
RUN mkdir -p backups temp uploads logs

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV STREAMLIT_SERVER_PORT=8501
ENV STREAMLIT_SERVER_ADDRESS=0.0.0.0

# Expose port
EXPOSE 8501

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8501/_stcore/health || exit 1

# Run application
CMD ["streamlit", "run", "litgrid.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

#### Docker Compose
```yaml
version: '3.8'

services:
  litgrid:
    build: .
    ports:
      - "8501:8501"
    volumes:
      - ./data:/app/data
      - ./backups:/app/backups
      - ./logs:/app/logs
    environment:
      - SQLITE_DB=/app/data/litgrid.db
      - SECRET_KEY=${SECRET_KEY}
      - EMAIL_ENABLED=true
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8501/_stcore/health"]
      interval: 30s
      timeout: 10s
      retries: 3

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./ssl:/etc/nginx/ssl
    depends_on:
      - litgrid
    restart: unless-stopped
```

### 🚀 **Production Deployment**

#### AWS EC2 Deployment
```bash
# Launch EC2 instance (Ubuntu 22.04 LTS)
# Configure security groups (ports 22, 80, 443, 8501)

# Connect to instance
ssh -i your-key.pem ubuntu@your-ec2-ip

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker ubuntu

# Clone repository
git clone https://github.com/la-b-ib/LitGrid.git
cd LitGrid

# Set environment variables
cp secrets.example.toml secrets.toml
# Edit secrets.toml with production values

# Deploy with Docker Compose
docker-compose up -d

# Setup SSL with Let's Encrypt
sudo apt install certbot
sudo certbot --nginx -d your-domain.com
```

#### Performance Optimization
```python
# Streamlit configuration for production
[server]
port = 8501
enableCORS = false
enableXsrfProtection = true
maxUploadSize = 50

[global]
developmentMode = false
disableWatchdogWarning = true

[client]
caching = true
toolbarMode = "minimal"

[theme]
primaryColor = "#1E88E5"
backgroundColor = "#FFFFFF"
```

---

## 🧪 Testing

### 🔬 **Test Structure**

```python
# test_litgrid.py
import pytest
import sqlite3
from litgrid import Database, Auth, EnhancedBookManager

class TestDatabase:
    """Database operation tests"""
    
    def setup_method(self):
        """Setup test database"""
        self.test_db = "test_litgrid.db"
        Database._db_path = self.test_db
        Database.init_pool()
    
    def teardown_method(self):
        """Cleanup test database"""
        import os
        if os.path.exists(self.test_db):
            os.remove(self.test_db)
    
    def test_user_creation(self):
        """Test user registration"""
        success, msg = Auth.register(
            "testuser", 
            "test@example.com", 
            "password123", 
            "Test User"
        )
        assert success, f"User creation failed: {msg}"
    
    def test_book_operations(self):
        """Test book CRUD operations"""
        # Test book creation
        book_data = {
            'title': 'Test Book',
            'author': 'Test Author',
            'isbn': '978-0123456789',
            'genre': 'Fiction'
        }
        
        success = Database.execute_update(
            "INSERT INTO books (title, author, isbn, genre) VALUES (?, ?, ?, ?)",
            (book_data['title'], book_data['author'], book_data['isbn'], book_data['genre'])
        )
        assert success, "Book creation failed"
        
        # Test book retrieval
        book = Database.execute_query(
            "SELECT * FROM books WHERE isbn = ?",
            (book_data['isbn'],),
            fetch_one=True
        )
        assert book is not None, "Book retrieval failed"
        assert book['title'] == book_data['title']

class TestAuthentication:
    """Authentication system tests"""
    
    def test_password_hashing(self):
        """Test password security"""
        password = "test_password"
        hashed = Auth.hash_password(password)
        
        assert hashed != password, "Password not hashed"
        assert Auth.verify_password(password, hashed), "Password verification failed"
    
    def test_login_flow(self):
        """Test complete login process"""
        # Create test user
        Auth.register("logintest", "login@test.com", "password123", "Login Test")
        
        # Test successful login
        user = Auth.login("logintest", "password123", "member")
        assert user is not None, "Valid login failed"
        assert user['username'] == "logintest"
        
        # Test failed login
        failed_user = Auth.login("logintest", "wrongpassword", "member")
        assert failed_user is None, "Invalid login succeeded"

class TestBookManagement:
    """Book management feature tests"""
    
    def test_isbn_validation(self):
        """Test ISBN validation"""
        valid_isbn13 = "978-0123456789"
        valid_isbn10 = "0123456789"
        invalid_isbn = "invalid"
        
        assert DataValidator.validate_isbn(valid_isbn13), "Valid ISBN-13 failed"
        assert DataValidator.validate_isbn(valid_isbn10), "Valid ISBN-10 failed"
        assert not DataValidator.validate_isbn(invalid_isbn), "Invalid ISBN passed"
    
    def test_fuzzy_search(self):
        """Test fuzzy search functionality"""
        # Setup test books
        test_books = [
            {'title': 'The Great Gatsby', 'author': 'F. Scott Fitzgerald'},
            {'title': 'To Kill a Mockingbird', 'author': 'Harper Lee'}
        ]
        
        # Test typo tolerance
        results = FuzzySearchEngine.search_books("Grat Gatsby", test_books, 60)
        assert len(results) > 0, "Fuzzy search failed to find similar match"

# Run tests
if __name__ == "__main__":
    pytest.main(["-v", "test_litgrid.py"])
```

### 📊 **Test Coverage**

```bash
# Install testing dependencies
pip install pytest pytest-cov

# Run tests with coverage
pytest --cov=litgrid --cov-report=html

# Coverage targets
- Database operations: 95%+
- Authentication: 100%
- Core business logic: 90%+
- UI components: 70%+
```

### 🔄 **Continuous Integration**

```yaml
# .github/workflows/test.yml
name: Test LitGrid

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: [3.11, 3.12, 3.13]
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v3
      with:
        python-version: ${{ matrix.python-version }}
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
        pip install pytest pytest-cov
    
    - name: Run tests
      run: |
        pytest --cov=litgrid --cov-report=xml
    
    - name: Upload coverage
      uses: codecov/codecov-action@v3
```

---

## 📄 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

```
MIT License

Copyright (c) 2025 Labib Bin Shahed

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

## 🤝 Contributing

We welcome contributions from the community! Please read our [Contributing Guidelines](CONTRIBUTING.md) for details on:

- 🐛 **Bug Reports**: How to report issues effectively
- 💡 **Feature Requests**: Suggesting new functionality
- 🔧 **Code Contributions**: Development workflow and standards
- 📚 **Documentation**: Improving project documentation
- 🧪 **Testing**: Writing and running tests

### 🚀 **Quick Contribution Guide**

1. **Fork the Repository**
   ```bash
   git clone https://github.com/your-username/LitGrid.git
   cd LitGrid
   ```

2. **Create Feature Branch**
   ```bash
   git checkout -b feature/amazing-feature
   ```

3. **Make Changes**
   - Follow code style guidelines
   - Add tests for new functionality
   - Update documentation as needed

4. **Test Your Changes**
   ```bash
   pytest tests/
   streamlit run litgrid.py  # Manual testing
   ```

5. **Submit Pull Request**
   - Clear description of changes
   - Reference related issues
   - Include screenshots for UI changes

### 👥 **Community**

- **Code of Conduct**: [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md)
- **Security Policy**: [SECURITY.md](SECURITY.md)
- **Development Setup**: [CONTRIBUTING.md](CONTRIBUTING.md)

---

## 📞 Contact

<div align="center">

### 👨‍💻 **Project Maintainer**

**Labib Bin Shahed**  
*Full-Stack Developer & Library Systems Specialist*

[![Email](https://img.shields.io/badge/Email-D14836?style=for-the-badge&logo=gmail&logoColor=white)](mailto:labib.45x@gmail.com)
[![GitHub](https://img.shields.io/badge/GitHub-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/la-b-ib)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/la-b-ib/)
[![Portfolio](https://img.shields.io/badge/Website-0A5C78?style=for-the-badge&logo=internet-explorer&logoColor=white)](https://la-b-ib.github.io/)
[![X](https://img.shields.io/badge/X-000000?style=for-the-badge&logo=twitter&logoColor=white)](https://x.com/la_b_ib_)

### 📧 **Support & Questions**

- **General Questions**: [labib.45x@gmail.com](mailto:labib.45x@gmail.com)
- **Security Issues**: [labib-x@protonmail.com](mailto:labib-x@protonmail.com)
- **Bug Reports**: [GitHub Issues](https://github.com/la-b-ib/LitGrid/issues)
- **Feature Requests**: [GitHub Discussions](https://github.com/la-b-ib/LitGrid/discussions)

</div>

---

## 🌟 **Acknowledgments**

### 🏆 **Special Thanks**

- **Streamlit Team**: For the amazing framework that powers our UI
- **SQLite Project**: For the reliable, embedded database engine
- **Python Community**: For the incredible ecosystem of libraries
- **Open Source Contributors**: For inspiration and best practices

### 📚 **Libraries & Dependencies**

This project stands on the shoulders of giants. Key dependencies include:

| Library | Purpose | Version |
|---------|---------|---------|
| `streamlit` | Web UI Framework | 1.35.0+ |
| `pandas` | Data Analysis | 2.2.0+ |
| `plotly` | Data Visualization | 5.20.0+ |
| `bcrypt` | Password Hashing | 4.2.0+ |
| `cryptography` | Data Encryption | 42.0.0+ |
| `fuzzywuzzy` | Fuzzy String Matching | 0.18.0+ |
| `qrcode` | QR Code Generation | 7.4.2+ |
| `openpyxl` | Excel File Handling | 3.1.0+ |
| `pillow` | Image Processing | 10.4.0+ |

### 🎯 **Project Stats**

<div align="center">

![Lines of Code](https://img.shields.io/badge/Lines_of_Code-7900+-green?style=for-the-badge)
![Database Tables](https://img.shields.io/badge/Database_Tables-25+-blue?style=for-the-badge)
![Features](https://img.shields.io/badge/Features-50+-orange?style=for-the-badge)
![Classes](https://img.shields.io/badge/Classes-35+-purple?style=for-the-badge)

**Total Development Time**: 200+ hours  
**Code Quality**: Production-ready with comprehensive error handling  
**Documentation**: Extensive inline comments and external documentation  
**Testing**: Unit tests with 85%+ coverage target

</div>

---

<div align="center">

### 🚀 **Ready to Get Started?**

[📥 **Download LitGrid**](https://github.com/la-b-ib/LitGrid/archive/main.zip) | [🌟 **Star on GitHub**](https://github.com/la-b-ib/LitGrid) | [📖 **Read the Docs**](https://github.com/la-b-ib/LitGrid/wiki)

**Made with ❤️ by [Labib Bin Shahed](https://github.com/la-b-ib)**

---

*"Empowering libraries worldwide with modern, accessible technology"*

**LitGrid v4.0** - The Future of Library Management is Here

</div>

<div align="center">

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://your-app-url.streamlit.app)

**A next-generation, enterprise-grade library management system with 210+ advanced features**

[![Python 3.13+](https://img.shields.io/badge/python-3.13+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/streamlit-1.29.0-FF4B4B.svg)](https://streamlit.io)
[![SQLite](https://img.shields.io/badge/database-SQLite-003B57.svg)](https://www.sqlite.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Status: Production Ready](https://img.shields.io/badge/status-production%20ready-brightgreen.svg)]()

### 🎉 **NEW in v4.0: 210+ Features | 34+ Visualizations | Advanced Analytics | Cloud Ready**

</div>

---

## � What's New in v2.0

### 🔥 Major Enhancements

- ✅ **Password Reset System** - Complete token-based password recovery
- ✅ **Password Change Feature** - Secure in-app password updates
- ✅ **34+ Advanced Visualizations** - 3D charts, radar, sunburst, heatmaps
- ✅ **Personal Statistics Dashboard** - Reading analytics, history, trends
- ✅ **6 Report Categories** - 29 comprehensive report types
- ✅ **Advanced Analytics** - Pattern recognition, health metrics, recommendations
- ✅ **Enhanced Account Management** - 3-tab interface with security settings
- ✅ **Library Health Dashboard** - Real-time system performance monitoring
- ✅ **Multi-Dimensional Analysis** - Complex data relationships visualization
- ✅ **Reading Pattern Recognition** - AI-based user preference detection

### 📊 Key Statistics

- **Total Features:** 210+ (up from 40)
- **Lines of Code:** 2,347 (67% increase)
- **Visualizations:** 34+ chart types (680% increase)
- **Report Types:** 29 comprehensive reports
- **Helper Functions:** 17 utility functions
- **Performance:** < 2s page load, < 100ms queries

---

## ✨ Core Features

### 🔐 Authentication & Security (15 Features)

- **Advanced Password Management**
  - ✅ Password reset via email (token-based)
  - ✅ Password change with verification
  - ✅ bcrypt hashing (12 rounds)
  - ✅ Session timeout (60 minutes)
  - ✅ Security tips and guidelines

- **User Account Management**
  - ✅ Role-Based Access Control (4 roles)
  - ✅ Member Tier System (Basic, Premium, Gold)
  - ✅ Secure registration with validation
  - ✅ Last login tracking
  - ✅ Account status management

### 📚 Book Management (25 Features)

- **Complete CRUD Operations**
  - ✅ Add, edit, delete books
  - ✅ Multiple copies management
  - ✅ ISBN validation
  - ✅ Publisher and author tracking
  - ✅ Genre classification (multi-genre support)

- **Advanced Features**
  - ✅ Book ratings and reviews
  - ✅ Availability tracking
  - ✅ Popularity metrics
  - ✅ Reading time estimation
  - ✅ Books never borrowed report

### 👥 Member Management (20 Features)

- **Member Operations**
  - ✅ Complete member directory
  - ✅ Advanced search and filtering
  - ✅ Tier-based privileges
  - ✅ Fine balance tracking
  - ✅ Activate/deactivate accounts

- **Member Analytics**
  - ✅ Top borrowers report
  - ✅ Registration trend analysis
  - ✅ Tier distribution visualization
  - ✅ Activity monitoring
  - ✅ Engagement scoring

### 📖 Borrowing & Returns (15 Features)

- **Checkout System**
  - ✅ Quick member/book search
  - ✅ Custom borrowing periods
  - ✅ Real-time availability checking
  - ✅ Due date calculation
  - ✅ Borrowing limit enforcement

- **Return System**
  - ✅ Overdue detection
  - ✅ Automatic fine calculation (₹5/day)
  - ✅ Fine balance updates
  - ✅ Active borrowings tracking
  - ✅ Due soon/overdue filters

### 📊 Advanced Reports & Analytics (50+ Features)

#### Report Categories
1. **Overview Dashboard** - Comprehensive library metrics
2. **Books Analytics** - 7 detailed book reports
3. **Members Analytics** - 6 member-focused reports
4. **Financial Analytics** - Revenue and fine tracking
5. **Trends & Patterns** - Behavioral analysis (NEW!)
6. **Advanced Visualizations** - Complex data viz (NEW!)

#### Visualization Types (34+)
- **Basic Charts:** Bar, Line, Area, Pie, Donut
- **Advanced Charts:** 3D Scatter, Radar, Sunburst, Bubble
- **Statistical:** Histogram, Box Plot, Violin Plot
- **Comparative:** Grouped/Stacked Bars, Multi-line
- **Interactive:** Hover tooltips, zoom, pan, export

---

## 🎯 Advanced Features

### 📈 Analytics & Intelligence

- **Pattern Recognition**
  - Reading behavior analysis
  - Favorite genre/author detection
  - Checkout pattern identification
  - Peak activity hours
  - Seasonal trends

- **Recommendation Engine**
  - Weighted scoring algorithm (rating 40%, popularity 30%, activity 20%, availability 10%)
  - Personalized book suggestions
  - Similar books identification
  - Trending books tracking

- **Health Monitoring**
  - Library health scores (0-100)
  - Book availability metrics
  - Member utilization rates
  - Return compliance tracking
  - Real-time dashboard

### 👤 Personal Dashboard (NEW!)

- **My Account - 3 Tabs:**
  1. **Profile** - Personal information, status, tier
  2. **Security** - Password change, security tips
  3. **My Statistics** - Reading analytics (NEW!)

- **Statistics Features:**
  - 📚 Total books read (lifetime)
  - 📖 Currently borrowed count
  - 📅 Total reading days
  - ⭐ Favorite genre (AI-detected)
  - 📊 Reading history table (last 10)
  - 📈 Trend visualization (days per book)

---

## 🛠️ Technology Stack

### Backend
- **Python 3.13+** - Modern Python with type hints
- **MariaDB 12.0.2** - High-performance database
- **mysql-connector-python** - Database driver with pooling

### Frontend
- **Streamlit 1.29.0+** - Rapid web app framework
- **Plotly 5.18.0+** - Interactive visualizations
- **Plotly Express** - Simplified chart creation

### Data Processing
- **Pandas 2.2.3+** - Data manipulation and analysis
- **NumPy 2.2.6+** - Numerical computing

### Security
- **bcrypt 4.3.0** - Password hashing
- **python-dotenv 1.1.0** - Environment management

---

## � Project Structure

```
LibraryManagementSystem-main/
├── litgrid_single.py           # Main application (2,347 lines)
├── lib.sql                      # Database schema (21 tables + 3 views)
├── .env                         # Environment configuration
├── requirements.txt             # Python dependencies
├── README.md                    # This file
├── FEATURES.md                  # Complete feature list (210+)
├── ENHANCEMENT_SUMMARY.md       # v2.0 enhancement details
├── QUICK_START.md              # Quick start guide
└── FILES.md                     # Project structure documentation
```

---

## 🚀 Quick Start

### Prerequisites
- Python 3.13+ installed
- MariaDB 12.0+ or MySQL 8.0+ installed
- 512MB RAM minimum
- Modern web browser

### Installation

1. **Clone the repository**
```bash
git clone <repository-url>
cd LibraryManagementSystem-main

- ISBN-based book identification---

- Publisher and publication year tracking

## 🌟 Features

### 📊 Analytics Dashboard

- **Admin Dashboard**: Library-wide statistics and trends### 🔐 Authentication & Authorization

  - Total books, members, active borrowings, overdue books- **Role-based access control** (Admin, Librarian, Member)

  - 30-day borrowing trend chart- **Secure password hashing** with bcrypt

  - Popular books visualization- **Session management** with automatic timeout

  - Overdue books tracking- **User registration** with email validation

- **Member Dashboard**: Personal reading statistics- **Member tier system** (Basic, Silver, Gold, Platinum)

  - Currently borrowed books

  - Books read this year### 📖 Advanced Book Management

  - Active reservations- **Comprehensive book catalog** with ISBN validation

  - Due date reminders- **Multiple authors and genres** per book

- **Book editions and series** tracking

### 🔐 Security- **Cover image upload** and management

- Password hashing with bcrypt (12 salt rounds)- **Book inventory management** across multiple libraries

- Session timeout management (60 minutes default)- **Barcode/QR code generation** for physical books

- SQL injection protection with parameterized queries- **Dewey Decimal Classification** support

- Environment-based configuration

### 🔄 Intelligent Borrowing System

### 🎨 Modern UI- **Automated checkout and return** processes

- Clean, professional interface- **Renewal system** with configurable limits

- Responsive design- **Fine calculation** for overdue books

- Interactive Plotly charts- **Borrowing history** tracking

- Custom CSS styling with gradient cards- **Member-specific borrowing limits** based on tier

- Real-time data updates- **Overdue notifications** and reminders

- **Book condition tracking**

## 🚀 Quick Start

### 📋 Reservation & Queue System

### Prerequisites- **Book reservation** with priority queue

- Python 3.8 or higher- **Automatic notifications** when books become available

- MySQL 8.0+ or MariaDB 11.0+- **Hold period management**

- pip package manager- **Reservation expiry** handling



### Installation### ⭐ Ratings & Reviews

- **5-star rating system**

1. **Clone or Download** this repository- **User reviews** with verification

- **Reading status tracking** (Reading, Completed, Want to Read)

2. **Install Python Dependencies**- **Reading history** and statistics

   ```bash

   pip install -r requirements.txt### 🤖 Smart Recommendations

   ```- **Personalized book recommendations** based on:

  - Reading history

3. **Setup Database**  - Genre preferences

     - Rating patterns

   Start MySQL/MariaDB:  - Popularity trends

   ```bash- **Trending books** section

   # macOS with Homebrew- **New arrivals** highlights

   brew services start mariadb

   ### 📊 Analytics & Reporting

   # Linux- **Real-time dashboard** with key metrics

   sudo systemctl start mysql- **Borrowing trends** visualization

   ```- **Popular books** analytics

   - **Member statistics** and demographics

   Import the database schema:- **Revenue tracking** from fines

   ```bash- **Inventory reports**

   mysql -u root -p < litgrid_schema.sql- **Custom report builder**

   ```- **Export to Excel/PDF**

   

   Or use MySQL shell:### 🔍 Advanced Search

   ```bash- **Multi-criteria search** (title, author, ISBN, genre)

   mysql -u root -p- **Faceted filtering**

   mysql> source litgrid_schema.sql;- **Fuzzy matching** for typo tolerance

   mysql> exit;- **Search history** and saved searches

   ```- **Autocomplete suggestions**



4. **Configure Environment**### 🔔 Notification System

   - **In-app notifications**

   Copy `.env.example` to `.env`:- **Email notifications** for:

   ```bash  - Due date reminders

   cp .env.example .env  - Overdue alerts

   ```  - Reserved book availability

     - System announcements

   Edit `.env` and set your database credentials:- **SMS notifications** (optional)

   ```env

   DB_HOST=localhost### 🎨 Modern User Interface

   DB_PORT=3306- **Clean, responsive design**

   DB_USER=root- **Dark/Light theme** support

   DB_PASSWORD=your_password_here- **Mobile-friendly** interface

   DB_NAME=litgrid- **Interactive data visualizations**

   ```- **Beautiful book cards** with covers

- **Custom styling** and animations

5. **Run the Application**

   ```bash### 🔧 System Management

   streamlit run litgrid_single.py- **System settings** configuration

   ```- **User management** for admins

- **Audit logs** for all actions

6. **Access the App**- **Multi-library support**

   - **Library sections** management

   Open your browser to: http://localhost:8501- **Publisher and author** management



## 🔑 Default Credentials---



After importing the database schema, you can login with:## 🚀 Getting Started



- **Username**: `admin`### Prerequisites

- **Password**: `admin123`

- **Role**: Administrator- Python 3.8 or higher

- MySQL 8.0 or higher (or MariaDB)

⚠️ **Important**: Change the default password after first login!- pip (Python package manager)



## 📁 Project Structure### Installation



```1. **Clone the repository**

LibraryManagementSystem/   ```bash

├── litgrid_single.py      # Main application (single file)   git clone https://github.com/yourusername/litgrid.git

├── litgrid_schema.sql     # Database schema with sample data   cd litgrid

├── requirements.txt       # Python dependencies   ```

├── .env                   # Environment configuration (create from .env.example)

├── .env.example          # Environment template2. **Create a virtual environment** (recommended)

├── .gitignore            # Git ignore rules   ```bash

├── .venv/                # Virtual environment (auto-created)   python -m venv .venv

└── README.md             # This file   

```   # On macOS/Linux

   source .venv/bin/activate

## 🗄️ Database Schema   

   # On Windows

The database includes 20+ tables:   .venv\Scripts\activate

   ```

### Core Tables

- `users` - User accounts with roles3. **Install dependencies**

- `roles` - Role definitions (admin, librarian, member)   ```bash

- `books` - Book catalog   pip install -r requirements.txt

- `book_inventory` - Physical book copies   ```

- `borrowing` - Checkout/return transactions

- `reservations` - Book reservation queue4. **Set up the database**

   ```bash

### Analytics & Features   # Start MySQL/MariaDB service

- `book_statistics` - Book popularity metrics   # macOS (using Homebrew)

- `book_ratings` - User ratings and reviews   brew services start mysql

- `reading_history` - User reading tracking   # or

- `notifications` - System notifications   brew services start mariadb

- `audit_log` - Activity tracking   

- `saved_searches` - User search preferences   # Import the database schema

   mysql -u root -p < litgrid_schema.sql

### Reference Data   ```

- `publishers`, `authors`, `genres`, `languages`

- Automated triggers for inventory and fine calculations5. **Configure environment variables**

- Stored procedures for checkout, return, and renewal operations   ```bash

   # Copy the example env file

## ⚙️ Configuration   cp .env.example .env

   

All configuration is managed through environment variables in `.env`:   # Edit .env with your database credentials

   nano .env

### Database Settings   ```

```env

DB_HOST=localhost   Update the following values in `.env`:

DB_PORT=3306   ```

DB_USER=root   DB_HOST=localhost

DB_PASSWORD=your_password   DB_PORT=3306

DB_NAME=litgrid   DB_USER=root

```   DB_PASSWORD=your_password

   DB_NAME=litgrid

### Application Settings   SECRET_KEY=your-secret-key-here

```env   ```

SESSION_TIMEOUT=60        # Session timeout in minutes

```6. **Run the application**

   ```bash

### Borrowing Rules (Configured in Database)   streamlit run litgrid.py

- Default borrowing period: 14 days   ```

- Maximum renewals: 2 times

- Fine per day: ₹5.007. **Access the application**

- Maximum fine cap: ₹500.00   

   Open your browser and navigate to: `http://localhost:8501`

### Member Tier Limits

- **Basic**: 2 books, 7-day borrowing### Default Login Credentials

- **Silver**: 5 books, 14-day borrowing

- **Gold**: 10 books, 21-day borrowing```

- **Platinum**: 20 books, 30-day borrowingUsername: admin

Password: admin123

## 🎯 User Roles```



### Admin⚠️ **Important:** Change the default password after first login!

- Full system access

- User management---

- System configuration

- View all analytics and reports## 📁 Project Structure



### Librarian```

- Book managementLibraryManagementSystem-main/

- Member management├── litgrid.py                 # Main application entry point

- Process borrowing and returns├── litgrid_schema.sql         # Database schema with advanced features

- View library statistics├── config.yaml                # Application configuration

├── requirements.txt           # Python dependencies

### Premium Member├── .env.example              # Environment variables template

- Extended borrowing periods├── README.md                 # This file

- Priority reservations│

- Higher book limits├── utils/                    # Utility modules

│   ├── __init__.py

### Member│   ├── database.py          # Database connection & pooling

- Browse and search books│   ├── config.py            # Configuration management

- Borrow and return books│   ├── auth.py              # Authentication & authorization

- View personal reading history│   ├── helpers.py           # Helper functions

- Rate and review books│   └── styling.py           # Custom UI styling

│

## 🐛 Troubleshooting├── modules/                  # Feature modules

│   ├── __init__.py

### Database Connection Error│   ├── auth_page.py         # Login & registration

```│   ├── dashboard.py         # Main dashboard

Error: Can't connect to MySQL server│   ├── books.py             # Book management

```│   ├── members.py           # Member management

**Solution**: │   ├── borrowing.py         # Borrowing & returns

1. Check if MySQL/MariaDB is running: `brew services list` (macOS)│   └── analytics.py         # Analytics & reports

2. Verify credentials in `.env` file│

3. Ensure database exists: `mysql -u root -p -e "SHOW DATABASES;"`├── assets/                   # Static assets

│   └── logo.png

### Module Not Found Error│

```└── uploads/                  # User uploads (book covers, etc.)

ModuleNotFoundError: No module named 'streamlit'```

```

**Solution**: Install dependencies: `pip install -r requirements.txt`---



### Port Already in Use## 🎯 Key Features Comparison

```

OSError: [Errno 48] Address already in use| Feature | Old System | LitGrid (New) |

```|---------|-----------|---------------|

**Solution**: | Authentication | ❌ None | ✅ Role-based with sessions |

- Streamlit will auto-select next available port (8502, 8503, etc.)| User Roles | ❌ Single type | ✅ 4 roles (Admin, Librarian, Premium, Basic) |

- Or stop other Streamlit apps: `killall streamlit`| Book Details | ⚠️ Basic | ✅ Comprehensive (covers, series, editions) |

| Search | ⚠️ Simple | ✅ Advanced with fuzzy matching |

### Password Login Fails| Borrowing | ⚠️ Manual | ✅ Automated with rules |

**Solution**: | Fines | ⚠️ Basic calculation | ✅ Auto-calculated with limits |

- Use default credentials: admin/admin123| Reservations | ❌ None | ✅ Queue system |

- Check if database was imported correctly| Ratings & Reviews | ❌ None | ✅ Full system |

- Verify user exists: `SELECT * FROM users;` in MySQL| Recommendations | ❌ None | ✅ AI-powered |

| Analytics | ❌ None | ✅ Comprehensive dashboards |

## 🔧 Development| Notifications | ❌ None | ✅ Email + In-app + SMS |

| Reports | ❌ None | ✅ Excel/PDF exports |

### Virtual Environment (Recommended)| Multi-library | ❌ Single | ✅ Multiple locations |

```bash| UI/UX | ⚠️ Basic | ✅ Modern & responsive |

# Create virtual environment| Mobile Support | ❌ No | ✅ Yes |

python -m venv .venv| Dark Mode | ❌ No | ✅ Yes |



# Activate---

source .venv/bin/activate  # macOS/Linux

.venv\Scripts\activate     # Windows## 🛠️ Configuration



# Install dependencies### Database Configuration

pip install -r requirements.txt

```Edit `.env` file:

```env

### Running in Development ModeDB_HOST=localhost

```bashDB_PORT=3306

streamlit run litgrid_single.py --server.runOnSave trueDB_USER=root

```DB_PASSWORD=your_password

DB_NAME=litgrid

## 📦 Dependencies```



Core packages (see `requirements.txt`):### Application Settings

- **streamlit** >= 1.29.0 - Web framework

- **mysql-connector-python** - MySQL database connectorEdit `config.yaml` to customize:

- **bcrypt** - Password hashing- Borrowing periods and limits

- **python-dotenv** - Environment configuration- Fine amounts and caps

- **plotly** - Interactive charts- Member tier privileges

- **pandas** - Data manipulation- Notification preferences

- **pyyaml** - YAML configuration- UI theme colors

- Feature toggles

## 🔐 Security Best Practices

---

1. **Change Default Passwords**: Immediately change admin password after first login

2. **Environment Variables**: Never commit `.env` file to version control## 📊 Database Schema Highlights

3. **Database Access**: Use non-root MySQL user in production

4. **HTTPS**: Use HTTPS in production (reverse proxy recommended)### Key Tables

5. **Regular Backups**: Backup database regularly- **users** - User accounts with roles and tiers

- **books** - Comprehensive book catalog

## 📈 Future Enhancements- **book_inventory** - Physical book copies across libraries

- **borrowing** - Checkout and return tracking

Planned features (see database schema):- **reservations** - Book reservation queue

- ✅ Book ratings and reviews- **book_ratings** - User ratings and reviews

- ✅ Reading history tracking- **notifications** - System notifications

- ✅ Book reservations- **audit_log** - Complete audit trail

- 📧 Email notifications

- 📱 SMS alerts### Advanced Features

- 📊 Advanced reporting- **Triggers** for automatic inventory updates

- 🔍 Full-text search- **Stored procedures** for complex operations

- 📚 Digital book management- **Views** for optimized queries

- 💳 Online fine payment- **Statistics tables** for fast analytics

- 📱 Mobile app support- **Full-text search** indexes



## 📄 License---



This project is open source and available for educational purposes.## 🎨 User Interface



## 🤝 Contributing### For Members

- **Browse books** with beautiful cover displays

Contributions are welcome! Please feel free to submit issues or pull requests.- **Search & filter** with advanced options

- **View book details** with ratings and reviews

## 📞 Support- **Borrow and reserve** books online

- **Track borrowed books** and due dates

For issues or questions:- **Receive notifications** for due dates and holds

1. Check the troubleshooting section- **Get personalized recommendations**

2. Review database logs: `SHOW VARIABLES LIKE 'log_error';`- **View reading history** and statistics

3. Check application logs in terminal

### For Librarians

## 🎉 Credits- **Manage book catalog** (add, edit, delete)

- **Process checkouts and returns**

Built with:- **Handle reservations**

- [Streamlit](https://streamlit.io/) - Web framework- **View member information**

- [MySQL](https://www.mysql.com/) - Database- **Generate reports**

- [Plotly](https://plotly.com/) - Data visualization- **Monitor overdue books**

- [bcrypt](https://github.com/pyca/bcrypt/) - Security- **Send notifications**



---### For Admins

- All librarian features plus:

**Version**: 2.0.0  - **User management** (create, edit, roles)

**Last Updated**: October 2025  - **System settings** configuration

**Status**: ✅ Production Ready- **Analytics dashboard**

- **Audit logs** viewing
- **Multi-library management**

---

## 🔒 Security Features

- **Password hashing** with bcrypt (salt rounds: 12)
- **Session management** with configurable timeout
- **Role-based access control** (RBAC)
- **SQL injection protection** via parameterized queries
- **Input validation** and sanitization
- **Audit logging** of all critical actions
- **Secure file uploads** with type validation

---

## 📧 Email Notifications

Configure SMTP settings in `.env`:
```env
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your-email@example.com
SMTP_PASSWORD=your-email-password
SMTP_FROM_EMAIL=noreply@litgrid.com
```

Automatic emails for:
- Due date reminders (2 days before)
- Overdue notices
- Reserved book availability
- Registration confirmation
- Password reset (if enabled)

---

## 🚧 Future Enhancements

- [ ] Mobile app (React Native / Flutter)
- [ ] Digital book support (EPUB, PDF readers)
- [ ] Integration with library catalog APIs
- [ ] Blockchain for transaction immutability
- [ ] AI chatbot for member support
- [ ] Social features (book clubs, discussions)
- [ ] Event management for library programs
- [ ] Resource booking (study rooms, computers)
- [ ] Multi-language support

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👥 Authors

- **Your Name** - Initial work - [YourGitHub](https://github.com/yourusername)

---

## 🙏 Acknowledgments

- Original project inspiration from [RohanRJ389/LibraryManagementSystem](https://github.com/RohanRJ389/LibraryManagementSystem)
- Streamlit for the amazing framework
- The open-source community

---

## 📞 Support

For support, email support@litgrid.com or open an issue on GitHub.

---

<div align="center">

**Built with ❤️ using Streamlit and MySQL**

⭐ Star this repo if you find it helpful!

</div>






