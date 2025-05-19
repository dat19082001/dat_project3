from abc import ABC, abstractmethod


class Product(ABC):
    def __init__(
        self,
        type,
        product_id,
        name,
        author,
        publisher,
        year,
        import_price,
        sale_price,
        quantity,
        sold_quantity,
    ):
        self.type = type
        self.product_id = product_id
        self.name = name
        self.author = author
        self.publisher = publisher
        self.year = year
        self.import_price = import_price
        self.sale_price = sale_price
        self.quantity = quantity
        self.sold_quantity = sold_quantity

    @abstractmethod
    def to_dict(self):
        pass

    @classmethod
    @abstractmethod
    def from_dict(cls, data):
        pass


class Book(Product):
    def __init__(
        self,
        type,
        product_id,
        name,
        author,
        publisher,
        year,
        import_price,
        sale_price,
        quantity,
        sold_quantity,
        page_count,
        book_format,
    ):
        super().__init__(
            type,
            product_id,
            name,
            author,
            publisher,
            year,
            import_price,
            sale_price,
            quantity,
            sold_quantity,
        )
        self.page_count = page_count
        self.book_format = book_format

    def to_dict(self):
        return {
            "type": "Book",
            "id": self.product_id,
            "name": self.name,
            "author": self.author,
            "publisher": self.publisher,
            "year": self.year,
            "import_price": self.import_price,
            "sale_price": self.sale_price,
            "quantity": self.quantity,
            "sold_quantity": self.sold_quantity,
            "page_count": self.page_count,
            "format": self.book_format,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            data["type"],
            data["id"],
            data["name"],
            data["author"],
            data["publisher"],
            data["year"],
            data["import_price"],
            data["sale_price"],
            data["quantity"],
            data["sold_quantity"],
            data["page_count"],
            data["format"],
        )


class MusicDisc(Product):
    def __init__(
        self,
        type,
        product_id,
        name,
        author,
        publisher,
        year,
        import_price,
        sale_price,
        quantity,
        sold_quantity,
        duration,
        size_kb,
    ):
        super().__init__(
            type,
            product_id,
            name,
            author,
            publisher,
            year,
            import_price,
            sale_price,
            quantity,
            sold_quantity,
        )
        self.duration = duration
        self.size_kb = size_kb

    def to_dict(self):
        return {
            "type": "MusicDisc",
            "id": self.product_id,
            "name": self.name,
            "author": self.author,
            "publisher": self.publisher,
            "year": self.year,
            "import_price": self.import_price,
            "sale_price": self.sale_price,
            "quantity": self.quantity,
            "sold_quantity": self.sold_quantity,
            "duration": self.duration,
            "size_kb": self.size_kb,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            data["type"],
            data["id"],
            data["name"],
            data["author"],
            data["publisher"],
            data["year"],
            data["import_price"],
            data["sale_price"],
            data["quantity"],
            data["sold_quantity"],
            data["duration"],
            data["size_kb"],
        )
