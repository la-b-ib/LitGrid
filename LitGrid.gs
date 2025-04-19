/**
 * LitGrid
 * Complete solution using Google Sheets + Apps Script
 * File: LitGrid.gs
 */

/*********************
 * CONFIGURATION
 *********************/
const CONFIG = {
  sheetId: SpreadsheetApp.getActiveSpreadsheet().getId(),
  finePerDay: 0.50, // $0.50 per day fine
  maxCheckoutDays: 14, // 2 weeks checkout period
  maxBooksPerMember: 5,
  appName: "LitGrid",
  version: "1.0"
};

/*********************
 * MAIN MENU SETUP
 *********************/
function onOpen() {
  const ui = SpreadsheetApp.getUi();
  const menu = ui.createMenu(CONFIG.appName);
  
  menu.addItem('Dashboard', 'showDashboard');
  menu.addSeparator();
  menu.addSubMenu(
    ui.createMenu('Books')
      .addItem('Add New Book', 'showAddBookForm')
      .addItem('Search Books', 'showBookSearch')
  );
  menu.addSubMenu(
    ui.createMenu('Members')
      .addItem('Add New Member', 'showAddMemberForm')
      .addItem('Search Members', 'showMemberSearch')
  );
  menu.addSubMenu(
    ui.createMenu('Transactions')
      .addItem('Check Out Book', 'showCheckoutForm')
      .addItem('Check In Book', 'showCheckinForm')
  );
  menu.addSubMenu(
    ui.createMenu('Reports')
      .addItem('Inventory Report', 'generateInventoryReport')
      .addItem('Overdue Books', 'generateOverdueReport')
      .addItem('Member Activity', 'generateMemberActivityReport')
  );
  menu.addSeparator();
  menu.addItem('About', 'showAbout');
  
  menu.addToUi();
}

/*********************
 * CORE FUNCTIONS
 *********************/

// BOOK MANAGEMENT
function addBook(bookData) {
  const sheet = getSheetByName('Books');
  const isbn = bookData.isbn || generateUniqueId('ISBN');
  
  const newRow = [
    isbn,
    bookData.title,
    bookData.author,
    bookData.publisher,
    bookData.publicationYear,
    bookData.genre,
    bookData.pages,
    bookData.copies,
    bookData.copies, // Available equals copies when new
    bookData.location,
    new Date(),
    new Date()
  ];
  
  sheet.appendRow(newRow);
  return { success: true, isbn };
}

function searchBooks(query) {
  const sheet = getSheetByName('Books');
  const data = sheet.getRange(2, 1, sheet.getLastRow() - 1, 12).getValues();
  
  const results = data.filter(book => {
    return (
      book[0].toString().toLowerCase().includes(query.toLowerCase()) || // ISBN
      book[1].toString().toLowerCase().includes(query.toLowerCase()) || // Title
      book[2].toString().toLowerCase().includes(query.toLowerCase())   // Author
    );
  }).map(book => ({
    isbn: book[0],
    title: book[1],
    author: book[2],
    publisher: book[3],
    copies: book[7],
    available: book[8]
  }));
  
  return results.slice(0, 10); // Return top 10 results
}

// MEMBER MANAGEMENT
function addMember(memberData) {
  const sheet = getSheetByName('Members');
  const memberId = generateUniqueId('M');
  
  const newRow = [
    memberId,
    memberData.name,
    memberData.email,
    memberData.phone,
    memberData.address,
    new Date(),
    'Active',
    memberData.notes || ''
  ];
  
  sheet.appendRow(newRow);
  return { success: true, memberId };
}

function searchMembers(query) {
  const sheet = getSheetByName('Members');
  const data = sheet.getRange(2, 1, sheet.getLastRow() - 1, 8).getValues();
  
  const results = data.filter(member => {
    return (
      member[0].toString().toLowerCase().includes(query.toLowerCase()) || // Member ID
      member[1].toString().toLowerCase().includes(query.toLowerCase()) || // Name
      member[2].toString().toLowerCase().includes(query.toLowerCase()) || // Email
      (member[3] && member[3].toString().toLowerCase().includes(query.toLowerCase())) // Phone
    );
  }).map(member => ({
    id: member[0],
    name: member[1],
    email: member[2],
    phone: member[3],
    status: member[6]
  }));
  
  return results.slice(0, 10); // Return top 10 results
}

