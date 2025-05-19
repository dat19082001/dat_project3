from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QPushButton, QHBoxLayout, QStackedWidget
from ui.product_widget import ProductManagerWidget
from ui.invoice_widget import InvoiceManagerWidget


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Quản Lý Cửa Hàng")
        self.resize(1500, 800)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.main_layout = QHBoxLayout(self.central_widget)

        self.sidebar = QVBoxLayout()
        self.main_layout.addLayout(self.sidebar, 1)

        self.stack = QStackedWidget()
        self.main_layout.addWidget(self.stack, 4)

        self.init_sidebar()
        self.init_widgets()

        #  Ban đầu bảng và thanh tìm kiếm sẽ được ẩn
       
        self.product_table_visible = False  # Thuộc tính cho bảng sản phẩm
        self.invoice_table_visible = False  # Thêm thuộc tính cho bảng hóa đơn
        self.product_widget.set_table_visibility(False)
        self.invoice_widget.set_table_visibility(False)
    

    def init_sidebar(self):
        self.btn_products = QPushButton("Quản lý sản phẩm")
        self.btn_invoices = QPushButton("Quản lý hóa đơn") 

        
        self.btn_products.clicked.connect(self.toggle_product_table)
        self.btn_invoices.clicked.connect(self.toggle_invoice_table)

        self.sidebar.addWidget(self.btn_products)
        self.sidebar.addWidget(self.btn_invoices)
        self.sidebar.addStretch()

    def init_widgets(self):
        self.product_widget = ProductManagerWidget()
        self.invoice_widget = InvoiceManagerWidget()

        
        self.stack.addWidget(self.product_widget)
        self.stack.addWidget(self.invoice_widget)

    def toggle_product_table(self):
    # Chuyển sang tab sản phẩm
        self.stack.setCurrentIndex(0)  # Tab sản phẩm là tab thứ 0
        # Cập nhật trạng thái của bảng sản phẩm
        self.product_widget.set_table_visibility(True)  # Hiển thị bảng sản phẩm

        # Ẩn bảng hóa đơn
        self.invoice_widget.set_table_visibility(False)

        # Gọi cập nhật bảng sản phẩm mỗi lần mở
        self.product_widget.load_products()

    def toggle_invoice_table(self):
    # Chuyển sang tab hóa đơn
        self.stack.setCurrentIndex(1)  # Tab hóa đơn là tab thứ 1
        # Cập nhật trạng thái của bảng hóa đơn
        self.invoice_widget.set_table_visibility(True)  # Hiển thị bảng hóa đơn

        # Ẩn bảng sản phẩm
        self.product_widget.set_table_visibility(False)

        # Gọi cập nhật bảng hóa đơn mỗi lần mở
        self.invoice_widget.load_invoices()
