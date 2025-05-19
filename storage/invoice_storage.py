import json
from models.invoice import Invoice
from models.product import Book, MusicDisc


def load_invoices(filename="data/invoices.json"):
    try:
        with open(filename, "r", encoding="utf-8") as f:
            data = json.load(f)
        return [Invoice.from_dict(inv, product_loader) for inv in data]
    except (json.JSONDecodeError, FileNotFoundError):
        return []


def save_invoice(invoice, filename="data/invoices.json"):
    try:
        with open(filename, "r", encoding="utf-8") as f:
            data = json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        data = []

    data.append(invoice.to_dict())

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)


def product_loader(data):
    if data["type"] == "Book":
        return Book.from_dict(data)
    elif data["type"] == "MusicDisc":
        return MusicDisc.from_dict(data)
    else:
        raise ValueError(f"Không xác định được loại sản phẩm: {data['type']}")