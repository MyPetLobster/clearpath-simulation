import json
import os
from datetime import datetime

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
        - phase_duration (int): The duration of each phase of the simulation.
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
        self.erts_base_weighted_collision_rate = 0
        self.erts_avg_weighted_collision_rate = 0
        self.erts_extrapolated_collisions = 0
        self.no_erts_collision_count = 0
        self.no_erts_car_count = 0
        self.no_erts_emergency_count = 0
        self.no_erts_collision_rate = 0
        self.no_erts_avg_weighted_collision_rate = 0
        self.no_erts_extrapolated_collisions = 0
        self.phase_duration = 300
        self.phase_two_active = False

    def __repr__(self):
        return f"ERTS Collision Count: {self.erts_collision_count}\n" \
               f"ERTS Car Count: {self.erts_car_count}\n" \
               f"ERTS Emergency Count: {self.erts_emergency_count}\n" \
               f"ERTS Collision Rate: {self.erts_collision_rate}\n" \
               f"ERTS Weighted Collision Rate: {self.erts_base_weighted_collision_rate}\n" \
               f"ERTS Avg Weighted Collision Rate: {self.erts_avg_weighted_collision_rate}\n" \
               f"No ERTS Collision Count: {self.no_erts_collision_count}\n" \
               f"No ERTS Car Count: {self.no_erts_car_count}\n" \
               f"No ERTS Emergency Count: {self.no_erts_emergency_count}\n" \
               f"No ERTS Collision Rate: {self.no_erts_collision_rate}\n" \
               f"No ERTS Avg Weighted Collision Rate: {self.no_erts_avg_weighted_collision_rate}\n"

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
        else:
            self.no_erts_collision_count = collision_count
            self.no_erts_car_count = car_count
            self.no_erts_emergency_count = emergency_count
            # self.no_erts_collision_rate = self.no_erts_collision_count / self.no_erts_emergency_count if self.no_erts_emergency_count > 0 else 0


    def finalize_analysis(self, export=True):
        self.erts_collision_rate = self.erts_collision_count / self.erts_emergency_count if self.erts_emergency_count > 0 else 0
        self.erts_base_weighted_collision_rate = self.calculate_weighted_collision_rate()
        self.erts_avg_weighted_collision_rate = self.calculate_avg_weighted_collision_rate(self.erts_emergency_count, self.erts_car_count, self.erts_collision_rate)
        self.no_erts_collision_rate = self.no_erts_collision_count / self.no_erts_emergency_count if self.no_erts_emergency_count > 0 else 0
        self.no_erts_avg_weighted_collision_rate = self.calculate_avg_weighted_collision_rate(self.no_erts_emergency_count, self.no_erts_car_count, self.no_erts_collision_rate)
        extrapolation_factor = self.no_erts_car_count / self.erts_car_count if self.erts_car_count > 0 else 0
        self.erts_extrapolated_collisions = self.erts_collision_count * extrapolation_factor

        if export:
            self.export_to_json()
        
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
    

    def calculate_avg_weighted_collision_rate(self, emergency_count, car_count, collision_rate):

        avg_emergency_count = (self.no_erts_emergency_count + self.erts_emergency_count) / 2
        avg_car_count = (self.no_erts_car_count + self.erts_car_count) / 2

        weighting_numerator = avg_emergency_count / emergency_count if emergency_count > 0 else 0
        weighting_denominator = avg_car_count / car_count if car_count > 0 else 0
        weighting_factor = weighting_numerator / weighting_denominator if weighting_denominator > 0 else 1
        avg_weighted_collision_rate = collision_rate * weighting_factor

        return avg_weighted_collision_rate
    
    def export_to_json(self):
        """
        Export the analytics data to a JSON file.

        Returns:
            str: The filename of the exported JSON file.
        """
        # create export dir if it doesn't exist
        if not os.path.exists("exports"):
            os.makedirs("exports")

        export_dict = self.create_export_dict()
        current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        filename = f"exports/analytics-{current_datetime}.json"

        with open(filename, "w") as file:
            json.dump(export_dict, file, indent=4)

        return filename
    

    def create_export_dict(self):
        """
        Export the analytics data to a JSON file.

        Returns:
            
        """
        current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        minutes = self.phase_duration // 60
        seconds = self.phase_duration % 60
        runtime = f"{minutes} minutes, {seconds} seconds"

        return {
            f"Analysis Data - {current_datetime}": {
                "Runtime": runtime,
                "ERTS - Inactive": {
                    "Collision Count": self.no_erts_collision_count,
                    "Car Count": self.no_erts_car_count,
                    "Emergency Count": self.no_erts_emergency_count,
                    "Collision Rate": self.no_erts_collision_rate,
                    "Avg Weighted Collision Rate": self.no_erts_avg_weighted_collision_rate
                },
                "ERTS - Active": {
                    "Collision Count": self.erts_collision_count,
                    "Car Count": self.erts_car_count,
                    "Emergency Count": self.erts_emergency_count,
                    "Collision Rate": self.erts_collision_rate,
                    "Base Weighted Collision Rate": self.erts_base_weighted_collision_rate,
                    "Avg Weighted Collision Rate": self.erts_avg_weighted_collision_rate,
                    "Extrapolated Collision Count": self.erts_extrapolated_collisions
                }
            }
        }