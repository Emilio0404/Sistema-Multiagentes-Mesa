from mesa import Agent
from enum import Enum

class Autobus(Agent):
  estados = Enum('Estados_Autobus', ['estacionado', 'en_movimiento'])
  horariosDeSalida = [30, 34, 38, 42, 46, 50, 54, 58, 62, 66, 70, 74, 78, 82]
  horariosDeRegreso = [i + 2 for i in horariosDeSalida]
  rutaDeIda = [
    (3, 7), (2, 7), (2, 8), (2, 9), (3, 9), (4, 9), (5, 9), (6, 9), (7, 9), (8, 9),
    (9, 9), (10, 9), (11, 9), (11, 10), (11, 11), (11, 12), (11, 13), (11, 14),
    (11, 15), (11, 16), (11, 17), (11, 18), (11, 19), (11, 20),
    (12, 20), (13, 20), (14, 20), (15, 20), (16, 20), (17, 20)
  ]
  rutaDeRegreso = [
    (17, 20), (16, 20), (15, 20), (14, 20), (13, 20), (12, 20), (11, 20), (10, 20),
    (9, 20), (8, 20), (8, 19), (8, 18), (8, 17), (8, 16), (8, 15), (8, 14), (8, 13),
    (8, 12), (7, 12), (6, 12), (5, 12), (4, 12), (3, 12), (2, 12), (1, 12), (1, 11),
    (1, 10), (1, 9), (1, 8), (1, 7), (2, 7), (3, 7)
  ]

  def __init__(self, unique_id, model): 
    super().__init__(unique_id, model)
    self.estado = Autobus.estados.estacionado
    self.pasajeros = []
    self.rutaActual = []


  def stage_1(self):
    # Se resetea aqui y no en stage3 para poder reportar la ruta a Unity
    if self.estado == Autobus.estados.en_movimiento:
        self.llegada_a_destino()

    if self.estado == Autobus.estados.estacionado:
      if self.model.horaActual in Autobus.horariosDeSalida:
        self.estado = Autobus.estados.en_movimiento
        self.rutaActual = self.rutaDeIda
        print("  AUTOBUS: Soy Autobus con id", self.unique_id, "y voy hacia el Tec")
      elif self.model.horaActual in Autobus.horariosDeRegreso:
        self.estado = Autobus.estados.en_movimiento
        self.rutaActual = self.rutaDeRegreso
        print("  AUTOBUS: Soy Autobus con id", self.unique_id, "y voy hacia el la estación")
    

  def stage_2(self):
    # No requiere implementacion, espera a que
    # las personas metan sus solicitudes
    pass


  def stage_3(self):
    # Camion sale hacia su destino
    if self.estado == Autobus.estados.en_movimiento:
      self.mover_camion()


  def mover_camion(self):
    for coordenada in self.rutaActual:
      self.model.grid.mesagrid.move_agent(self, coordenada)
      for pasajero in self.pasajeros:
        pasajero.setEstado("en_transito")
        self.model.grid.mesagrid.move_agent(pasajero, coordenada)


  def llegada_a_destino(self):
    self.estado = Autobus.estados.estacionado
    self.rutaActual = []
    for pasajero in self.pasajeros: 
        pasajero.setEstado('en_pausa')
    self.pasajeros = []


  def aceptar_pasajero(self, pasajero):
    self.pasajeros.append(pasajero)


  def get_datos_pasajeros(self):
    pasajeros = []
    for pasajero in self.pasajeros:
      pasajeros.append(pasajero.unique_id)
    return pasajeros