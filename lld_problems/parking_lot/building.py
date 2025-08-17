
class ParkingBuilding:
    def __init__(self, name):
        self.id = id(self)
        self.floors = []
        self.name = name
    
    def add_floor(self, floor):
        self.floors.append(floor)

    def get_all_spots(self, vehicle_type):
        spots = []
        for floor in self.floors:
            spots.extend(floor.get_available_spots(vehicle_type))
        return spots

