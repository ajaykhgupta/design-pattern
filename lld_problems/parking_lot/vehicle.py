from enum import Enum

class VehicleType(Enum):
    Car = "CAR"
    BUS = "BUS"
    BIKE = "BIKE"

class Vehicle:
    def __init__(self, license_plate, vehicle_type: VehicleType):
        if not isinstance(vehicle_type, VehicleType):
            raise ValueError(f"Vehicle type should be any one of {list(VehicleType)}")
        self.license_plate = license_plate
        self.vehicle_type = vehicle_type
