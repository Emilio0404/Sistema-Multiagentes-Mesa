# NOTA: ESTA NO ES EL AGENTE QUE SE IMPLEMENTÓ PARA LA ENTREGA
# SE EMPEZÓ PERO NO ES FUNCIONAL

from mesa import Agent
from enum import Enum

class Carro(Agent):
  estados = Enum('Estados_Carro', ['estacionado', 'frenado', 'pickup_en_progreso', 'en_transito'])

  def __init__(self, unique_id, model, horaDeIda, horaDeRegreso, coordenadasCasa):
    super().__init__(unique_id, model)
    self.horaDeIda = horaDeIda
    self.horaDeRegreso = horaDeRegreso
    self.coordenadasCasa = coordenadasCasa
    self.asientosOcupados = 1
    self.estado = Carro.estados.estacionado
    self.pasajeros = []

  def stage_1(self):
    if self.estado == Carro.estados.estacionado:
      if self.horaDeIda == self.model.horaActual:
        self.estado = Carro.estados.en_transito
        print("  RUTA: Soy Carro con id", self.unique_id, "y voy hacia el Tec")
      elif self.horaDeRegreso == self.model.horaActual:
        self.estado = Carro.estados.en_transito
        print("  RUTA: Soy Carro con id", self.unique_id, "y de regreso a mi casa")

  def stage_2(self):
    # Falta implementacion
    pass

  def stage_3(self):
    # Falta implementacion
    pass