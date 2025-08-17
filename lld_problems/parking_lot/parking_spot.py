
class ParkingSpot:
    def __init__(self, vehicle_type_supported, ev_supported=False):
        self.id = id(self)
        self.vehicle_type_supported = vehicle_type_supported
        self.is_occupied = False
        self.ev_supported = ev_supported
        # self.floor = floor
        self.vehicle = None

    def is_available_for(self, vehicle_type):
        return not self.is_occupied and self.vehicle_type_supported == vehicle_type
    
    # def get_floor_number(self):
    #     return self.floor.floor_num

    # def get_building(self):
    #     return self.floor.building
    
    def assign_vehicle(self, vehicle):
        self.is_occupied = True
        self.vehicle = vehicle
    
    def remove_vehicle(self):
        self.is_occupied = False
        self.vehicle = None
