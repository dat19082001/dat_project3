from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton,
    QTableWidget, QTableWidgetItem, QDateTimeEdit, QMessageBox, QInputDialog
)
from PyQt5.QtCore import QDateTime, Qt
from models.invoice import Invoice
from models.customer import Customer
from storage.product_storage import load_products, save_products
from storage.invoice_storage import save_invoice
import re

class AddInvoiceDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Thêm Hóa Đơn")
        self.layout = QVBoxLayout(self)

        # Mã hóa đơn
        self.invoice_id_label = QLabel("Mã hóa đơn:")
        self.invoice_id_value = QLineEdit()
        self.invoice_id_value.setReadOnly(True)
        self.invoice_id_value.setText(str(parent.generate_invoice_id()))
        self.layout.addWidget(self.invoice_id_label)
        self.layout.addWidget(self.invoice_id_value)

        # Thông tin khách hàng
        self.customer_name_label = QLabel("Tên khách hàng:")
        self.customer_name_input = QLineEdit()
        self.layout.addWidget(self.customer_name_label)
        self.layout.addWidget(self.customer_name_input)

        self.customer_phone_label = QLabel("Số điện thoại:")
        self.customer_phone_input = QLineEdit()
        self.layout.addWidget(self.customer_phone_label)
        self.layout.addWidget(self.customer_phone_input)

        # Thời gian tạo
        self.created_at_label = QLabel("Thời gian tạo:")
        self.created_at_input = QDateTimeEdit(QDateTime.currentDateTime())
        self.created_at_input.setDisplayFormat("yyyy-MM-dd HH:mm:ss")
        self.layout.addWidget(self.created_at_label)
        self.layout.addWidget(self.created_at_input)

        # Danh sách sản phẩm
        self.layout.addWidget(QLabel("Danh sách sản phẩm:"))
        self.product_list_table = QTableWidget()
        self.product_list_table.setColumnCount(5)
        self.product_list_table.setHorizontalHeaderLabels(["Mã SP", "Loại SP", "Tên SP", "Tồn kho", "Giá bán"])
        self.layout.addWidget(self.product_list_table)

        # Sản phẩm trong hóa đơn
        self.layout.addWidget(QLabel("Sản phẩm trong hóa đơn:"))
        self.product_table = QTableWidget()
        self.product_table.setColumnCount(6)
        self.product_table.setHorizontalHeaderLabels(["Mã sản phẩm", "Loại sản phẩm", "Tên sản phẩm", "Số lượng", "Giá", "Xóa"])
        self.layout.addWidget(self.product_table)
        self.total_amount_label = QLabel("Tổng tiền: 0 VNĐ")
        self.layout.addWidget(self.total_amount_label)
        
        # Tạo dict lưu giá trị cũ của số lượng và giá bán
        self._last_qty_values = {}
        self._last_price_values = {}
        
        try:
            self.product_table.cellDoubleClicked.disconnect()
        except TypeError:
            pass

        self.product_table.cellDoubleClicked.connect(self.handle_delete_click)
        self.product_table.cellChanged.connect(self.on_product_table_cell_changed)

        # Nút thao tác
        self.btn_layout = QHBoxLayout()
        self.btn_add_product = QPushButton("Thêm sản phẩm")
        self.btn_save = QPushButton("Lưu hóa đơn")
        self.btn_cancel = QPushButton("Hủy")

        self.btn_add_product.clicked.connect(self.add_product)
        self.btn_save.clicked.connect(self.save_invoice)
        self.btn_cancel.clicked.connect(self.reject)
        



        self.btn_layout.addWidget(self.btn_add_product)
        self.btn_layout.addWidget(self.btn_save)
        self.btn_layout.addWidget(self.btn_cancel)
        self.layout.addLayout(self.btn_layout)

        self.load_products_to_table()
        self.resize(900, 600)

    def load_products_to_table(self):
        self.products = load_products()
        self.products.sort(key=lambda p: p.product_id)

        table = self.product_list_table
        table.setRowCount(len(self.products))

        try:
            table.cellDoubleClicked.disconnect()
        except TypeError:
            pass

        for row, product in enumerate(self.products):
            items = [
                QTableWidgetItem(product.product_id),
                QTableWidgetItem(product.type),
                QTableWidgetItem(product.name),
                QTableWidgetItem(str(product.quantity)),
                QTableWidgetItem(str(product.sale_price))
            ]
            for col, item in enumerate(items):
                item.setFlags(item.flags() ^ Qt.ItemIsEditable)
                table.setItem(row, col, item)

        table.cellDoubleClicked.connect(self.handle_select_product)

    def handle_select_product(self, row):
        product = self.products[row]
        quantity, ok = QInputDialog.getInt(
            self,
            "Chọn số lượng",
            f"Thêm sản phẩm '{product.name}' vào hóa đơn.\nTồn kho: {product.quantity}\n\nNhập số lượng:",
            min=1,
            max=product.quantity
        )
        if ok:
            self.add_product_to_invoice(product, quantity)

    def add_product_to_invoice(self, product, select_sold_quantity):
        if product.quantity < select_sold_quantity:
            QMessageBox.warning(self, "Lỗi", f"Số lượng sản phẩm {product.name} không đủ. Tồn kho: {product.quantity}")
            return

        added = False
        for row in range(self.product_table.rowCount()):
            if self.product_table.item(row, 0).text() == product.product_id:
                old_qty = int(self.product_table.item(row, 3).text())
                new_qty = old_qty + select_sold_quantity
                self.product_table.setItem(row, 3, QTableWidgetItem(str(new_qty)))
                
                item_qty = self.product_table.item(row, 3)
                item_qty.setFlags(item_qty.flags() | Qt.ItemIsEditable)
                
                added = True
                break

        if not added:
            row_pos = self.product_table.rowCount()
            self.product_table.insertRow(row_pos)
            
             # Mã sản phẩm (cột 0) - không sửa được
            item_id = QTableWidgetItem(product.product_id)
            item_id.setFlags(item_id.flags() & ~Qt.ItemIsEditable)
            self.product_table.setItem(row_pos, 0, item_id)
           
            # Loại sản phẩm (cột 1) - không sửa được
            
            item_type = QTableWidgetItem(product.type)
            item_type.setFlags(item_type.flags() & ~Qt.ItemIsEditable)
            self.product_table.setItem(row_pos, 1, item_type)
            
            # Tên sản phẩm (cột 2) - không sửa được
            item_name = QTableWidgetItem(product.name)
            item_name.setFlags(item_name.flags() & ~Qt.ItemIsEditable)
            self.product_table.setItem(row_pos, 2, item_name)
            
            # Số lượng (cột 3) - cho phép sửa
            item_qty = QTableWidgetItem(str(select_sold_quantity))
            item_qty.setFlags(item_qty.flags() | Qt.ItemIsEditable)
            self.product_table.setItem(row_pos, 3, item_qty)

            # Giá bán (cột 4) -  sửa được
            item_price = QTableWidgetItem(str(product.sale_price))
            item_price.setFlags(item_price.flags() | Qt.ItemIsEditable)
            self.product_table.setItem(row_pos, 4, item_price)
            
            
            delete_item = QTableWidgetItem("X")
            delete_item.setTextAlignment(Qt.AlignCenter)
            delete_item.setForeground(Qt.red)
            delete_item.setFlags(delete_item.flags() & ~Qt.ItemIsEditable)
            self.product_table.setItem(row_pos, 5, delete_item)
            
        self.update_total_amount_label()
        
    def on_product_table_cell_changed(self, row, column):
        if column == 3:  # Cột số lượng
            item = self.product_table.item(row, column)
            if not item:
                return
            new_text = item.text()

            old_value = self._last_qty_values.get(row, "1")  # Giá trị cũ lấy từ dict

            try:
                new_qty = int(new_text)
                if new_qty < 0:
                    raise ValueError
            except ValueError:
                QMessageBox.warning(self, "Lỗi", "Số lượng phải là số nguyên không âm.")
                self.product_table.blockSignals(True)
                self.product_table.setItem(row, column, QTableWidgetItem(old_value))
                self.product_table.blockSignals(False)
                return

            # Kiểm tra tồn kho
            product_id = self.product_table.item(row, 0).text()
            original_product = next((p for p in self.products if p.product_id == product_id), None)
            if original_product and new_qty > original_product.quantity:
                QMessageBox.warning(
                    self,
                    "Lỗi",
                    f"Số lượng không được vượt quá tồn kho ({original_product.quantity})."
                )
                self.product_table.blockSignals(True)
                self.product_table.setItem(row, column, QTableWidgetItem(str(original_product.quantity)))
                self.product_table.blockSignals(False)
                # Cập nhật lại giá trị lưu
                self._last_qty_values[row] = str(original_product.quantity)
                return

            # Giá trị hợp lệ => cập nhật _last_qty_values
            self._last_qty_values[row] = str(new_qty)

        elif column == 4:  # Cột giá bán
            item = self.product_table.item(row, column)
            if not item:
                return
            new_text = item.text()
            old_value = self._last_price_values.get(row, "0")

            try:
                new_price = float(new_text)
                if new_price < 0:
                    raise ValueError
            except ValueError:
                QMessageBox.warning(self, "Lỗi", "Giá bán phải là số không âm hợp lệ.")
                self.product_table.blockSignals(True)
                self.product_table.setItem(row, column, QTableWidgetItem(old_value))
                self.product_table.blockSignals(False)
                return

            # Giá trị hợp lệ => cập nhật _last_price_values
            self._last_price_values[row] = f"{new_price}"

        self.update_total_amount_label()



    def get_products_from_table(self):
        products = []
        for row in range(self.product_table.rowCount()):
            product_id = self.product_table.item(row, 0).text()
            sold_quantity = int(self.product_table.item(row, 3).text())
            sale_price = float(self.product_table.item(row, 4).text())

            original_product = next((p for p in self.products if p.product_id == product_id), None)
            if original_product:
                product_copy = original_product.__class__.from_dict(original_product.to_dict())
                product_copy.sold_quantity = sold_quantity
                product_copy.sale_price = sale_price
                products.append(product_copy)
        return products

    def save_invoice(self):
        invoice_id = self.invoice_id_value.text()
        customer_name = self.customer_name_input.text().strip()
        customer_phone = self.customer_phone_input.text().strip()
        created_at = self.created_at_input.dateTime().toString("yyyy-MM-dd HH:mm:ss")

        if not customer_name or not customer_phone:
            QMessageBox.warning(self, "Lỗi", "Vui lòng nhập đầy đủ thông tin khách hàng.")
            return
        
        if not re.fullmatch(r"0\d{9}", customer_phone):
            QMessageBox.warning(self, "Lỗi", "Số điện thoại phải có 10 chữ số và bắt đầu bằng số 0.")
            return
        if self.product_table.rowCount() == 0:
            QMessageBox.warning(self, "Lỗi", "Hóa đơn phải có ít nhất một sản phẩm.")
            return

        customer = Customer(name=customer_name.title(), phone=customer_phone)
        invoice_products = self.get_products_from_table()

        if not invoice_products:
            QMessageBox.warning(self, "Lỗi", "Vui lòng chọn ít nhất một sản phẩm.")
            return

        # Kiểm tra nếu có sản phẩm trong hóa đơn có số lượng = 0
        has_zero_quantity = any(
            int(self.product_table.item(row, 3).text()) == 0
            for row in range(self.product_table.rowCount())
        )

        if has_zero_quantity:
            QMessageBox.warning(
                self,
                "Cảnh báo số lượng",
                "Có sản phẩm trong hóa đơn đang có số lượng = 0.\n"
                "Vui lòng kiểm tra lại hoặc xóa khỏi hóa đơn trước khi lưu."
            )
            return

                
        total_amount = self.calculate_total_amount()
        if total_amount == 0:
            QMessageBox.warning(
                self,
                "Tổng tiền bằng 0",
                "Tổng tiền hóa đơn bằng 0.\n"
                "Vui lòng kiểm tra lại số lượng sản phẩm hoặc hủy bỏ hóa đơn không cần thiết."
            )
            return

        for inv_product in invoice_products:
            for p in self.products:
                if p.product_id == inv_product.product_id:
                    if p.quantity >= inv_product.sold_quantity:
                        p.quantity -= inv_product.sold_quantity
                        p.sold_quantity += inv_product.sold_quantity
                    else:
                        QMessageBox.warning(self, "Lỗi", f"Sản phẩm {p.name} không đủ hàng.")
                        return

        save_products(self.products)

        invoice = Invoice(
            invoice_id=invoice_id,
            customer={'name': customer.name, 'phone': customer.phone},
            created_at=created_at,
            products=invoice_products
        )

        save_invoice(invoice)
        self.parent().invoices.append(invoice)

        total = self.calculate_total_amount()
        QMessageBox.information(self, "Hóa đơn đã lưu", f"Hóa đơn lưu thành công.\nTổng tiền: {total:,.1f} VNĐ")

        self.accept()

    def calculate_total_amount(self):
        total = 0.0
        for row in range(self.product_table.rowCount()):
            qty_item= self.product_table.item(row, 3)
            price_item = self.product_table.item(row, 4)
            if not qty_item or not price_item:
                continue

            try:
                quantity = int(qty_item.text())
                price = float(price_item.text())
                if quantity <= 0 or price <= 0:
                    continue
                total += quantity * price
            except ValueError:
                continue 
        return total
    
    def update_total_amount_label(self):
        total = self.calculate_total_amount()
        self.total_amount_label.setText(f"Tổng tiền dự kiến: {total:,.1f} VNĐ")

    def add_product(self):
        QMessageBox.information(self, "Chọn sản phẩm", "Vui lòng chọn từ danh sách sản phẩm có sẵn.")
        
        
        
    def handle_delete_click(self, row, column):
        
        if column !=  self.product_table.columnCount() - 1:
            return

        product_name = self.product_table.item(row, 2).text()  # Tên sản phẩm ở cột 2

        reply = QMessageBox.question(
            self,
            "Xác nhận xóa",
            f"Bạn có chắc muốn xóa sản phẩm '{product_name}' khỏi hóa đơn?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.Yes
        )

        if reply == QMessageBox.Yes:
            self.product_table.removeRow(row)
            new_last_qty = {}
            new_last_price = {}
            for r in range(self.product_table.rowCount()):
                qty_item = self.product_table.item(r, 3)
                price_item = self.product_table.item(r, 4)
                if qty_item:
                    new_last_qty[r] = qty_item.text()
                if price_item:
                    new_last_price[r] = price_item.text()
            self._last_qty_values = new_last_qty
            self._last_price_values = new_last_price

            self.update_total_amount_label()

