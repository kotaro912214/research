from simulation import Simulation
import myfunc

sim_5 = Simulation(params={
    'NUMBER_OF_EMPLOYEES': 4,
    'TIME': 60 * 8,
    'C_IN': 100,
    'C_OUT': 205,
    'C_E_FULL': 10000,
    'PRICE_PER_15': 205,
    'FUEL_CONSUMPTION': 35,
    'NUMBER_OF_STATIONS': 10
  })
sim_5.make_stations_coord()
sim_5.make_stations_links()
sim_5.make_available_cars()

print(myfunc.my_round(2.823321, 2))
