from simulation import Simulation

# continuous_time = Simulation(params={
#     'NUMBER_OF_EMPLOYEES': 1,
#     'TIME': 60 * 8,
#     'C_IN': 100,
#     'C_OUT': 205,
#     'C_E_FULL': 10000,
#     'PRICE_PER_15': 205,
#     'FUEL_CONSUMPTION': 35,
#     'NUMBER_OF_STATIONS': 5,
#     'SELECT_RATIO': 5,
#     'CONFIG_NAME': 'continuous_time',
#     'MAKE_RANDOM_DEMANDS': False,
#     'RELOCATE': True,
#     'CONTINUOUS_TIME': True
# })

# continuous_time.get_all_datas()
# continuous_time.excute()
# continuous_time.draw_rsf_graph()
# continuous_time.draw_rse_graph()

# no_continuous_time = Simulation(params={
#     'NUMBER_OF_EMPLOYEES': 1,
#     'TIME': 60 * 8,
#     'C_IN': 100,
#     'C_OUT': 205,
#     'C_E_FULL': 10000,
#     'PRICE_PER_15': 205,
#     'FUEL_CONSUMPTION': 35,
#     'NUMBER_OF_STATIONS': 5,
#     'SELECT_RATIO': 5,
#     'CONFIG_NAME': 'no_continuous_time',
#     'MAKE_RANDOM_DEMANDS': False,
#     'RELOCATE': True,
#     'CONTINUOUS_TIME': False
# })

# no_continuous_time.get_all_datas()
# no_continuous_time.excute()
# no_continuous_time.draw_rsf_graph()
# no_continuous_time.draw_rse_graph()


# for mu in [i / 10 for i in range(-30, 35, 1)]:
#     for sigma in [j / 10 for j in range(0, 21, 1)]:
#         vms = Simulation(params={
#             'NUMBER_OF_EMPLOYEES': 1,
#             'TIME': 60 * 2,
#             'C_IN': 100,
#             'C_OUT': 205,
#             'C_E_FULL': 10000,
#             'PRICE_PER_15': 205,
#             'FUEL_CONSUMPTION': 35,
#             'NUMBER_OF_STATIONS': 5,
#             'SELECT_RATIO': 5,
#             'CONFIG_NAME': 'vhecle_mu_sigma2',
#             'MAKE_RANDOM_DEMANDS': True,
#             'RELOCATE': True,
#             'CONTINUOUS_TIME': True,
#             'VHECLES': 3,
#             'MU': mu,
#             'SIGMA': sigma
#         })
#         vms.get_all_datas()
#         vms.excute()

# for i in range(11, 21):
#     vms = Simulation(params={
#         'NUMBER_OF_EMPLOYEES': 1,
#         'TIME': 60 * 3,
#         'C_IN': 100,
#         'C_OUT': 205,
#         'C_E_FULL': 10000,
#         'PRICE_PER_15': 205,
#         'FUEL_CONSUMPTION': 35,
#         'NUMBER_OF_STATIONS': 5,
#         'SELECT_RATIO': i,
#         'CONFIG_NAME': 'ratio' + str(i),
#         'MAKE_RANDOM_DEMANDS': True,
#         'RELOCATE': True,
#         'CONTINUOUS_TIME': True,
#         'VHECLES': False,
#         'MU': -2.15,
#         'SIGMA': 1.27
#     })
#     vms.get_all_datas()
#     vms.excute()

# static_capa.draw_rsf_graph()
# static_capa.draw_rse_graph()

dynamic_capa = Simulation(params={
    'NUMBER_OF_EMPLOYEES': 1,
    'TIME': 60 * 3,
    'C_IN': 100,
    'C_OUT': 205,
    'C_E_FULL': 10000,
    'PRICE_PER_15': 205,
    'FUEL_CONSUMPTION': 35,
    'NUMBER_OF_STATIONS': 5,
    'SELECT_RATIO': 5,
    'CONFIG_NAME': 'capa_final',
    'MAKE_RANDOM_DEMANDS': True,
    'RELOCATE': True,
    'CONTINUOUS_TIME': True,
    'VHECLES': 2,
    'MU': -2.15,
    'SIGMA': 1.27
})

dynamic_capa.get_all_datas()
dynamic_capa.excute()
# dynamic_capa.draw_rsf_graph()
# dynamic_capa.draw_rse_graph()
