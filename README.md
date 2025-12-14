## <samp>LitGrid

<samp>
  
**LitGrid is a comprehensive, modern library management system designed for educational institutions, public libraries, and private collections. Built with **Python**, **Streamlit**, and SQLite, it offers a complete solution for managing books, users, borrowing activities, and administrative tasks. </samp>**

<hr>

<details>
  
**<summary>LitGrid Overview</summary>**

- **Project Goals – Full library management (catalog, users, borrowing, fines), intuitive dashboards, advanced analytics, multi-layer security, MIT open source.**

- **Unique Value – Single-file Python deployment (7.9k LOC), PDF sharing system, fuzzy search, real-time analytics, privacy controls, multi-role support, offline SQLite storage.**

- **Core Features – Catalog & user management, check-in/out with renewals, fine tracking, inventory with barcodes, AI-powered recommendations, role-based dashboards, community reviews, personal analytics.**

- **Enterprise Tools – 20+ visualizations, financial/member/collection reports, MFA, encryption, audit logs, rate limiting, DB backup/restore, bulk ops, barcode/QR utilities, JSON config manager.**

</details>

<details>
  
**<summary>LitGrid Preview</summary>**

<p align="left">
  <img src="https://raw.githubusercontent.com/la-b-ib/LitGrid/main/preview/img/prev%207.png" width="32%" />

  <img src="https://raw.githubusercontent.com/la-b-ib/LitGrid/main/preview/img/prev%209.png" width="32%" />
  <img src="https://raw.githubusercontent.com/la-b-ib/LitGrid/main/preview/img/prev%205.png" width="32%" />
  <img src="https://raw.githubusercontent.com/la-b-ib/LitGrid/main/preview/img/prev%203.png" width="32%" /> 
  <img src="https://raw.githubusercontent.com/la-b-ib/LitGrid/main/preview/img/prev%2010.png" width="32%" />
  <img src="https://raw.githubusercontent.com/la-b-ib/LitGrid/main/preview/img/prev%2011.png" width="32%" />
</p>



</details>



<details>
  
**<summary>System Architecture</summary>**


```mermaid
%%{init: {'theme': 'base', 'themeVariables': { 'primaryColor': '#fff', 'edgeLabelBackground':'#fff', 'tertiaryColor': '#f4f4f4'}, 'flowchart': {'curve': 'basis', 'nodeSpacing': 50, 'rankSpacing': 50}} }%%

flowchart TD
    %% Global Styling
    classDef presentation stroke:#1565c0,stroke-width:6px,color:#0d47a1,rx:10,ry:10;
    classDef business stroke:#7b1fa2,stroke-width:6px,color:#4a148c,rx:10,ry:10;
    classDef data stroke:#2e7d32,stroke-width:6px,color:#1b5e20,rx:10,ry:10;
    classDef storage stroke:#e65100,stroke-width:6px,color:#bf360c,rx:5,ry:5;
    classDef external stroke:#c2185b,stroke-width:6px,color:#880e4f,rx:10,ry:10;

    %% Nodes (no subgraph boxes)
    A[**Streamlit Web Interface**]
    B[**User Authentication**]
    C[**Role-Based Navigation**]

    D[**User Management**]
    E[**Book Management**]
    F[**Borrowing System**]
    G[**Analytics Engine**]
    H[**Security Manager**]
    I[**PDF Library Manager**]

    J[**Database Manager**]
    K[**File Handler**]
    L[**Cache Manager**]

    M[(**SQLite Database**)]
    N[(**File System Storage**)]
    O[(**Session State**)]

    P[**Email Service**]
    Q[**Backup System**]
    R[**Export Services**]

    %% Connections (all solid and bold)
    A ==> B
    A ==> C
    
    B ==> H
    
    C ==> D
    C ==> E
    C ==> F
    C ==> G
    C ==> I

    D ==> J
    E ==> J
    F ==> J
    G ==> J
    H ==> J
    I ==> J
    I ==> K
    
    J ==> M
    J ==> O
    K ==> N
    
    G ==> P
    F ==> P
    J ==> Q
    G ==> R

    %% Assign Classes
    class A,B,C presentation
    class D,E,F,G,H,I business
    class J,K,L data
    class M,N,O storage
    class P,Q,R external

```

</details>

## Core Components
 

- **Presentation Layer** – Streamlit UI with custom CSS, secure session authentication, and role‑based dynamic navigation.  
- **Business Logic Layer** – User and book management with CRUD, fuzzy search, AI recommendations, borrowing/renewals/fines, analytics engine, encryption, audit logging, RBAC, and advanced PDF library with privacy controls.  
- **Data Layer** – SQLite with connection pooling and integrity checks, PDF/image handling with backup/restore, and cache manager for session state and temporary data.  

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




#### Genre Performance Tracking


- **Library Metrics** – Real‑time stats (books, users, transactions, fines), trend analysis, performance indicators, and health monitoring.  
- **Genre & Community Insights** – Circulation by genre, user preferences, seasonal trends, collection balance, leaderboards, reviews, and PDF contributions.  
- **Advanced Analytics** – Multi‑dimensional visualizations (3D plots, heatmaps), correlation analysis, and predictive demand forecasting.  
- **Password Security** – Bcrypt hashing with salt, complexity validation, token‑based reset, and secure session management.




<details>
  
**<summary>Libraries & Dependencies</summary>**
  

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


</details>
