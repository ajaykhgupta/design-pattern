
class ParkingFloor:
    def __init__(self, floor_num, building):
        self.id = id(self)
        self.floor_num = floor_num
        # self.building = building
        self.spots = []
    
    def add_spots(self, spot):
        self.spots.append(spot)

    def get_available_spots(self, vehicle_type):
        return [spot for spot in self.spots if spot.is_available_for(vehicle_type)]

