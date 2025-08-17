import datetime

class ParkingTicket:
    def __init__(self, ticket_id, vehicle, spot):
        self.ticket_id = ticket_id
        self.vehicle = vehicle
        self.spot = spot
        self.entry_time = datetime.datetime.now()
        self.exit_time = None
        self.fee_paid = False

    def close_ticket(self):
        self.exit_time = datetime.datetime.now()