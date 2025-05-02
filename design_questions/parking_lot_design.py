import uuid
from datetime import datetime
import time
from abc import ABC,abstractmethod
from math import *
import threading


        


#-----------------Fee Strategy---------------------------

class FeeStrategy(ABC):
    @abstractmethod
    def calculate_fee(self,entry_time,exit_time,spot_type):
        raise NotImplementedError()


class DailyRateStrategy(FeeStrategy):
    def __init__(self):
        self.rates =  {"small": 100, "medium": 150, "large": 200}

    def calculate_fee(self,entry_time,exit_time,spot_type):
        total_duration_hours = ceil((exit_time-entry_time).hours//24)
        return total_duration_hours*self.rates.get(spot_type,150)

class HourlyRateStrategy(FeeStrategy):
    def __init__(self):
        self.rates = {"small": 10, "medium": 20, "large": 30}

    def calculate_fee(self, entry_time, exit_time,spot_type):
        duration = (exit_time - entry_time).seconds // 3600 + 1
        return duration * self.rates.get(spot_type, 20)

class CalculateFeesStrategy:
    def __init__(self,strategy:FeeStrategy):
        self._strategy = strategy
    
    def set_strategy(self,strategy:FeeStrategy):
        self._strategy = strategy
    
    def calculate_fees(self,entry_time,exit_time,spot_type):
        return self._strategy.calculate_fee(entry_time,exit_time,spot_type)
    

#-----------------Entry and Exit Gate-----------------

class EntryGate:
    def __init__(self,gate_id,parking_lot):
        self.gate_id = gate_id
        self.parking_lot = parking_lot
    
    def park_vehicle(self,license_plate,vehicle_type,required_spot_type,strategy:FeeStrategy):
        return self.parking_lot.park_vehicle(license_plate,vehicle_type,required_spot_type,strategy,self.gate_id)

class ExitGate:
    def __init__(self, gate_id, parking_lot):
        self.gate_id = gate_id
        self.parking_lot = parking_lot

    def unpark_vehicle(self, ticket_id):
        return self.parking_lot.unpark_vehicle(ticket_id, exit_gate_id=self.gate_id)


#----------------------Parking Spot Class-----------------------------------------------

class ParkingSpot:
    def __init__(self,spot_id,spot_type):
        self.spot_id = spot_id
        self.spot_type = spot_type
        self.is_free =True
        self.license_plate = None
        self.vehicle_type = None
    
    def assign_vehicle(self,license_plate,vehicle_type):
        self.is_free = False
        self.vehicle_type = vehicle_type
        self.license_plate = license_plate

    def remove_vehicle(self):
        self.is_free = True
        self.license_plate = None
        self.vehicle_type = None
    

#-----------------------------------Parking Ticket Class------------------------------------


class ParkingTicket:
    def __init__(self, license_plate, vehicle_type, spot_id,strategy,entry_gate_id):
        self.ticket_id = str(uuid.uuid4())
        self.license_plate = license_plate
        self.vehicle_type = vehicle_type
        self.spot_id = spot_id
        self.entry_time = datetime.now()
        self.exit_time = None
        self.strategy = CalculateFeesStrategy(strategy)
        self.entry_gate_id = entry_gate_id
        self.exit_gate_id = None

    def close_ticket(self,exit_gate_id):
        self.exit_gate_id = exit_gate_id
        self.exit_time = datetime.now()

#-------------------------------Parking Floor class----------------------------
    
class ParkingFloor:
    def __init__(self,floor_number):
        self.floor_number = floor_number
        self.spots = []
        self.lock = threading.Lock()  # Lock to protect spot allocation
    
    def add_spot(self,spot_id,spot_type):
        self.spots.append(ParkingSpot(spot_id,spot_type))
    
    def get_spot(self,spot_id):
        for spot in self.spots:
            if spot.spot_id == spot_id:
                return spot
        return []

    def find_and_allocate_spot(self,spot_type,vehicle_type,license_plate):
        with self.lock:  # Lock the entire allocation process
            for spot in self.spots:
                if spot.is_free and spot.spot_type == spot_type:
                    spot.assign_vehicle(vehicle_type, license_plate)
                    return spot
            return None  # No spot available
    
    def show_available_spots(self):
        available = {"small": 0, "medium": 0, "large": 0}
        for spot in self.spots:
            if spot.is_free:
                available[spot.spot_type] += 1
        print("📊 Available Spots:")
        for spot_type, count in available.items():
            print(f"  {spot_type.capitalize()}: {count}")

#--------------------------------------Parking Lot Class---------------------------

class ParkingLot:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ParkingLot, cls).__new__(cls)
            # initialize instance variables
            cls._instance.floors = []
            cls._instance.active_tickets = {}
        return cls._instance

    def add_floor(self,floor:ParkingFloor):
        self.floors.append(floor)

    def park_vehicle(self,license_plate,vehicle_type,required_spot_type,strategy:FeeStrategy,entry_gate_id):
        for floor in self.floors:
            allocated_spot = floor.find_and_allocate_spot(required_spot_type,vehicle_type,license_plate)
            if allocated_spot :
                ticket = ParkingTicket(license_plate,vehicle_type,allocated_spot.spot_id,strategy,entry_gate_id)
                self.active_tickets[ticket.ticket_id] = ticket
                print(f"✅ Vehicle parked at spot {allocated_spot.spot_id}. Ticket ID: {ticket.ticket_id}. Floor: {floor.floor_number}")
                return ticket
                
        print("❌ No available spots for this vehicle type.")
        return None

    def unpark_vehicle(self,ticket_id,exit_gate_id):
        ticket = self.active_tickets.get(ticket_id)
        if not ticket:
            print("No such active ticket")
            return
        
        for floor in self.floors:
            spot = floor.get_spot(ticket.spot_id)
            if spot != []:
                spot.remove_vehicle()
                ticket.close_ticket(exit_gate_id)
                print(f"🚗 Vehicle with license plate {ticket.license_plate} has exited from floor {floor.floor_number}")
                print(f"🕒 Duration: {(ticket.exit_time - ticket.entry_time).seconds} seconds")
                fees = ticket.strategy.calculate_fees(ticket.entry_time,ticket.exit_time,spot.spot_type)
                print(f"With total fees: {fees}")
                del self.active_tickets[ticket_id]
                return
        print("No spot found for this ticket")

    
def simulate_entry(gate, license_plate,vehicle_type, spot_type,strategy):
    ticket = gate.parking_lot.park_vehicle(license_plate, vehicle_type, spot_type,strategy,gate.gate_id)
    if ticket:
        print(f"Ticket issued: {ticket.ticket_id} for {license_plate}")
    else:
        print(f"Failed to park {license_plate}")



    
# Create parking lot
if __name__ == '__main__':
    lot = ParkingLot()
    floor1 = ParkingFloor(1)
    floor1.add_spot("F1_S1", "small")
    floor1.add_spot("F1_S2", "medium")

    floor2 = ParkingFloor(2)
    floor2.add_spot("F2_S1", "large")
    floor2.add_spot("F2_S2", "small")

    lot.add_floor(floor1)
    lot.add_floor(floor2)

    gate1 = EntryGate("G1", lot)
    gate2 = EntryGate("G2", lot)

    t1 = threading.Thread(target=simulate_entry, args=(gate1, "DL123", "car","medium",HourlyRateStrategy()))
    t2 = threading.Thread(target=simulate_entry, args=(gate2, "DL456", "van","medium",DailyRateStrategy()))

    t1.start()
    t2.start()
    t1.join()
    t2.join()
