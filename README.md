# dat_project3
# Store Management System

A simple desktop application for managing a small store, built with **Python** and **PyQt5**. The system supports managing products, invoices, and customers, with data stored in JSON files.

## 🚀 Key Features

- **Product Management**: Add, edit, delete, and search products (Books and Music Discs).
- **Invoice Management**: Create and save invoices with product and customer details.
- **Data Storage**: All information is stored in JSON files—no database required.

## 🧱 Project Structure

```
store_test/
├── data/               # JSON files for products and invoices
├── models/             # Data models: Product, Invoice, Customer
├── storage/            # Load/save data to/from JSON files
├── support/            # Business logic helpers for invoices and products
├── ui/                 # PyQt5 user interface components
├── main_gui.py         # Entry point of the GUI application
```

## ⚙️ Setup Instructions

### Requirements

- Python 3.10+
- Dependencies:
  ```bash
  pip install PyQt5
  ```

### Run the Application

```bash
python main_gui.py
```

## 📦 Data Format

All data is stored in the `data/` folder:

- `products.json`: Product list
- `invoices.json`: Invoice list

## ✨ Extensibility

The project is modular and can be easily extended with new features, such as:

- Integration with SQLite or MySQL databases
- Revenue and inventory reports
- User roles and authentication (e.g., Admin vs. Staff)

