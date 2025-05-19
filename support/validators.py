def to_text(value: str) -> str:
    return value.strip().title()

def to_int(value: str, positive_only: bool = False) -> int:
    try:
        num = int(value.strip())
    except ValueError:
        raise ValueError("Giá trị phải là một số nguyên hợp lệ.")

    if positive_only and num < 0:
        raise ValueError("Giá trị phải là số nguyên không âm.")

    return num


def to_float(value: str) -> float:
    return float(value.strip())

def to_year(value: str) -> int:
    year = int(value.strip())
    if year < 0 or year > 2100:
        raise ValueError("Năm không hợp lệ.")
    return year

def validate_positive_number(value: str) -> float:
    num = float(value.strip())
    if num < 0:
        raise ValueError("Giá trị phải lớn hơn hoặc bằng 0.")
    return num

def validate_non_empty(*args: str) -> bool:
    return all(arg.strip() for arg in args)

def validate_product_id(pid: str) -> str:
    pid = pid.strip()
    if not (pid.isdigit() and len(pid) == 3):
        raise ValueError("Mã sản phẩm phải gồm đúng 3 chữ số (ví dụ: 001, 123).")
    return pid

from PyQt5.QtWidgets import QLineEdit, QInputDialog, QMessageBox
from datetime import datetime
from models.customer import Customer


def get_text_input(parent, label):
    while True:
        text, ok = QInputDialog.getText(parent, "Nhập dữ liệu", label)
        if not ok:
            return None
        text = text.strip()
        if text:
            return text.title()
        QMessageBox.warning(parent, "Lỗi", "Không được để trống.")


def get_id_input(parent, label):
    while True:
        text, ok = QInputDialog.getText(parent, "Nhập ID", label)
        if not ok:
            return None
        text = text.strip()
        if text.isdigit() and len(text) == 3:
            return text
        QMessageBox.warning(parent, "Lỗi định dạng", "ID phải gồm đúng 3 chữ số.")


def get_int_input(parent, label):
    while True:
        value, ok = QInputDialog.getInt(parent, "Nhập số nguyên", label, min=0)
        if ok:
            return value


def get_float_input(parent, label):
    while True:
        text, ok = QInputDialog.getText(parent, "Nhập số thực", label)
        if not ok:
            return None
        try:
            value = float(text.strip())
            if value < 0:
                raise ValueError
            return value
        except ValueError:
            QMessageBox.warning(parent, "Lỗi định dạng", "Vui lòng nhập một số thực hợp lệ (>= 0).")


def get_year_input(parent, label):
    current_year = datetime.now().year
    while True:
        text, ok = QInputDialog.getText(parent, "Nhập năm", label)
        if not ok:
            return None
        text = text.strip().zfill(4)
        if not text.isdigit():
            QMessageBox.warning(parent, "Lỗi định dạng", "Năm phải là số.")
            continue
        year = int(text)
        if year >= current_year:
            QMessageBox.warning(parent, "Lỗi", f"Năm phải nhỏ hơn {current_year}.")
        else:
            return year


def get_optional_text(parent, label, default):
    text, ok = QInputDialog.getText(parent, "Nhập dữ liệu (tùy chọn)", label)
    if not ok or not text.strip():
        return default
    return text.strip().title()


def get_optional_int(parent, label, default):
    text, ok = QInputDialog.getText(parent, "Nhập số nguyên (tùy chọn)", label)
    if not ok or not text.strip():
        return default
    try:
        value = int(text.strip())
        if value < 0:
            raise ValueError
        return value
    except ValueError:
        QMessageBox.warning(parent, "Lỗi", "Vui lòng nhập số nguyên hợp lệ hoặc để trống.")
        return get_optional_int(parent, label, default)


def get_optional_float(parent, label, default):
    text, ok = QInputDialog.getText(parent, "Nhập số thực (tùy chọn)", label)
    if not ok or not text.strip():
        return default
    try:
        value = float(text.strip())
        if value < 0:
            raise ValueError
        return value
    except ValueError:
        QMessageBox.warning(parent, "Lỗi", "Vui lòng nhập số thực hợp lệ hoặc để trống.")
        return get_optional_float(parent, label, default)


def get_optional_year(parent, label, default):
    current_year = datetime.now().year
    text, ok = QInputDialog.getText(parent, "Nhập năm (tùy chọn)", label)
    if not ok or not text.strip():
        return default
    text = text.strip().zfill(4)
    if not text.isdigit():
        QMessageBox.warning(parent, "Lỗi", "Năm phải là số.")
        return get_optional_year(parent, label, default)
    year = int(text)
    if year >= current_year:
        QMessageBox.warning(parent, "Lỗi", f"Năm phải nhỏ hơn {current_year}.")
        return get_optional_year(parent, label, default)
    return year


def get_phone_input(parent, label):
    while True:
        text, ok = QInputDialog.getText(parent, "Nhập số điện thoại", label)
        if not ok:
            return None
        phone = text.strip()
        if phone.isdigit() and len(phone) == 10 and phone.startswith("0"):
            return phone
        QMessageBox.warning(parent, "Lỗi định dạng", "Số điện thoại phải gồm 10 chữ số và bắt đầu bằng 0.")


def get_customer_info(parent):
    name = get_text_input(parent, "Nhập tên khách hàng:")
    if name is None:
        return None
    phone = get_phone_input(parent, "Nhập số điện thoại:")
    if phone is None:
        return None
    return Customer(name, phone)
