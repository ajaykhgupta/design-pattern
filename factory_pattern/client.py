from payment_factory import PaymentFactory

factory = PaymentFactory()
# Things that can be improved but not that important is making this input class name not case sensitive and taking
# input as paypalpayment.
payment = factory.create("PaypalPayment")
payment.pay(1000.0)
