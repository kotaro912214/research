from simulation import Simulation

# car3_time30 = Simulation(params={
#     'NUMBER_OF_EMPLOYEES': 1,
#     'TIME': 30,
#     'C_IN': 100,
#     'C_OUT': 205,
#     'C_E_FULL': 10000,
#     'PRICE_PER_15': 205,
#     'FUEL_CONSUMPTION': 35,
#     'NUMBER_OF_STATIONS': 3,
#     'SELECT_RATIO': 5,
#     'CONFIG_NAME': 'car3_time30',
#     'MAKE_RANDOM_DEMANDS': False,
#     'RELOCATE': True
# })

# car3_time30.get_all_datas()
# car3_time30.excute()

car3_time30 = Simulation(params={
    'NUMBER_OF_EMPLOYEES': 1,
    'TIME': 30,
    'C_IN': 100,
    'C_OUT': 205,
    'C_E_FULL': 10000,
    'PRICE_PER_15': 205,
    'FUEL_CONSUMPTION': 35,
    'NUMBER_OF_STATIONS': 5,
    'SELECT_RATIO': 4,
    'CONFIG_NAME': 'only_rsf_avail',
    'MAKE_RANDOM_DEMANDS': True,
    'RELOCATE': True
})

car3_time30.get_all_datas()
car3_time30.excute()
