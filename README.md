# Britez Footwear Billing System

## Overview
A comprehensive desktop application for managing product sales, billing, and inventory tracking for a footwear store.

## Features
- Product Management
- Invoice Generation
- Transaction Tracking
- Admin Panel
- PDF Invoice Export

## Prerequisites
- Python 3.8+
- Required Libraries:
  - customtkinter
  - sqlite3
  - fpdf
  - tkinter

## Installation

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/britez-footwear-billing.git
cd britez-footwear-billing
```

### 2. Install Dependencies
```bash
pip install customtkinter fpdf
```

## Configuration
- Default Admin Password: `2345`
- Database: `britez_footwear.db` (SQLite)

## Usage

### Running the Application
```bash
python billing_system.py
```

### Main Screens
1. **Home Screen**
   - Billing Page
   - Admin Page
   - Exit

2. **Billing Page**
   - Enter Customer Details
   - Add Products
   - Generate Invoice
   - Payment Processing

3. **Admin Panel**
   - Add Products
   - View Database
   - Transaction History

## Database Schema

### Products Table
- ProductID (Primary Key)
- Name
- Price

### Transactions Table
- TransactionID (Primary Key)
- CustomerName
- Phone
- Products
- Quantity
- TotalPrice
- CustomerCashGiven
- Balance
- PaymentMode
- Date

## Security
- Admin access protected by password
- Secure transaction recording

## Troubleshooting
- Ensure all dependencies are installed
- Check database connectivity
- Verify Python version compatibility

## Contributing
1. Fork the repository
2. Create feature branch
3. Commit changes
4. Push to branch
5. Create pull request



