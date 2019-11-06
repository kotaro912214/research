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

# station10_time3h = Simulation(params={
#     'NUMBER_OF_EMPLOYEES': 2,
#     'TIME': 60 * 3,
#     'C_IN': 100,
#     'C_OUT': 205,
#     'C_E_FULL': 10000,
#     'PRICE_PER_15': 205,
#     'FUEL_CONSUMPTION': 35,
#     'NUMBER_OF_STATIONS': 10,
#     'SELECT_RATIO': 5,
#     'CONFIG_NAME': 'do_relocate',
#     'MAKE_RANDOM_DEMANDS': False,
#     'RELOCATE': False
# })

# station10_time3h.get_all_datas()
# station10_time3h.excute()

# station5_time2h = Simulation(params={
#     'NUMBER_OF_EMPLOYEES': 5,
#     'TIME': 60 * 2,
#     'C_IN': 100,
#     'C_OUT': 205,
#     'C_E_FULL': 10000,
#     'PRICE_PER_15': 205,
#     'FUEL_CONSUMPTION': 35,
#     'NUMBER_OF_STATIONS': 5,
#     'SELECT_RATIO': 5,
#     'CONFIG_NAME': 'for_contest',
#     'MAKE_RANDOM_DEMANDS': False,
#     'RELOCATE': True
# })

# station5_time2h.get_all_datas()
# station5_time2h.excute()

rse = Simulation(params={
    'NUMBER_OF_EMPLOYEES': 1,
    'TIME': 60,
    'C_IN': 100,
    'C_OUT': 205,
    'C_E_FULL': 10000,
    'PRICE_PER_15': 205,
    'FUEL_CONSUMPTION': 35,
    'NUMBER_OF_STATIONS': 5,
    'SELECT_RATIO': 3,
    'CONFIG_NAME': 'for_cost',
    'MAKE_RANDOM_DEMANDS': True,
    'RELOCATE': False
})

rse.get_all_datas()
rse.excute()
# rse.draw_rsf_graph()
# rse.draw_rse_graph()
