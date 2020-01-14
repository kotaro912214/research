from simulation import Simulation
# from prev_simulation import Simulation


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

# one_one = Simulation(params={
#     'NUMBER_OF_EMPLOYEES': 1,
#     'TIME': 60*4,
#     'NUMBER_OF_STATIONS': 10,
#     'SELECT_RATIO': 3,
#     'CONFIG_NAME': '1.1',
#     'MAKE_RANDOM_DEMANDS': False,
#     'RANDOM_MODE': 'poisson',
#     'RELOCATE': False,
#     'CONTINUOUS_TIME': False,
#     'ELASTIC_VHECLES': -1,
#     'MU': -2.15,
#     'SIGMA': 1.27,
#     'SIGNIFICANT_DIGIT': 4,
#     'W_T': 0.1,
#     'HUB_STATIONS': [],
#     'LAMBDA': 0.003,
#     'DEMAND_PATH': ''
# })

# one_one.get_all_datas()
# one_one.excute()

# one_two = Simulation(params={
#     'NUMBER_OF_EMPLOYEES': 1,
#     'TIME': 60*4,
#     'NUMBER_OF_STATIONS': 10,
#     'SELECT_RATIO': 3,
#     'CONFIG_NAME': '1.2',
#     'MAKE_RANDOM_DEMANDS': False,
#     'RANDOM_MODE': 'poisson',
#     'RELOCATE': True,
#     'CONTINUOUS_TIME': False,
#     'ELASTIC_VHECLES': -1,
#     'MU': -2.15,
#     'SIGMA': 1.27,
#     'SIGNIFICANT_DIGIT': 4,
#     'W_T': 0.1,
#     'HUB_STATIONS': [],
#     'LAMBDA': 0.003,
#     'DEMAND_PATH': ''
# })

# one_two.get_all_datas()
# one_two.excute()

# two_one = Simulation(params={
#     'NUMBER_OF_EMPLOYEES': 1,
#     'TIME': 60*4,
#     'NUMBER_OF_STATIONS': 10,
#     'SELECT_RATIO': 3,
#     'CONFIG_NAME': '2.1',
#     'MAKE_RANDOM_DEMANDS': False,
#     'RANDOM_MODE': 'poisson',
#     'RELOCATE': False,
#     'CONTINUOUS_TIME': True,
#     'ELASTIC_VHECLES': -1,
#     'MU': -2.15,
#     'SIGMA': 1.27,
#     'SIGNIFICANT_DIGIT': 4,
#     'W_T': 0.1,
#     'HUB_STATIONS': [],
#     'LAMBDA': 0.003,
#     'DEMAND_PATH': ''
# })

# two_one.get_all_datas()
# two_one.excute()

# two_two_one = Simulation(params={
#     'NUMBER_OF_EMPLOYEES': 1,
#     'TIME': 60*4,
#     'NUMBER_OF_STATIONS': 10,
#     'SELECT_RATIO': 3,
#     'CONFIG_NAME': '2.2.1',
#     'MAKE_RANDOM_DEMANDS': False,
#     'RANDOM_MODE': 'poisson',
#     'RELOCATE': True,
#     'CONTINUOUS_TIME': True,
#     'ELASTIC_VHECLES': -1,
#     'MU': -2.15,
#     'SIGMA': 1.27,
#     'SIGNIFICANT_DIGIT': 4,
#     'W_T': 0.1,
#     'HUB_STATIONS': [],
#     'LAMBDA': 0.003,
#     'DEMAND_PATH': ''
# })

# two_two_one.get_all_datas()
# two_two_one.excute()

# two_two_two = Simulation(params={
#     'NUMBER_OF_EMPLOYEES': 1,
#     'TIME': 60*4,
#     'NUMBER_OF_STATIONS': 10,
#     'SELECT_RATIO': 1,
#     'CONFIG_NAME': '2.2.2',
#     'MAKE_RANDOM_DEMANDS': False,
#     'RANDOM_MODE': 'poisson',
#     'RELOCATE': True,
#     'CONTINUOUS_TIME': True,
#     'ELASTIC_VHECLES': -1,
#     'MU': -2.15,
#     'SIGMA': 1.27,
#     'SIGNIFICANT_DIGIT': 4,
#     'W_T': 0.1,
#     'HUB_STATIONS': [1],
#     'LAMBDA': 0.003,
#     'DEMAND_PATH': ''
# })

# two_two_two.get_all_datas()
# two_two_two.excute()


test_experiment = Simulation(params={
    'NUMBER_OF_EMPLOYEES': 1,
    'TIME': 60 * 4,
    'NUMBER_OF_STATIONS': 10,
    'SELECT_RATIO': 1,
    'CONFIG_NAME': 'test_experiment',
    'MAKE_RANDOM_DEMANDS': True,
    'RANDOM_MODE': 'poisson',
    'RELOCATE': False,
    'CONTINUOUS_TIME': True,
    'ELASTIC_VHECLES': -1,
    'MU': -2.15,
    'SIGMA': 1.27,
    'SIGNIFICANT_DIGIT': 4,
    'W_T': 0.1,
    'HUB_STATIONS': [],
    'LAMBDA': 0.003,
    'DEMAND_PATH': ''
})

test_experiment.get_all_datas()
for i in range(10):
    test_experiment.excute()

# b = Simulation(params={
#     'NUMBER_OF_EMPLOYEES': 1,
#     'TIME': 4 * 60,
#     'NUMBER_OF_STATIONS': 10,
#     'SELECT_RATIO': 1,
#     'CONFIG_NAME': 'b',
#     'MAKE_RANDOM_DEMANDS': True,
#     'RELOCATE': True,
#     'CONTINUOUS_TIME': True,
#     'ELASTIC_VHECLES': -1,
#     'MU': -1.15,
#     # 'SIGMA': 0.604,
#     'SIGMA': 0.7,
#     'SIGNIFICANT_DIGIT': 4
# })

# b.get_all_datas()
# b.excute()
