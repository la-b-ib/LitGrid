# 📚 LitGrid - Library Management System

A modern, comprehensive library management system built with Python and Streamlit.

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- MySQL/MariaDB 8.0+

### Installation

1. Install dependencies
```bash
pip install -r requirements.txt
```

2. Configure database - Edit .env file:
```env
DB_HOST=localhost
DB_PORT=3306
DB_USER=your_user
DB_PASSWORD=your_password
DB_NAME=litgrid
```

3. Run the application
```bash
streamlit run litgrid.py
```

4. Access the app at http://localhost:8501

## 🔑 Default Login

- Username: admin
- Password: admin123

⚠️ Change the password after first login!

## ✨ Features

- Book Management (Add, Edit, Delete, Search)
- User Management (Roles, Tiers, Profiles)
- Borrowing & Returns System
- Fine Tracking & Payments
- Reports & Analytics
- Barcode & QR Code Generation
- Database Backup & Restore
- Excel Export
- Smart Search

## 📦 Tech Stack

- Framework: Streamlit
- Database: MySQL/MariaDB
- Language: Python 3.9+
- Visualization: Plotly

## 📁 Files

- litgrid.py - Main application
- requirements.txt - Dependencies
- .env - Database config
- .streamlit/ - App configuration

## 🔧 Troubleshooting

Database connection failed: Check .env credentials

Module not found: pip install -r requirements.txt

Port in use: streamlit run litgrid.py --server.port 8502

---

Made with ❤️ and Python
