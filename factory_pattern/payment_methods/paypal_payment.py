from .payment import Payment

class PaypalPayment(Payment):

    def pay(self, amount: float):
        print(f"Successfully paid ${amount} to merchant using a paypal.")
