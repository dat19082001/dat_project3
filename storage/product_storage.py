import json
from models.product import Book, MusicDisc


def load_products(filename="data/products.json"):
    try:
        with open(filename, "r", encoding="utf-8") as f:
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        # Nếu file không tồn tại hoặc bị rỗng/sai định dạng → trả danh sách rỗng
        return []

    products = []
    for item in data:
        if item["type"] == "Book":
            products.append(Book.from_dict(item))
        elif item["type"] == "MusicDisc":
            products.append(MusicDisc.from_dict(item))
    return products


def save_products(products, filename="data/products.json"):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump([p.to_dict() for p in products], f, indent=4, ensure_ascii=False)
