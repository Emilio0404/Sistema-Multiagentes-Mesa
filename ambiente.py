from mesa import Model
from mesa.time import StagedActivation

from random import randint
from random import choice

from carro import Carro
from persona import Persona
from mapaTec import MapaTec


class Ambiente(Model):
  def __init__(self, numPersonas, numCarros):
    self.numPersonas = numPersonas
    self.numCarros = numCarros
    self.solicitudesCarpool = []
    self.horaActual = 0
    self.schedule = StagedActivation(self, ["stage_1", "stage_2", "stage_3"])
    self.grid = MapaTec(self.schedule, self)
    self.crear_carros()
    self.crear_personas()


  def step(self):
    self.schedule.step()
    self.horaActual += 1
    self.mandar_json_a_unity()


  def crear_carros(self):
    for i in range(0, self.numCarros):
      horarios = self.generar_horarios_movimiento()
      tmpAgent = Carro("Carro" + str(i), self, horarios[0], horarios[1], choice(self.grid.casas))
      self.schedule.add(tmpAgent)


  def crear_personas(self):
    for i in range(0, self.numPersonas):
      horarios = self.generar_horarios_movimiento()
      tmpAgent = Persona("Persona" + str(i), self, horarios[0], horarios[1], choice(self.grid.casas))
      self.schedule.add(tmpAgent)


  def generar_horarios_movimiento(self):
    horaDeIda = randint(7 * 4, 19 * 4)
    horaDeRegreso = randint(horaDeIda + 1, 21 * 4)
    return [horaDeIda, horaDeRegreso]


  def mandar_json_a_unity(self):
    # Falta implementación
    pass