class Analytics:
    """
    Class for storing and updating analytics data when operating in analysis mode.

    Attributes:
        - erts_collision_count (int): The total number of collisions detected with ERTS active.
        - erts_car_count (int): The total number of cars generated with ERTS active.
        - erts_emergency_count (int): The total number of emergency vehicles generated with ERTS active.
        - erts_collision_rate (float): The collision rate with ERTS active.
        - erts_weighted_collision_rate (float): The weighted collision rate with ERTS active.
        - no_erts_collision_count (int): The total number of collisions detected with ERTS inactive.
        - no_erts_car_count (int): The total number of cars generated with ERTS inactive.
        - no_erts_emergency_count (int): The total number of emergency vehicles generated with ERTS inactive.
        - no_erts_collision_rate (float): The collision rate with ERTS inactive.
        - no_erts_weighted_collision_rate (float): The weighted collision rate with ERTS inactive.
        - phase_two_active (bool): Whether or not phase two of the simulation is active.

    Methods:
        - update: Update the analytics data with the latest collision data.
        - calculate_weighted_collision_rates: Calculate the weighted collision rates for ERTS and non-ERTS vehicles.
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
        self.phase_two_active = False

    def __repr__(self):
        return f"ERTS Collision Count: {self.erts_collision_count}\n" \
               f"ERTS Car Count: {self.erts_car_count}\n" \
               f"ERTS Emergency Count: {self.erts_emergency_count}\n" \
               f"ERTS Collision Rate: {self.erts_collision_rate}\n" \
               f"ERTS Weighted Collision Rate: {self.erts_weighted_collision_rate}\n" \
               f"No ERTS Collision Count: {self.no_erts_collision_count}\n" \
               f"No ERTS Car Count: {self.no_erts_car_count}\n" \
               f"No ERTS Emergency Count: {self.no_erts_emergency_count}\n" \
               f"No ERTS Collision Rate: {self.no_erts_collision_rate}\n" \
               f"No ERTS Weighted Collision Rate: {self.no_erts_weighted_collision_rate}\n"

    def update(self, collision_count, erts_active, car_count, emergency_count):
        """
        Update the analytics data with the latest collision data.
        
        Args:
            - collision_count (int): The total number of collisions detected.
            - erts_active (bool): Whether or not ERTS is active.
            - car_count (int): The total number of cars in the simulation.
            - emergency_count (int): The total number of emergency vehicles in the simulation.

        Modifies:
            - All attributes of the class.
        """

        weighted_collision_rates = list(self.calculate_weighted_collision_rates())
        if erts_active:
            self.phase_two_active = True
            self.erts_collision_count = collision_count
            self.erts_car_count = car_count
            self.erts_emergency_count = emergency_count
            total_erts_vehicles = self.erts_car_count + self.erts_emergency_count
            self.erts_collision_rate = self.erts_collision_count / total_erts_vehicles if total_erts_vehicles > 0 else 0
            self.erts_weighted_collision_rate = weighted_collision_rates[0]
        else:
            if not self.phase_two_active:
                self.no_erts_collision_count = collision_count
                self.no_erts_car_count = car_count
                self.no_erts_emergency_count = emergency_count
                total_no_erts_vehicles = self.no_erts_car_count + self.no_erts_emergency_count
                self.no_erts_collision_rate = self.no_erts_collision_count / total_no_erts_vehicles if total_no_erts_vehicles > 0 else 0
                self.no_erts_weighted_collision_rate = weighted_collision_rates[1]

    def calculate_weighted_collision_rates(self):
        """
        Calculate the weighted collision rates for ERTS and non-ERTS vehicles.

        Returns:
            - tuple: A tuple containing the weighted collision rates for ERTS and non-ERTS vehicles.
        """
        # Ensure there's no division by zero
        if self.erts_car_count + self.erts_emergency_count == 0 or self.no_erts_car_count + self.no_erts_emergency_count == 0:
            return 0.0, 0.0
        
        # Calculate total vehicles in each phase
        total_erts_vehicles = self.erts_car_count + self.erts_emergency_count
        total_no_erts_vehicles = self.no_erts_car_count + self.no_erts_emergency_count

        # Calculate weighting factor
        weighting_factor = total_no_erts_vehicles / total_erts_vehicles

        # Calculate weighted collision rates
        self.erts_weighted_collision_rate = self.erts_collision_rate * weighting_factor
        self.no_erts_weighted_collision_rate = self.no_erts_collision_rate  # No need to adjust this as it's the baseline

        return self.erts_weighted_collision_rate, self.no_erts_weighted_collision_rate