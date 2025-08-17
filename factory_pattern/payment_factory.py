from inspect import getmembers, isclass, isabstract
import payment_methods

class PaymentFactory:
    payment_implementations = {}

    def __init__(self):
        self.load_payment_methods()


    def load_payment_methods(self):
        # this help us get all the implementatino done in the package payment_methods. 
        # so we want to get all the class and don't want to get the abstract class i.e payment.py file class.

        # This approach also helps in dynamically adding a new payment factory without changing the payment factory.

        implementations = getmembers(payment_methods, lambda m: isclass(m) and not isabstract(m))
        """
            {'CreditCardPayment': <class 'payment_methods.credit_card_payment.CreditCardPayment'>, 'GooglePayPayment': <class 'payment_methods.google_pay_payment.GooglePayPayment'>, 'PaypalPayment': <class 'payment_methods.paypal_payment.PaypalPayment'>}
        """
        for name, _type in implementations:
            if isclass(_type) and issubclass(_type, payment_methods.Payment):
                self.payment_implementations[name] = _type
            

    def create(self, payment_type: str):
        if payment_type in self.payment_implementations:
            return self.payment_implementations[payment_type]()
        else:
            raise ValueError(f"{payment_type} is not currently supported as payment method.")
