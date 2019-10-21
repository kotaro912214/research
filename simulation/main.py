from simulation import Simulation

sim_5 = Simulation(params={
    'NUMBER_OF_EMPLOYEES': 1,
    'TIME': 30,
    'C_IN': 100,
    'C_OUT': 205,
    'C_E_FULL': 10000,
    'PRICE_PER_15': 205,
    'FUEL_CONSUMPTION': 35,
    'NUMBER_OF_STATIONS': 5,
    'SELECT_RATIO': 10,
    'CONFIG_NAME': 'car5_nojockey',
    'MAKE_RANDOM_DEMANDS': True
})

sim_5.get_all_datas()
sim_5.excute()
