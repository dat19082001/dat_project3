class Customer:
    def __init__(self, name, phone):
        self.name = name
        self.phone = phone

    def to_dict(self):
        return {"name": self.name, "phone": self.phone}

    @classmethod
    def from_dict(cls, data):
        return cls(data["name"], data["phone"])
