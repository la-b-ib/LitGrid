# 📚 LitGrid v4.0 - Advanced Library Management System

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






