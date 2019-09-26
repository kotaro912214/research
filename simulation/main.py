from simulation import Simulation

sim_5 = Simulation(params={
    'NUMBER_OF_EMPLOYEES': 4,
    'TIME': 60 * 8,
    'C_IN': 100,
    'C_OUT': 205,
    'C_E_FULL': 10000,
    'PRICE_PER_15': 205,
    'FUEL_CONSUMPTION': 35,
    'NUMBER_OF_STATIONS': 5,
    'CONFIG_NAME': 'test_5'
})
# sim_5.get_station_codes_and_coords()
# sim_5.get_station_urls()
# sim_5.get_station_capacities()
sim_5.get_station_transitions()
