import random
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTableWidget, QTableWidgetItem,
    QLabel, QLineEdit
)
from storage.invoice_storage import load_invoices
from ui.add_invoice_dialog import AddInvoiceDialog 
from PyQt5.QtCore import Qt
from ui.handle_filter_by_date import handle_filter_by_date


class InvoiceManagerWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.filtered_invoices = []
        self.invoices = []
        self.layout = QVBoxLayout(self)
        
        # self.load_invoices()

        self.init_search_bar()
        self.init_table()
        self.init_buttons()
        self.load_invoices()

        self.set_table_visibility(False)

    def init_search_bar(self):
        self.search_layout = QHBoxLayout()
        self.search_label = QLabel("Tìm kiếm")
        self.search_input = QLineEdit()
        self.search_input.textChanged.connect(self.load_invoices)

        self.search_layout.addWidget(self.search_label)
        self.search_layout.addWidget(self.search_input)
        self.layout.addLayout(self.search_layout)

    def init_table(self):
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels([
            "Mã hóa đơn", "Tên KH", "SĐT", "Sản phẩm", "Tổng tiền", "Thời gian"
        ])
        self.layout.addWidget(self.table)

    def init_buttons(self):
        self.btn_layout = QHBoxLayout()
        self.btn_add = QPushButton("Thêm hóa đơn")
        self.btn_add.clicked.connect(self.handle_add_invoice)

        self.btn_filter = QPushButton("Lọc theo thời gian")
        # self.btn_filter.clicked.connect(self.handle_filter_by_date)
        self.btn_filter.clicked.connect(lambda: handle_filter_by_date(self))


        self.btn_layout.addWidget(self.btn_add)
        self.btn_layout.addWidget(self.btn_filter)
        self.layout.addLayout(self.btn_layout)

    def load_invoices(self):
        keyword = self.search_input.text().lower()
        self.invoices = load_invoices()
        self.filtered_invoices = [
            inv for inv in self.invoices
            if keyword in inv.customer.name.lower() or keyword in inv.customer.phone
            or any(keyword in p.product_id for p in inv.products)
        ]

        self.table.setRowCount(len(self.filtered_invoices))
      
        for row, inv in enumerate(self.filtered_invoices):
            items = [
            QTableWidgetItem(str(inv.invoice_id)),
            QTableWidgetItem(inv.customer.name),
            QTableWidgetItem(inv.customer.phone),
        ]
            # Cột sản phẩm
            product_details = "\n".join([f"ID: {p.product_id} * ({p.sold_quantity})" for p in inv.products])
            product_item = QTableWidgetItem(product_details)
            product_item.setTextAlignment(Qt.AlignTop)
            items.append(product_item)
            
            # Cột tổng tiền
            items.append(QTableWidgetItem(str(inv.total_amount())))

            # Cột thời gian: chia ngày và giờ thành 2 dòng
            created_at = inv.created_at.replace(" ", "\n")
            created_item = QTableWidgetItem(created_at)
            created_item.setTextAlignment(Qt.AlignTop)
            items.append(created_item)
            
            # Gán item và tắt chỉnh sửa
            for col, item in enumerate(items):
                item.setFlags(item.flags() & ~Qt.ItemIsEditable)
                self.table.setItem(row, col, item)

            # Căn chỉnh chiều cao theo số dòng tối đa
            num_lines = max(len(product_details.split("\n")), 2)  # ít nhất 2 dòng cho ngày/giờ
            self.table.setRowHeight(row, num_lines * 20)

    def handle_add_invoice(self):
        dialog = AddInvoiceDialog(self)  # Cần tạo dialog này giống như AddProductDialog
        if dialog.exec_():
            self.load_invoices()

    def set_table_visibility(self, visible: bool):
        self.table.setVisible(visible)
        self.search_input.setVisible(visible)
        self.search_label.setVisible(visible)
        self.btn_add.setVisible(visible)

    def generate_invoice_id(self):
        # Tạo mã hóa đơn ngẫu nhiên gồm 9 chữ số
        return ''.join(random.choices('0123456789', k=9))


    def update_table_with_filtered(self):
        self.table.setRowCount(len(self.filtered_invoices))
        for row, inv in enumerate(self.filtered_invoices):
            items = [
                QTableWidgetItem(str(inv.invoice_id)),
                QTableWidgetItem(inv.customer.name),
                QTableWidgetItem(inv.customer.phone),
            ]
            product_details = "\n".join([f"ID: {p.product_id} * ({p.sold_quantity})" for p in inv.products])
            product_item = QTableWidgetItem(product_details)
            product_item.setTextAlignment(Qt.AlignTop)
            items.append(product_item)
            items.append(QTableWidgetItem(str(inv.total_amount())))
            created_at = inv.created_at.replace(" ", "\n")
            created_item = QTableWidgetItem(created_at)
            created_item.setTextAlignment(Qt.AlignTop)
            items.append(created_item)

            for col, item in enumerate(items):
                item.setFlags(item.flags() & ~Qt.ItemIsEditable)
                self.table.setItem(row, col, item)

            num_lines = max(len(product_details.split("\n")), 2)
            self.table.setRowHeight(row, num_lines * 20)
