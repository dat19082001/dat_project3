from datetime import datetime
from models.customer import Customer
from models.product import Product


class Invoice:
    def __init__(self, invoice_id, products, customer=None, created_at=None):
        self.invoice_id = invoice_id
        self.products = products  # List[Product]
        self.customer = customer
        self.created_at = created_at if created_at else datetime.now().strftime("%Y-%m-%d %H:%M:%S")
      

    def total_amount(self):
        total = 0
        for p in self.products:
            # Nếu là từ điển, chuyển thành đối tượng Product
            if isinstance(p, dict):
                p = Product.from_dict(p)
            if hasattr(p, 'sale_price') and hasattr(p, 'sold_quantity'):
                total += p.sale_price * p.sold_quantity
        return total



    def to_dict(self):
        return {
            "invoice_id": self.invoice_id,
            "customer": self.customer.to_dict() if isinstance(self.customer, Customer) else self.customer,
            "created_at": self.created_at,
            "total_amount": self.total_amount(),
            "products": [p.to_dict() for p in self.products],
        }

    @classmethod
    def from_dict(cls, data, product_loader):
        products = [product_loader(p) for p in data["products"]]
        customer_data = data.get("customer")
        customer = Customer.from_dict(customer_data) if customer_data else None
        return cls(
            invoice_id=data["invoice_id"],
            products=products,
            customer=customer,
            created_at=data.get("created_at")
        )


class InvoiceManager:
    def __init__(self, invoice_file, product_list, storage):
        self.invoice_file = invoice_file
        self.product_list = product_list
        self.storage = storage  # reference to invoice_storage module

    def create_invoice(self, invoice_id, sold_products, customer):
        invoice = Invoice(invoice_id, sold_products, customer)
        self._update_stock(sold_products)
        self.storage.save_invoice(self.invoice_file, invoice)
        return invoice

    # def _update_stock(self, sold_products):
    #     for sold in sold_products:
    #         for prod in self.product_list:
    #             if prod.product_id == sold.product_id:
    #                 if prod.quantity < sold.sold_quantity:
    #                     raise ValueError(f"Not enough stock for product {prod.name}")
    #                 prod.quantity -= sold.sold_quantity
    #                 prod.sold_quantity += sold.sold_quantity

    def load_invoices(self):
        return self.storage.load_invoices(self.invoice_file)
