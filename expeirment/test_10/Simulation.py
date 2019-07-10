import get_station
from pathlib import Path, PureWindowsPath

class Simulation():

  def __init__(self, params={
    'NUMBER_OF_EMPLOYEES': 4,
    'TIME': 60 * 8,
    'C_IN': 100,
    'C_OUT': 205,
    'C_E_FULL': 10000,
    'PRICE_PER_15': 205,
    'FUEL_CONSUMPTION': 35,
    'NUMBER_OF_STATIONS': 10
  }):
    self.NUMBER_OF_EMPLOYEES = params['NUMBER_OF_EMPLOYEES']
    self.TIME = params['TIME']
    self.C_IN = params['C_IN']
    self.C_OUT  = params['C_OUT']
    self.C_E_FULL  = params['C_E_FULL']
    self.PRICE_PER_15  = params['PRICE_PER_15']
    self.FUEL_CONSUMPTION  = params['FUEL_CONSUMPTION']
    self.NUMBER_OF_STATIONS  = params['NUMBER_OF_STATIONS']
    self.C_E_DAY = self.C_E_FULL * (self.TIME / 8 * 60)



if (__name__ == '__main__'):
  print('hs')