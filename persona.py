from enum import Enum
from mesa import Agent

from solicitudPickup import SolicitudPickup
from autobus import Autobus

class Persona(Agent):
  estados = Enum('Estados_Persona', ['en_pausa', 'decidiendo', 'esperando_pickup', 'usar_camion', 'en_transito'])
  
  def __init__(self, unique_id, model, horaDeIda, horaDeRegreso, coordenadasCasa):
    super().__init__(unique_id, model)
    self.horaDeIda = horaDeIda
    self.horaDeRegreso = horaDeRegreso
    self.estado = Persona.estados.en_pausa
    self.coordenadasCasa = coordenadasCasa
    self.solicitudActual = None
    self.origen = None
    self.destino = None


  def stage_1(self):
    if self.estado == Persona.estados.en_pausa:
      if self.horaDeIda == self.model.horaActual:
        self.estado = Persona.estados.decidiendo
        print("  SOLICITUD: Soy Persona con id", self.unique_id, "y quiero ir al Tec")
      elif self.horaDeRegreso == self.model.horaActual:
        self.estado = Persona.estados.decidiendo
        print("  SOLICITUD: Soy Persona con id", self.unique_id, "y quiero regresar a mi casa")

    # Solo se genera una nueva solicitud en caso de que non haya una del step pasado
    if self.estado == Persona.estados.decidiendo and self.solicitudActual is None:
      self.pedir_pickup()
       

  def stage_2(self):
    # Metodo no se implementa debido a que se está esperando a que 
    # los carros lean el request del pickup. Sin embargo, MESA requiere que, al usar
    # StagedActivation, todos los agentes implementen todos los stages.

    # Para que la Persona sea notificada de que la van a recoger, 
    # se requiere que el estado de la persona lo modifique quien le vaya a recoger.
    pass


  def stage_3(self):
    if self.estado == Persona.estados.decidiendo: # Ningun carro acepto solicitud
      if self.hay_disponibilidad_camion():
        self.estado = Persona.estados.usar_camion
        self.eliminar_solicitud_carpool()
        self.moverse_a_camion()
      else:
        self.horaDeIda += 1 # Se tiene que recorrer la hora para no perder el siguiente camion
    # Else
      # Nadie acepto solicitud y no hay camion, esperar a siguiente step para y volver a intentar


  def pedir_pickup(self):
    if self.model.horaActual == self.horaDeIda:
      self.origen = self.coordenadasCasa
      self.destino = self.model.grid.coordenadasTec
    else:
      self.origen = self.model.grid.coordenadasTec
      self.destino = self.coordenadasCasa
    self.solicitudActual = SolicitudPickup(self, self.origen, self.destino)
    self.model.solicitudesCarpool.append(self.solicitudActual)


  def hay_disponibilidad_camion(self):
    # Checar si camion sale en menos de 30 minutos
    if self.model.horaActual == self.horaDeIda:
      for horario in Autobus.horariosDeSalida:
        if horario <= (self.horaDeIda + 2) and horario >= self.horaDeIda:
          return True
      return False
    
    elif self.model.horaActual == self.horaDeRegreso:
      for horario in Autobus.horariosDeRegreso:
        if horario <= (self.horaDeRegreso + 2) and horario >= self.horaDeRegreso:
          return True
      return False


  def moverse_a_camion(self):
    print("  MOVIMIENTO: Soy Persona con id", self.unique_id, "y voy al camion")
    self.model.camion.aceptar_pasajero(self)
    if self.model.horaActual == self.horaDeIda:
      self.model.grid.mesagrid.move_agent(self, self.model.grid.estacionCamion)
    elif self.model.horaActual == self.horaDeRegreso:
      self.model.grid.mesagrid.move_agent(self, self.model.grid.salidaCamionTec)
    

  def setEstado(self, nuevoEstado):
    if nuevoEstado in Persona.estados._member_names_:
      self.estado = Persona.estados[nuevoEstado]
    else:
      raise TypeError("No es un estado valido")


  def eliminar_solicitud_carpool(self):
    self.model.solicitudesCarpool.remove(self.solicitudActual)
    self.solicitudActual = None