// TRANSACTION MANAGEMENT
function checkoutBook(isbn, memberId) {
  const booksSheet = getSheetByName('Books');
  const membersSheet = getSheetByName('Members');
  const transactionsSheet = getSheetByName('Transactions');
  
  // Validate member
  const memberData = membersSheet.getRange(2, 1, membersSheet.getLastRow() - 1, 8)
    .getValues()
    .find(m => m[0] === memberId);
  
  if (!memberData) {
    return { success: false, error: 'Member not found' };
  }
  
  if (memberData[6] !== 'Active') {
    return { success: false, error: 'Member is not active' };
  }
  
  // Validate book
  const bookData = booksSheet.getRange(2, 1, booksSheet.getLastRow() - 1, 12)
    .getValues()
    .find(b => b[0] === isbn);
  
  if (!bookData) {
    return { success: false, error: 'Book not found' };
  }
  
  if (bookData[8] < 1) {
    return { success: false, error: 'No copies available' };
  }
  
  // Check if member has reached max checkout limit
  const memberTransactions = transactionsSheet.getRange(2, 1, transactionsSheet.getLastRow() - 1, 8)
    .getValues()
    .filter(t => t[2] === memberId && t[6] === 'Checked Out');
  
  if (memberTransactions.length >= CONFIG.maxBooksPerMember) {
    return { success: false, error: 'Member has reached maximum checkout limit' };
  }
  
  // Create transaction
  const transactionId = generateUniqueId('T');
  const checkoutDate = new Date();
  const dueDate = new Date();
  dueDate.setDate(dueDate.getDate() + CONFIG.maxCheckoutDays);
  
  transactionsSheet.appendRow([
    transactionId,
    isbn,
    memberId,
    checkoutDate,
    dueDate,
    null, // Return date
    'Checked Out',
    0 // Fine amount
  ]);
  
  // Update book availability
  const bookRow = booksSheet.getRange(2, 1, booksSheet.getLastRow() - 1, 12)
    .getValues()
    .findIndex(b => b[0] === isbn) + 2;
  
  const availableCol = 9; // Column I
  booksSheet.getRange(bookRow, availableCol).setValue(bookData[8] - 1);
  
  return { 
    success: true,
    transactionId,
    dueDate: formatDate(dueDate)
  };
}

function checkinBook(isbn, memberId) {
  const booksSheet = getSheetByName('Books');
  const transactionsSheet = getSheetByName('Transactions');
  const finesSheet = getSheetByName('Fines');
  
  // Find the transaction
  const transactions = transactionsSheet.getRange(2, 1, transactionsSheet.getLastRow() - 1, 8).getValues();
  const transactionIndex = transactions.findIndex(t => 
    t[1] === isbn && t[2] === memberId && t[6] === 'Checked Out'
  );
  
  if (transactionIndex === -1) {
    return { success: false, error: 'No matching checkout found' };
  }
  
  const transaction = transactions[transactionIndex];
  const returnDate = new Date();
  const dueDate = new Date(transaction[4]);
  
  // Calculate fine if overdue
  let fineAmount = 0;
  if (returnDate > dueDate) {
    const diffDays = Math.ceil((returnDate - dueDate) / (1000 * 60 * 60 * 24));
    fineAmount = diffDays * CONFIG.finePerDay;
    
    // Record fine
    finesSheet.appendRow([
      generateUniqueId('F'),
      transaction[0],
      memberId,
      fineAmount,
      'Unpaid',
      null,
      `Overdue by ${diffDays} days`
    ]);
  }
  
  // Update transaction
  const transactionRow = transactionIndex + 2;
  transactionsSheet.getRange(transactionRow, 6).setValue(returnDate); // Return date
  transactionsSheet.getRange(transactionRow, 7).setValue('Returned'); // Status
  transactionsSheet.getRange(transactionRow, 8).setValue(fineAmount); // Fine amount
  
  // Update book availability
  const bookData = booksSheet.getRange(2, 1, booksSheet.getLastRow() - 1, 12)
    .getValues()
    .find(b => b[0] === isbn);
  
  const bookRow = booksSheet.getRange(2, 1, booksSheet.getLastRow() - 1, 12)
    .getValues()
    .findIndex(b => b[0] === isbn) + 2;
  
  const availableCol = 9; // Column I
  booksSheet.getRange(bookRow, availableCol).setValue(bookData[8] + 1);
  
  return { 
    success: true,
    fineAmount: fineAmount.toFixed(2),
    isOverdue: fineAmount > 0
  };
}

