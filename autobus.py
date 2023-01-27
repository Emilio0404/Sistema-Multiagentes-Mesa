from mesa import Agent
from enum import Enum

class Autobus(Agent):
  estados = Enum('Estados_Autobus', ['estacionado', 'frenado', 'en_movimiento'])
  horariosDeSalida = [30, 34, 38, 42, 46, 50, 54, 58, 62, 66, 70, 74, 78, 82]
  horariosDeRegreso = [i + 2 for i in horariosDeSalida]

  def __init__(self, unique_id, model): 
    super().__init__(unique_id, model)
    self.estado = Autobus.estados.estacionado
    self.pasajeros = []

  def stage_1(self):
    if self.estado == Autobus.estados.estacionado:
      if self.model.horaActual in Autobus.horariosDeSalida:
        self.estado = Autobus.estados.en_movimiento
        print("  AUTOBUS: Soy Autobus con id", self.unique_id, "y voy hacia el Tec") 
    
  def stage_2(self):
    pass

  def stage_3(self):
    self.estado = Autobus.estados.estacionado
    #print("  Autobus: Soy Autobus con id", self.unique_id, "y llegue al Tec")