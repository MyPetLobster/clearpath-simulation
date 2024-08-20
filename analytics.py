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
               f"No ERTS Collision Rate: {self.no_erts_collision_rate}\n" 

    def update(self, collision_count, car_count, emergency_count, analysis_mode_active):
        """
        Update the analytics data with the latest collision data.
        
        Args:
            - collision_count (int): The total number of collisions detected.
            - car_count (int): The total number of cars in the simulation.
            - emergency_count (int): The total number of emergency vehicles in the simulation.

        Modifies:
            - All attributes of the class.
        """
        if not analysis_mode_active:
            return
        
        if self.phase_two_active:
            self.erts_collision_count = collision_count
            self.erts_car_count = car_count
            self.erts_emergency_count = emergency_count
            self.erts_collision_rate = self.erts_collision_count / self.erts_emergency_count if self.erts_emergency_count > 0 else 0
            self.erts_weighted_collision_rate = self.calculate_weighted_collision_rate()
        else:
            self.no_erts_collision_count = collision_count
            self.no_erts_car_count = car_count
            self.no_erts_emergency_count = emergency_count
            self.no_erts_collision_rate = self.no_erts_collision_count / self.no_erts_emergency_count if self.no_erts_emergency_count > 0 else 0
            
    def calculate_weighted_collision_rate(self):
        """
        Calculate the weighted collision rate for ERTS vehicles.

        Returns:
            float: The weighted collision rate for ERTS vehicles.
        """
        weighting_numerator = (self.no_erts_emergency_count / self.erts_emergency_count) if self.erts_emergency_count > 0 else 0
        weighting_denominator = (self.no_erts_car_count / self.erts_car_count) if self.erts_car_count > 0 else 0
        weighting_factor = weighting_numerator / weighting_denominator if weighting_denominator > 0 else 1
        erts_weighted_collision_rate = self.erts_collision_rate * weighting_factor


        return erts_weighted_collision_rate