/*********************
 * UI FUNCTIONS
 *********************/

function showDashboard() {
  const html = HtmlService.createHtmlOutputFromFile('Dashboard')
    .setWidth(1000)
    .setHeight(600)
    .setTitle(`${CONFIG.appName} Dashboard`);
  
  SpreadsheetApp.getUi().showModalDialog(html, 'Library Dashboard');
}

function showAddBookForm() {
  const html = HtmlService.createHtmlOutputFromFile('AddBookForm')
    .setWidth(500)
    .setHeight(600);
  
  SpreadsheetApp.getUi().showModalDialog(html, 'Add New Book');
}

function showAddMemberForm() {
  const html = HtmlService.createHtmlOutputFromFile('AddMemberForm')
    .setWidth(500)
    .setHeight(500);
  
  SpreadsheetApp.getUi().showModalDialog(html, 'Add New Member');
}

function showCheckoutForm() {
  const html = HtmlService.createHtmlOutputFromFile('CheckoutForm')
    .setWidth(600)
    .setHeight(600);
  
  SpreadsheetApp.getUi().showModalDialog(html, 'Check Out Book');
}

function showCheckinForm() {
  const html = HtmlService.createHtmlOutputFromFile('CheckinForm')
    .setWidth(600)
    .setHeight(500);
  
  SpreadsheetApp.getUi().showModalDialog(html, 'Check In Book');
}

function showBookSearch() {
  const html = HtmlService.createHtmlOutputFromFile('BookSearch')
    .setWidth(800)
    .setHeight(600);
  
  SpreadsheetApp.getUi().showModalDialog(html, 'Search Books');
}

function showMemberSearch() {
  const html = HtmlService.createHtmlOutputFromFile('MemberSearch')
    .setWidth(800)
    .setHeight(600);
  
  SpreadsheetApp.getUi().showModalDialog(html, 'Search Members');
}

function showAbout() {
  const html = HtmlService.createHtmlOutput(`
    <style>
      body { font-family: Arial, sans-serif; margin: 20px; }
      h2 { color: #4285f4; }
      .logo { font-size: 48px; color: #4285f4; text-align: center; }
      .info { margin-top: 20px; }
    </style>
    <h2 style="text-align:center;">${CONFIG.appName}</h2>
    <div class="info">
      <p><strong>Version:</strong> ${CONFIG.version}</p>
      <p><strong>Description:</strong> LitGrid : A complete library management system built on Google Sheets and Apps Script.</p>
      <p><strong>Developer:</strong> Labib Bin Shahed</p>
      <p><strong>Email:</strong> labib-x@protonmail.com</p>
    </div>
  `).setWidth(500).setHeight(400);
  
  SpreadsheetApp.getUi().showModalDialog(html, 'About');
}

/*********************
 * REPORTING FUNCTIONS
 *********************/

function generateInventoryReport() {
  const booksSheet = getSheetByName('Books');
  const data = booksSheet.getRange(2, 1, booksSheet.getLastRow() - 1, 12).getValues();
  
  const report = data.map(book => ({
    ISBN: book[0],
    Title: book[1],
    Author: book[2],
    Available: `${book[8]}/${book[7]}`,
    Location: book[9]
  }));
  
  const html = buildReportHtml('Inventory Report', report);
  showHtmlDialog(html, 'Inventory Report', 800, 600);
}

