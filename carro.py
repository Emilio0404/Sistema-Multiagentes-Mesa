from mesa import Agent
from enum import Enum

class Carro(Agent):
  estados = Enum('Estados_Carro', ['estacionado', 'frenado', 'pickup_en_progreso', 'en_transito'])

  def __init__(self, unique_id, model, horaDeIda, horaDeRegreso, coordenadasCasa):
    super().__init__(unique_id, model)
    self.horaDeIda = horaDeIda
    self.horaDeRegreso = horaDeRegreso
    self.coordenadasCasa = coordenadasCasa
    self.origen = None
    self.destino = None
    self.asientosOcupados = 1
    self.estado = Carro.estados.estacionado
    self.solicitudesAceptadas = []
    self.ruta = []


  def stage_1(self):
    if self.estado == Carro.estados.estacionado:
      if self.horaDeIda == self.model.horaActual:
        self.estado = Carro.estados.en_transito
        self.origen = self.coordenadasCasa
        self.destino = self.model.grid.coordenadasTec
        print("  RUTA: Soy Carro con id", self.unique_id, "y voy hacia el Tec")
      elif self.horaDeRegreso == self.model.horaActual:
        self.estado = Carro.estados.en_transito
        self.origen = self.model.grid.coordenadasTec
        self.destino = self.coordenadasCasa
        print("  RUTA: Soy Carro con id", self.unique_id, "y voy de regreso a mi casa")


  def stage_2(self):
    if self.estado == Carro.estados.en_transito:
      self.aceptar_solicitudes()

      tempPasajeros = []
      for solicitud in self.solicitudesAceptadas:
        tempPasajeros.append(solicitud.persona.unique_id)
      print("    Voy a llevar a", tempPasajeros)

      self.generar_ruta()


  def stage_3(self):
    # Ir por personas
    # Marcar como recogidas

    # Llego a su destino
    self.estado = Carro.estados.estacionado
    self.solicitudesAceptadas = []
    self.asientosOcupados = 1


  def aceptar_solicitudes(self):
    # Desde punto de origen hacia el Tec
    if self.destino == self.model.grid.coordenadasTec:
      for solicitud in self.model.solicitudesCarpool:
        if not self.hay_espacio_en_carro():
          break

        # Criterio de seleccion para las rutas
        if solicitud.destino == self.model.grid.coordenadasTec:
          self.solicitudesAceptadas.append(solicitud)
          self.asientosOcupados += 1
          self.model.solicitudesCarpool.remove(solicitud)
          solicitud.persona.setEstado("esperando_pickup")


    elif self.origen == self.model.grid.coordenadasTec:
      for solicitud in self.model.solicitudesCarpool:
        if not self.hay_espacio_en_carro():
          break

        # Criterio de seleccion para las rutas
        if solicitud.origen == self.model.grid.coordenadasTec:
          self.solicitudesAceptadas.append(solicitud)
          self.asientosOcupados += 1
          self.model.solicitudesCarpool.remove(solicitud)
          solicitud.persona.setEstado("esperando_pickup")
      

  def generar_ruta(self):
    # Agregar pasajeros actuales a la ruta
    # Interpolar ruta entre esos puntos
    pass

  def hay_espacio_en_carro(self):
    return len(self.solicitudesAceptadas) < 4