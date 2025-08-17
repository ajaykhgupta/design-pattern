from abc import ABC, abstractmethod

class Payment(ABC):
    @abstractmethod
    def pay(self, amount):
        pass

class CashPayment(Payment):
    def pay(self, amount):
        print(f"Paid ₹{amount} in cash")

class UPIPayment(Payment):
    def pay(self, amount):
        print(f"Paid ₹{amount} via UPI")

class CardPayment(Payment):
    def pay(self, amount):
        print(f"Paid ₹{amount} via Card")
