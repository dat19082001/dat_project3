# from abc import ABC, abstractmethod
# from .product import Book, MusicDisc
# from models.product import Book, MusicDisc
# from support.format_input import input_id, input_text, input_float, input_int, input_year


# class ProductFactory(ABC):
#     @abstractmethod
#     def create_product_from_input(self):
#         pass


# def get_common_input():
#     return {
#         "product_id": input_id("ID sản phẩm: "),
#         "name": input_text("Tên sản phẩm: "),
#         "author": input_text("Tác giả: "),
#         "publisher": input_text("Nhà xuất bản: "),
#         "year": input_year("Năm xuất bản: "),
#         "import_price": input_float("Giá nhập: "),
#         "sale_price": input_float("Giá bán: "),
#         "quantity": input_int("Số lượng trong kho: "),
#         "sold_quantity": 0,
#     }


# class BookFactory(ProductFactory):
#     def create_product_from_input(self):
#         common = get_common_input()
#         page_count = int(input("Page Count: "))
#         book_format = input("Format (e.g., Hardcover, PDF): ")
#         return Book(**common, page_count=page_count, book_format=book_format)

#     @staticmethod
#     def create_product():
#         factory = BookFactory()
#         return factory.create_product_from_input()
    
#     @staticmethod
#     def create_product_from_dict(data):
#         return Book(**data)


# class MusicDiscFactory(ProductFactory):
#     def create_product_from_input(self):
#         common = get_common_input()
#         duration = int(input("Duration (in seconds): "))
#         size_kb = int(input("Size (KB): "))
#         return MusicDisc(**common, duration=duration, size_kb=size_kb)

#     @staticmethod
#     def create_product():
#         factory = MusicDiscFactory()
#         return factory.create_product_from_input()
    
#     @staticmethod
#     def create_product_from_dict(data):
#         return MusicDisc(**data)