function generateOverdueReport() {
  const transactionsSheet = getSheetByName('Transactions');
  const booksSheet = getSheetByName('Books');
  const membersSheet = getSheetByName('Members');
  
  const today = new Date();
  const transactions = transactionsSheet.getRange(2, 1, transactionsSheet.getLastRow() - 1, 8).getValues();
  
  const overdue = transactions.filter(t => {
    return t[6] === 'Checked Out' && new Date(t[4]) < today;
  });
  
  const report = overdue.map(t => {
    const book = booksSheet.getRange(2, 1, booksSheet.getLastRow() - 1, 12)
      .getValues()
      .find(b => b[0] === t[1]);
    
    const member = membersSheet.getRange(2, 1, membersSheet.getLastRow() - 1, 8)
      .getValues()
      .find(m => m[0] === t[2]);
    
    const dueDate = new Date(t[4]);
    const daysOverdue = Math.ceil((today - dueDate) / (1000 * 60 * 60 * 24));
    const fine = daysOverdue * CONFIG.finePerDay;
    
    return {
      'Transaction ID': t[0],
      'Book Title': book ? book[1] : 'Unknown',
      'Member Name': member ? member[1] : 'Unknown',
      'Due Date': formatDate(dueDate),
      'Days Overdue': daysOverdue,
      'Fine Amount': `$${fine.toFixed(2)}`
    };
  });
  
  const html = buildReportHtml('Overdue Books Report', report);
  showHtmlDialog(html, 'Overdue Books Report', 1000, 600);
}

function generateMemberActivityReport() {
  const transactionsSheet = getSheetByName('Transactions');
  const membersSheet = getSheetByName('Members');
  
  const members = membersSheet.getRange(2, 1, membersSheet.getLastRow() - 1, 8).getValues();
  const transactions = transactionsSheet.getRange(2, 1, transactionsSheet.getLastRow() - 1, 8).getValues();
  
  const report = members.map(member => {
    const memberTransactions = transactions.filter(t => t[2] === member[0]);
    
    return {
      'Member ID': member[0],
      'Name': member[1],
      'Total Checkouts': memberTransactions.length,
      'Active Checkouts': memberTransactions.filter(t => t[6] === 'Checked Out').length,
      'Overdue Items': memberTransactions.filter(t => {
        return t[6] === 'Checked Out' && new Date(t[4]) < new Date();
      }).length
    };
  });
  
  const html = buildReportHtml('Member Activity Report', report);
  showHtmlDialog(html, 'Member Activity Report', 900, 600);
}

/*********************
 * HELPER FUNCTIONS
 *********************/

function getDashboardStats() {
  const booksSheet = getSheetByName('Books');
  const membersSheet = getSheetByName('Members');
  const transactionsSheet = getSheetByName('Transactions');
  
  const totalBooks = booksSheet.getLastRow() - 1;
  const totalMembers = membersSheet.getLastRow() - 1;
  
  // Get checked out books
  const transactions = transactionsSheet.getRange(2, 1, transactionsSheet.getLastRow() - 1, 8).getValues();
  const checkedOut = transactions.filter(t => t[6] === 'Checked Out').length;
  
  // Get overdue books
  const today = new Date();
  const overdueBooks = transactions.filter(t => {
    return t[6] === 'Checked Out' && new Date(t[4]) < today;
  }).length;
  
  return {
    totalBooks,
    totalMembers,
    checkedOut,
    overdueBooks
  };
}

function getSheetByName(name) {
  return SpreadsheetApp.getActiveSpreadsheet().getSheetByName(name);
}

function generateUniqueId(prefix = '') {
  return prefix + Utilities.getUuid().split('-')[0];
}

function formatDate(date) {
  return Utilities.formatDate(date, Session.getScriptTimeZone(), "yyyy-MM-dd");
}

function buildReportHtml(title, data) {
  if (data.length === 0) {
    return `<h2>${title}</h2><p>No data found</p>`;
  }
  
  const headers = Object.keys(data[0]);
  const headerHtml = headers.map(h => `<th>${h}</th>`).join('');
  
  const rowsHtml = data.map(item => {
    const cells = headers.map(header => `<td>${item[header]}</td>`);
    return `<tr>${cells.join('')}</tr>`;
  }).join('');
  
  return `
    <style>
      body { font-family: Arial, sans-serif; margin: 20px; }
      h2 { color: #4285f4; }
      table { width: 100%; border-collapse: collapse; margin-top: 20px; }
      th { background: #4285f4; color: white; padding: 10px; text-align: left; }
      td { padding: 8px; border-bottom: 1px solid #ddd; }
      tr:hover { background: #f5f5f5; }
    </style>
    <h2>${title}</h2>
    <table>
      <thead><tr>${headerHtml}</tr></thead>
      <tbody>${rowsHtml}</tbody>
    </table>
    <p>Total records: ${data.length}</p>
  `;
}

