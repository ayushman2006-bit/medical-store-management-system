# Pharmaceutical Management System

A desktop-based pharmaceutical inventory and billing management system built with Python and MySQL.

The application helps manage medicines, track inventory, generate bills, monitor stock levels, and identify medicines that are expired or nearing expiry.

## Features

- Medicine inventory management
- Add, search, update, and delete medicines
- Medicine name autocomplete
- Low-stock monitoring
- Inventory value calculation
- Expiry and upcoming-expiry alerts
- Billing system
- Automatic stock deduction after successful billing
- Transaction-safe billing with rollback support
- Bill history
- MySQL database integration
- Environment-based database configuration
- Modular database architecture

## Technologies Used

- Python
- Tkinter / ttkbootstrap
- MySQL
- MySQL Connector/Python
- python-dotenv

## Project Structure

```text
medical-store-management-system/
│
├── .env.example
├── .gitignore
├── billing_db.py
├── db_connection.py
├── main.py
├── medicine_db.py
├── requirements.txt
└── schema.sql
## Screenshots
```
## Screenshots

### Main Dashboard

<p align="center">
  <img src="screenshots/Main_UI.jpeg" width="90%">
</p>

### Application Features

<p align="center">
  <img src="screenshots/search_update_with_autocomplete_feature.jpeg" width="48%">
  <img src="screenshots/bill_generate.jpeg" width="48%">
</p>

<p align="center">
  <img src="screenshots/bill_history.jpeg" width="48%">
  <img src="screenshots/low_stock.jpeg" width="48%">
</p>

<p align="center">
  <img src="screenshots/expiry_date_warning.jpeg" width="48%">
</p>
