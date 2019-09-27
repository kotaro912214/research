from simulation import Simulation

sim_5 = Simulation(params={
    'NUMBER_OF_EMPLOYEES': 4,
    'TIME': 15,
    'C_IN': 100,
    'C_OUT': 205,
    'C_E_FULL': 10000,
    'PRICE_PER_15': 205,
    'FUEL_CONSUMPTION': 35,
    'NUMBER_OF_STATIONS': 3,
    'SELECT_RATIO': 10,
    'CONFIG_NAME': 'sim_3_nojockey'
})

sim_5.get_all_datas()
sim_5.excute()
