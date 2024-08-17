# self.analytics = {
#     "erts_collision_count": 0,
#     "erts_car_count": 0,
#     "erts_emergency_count": 0,
#     "erts_collision_rate": 0,
#     "no_erts_collision_count": 0,
#     "no_erts_car_count": 0,
#     "no_erts_emergency_count": 0,
#     "no_erts_collision_rate": 0
# }

class Analytics:
    """
    Class for storing and updating analytics data when operating in analysis mode.
    """
    def __init__(self):
        self.erts_collision_count = 0
        self.erts_car_count = 0
        self.erts_emergency_count = 0
        self.erts_collision_rate = 0
        self.erts_weighted_collision_rate = 0
        self.no_erts_collision_count = 0
        self.no_erts_car_count = 0
        self.no_erts_emergency_count = 0
        self.no_erts_collision_rate = 0
        self.no_erts_weighted_collision_rate = 0

    def update(self, collision_count, erts_active, car_count, emergency_count):
        if erts_active:
            self.erts_collision_count += collision_count
            self.erts_car_count += car_count
            self.erts_emergency_count += emergency_count
            total_erts_vehicles = self.erts_car_count + self.erts_emergency_count
            self.erts_collision_rate = self.erts_collision_count / total_erts_vehicles
        else:
            self.no_erts_collision_count += collision_count
            self.no_erts_car_count += car_count
            self.no_erts_emergency_count += emergency_count
            total_no_erts_vehicles = self.no_erts_car_count + self.no_erts_emergency_count
            self.no_erts_collision_rate = self.no_erts_collision_count / total_no_erts_vehicles

    def calculate_weighted_collision_rate(self):
        # Ensure there's no division by zero
        if self.erts_car_count + self.erts_emergency_count == 0 or self.no_erts_car_count + self.no_erts_emergency_count == 0:
            return
        
        # Calculate total vehicles in each phase
        total_erts_vehicles = self.erts_car_count + self.erts_emergency_count
        total_no_erts_vehicles = self.no_erts_car_count + self.no_erts_emergency_count

        # Calculate weighting factor
        weighting_factor = total_no_erts_vehicles / total_erts_vehicles

        # Calculate weighted collision rates
        self.erts_weighted_collision_rate = self.erts_collision_rate * weighting_factor
        self.no_erts_weighted_collision_rate = self.no_erts_collision_rate  # No need to adjust this as it's the baseline

        