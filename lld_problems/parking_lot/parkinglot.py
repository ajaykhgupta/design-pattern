from threading import Lock
from strategy import SpotAllocationStrategy
from ticket import ParkingTicket
from fee_policy import FeePolicy

class ParkingLot:
    instance = None
    lock = Lock()
    _initialized=False

    def __init__(self):
        if ParkingLot._initialized:
            raise RuntimeError("This is a singleton class! Invoke get_instance.")
        self.buildings = []
        self.entrances = []
        self.exits = []
        self.strategy = SpotAllocationStrategy()
        self.ticket_counter = 1
        self.active_tickets = {}
        ParkingLot._initialized = True


    @classmethod
    def get_instance(cls):
        if not cls.instance:
            with cls.lock:
                if not cls.instance:
                    cls.instance = cls.__new__(cls)
                    cls.__init__(cls.instance)
        return cls.instance

    def add_building(self, building):
        self.buildings.append(building)
    
    def add_entrance(self, entrance):
        self.entrances.append(entrance)

    def add_exit(self, exit):
        self.exits.append(exit)

    def park_vehicle(self, vehicle):
        spot = self.strategy.find_available_spot(self.buildings, vehicle.vehicle_type)
        if not spot:
            print("No spot available")
            return
        spot.assign_vehicle(vehicle)
        ticket = ParkingTicket(self.ticket_counter, vehicle, spot)
        self.ticket_counter += 1
        self.active_tickets[ticket.ticket_id] = ticket
        print(f"Vehicle parked. Ticket ID: {ticket.ticket_id}")
        return ticket

    def unpark_vehicle(self, ticket_id, payment_method):
        ticket = self.active_tickets.get(ticket_id)
        if not ticket:
            print("Invalid ticket ID")
            return
        ticket.close_ticket()
        fee = FeePolicy.calculate_fee(ticket.entry_time, ticket.exit_time)
        payment_method.pay(fee)
        ticket.spot.remove_vehicle()
        ticket.fee_paid = True
        del self.active_tickets[ticket_id]
        print(f"Vehicle unparked. Total Fee: ₹{fee}")