function showHtmlDialog(html, title, width, height) {
  const htmlOutput = HtmlService.createHtmlOutput(html)
    .setWidth(width)
    .setHeight(height);
  
  SpreadsheetApp.getUi().showModalDialog(htmlOutput, title);
}

/*********************
 * INITIALIZATION
 *********************/

function initializeSystem() {
  // Create sheets if they don't exist
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  
  const sheets = ['Books', 'Members', 'Transactions', 'Fines', 'Dashboard', 'Reports'];
  sheets.forEach(sheetName => {
    if (!ss.getSheetByName(sheetName)) {
      const sheet = ss.insertSheet(sheetName);
      
      // Add headers based on sheet
      switch(sheetName) {
        case 'Books':
          sheet.appendRow([
            'ISBN', 'Title', 'Author', 'Publisher', 'Publication Year', 
            'Genre', 'Pages', 'Copies', 'Available', 'Location', 
            'Added Date', 'Last Updated'
          ]);
          break;
        case 'Members':
          sheet.appendRow([
            'Member ID', 'Name', 'Email', 'Phone', 'Address', 
            'Membership Date', 'Status', 'Notes'
          ]);
          break;
        case 'Transactions':
          sheet.appendRow([
            'Transaction ID', 'Book ISBN', 'Member ID', 'Checkout Date', 
            'Due Date', 'Return Date', 'Status', 'Fine Amount'
          ]);
          break;
        case 'Fines':
          sheet.appendRow([
            'Fine ID', 'Transaction ID', 'Member ID', 'Amount', 
            'Paid Status', 'Payment Date', 'Notes'
          ]);
          break;
      }
      
      // Format headers
      const headerRange = sheet.getRange(1, 1, 1, sheet.getLastColumn());
      headerRange.setFontWeight('bold');
      headerRange.setBackground('#f0f0f0');
    }
  });
  
  // Hide some sheets from direct user access
  ['Transactions', 'Fines'].forEach(sheetName => {
    const sheet = ss.getSheetByName(sheetName);
    if (sheet) sheet.hideSheet();
  });
  
  // Set up the dashboard sheet
  const dashboard = ss.getSheetByName('Dashboard');
  if (dashboard) {
    dashboard.clear();
    dashboard.appendRow(['Welcome to LitGrid']);
    dashboard.getRange('A1').setFontSize(18).setFontWeight('bold');
    dashboard.getRange('A2').setValue('Use the custom menu to access all features');
  }
  
  // Add some sample data if sheets are empty
  addSampleDataIfEmpty();
}

function addSampleDataIfEmpty() {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  
  // Sample books
  const booksSheet = ss.getSheetByName('Books');
  if (booksSheet.getLastRow() <= 1) {
    const sampleBooks = [
      ['978-0061120084', 'To Kill a Mockingbird', 'Harper Lee', 'HarperCollins', 1960, 'Fiction', 336, 5, 5, 'Fiction A1'],
      ['978-0451524935', '1984', 'George Orwell', 'Signet Classics', 1949, 'Dystopian', 328, 3, 3, 'Fiction B2'],
      ['978-0743273565', 'The Great Gatsby', 'F. Scott Fitzgerald', 'Scribner', 1925, 'Classic', 180, 4, 4, 'Fiction A3']
    ];
    sampleBooks.forEach(book => booksSheet.appendRow(book));
  }
  
  // Sample members
  const membersSheet = ss.getSheetByName('Members');
  if (membersSheet.getLastRow() <= 1) {
    const sampleMembers = [
      ['M1001', 'John Smith', 'john@example.com', '555-0101', '123 Main St', new Date(), 'Active', ''],
      ['M1002', 'Jane Doe', 'jane@example.com', '555-0102', '456 Oak Ave', new Date(), 'Active', '']
    ];
    sampleMembers.forEach(member => membersSheet.appendRow(member));
  }
}
