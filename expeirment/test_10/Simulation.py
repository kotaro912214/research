class Simulation():

  def __init__(self, *args, **kwargs):
    self.NUMBER_OF_EMPLOYEES = 4
    self.TIME = 60 * 8
    self.C_IN = 100
    self.C_OUT = 205
    self.C_E = 10000 * (self.TIME / (8*60))
    self.PRICE_PER_15 = 205
    self.FUEL_CONSUMPTION = 35
    self.NUMBER_OF_STATIONS = 10

  