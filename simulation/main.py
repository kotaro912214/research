from simulation import Simulation

continuous_time = Simulation(params={
    'NUMBER_OF_EMPLOYEES': 1,
    'TIME': 60 * 8,
    'C_IN': 100,
    'C_OUT': 205,
    'C_E_FULL': 10000,
    'PRICE_PER_15': 205,
    'FUEL_CONSUMPTION': 35,
    'NUMBER_OF_STATIONS': 5,
    'SELECT_RATIO': 5,
    'CONFIG_NAME': 'continuous_time',
    'MAKE_RANDOM_DEMANDS': False,
    'RELOCATE': True,
    'CONTINUOUS_TIME': True
})

# continuous_time.get_all_datas()
# continuous_time.excute()
continuous_time.draw_rsf_graph()
continuous_time.draw_rse_graph()

no_continuous_time = Simulation(params={
    'NUMBER_OF_EMPLOYEES': 1,
    'TIME': 60 * 8,
    'C_IN': 100,
    'C_OUT': 205,
    'C_E_FULL': 10000,
    'PRICE_PER_15': 205,
    'FUEL_CONSUMPTION': 35,
    'NUMBER_OF_STATIONS': 5,
    'SELECT_RATIO': 5,
    'CONFIG_NAME': 'no_continuous_time',
    'MAKE_RANDOM_DEMANDS': False,
    'RELOCATE': True,
    'CONTINUOUS_TIME': False
})

# no_continuous_time.get_all_datas()
# no_continuous_time.excute()
no_continuous_time.draw_rsf_graph()
no_continuous_time.draw_rse_graph()
