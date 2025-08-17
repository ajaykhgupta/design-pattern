class SpotAllocationStrategy:

    def find_available_spot(self, buildings, vehicle_type):
        for building in buildings:
            spots = building.get_all_spots(vehicle_type)
            if spots:
                return spots[0]  # Pick the first available one
        return None
