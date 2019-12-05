from simulation import Simulation


def check_time_config_affection():
    for b in [True, False]:
        continuous_time = Simulation(params={
            'NUMBER_OF_EMPLOYEES': 1,
            'TIME': 60 * 8,
            'NUMBER_OF_STATIONS': 5,
            'SELECT_RATIO': 5,
            'CONFIG_NAME': 'continuous_time',
            'MAKE_RANDOM_DEMANDS': False,
            'RELOCATE': b,
            'CONTINUOUS_TIME': True,
            'ELASTIC_VHECLES': -1,
            'MU': -2.15,
            'SIGMA': 1.27
        })

        continuous_time.get_all_datas()
        continuous_time.excute()

    continuous_time.draw_rsf_graph()
    continuous_time.draw_rse_graph()

    for b in [True, False]:
        no_continuous_time = Simulation(params={
            'NUMBER_OF_EMPLOYEES': 1,
            'TIME': 60 * 8,
            'NUMBER_OF_STATIONS': 5,
            'SELECT_RATIO': 5,
            'CONFIG_NAME': 'no_continuous_time',
            'MAKE_RANDOM_DEMANDS': False,
            'RELOCATE': b,
            'CONTINUOUS_TIME': False,
            'ELASTIC_VHECLES': -1,
            'MU': -2.15,
            'SIGMA': 1.27
        })

        no_continuous_time.get_all_datas()
        no_continuous_time.excute()

    no_continuous_time.draw_rsf_graph()
    no_continuous_time.draw_rse_graph()


def check_capa_and_vhecle_ratio():
    for i in [100, 50, 20, 2]:
        for j in range(i + 1):
            elastic_capa = Simulation(params={
                'NUMBER_OF_EMPLOYEES': 1,
                'TIME': 60 * 8,
                'NUMBER_OF_STATIONS': 5,
                'SELECT_RATIO': 5,
                'CONFIG_NAME': 'capa' + str(i),
                'MAKE_RANDOM_DEMANDS': False,
                'RELOCATE': True,
                'CONTINUOUS_TIME': True,
                'ELASTIC_VHECLES': j,
                'MU': -2.15,
                'SIGMA': 1.27
            })

            elastic_capa.get_all_datas()
            elastic_capa.excute()


# check_v_coords = Simulation(params={
#     'NUMBER_OF_EMPLOYEES': 1,
#     'TIME': 30,
#     'NUMBER_OF_STATIONS': 3,
#     'SELECT_RATIO': 5,
#     'CONFIG_NAME': 'v_coords_test',
#     'MAKE_RANDOM_DEMANDS': False,
#     'RELOCATE': True,
#     'CONTINUOUS_TIME': False,
#     'ELASTIC_VHECLES': -1,
#     'MU': -1.15,
#     'SIGMA': 1.27,
#     'SIGNIFICANT_DIGIT': 4
# })

# check_v_coords.get_all_datas()
# check_v_coords.excute()
# check_v_coords.draw_vhecle_transitflow()

check_cost = Simulation(params={
    'NUMBER_OF_EMPLOYEES': 1,
    'TIME': 30,
    'NUMBER_OF_STATIONS': 5,
    'SELECT_RATIO': 1,
    'CONFIG_NAME': 'hub_function',
    'MAKE_RANDOM_DEMANDS': False,
    'RELOCATE': True,
    'CONTINUOUS_TIME': False,
    'ELASTIC_VHECLES': -1,
    'MU': -2.15,
    'SIGMA': 1.27,
    'SIGNIFICANT_DIGIT': 4,
    'W_T': 0.1,
    'HUB_STATIONS': [1],
    'LAMBDA': 0.03
})

check_cost.get_all_datas()
check_cost.excute()
# check_cost.draw_vhecle_transitflow()
