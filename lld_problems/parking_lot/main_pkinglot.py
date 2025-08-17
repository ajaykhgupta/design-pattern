from threading import Lock
from parkinglot import ParkingLot
from building import ParkingBuilding
from parking_floor import ParkingFloor
from parking_spot import ParkingSpot
from vehicle import Vehicle
from payment import CashPayment
from entrance import Entrance
from exit import Exit


pk = ParkingLot.get_instance()
b1 = ParkingBuilding(name="building1")
b2 = ParkingBuilding(name="building2")
pk.add_building(building=b1)
pk.add_building(building=b2)


build_1_floor1 = ParkingFloor(building=b1, floor_num=1)
build_1_floor2 = ParkingFloor(building=b1, floor_num=2)
build_2_floor1 = ParkingFloor(building=b2, floor_num=1)
b1.add_floor(build_1_floor1)
b1.add_floor(build_1_floor2)
b1.add_floor(build_2_floor1)

vehicle1 = Vehicle("KA-01-HH-1234", "Car")
vehicle2 = Vehicle("KA-01-HH-1414", "Car")
vehicle3 = Vehicle("KA-01-HH-1413", "Car")
vehicle4 = Vehicle("KA-01-HH-1412", "Car")
vehicle5 = Vehicle("KA-01-HH-1411", "Car")

spots2 = ParkingSpot(ev_supported=True, vehicle_type_supported="Car")
spots1 = ParkingSpot(ev_supported=True, vehicle_type_supported="Car")
spots3 = ParkingSpot(ev_supported=True, vehicle_type_supported="Bike")
spots4 = ParkingSpot(ev_supported=True, vehicle_type_supported="Bike")
spots5 = ParkingSpot(ev_supported=True, vehicle_type_supported="Car")
# spots1 = ParkingSpot(ev_supported=True, floor=build_1_floor1, vehicle_type=vehicle1)
# spots2 = ParkingSpot(ev_supported=True, floor=build_1_floor1, vehicle_type=vehicle2)
# spots3 = ParkingSpot(ev_supported=True, floor=build_1_floor1, vehicle_type=vehicle3)
# spots4 = ParkingSpot(ev_supported=True, floor=build_1_floor2, vehicle_type=vehicle4)
# spots5 = ParkingSpot(ev_supported=True, floor=build_1_floor2, vehicle_type=vehicle5)


build_1_floor1.add_spots(spots1)
build_1_floor1.add_spots(spots2)
build_1_floor1.add_spots(spots3)
build_1_floor2.add_spots(spots4)
build_1_floor2.add_spots(spots5)

entrance = Entrance(1, "Main Gate")
exit_gate = Exit(1, "Exit A")
pk.add_entrance(entrance)
pk.add_exit(exit_gate)

vehicle = Vehicle("KA-01-AA-1234", "Car")
ticket = pk.park_vehicle(vehicle)

# Unpark
if ticket:
    pk.unpark_vehicle(ticket.ticket_id, CashPayment())


