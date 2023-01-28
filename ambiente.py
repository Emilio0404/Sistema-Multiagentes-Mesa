from mesa import Model
from mesa.time import StagedActivation

from random import randint
from random import choice

from carro import Carro
from persona import Persona
from mapaTec import MapaTec
from autobus import Autobus


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
    self.crear_autobus()


  def step(self):
    self.schedule.step()
    self.horaActual += 1
    self.mandar_json_a_unity()


  def crear_carros(self):
    for i in range(0, self.numCarros):
      horarios = self.generar_horarios_movimiento()
      origen = choice(self.grid.casas)
      tmpAgent = Carro("Carro" + str(i), self, horarios[0], horarios[1], origen)
      self.schedule.add(tmpAgent)
      self.grid.mesagrid.place_agent(tmpAgent, origen)


  def crear_personas(self):
    for i in range(0, self.numPersonas):
      horarios = self.generar_horarios_movimiento()
      origen = choice(self.grid.casas)
      tmpAgent = Persona("Persona" + str(i), self, horarios[0], horarios[1], origen)
      self.schedule.add(tmpAgent)
      self.grid.mesagrid.place_agent(tmpAgent, origen)

  
  def crear_autobus(self):
      tmpAgent = Autobus("Autobus" + str(1), self)
      self.schedule.add(tmpAgent)
      self.grid.mesagrid.place_agent(tmpAgent, self.grid.estacionCamion)


  def generar_horarios_movimiento(self):
    horaDeIda = randint(7 * 4, 19 * 4)
    horaDeRegreso = randint(horaDeIda + 1, 21 * 4) # Sumar uno para evitar generar misma hora de ida y regreso
    return [horaDeIda, horaDeRegreso]


  def mandar_json_a_unity(self):
    # Falta implementación
    pass