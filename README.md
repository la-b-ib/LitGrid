## LitGrid  <a href=""><img align="right" width="150" height="150" src="https://raw.githubusercontent.com/la-b-ib/LitGrid/main/preview/gif/book.gif"></a>

<samp>
  
**LitGrid** is a comprehensive, modern library management system designed for educational institutions, public libraries, and private collections. Built with **Python**, **Streamlit**, and **SQLite**, it offers a complete solution for managing books, users, borrowing activities, and administrative tasks. </samp>

<hr>

<div align="left">

![LitGrid Logo](https://img.shields.io/badge/LitGrid-v4.0-blue?style=for-the-badge&logo=library)
[![License: AGPL v3](https://img.shields.io/badge/License-AGPL%20v3-blue.svg?style=for-the-badge)](https://www.gnu.org/licenses/agpl-3.0)
[![Python](https://img.shields.io/badge/Python-3.13+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io/)
[![SQLite](https://img.shields.io/badge/SQLite-07405E?style=for-the-badge&logo=sqlite&logoColor=white)](https://www.sqlite.org/)
[![Live Demo](https://img.shields.io/badge/Live-Demo-brightgreen?style=for-the-badge)](https://litgrid.streamlit.app/)


</div>

---
## Overview

- Project Goals – Full library management (catalog, users, borrowing, fines), intuitive dashboards, advanced analytics, multi-layer security, MIT open source.

- Unique Value – Single-file Python deployment (7.9k LOC), PDF sharing system, fuzzy search, real-time analytics, privacy controls, multi-role support, offline SQLite storage.

- Core Features – Catalog & user management, check-in/out with renewals, fine tracking, inventory with barcodes, AI-powered recommendations, role-based dashboards, community reviews, personal analytics.

- Enterprise Tools – 20+ visualizations, financial/member/collection reports, MFA, encryption, audit logs, rate limiting, DB backup/restore, bulk ops, barcode/QR utilities, JSON config manager.

## LitGrid Preview

<p align="left">
  <img src="https://raw.githubusercontent.com/la-b-ib/LitGrid/main/preview/img/prev%201.png" width="32%" />
  <img src="https://raw.githubusercontent.com/la-b-ib/LitGrid/main/preview/img/prev%202.png" width="32%" />
  <img src="https://raw.githubusercontent.com/la-b-ib/LitGrid/main/preview/img/prev%203.png" width="32%" />    
</p>
<p align="left">
  <img src="https://raw.githubusercontent.com/la-b-ib/LitGrid/main/preview/img/prev%204.png" width="32%" />
  <img src="https://raw.githubusercontent.com/la-b-ib/LitGrid/main/preview/img/prev%205.png" width="32%" />
  <img src="https://raw.githubusercontent.com/la-b-ib/LitGrid/main/preview/img/prev%206.png" width="32%" />    
</p>
<p align="left">
  <img src="https://raw.githubusercontent.com/la-b-ib/LitGrid/main/preview/img/prev%207.png" width="32%" />
  <img src="https://raw.githubusercontent.com/la-b-ib/LitGrid/main/preview/img/prev%208.png" width="32%" />
  <img src="https://raw.githubusercontent.com/la-b-ib/LitGrid/main/preview/img/prev%209.png" width="32%" />    
</p>
<p align="left">
  <img src="https://raw.githubusercontent.com/la-b-ib/LitGrid/main/preview/img/prev%2010.png" width="32%" />
  <img src="https://raw.githubusercontent.com/la-b-ib/LitGrid/main/preview/img/prev%2011.png" width="32%" />
  <img src="https://raw.githubusercontent.com/la-b-ib/LitGrid/main/preview/img/prev%2012.png" width="32%" />    
</p>

<hr>




## System Architecture

**LitGrid follows a modular, layered architecture designed for maintainability and scalability:**

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
<hr>

## Core Components
 

- **Presentation Layer** – Streamlit UI with custom CSS, secure session authentication, and role‑based dynamic navigation.  
- **Business Logic Layer** – User and book management with CRUD, fuzzy search, AI recommendations, borrowing/renewals/fines, analytics engine, encryption, audit logging, RBAC, and advanced PDF library with privacy controls.  
- **Data Layer** – SQLite with connection pooling and integrity checks, PDF/image handling with backup/restore, and cache manager for session state and temporary data.  

---

## Database Schema

**LitGrid uses a comprehensive SQLite database with 25+ tables supporting all features:**

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

<hr>

## Key Relationships  <a href=""><img align="right" width="150" height="150" src="https://raw.githubusercontent.com/la-b-ib/LitGrid/main/preview/gif/interface.gif"></a>

- **Users ↔ Books**: Many-to-many through borrowing and transactions
- **Books ↔ Inventory**: One-to-many for multiple copies
- **Users ↔ PDF Library**: One-to-many for personal collections
- **Books ↔ Reviews**: One-to-many for community feedback
- **Users ↔ Privacy**: One-to-one for personal settings

---



### ⚡ Quick Start (5 minutes)


**Prerequisites** – Requires Python 3.13+, pip, Git, and SQLite3 (bundled with Python).
* **Setup** – `git clone https://github.com/la-b-ib/LitGrid.git && cd LitGrid` → `pip install -r requirements.txt`  
* **Run** – `streamlit run litgrid.py` → open `http://localhost:8501`  
* **Access** – Login with demo (`demo/demo123`) or register as new member to explore features.  




## User Roles & Permissions



* **Member** – Browse/search catalog, manage profile, upload/share PDFs, request checkouts/returns, rate/review, track stats.  
* **Librarian** – Member rights + manage books/inventory, process/approve checkouts/renewals, handle fines/payments, generate reports.  
* **Administrator** – Librarian rights + user management, system config, DB backup/restore, advanced analytics, security/audit, monitoring.  


## Authentication System


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
<hr>

### 🔒 Admin Security
- **Primary Login**: Standard username/password
- **Security Key**: Additional password for sensitive operations
- **Functional Admin**: Hidden admin with special privileges
- **Session Management**: Automatic timeout and renewal

<hr>

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
<hr>

### 🔄 Borrowing Process


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


## **Authentication & Authorization**

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


- **Library Metrics** – Real‑time stats (books, users, transactions, fines), trend analysis, performance indicators, and health monitoring.  
- **Genre & Community Insights** – Circulation by genre, user preferences, seasonal trends, collection balance, leaderboards, reviews, and PDF contributions.  
- **Advanced Analytics** – Multi‑dimensional visualizations (3D plots, heatmaps), correlation analysis, and predictive demand forecasting.  
- **Password Security** – Bcrypt hashing with salt, complexity validation, token‑based reset, and secure session management.


---

## **Libraries & Dependencies**


| Library       | Purpose              | Version  | Type            | Key Feature              | Usage Context            |
|---------------|----------------------|----------|-----------------|--------------------------|--------------------------|
| `streamlit`   | Web UI Framework     | 1.35.0+  | Frontend        | Responsive dashboards    | Presentation Layer       |
| `pandas`      | Data Analysis        | 2.2.0+   | Data Handling   | Tabular data ops         | Business Logic Layer     |
| `plotly`      | Data Visualization   | 5.20.0+  | Visualization   | Interactive charts       | Analytics Engine         |
| `bcrypt`      | Password Hashing     | 4.2.0+   | Security        | Secure password storage  | Auth System              |
| `cryptography`| Data Encryption      | 42.0.0+  | Security        | Encryption primitives    | Security Manager         |
| `fuzzywuzzy`  | Fuzzy String Matching| 0.18.0+  | Search Engine   | Typo‑tolerant matching   | Smart Search             |
| `qrcode`      | QR Code Generation   | 7.4.2+   | Utility         | QR code creation         | Admin Tools              |
| `openpyxl`    | Excel File Handling  | 3.1.0+   | Data I/O        | XLSX read/write          | Bulk Operations          |
| `pillow`      | Image Processing     | 10.4.0+  | Media Handling  | Image manipulation       | File Handler             |


<hr>
