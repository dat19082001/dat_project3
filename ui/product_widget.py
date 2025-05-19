from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QHBoxLayout, QTableWidget, QTableWidgetItem, QLineEdit, QLabel, QMessageBox
from storage.product_storage import load_products, save_products
from ui.add_product_dialog import AddProductDialog
from models.product import Book, MusicDisc
from PyQt5.QtCore import Qt


class ProductManagerWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.filtered_products = []  # Đảm bảo biến tồn tại từ đầu
        self.products = []           # Danh sách tất cả sản phẩm
        self.layout = QVBoxLayout(self)

        self.init_search_bar()
        self.init_table()
        self.init_buttons()
        self.load_products()
        
        # Ẩn toàn bộ giao diện bảng khi khởi tạo
        self.set_table_visibility(False)

    def init_search_bar(self):
        self.search_layout = QHBoxLayout()
        self.search_label = QLabel("Tìm kiếm:")
        self.search_input = QLineEdit()
        self.search_input.textChanged.connect(self.load_products)
        
        self.search_layout.addWidget(self.search_label)
        self.search_layout.addWidget(self.search_input)
        self.layout.addLayout(self.search_layout)

    def init_table(self):
        self.table = QTableWidget()
        self.table.setColumnCount(11)
        self.table.setHorizontalHeaderLabels(["Mã SP", "Loại SP", "Tên SP", "Tác giả", "Nhà xuất bản", "Năm xuất bản",
        "Tồn kho", "Đã bán", "Giá bán",
        "Số trang / Thời lượng", "Định dạng / Dung lượng (KB)"])
        self.layout.addWidget(self.table)
        self.table.setFixedSize(1000, 600)


    def init_buttons(self):
        self.btn_layout = QHBoxLayout()
        self.btn_add = QPushButton("Thêm")
        self.btn_edit = QPushButton("Sửa")
        self.btn_delete = QPushButton("Xóa")

        self.btn_add.clicked.connect(self.handle_add_product)
        self.btn_edit.clicked.connect(self.handle_edit_product)
        self.btn_delete.clicked.connect(self.handle_delete_product)
    

        self.btn_layout.addWidget(self.btn_add)
        self.btn_layout.addWidget(self.btn_edit)
        self.btn_layout.addWidget(self.btn_delete)
        self.layout.addLayout(self.btn_layout)

    def load_products(self):
        keyword = self.search_input.text().lower()
        self.products = load_products()
        self.products.sort(key=lambda p: p.product_id)
        self.filtered_products = [
            p for p in self.products
            if keyword in p.name.lower()
            or keyword in p.type.lower()
            or keyword in p.author.lower()
            or keyword in p.publisher.lower()
            or keyword in str(p.year) 
        ]

      

        self.table.setRowCount(len(self.filtered_products))
        for row, prod in enumerate(self.filtered_products):
            common_items = [
                prod.product_id,
                prod.type,
                prod.name,
                prod.author,
                prod.publisher,
                str(prod.year),
                str(prod.quantity),
                str(prod.sold_quantity),
                str(prod.sale_price),
            ]
            
            # Trường đặc trưng theo loại sản phẩm
            if isinstance(prod, Book):
                extra1 = str(prod.page_count)
                extra2 = prod.book_format
            elif isinstance(prod, MusicDisc):
                extra1 = str(prod.duration)
                extra2 = str(prod.size_kb)
            else:
                extra1 = ""
                extra2 = ""
                
            items = [QTableWidgetItem(str(field)) for field in (common_items + [extra1, extra2])]

            for col, item in enumerate(items):
                item.setFlags(item.flags() & ~Qt.ItemIsEditable)  # Không cho sửa
                self.table.setItem(row, col, item)
            
            


    def handle_add_product(self):
        dialog = AddProductDialog(self)
        if dialog.exec_():
            self.load_products()
            
    def handle_edit_product(self):
        selected = self.table.currentRow()
        if selected < 0 or selected >= len(self.filtered_products):
            QMessageBox.warning(self, "Chưa chọn sản phẩm", "Vui lòng chọn một sản phẩm để sửa.")
            return

        product = self.filtered_products[selected]
        dialog = AddProductDialog(self)
        dialog.set_edit_mode(product)
        if dialog.exec_():
            self.load_products()

    def handle_delete_product(self):
        selected = self.table.currentRow()
        if selected < 0 or selected >= len(self.filtered_products):
            QMessageBox.warning(self, "Chưa chọn sản phẩm", "Vui lòng chọn một sản phẩm để xóa.")
            return

        product = self.filtered_products[selected]
        confirm = QMessageBox.question(
            self,
            "Xác nhận xóa",
            f"Bạn có chắc muốn xóa sản phẩm '{product.name}'?",
            QMessageBox.Yes | QMessageBox.No
        )

        if confirm == QMessageBox.Yes:
            self.products = [p for p in self.products if p.product_id != product.product_id]
            save_products(self.products)
            self.load_products()

    def set_table_visibility(self, visible: bool):
        self.table.setVisible(visible)
        self.search_input.setVisible(visible)
        self.search_label.setVisible(visible)
        self.btn_add.setVisible(visible)
        self.btn_edit.setVisible(visible)
        self.btn_delete.setVisible(visible)
