from simulation import Simulation

sim_5 = Simulation(params={
    'NUMBER_OF_EMPLOYEES': 1,
    'TIME': 30,
    'C_IN': 100,
    'C_OUT': 205,
    'C_E_FULL': 10000,
    'PRICE_PER_15': 205,
    'FUEL_CONSUMPTION': 35,
    'NUMBER_OF_STATIONS': 3,
    'SELECT_RATIO': 1,
    'CONFIG_NAME': 'test_for_reloc',
    'MAKE_RANDOM_DEMANDS': False
})

sim_5.get_all_datas()
sim_5.excute()
