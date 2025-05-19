from PyQt5.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QDateTimeEdit
from PyQt5.QtCore import QDateTime

class FilterByDateDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Lọc hóa đơn theo thời gian")
        self.setFixedSize(300, 150)
        layout = QVBoxLayout(self)

        hlayout_start = QHBoxLayout()
        hlayout_end = QHBoxLayout()

        self.start_label = QLabel("Thời gian bắt đầu:")
        self.start_input = QDateTimeEdit(QDateTime.currentDateTime())
        self.start_input.setDisplayFormat("yyyy-MM-dd HH:mm:ss")

        self.end_label = QLabel("Thời gian kết thúc:")
        self.end_input = QDateTimeEdit(QDateTime.currentDateTime())
        self.end_input.setDisplayFormat("yyyy-MM-dd HH:mm:ss")

        hlayout_start.addWidget(self.start_label)
        hlayout_start.addWidget(self.start_input)

        hlayout_end.addWidget(self.end_label)
        hlayout_end.addWidget(self.end_input)

        layout.addLayout(hlayout_start)
        layout.addLayout(hlayout_end)

        btn_layout = QHBoxLayout()
        self.btn_ok = QPushButton("Lọc")
        self.btn_cancel = QPushButton("Hủy")

        self.btn_ok.clicked.connect(self.accept)
        self.btn_cancel.clicked.connect(self.reject)

        btn_layout.addWidget(self.btn_ok)
        btn_layout.addWidget(self.btn_cancel)

        layout.addLayout(btn_layout)

    def get_date_range(self):
        fmt = "yyyy-MM-dd HH:mm:ss"
        return (
            self.start_input.dateTime().toString(fmt),
            self.end_input.dateTime().toString(fmt)
        )

