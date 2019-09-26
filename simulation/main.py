from simulation import Simulation

sim_5 = Simulation(params={
    'NUMBER_OF_EMPLOYEES': 4,
    'TIME': 60 * 8,
    'C_IN': 100,
    'C_OUT': 205,
    'C_E_FULL': 10000,
    'PRICE_PER_15': 205,
    'FUEL_CONSUMPTION': 35,
    'NUMBER_OF_STATIONS': 3,
    'SELECT_RATIO': 5,
    'CONFIG_NAME': 'sim_5_nojockey'
})

sim_5.get_all_datas()
