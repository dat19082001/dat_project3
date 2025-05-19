from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QComboBox, QMessageBox
)
from models.product import Book, MusicDisc
from storage.product_storage import load_products, save_products
from support.validators import (
    to_text, to_int, to_year,
    validate_non_empty, validate_positive_number, validate_product_id
)



class AddProductDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Thêm sản phẩm")
        self.setMinimumWidth(400)
        self.editing_product = None
        self.init_ui()

    def init_ui(self):
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # Các input chung
        self.type_input = QComboBox()
        self.type_input.addItems(["Book", "MusicDisc"])
        self.type_input.currentTextChanged.connect(self.update_type_fields)

        self.id_input = QLineEdit()
        self.name_input = QLineEdit()
        self.author_input = QLineEdit()
        self.publisher_input = QLineEdit()
        self.year_input = QLineEdit()
        self.import_price_input = QLineEdit()
        self.sale_price_input = QLineEdit()
        self.quantity_input = QLineEdit()

        # Input riêng cho từng loại
        self.page_count_input = QLineEdit()
        self.format_input = QLineEdit()
        self.duration_input = QLineEdit()
        self.size_kb_input = QLineEdit()

        # Thêm các trường cơ bản vào layout
        self.layout.addLayout(self._create_row("Loại sản phẩm:", self.type_input))
        self.layout.addLayout(self._create_row("Mã sản phẩm:", self.id_input))
        self.layout.addLayout(self._create_row("Tên sản phẩm:", self.name_input))
        self.layout.addLayout(self._create_row("Tác giả:", self.author_input))
        self.layout.addLayout(self._create_row("NXB:", self.publisher_input))
        self.layout.addLayout(self._create_row("Năm:", self.year_input))
        self.layout.addLayout(self._create_row("Giá nhập:", self.import_price_input))
        self.layout.addLayout(self._create_row("Giá bán:", self.sale_price_input))
        self.layout.addLayout(self._create_row("Số lượng:", self.quantity_input))

        # Layout chứa các trường riêng
        self.extra_fields_layout = QVBoxLayout()
        self.layout.addLayout(self.extra_fields_layout)

        # Nút thao tác
        btn_layout = QHBoxLayout()
        self.btn_ok = QPushButton("Thêm")
        btn_cancel = QPushButton("Hủy")
        self.btn_ok.clicked.connect(self.save_product)
        btn_cancel.clicked.connect(self.reject)
        btn_layout.addWidget(self.btn_ok)
        btn_layout.addWidget(btn_cancel)

        self.layout.addLayout(btn_layout)

        # Gọi để hiển thị đúng trường ban đầu
        self.update_type_fields(self.type_input.currentText())

    def _create_row(self, label, widget):
        layout = QHBoxLayout()
        layout.addWidget(QLabel(label))
        layout.addWidget(widget)
        return layout

    def update_type_fields(self, product_type):
    # Xóa toàn bộ layout và widget con trong extra_fields_layout
        while self.extra_fields_layout.count():
            item = self.extra_fields_layout.takeAt(0)
            if item is not None:
                widget = item.widget()
                layout = item.layout()

                if widget:
                    widget.setParent(None)
                elif layout:
                    # Xử lý layout con
                    while layout.count():
                        sub_item = layout.takeAt(0)
                        sub_widget = sub_item.widget()
                        if sub_widget:
                            sub_widget.setParent(None)
                    layout.setParent(None)

        # Thêm lại các field tùy theo loại sản phẩm
        if product_type == "Book":
            self.extra_fields_layout.addLayout(self._create_row("Số trang:", self.page_count_input))
            self.extra_fields_layout.addLayout(self._create_row("Khổ giấy:", self.format_input))
        elif product_type == "MusicDisc":
            self.extra_fields_layout.addLayout(self._create_row("Thời lượng:", self.duration_input))
            self.extra_fields_layout.addLayout(self._create_row("Kích thước KB:", self.size_kb_input))

        self.adjustSize()


    def set_edit_mode(self, product):
        self.setWindowTitle("Chỉnh sửa sản phẩm")
        self.editing_product = product

        if product.type == "Book":
            self.type_input.setCurrentText("Book")
        elif isinstance(product, MusicDisc):
            self.type_input.setCurrentText("MusicDisc")

        self.id_input.setText(product.product_id)
        self.id_input.setEnabled(False)
        self.name_input.setText(product.name)
        self.author_input.setText(product.author)
        self.publisher_input.setText(product.publisher)
        self.year_input.setText(str(product.year))
        self.import_price_input.setText(str(product.import_price))
        self.sale_price_input.setText(str(product.sale_price))
        self.quantity_input.setText(str(product.quantity))
        self.btn_ok.setText("Lưu")

        if isinstance(product, Book):
            self.page_count_input.setText(str(product.page_count))
            self.format_input.setText(product.book_format)
        elif isinstance(product, MusicDisc):
            self.duration_input.setText(str(product.duration))
            self.size_kb_input.setText(str(product.size_kb))

    def save_product(self):
        try:
            pid = validate_product_id(self.id_input.text())
        except ValueError as e:
            QMessageBox.warning(self, "Sai định dạng", str(e))
            return

        name = to_text(self.name_input.text())
        author = to_text(self.author_input.text())
        publisher = to_text(self.publisher_input.text())
        year_text = self.year_input.text().strip()
        import_price_text = self.import_price_input.text().strip()
        sale_price_text = self.sale_price_input.text().strip()
        quantity_text = self.quantity_input.text().strip()
        ptype = self.type_input.currentText()

        if not validate_non_empty(pid, name, author, publisher, year_text, import_price_text, sale_price_text, quantity_text):
            QMessageBox.warning(self, "Thiếu thông tin", "Vui lòng nhập đầy đủ thông tin chung.")
            return

        try:
            year = to_year(year_text)
            import_price = validate_positive_number(import_price_text)
            sale_price = validate_positive_number(sale_price_text)
            quantity = to_int(quantity_text)
        except ValueError as e:
            QMessageBox.warning(self, "Lỗi định dạng", str(e))
            return

        sold_quantity = self.editing_product.sold_quantity if self.editing_product else 0

        try:
            if ptype == "Book":
                page_count = to_int(self.page_count_input.text())
                book_format = to_text(self.format_input.text())
                product = Book("Book", pid, name, author, publisher, year,
                               import_price, sale_price, quantity, sold_quantity,
                               page_count, book_format)
            else:
                duration = to_int(self.duration_input.text())
                size_kb = to_int(self.size_kb_input.text())
                product = MusicDisc("MusicDisc", pid, name, author, publisher, year,
                                    import_price, sale_price, quantity, sold_quantity,
                                    duration, size_kb)
        except ValueError as e:
            QMessageBox.warning(self, "Lỗi định dạng", str(e))
            return

        products = load_products()
        if not self.editing_product:
            if any(p.product_id == pid for p in products):
                QMessageBox.warning(self, "Trùng mã", f"Đã tồn tại sản phẩm với mã: {pid}")
                return
            products.append(product)
        else:
            reply = QMessageBox.question(
                self, "Xác nhận", "Bạn có chắc muốn lưu thay đổi?",
                QMessageBox.Yes | QMessageBox.No
            )
            if reply != QMessageBox.Yes:
                return
            products = [p if p.product_id != pid else product for p in products]
        products.sort(key=lambda p: p.product_id)
        save_products(products)
        QMessageBox.information(self, "Thành công", "Đã lưu sản phẩm.")
        self.accept()
