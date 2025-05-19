from PyQt5.QtWidgets import QDialog, QMessageBox
from ui.filter_by_date_dialog import FilterByDateDialog  


def handle_filter_by_date(self):
    dialog = FilterByDateDialog(self)
    if dialog.exec_() == QDialog.Accepted:
        start_str, end_str = dialog.get_date_range()
        if start_str > end_str:

                    QMessageBox.warning(self, "Lỗi", "Thời gian bắt đầu phải nhỏ hơn hoặc bằng thời gian kết thúc.")
                    return

        filtered = []
        total_revenue = 0
        total_profit = 0

        for inv in self.invoices:
            # inv.created_at là str "yyyy-MM-dd HH:mm:ss", parse về QDateTime
            inv_str = inv.created_at
            if start_str <= inv_str <= end_str:
                filtered.append(inv)
                total_revenue += inv.total_amount()
                # Tính lợi nhuận = (giá bán - giá nhập) * số lượng bán
                for p in inv.products:
                    profit_per_product = (p.sale_price - p.import_price) * p.sold_quantity
                    total_profit += profit_per_product

        if not filtered:
            QMessageBox.information(self, "Kết quả lọc", "Không tìm thấy hóa đơn trong khoảng thời gian đã chọn.")
            return

        # Hiển thị kết quả lọc
        self.filtered_invoices = filtered
        self.update_table_with_filtered()
        QMessageBox.information(
            self,
            "Kết quả lọc",
            f"Tìm thấy {len(filtered)} hóa đơn.\n"
            f"Tổng doanh thu: {total_revenue:,.1f} VNĐ\n"
            f"Tổng lợi nhuận: {total_profit:,.1f} VNĐ"
        )

