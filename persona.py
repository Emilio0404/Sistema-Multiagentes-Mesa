from enum import Enum
from mesa import Agent

from solicitudPickup import SolicitudPickup

class Persona(Agent):
  estados = Enum('Estados_Persona', ['en_pausa', 'decidiendo', 'esperando_pickup', 'usar_camion', 'en_transito'])
  
  def __init__(self, unique_id, model, horaDeIda, horaDeRegreso, coordenadasCasa):
    super().__init__(unique_id, model)
    self.horaDeIda = horaDeIda
    self.horaDeRegreso = horaDeRegreso
    self.estado = Persona.estados.en_pausa
    self.coordenadasCasa = coordenadasCasa


  def stage_1(self):
    if self.estado == Persona.estados.en_pausa:
      if self.horaDeIda == self.model.horaActual:
        self.estado = Persona.estados.decidiendo
        print("  SOLICITUD: Soy Persona con id", self.unique_id, "y quiero ir al Tec")
      elif self.horaDeRegreso == self.model.horaActual:
        self.estado = Persona.estados.decidiendo
        print("  SOLICITUD: Soy Persona con id", self.unique_id, "y quiero regresar a mi casa")

    if self.estado == Persona.estados.decidiendo:
       self.pedir_pickup()
       self.estado = Persona.estados.en_pausa # Temporal

  def stage_2(self):
    # Metodo no se implementa debido a que se está esperando a que 
    # los carros lean el request del pickup. Sin embargo, MESA requiere que, al usar
    # StagedActivation, todos los agentes implementen todos los stages.

    # Para que la Persona sea notificada de que la van a recoger, 
    # se requiere que el estado de la persona lo modifique quien le vaya a recoger.
    pass


  def stage_3(self):
    if self.estado == Persona.estados.esperando_pickup:
        pass
    elif self.estado == Persona.estados.decidiendo: # Ningun carro acepto solicitud
        if self.hay_disponibilidad_camion():
            self.estado = Persona.estados.usar_camion
            self.moverse_a_camion()
    # Else
      # Nadie acepto solicutud y no hay camion, esperar a siguiente step para y volver a intentar


  def pedir_pickup(self):
    if self.model.horaActual == self.horaDeIda:
      origen = self.coordenadasCasa
      destino = "Tec de Monterrey"
    else:
      origen = "Tec de Monterrey"
      destino = self.coordenadasCasa
    nuevaSolicitud = SolicitudPickup(self.unique_id, origen, destino)
    self.model.solicitudesCarpool.append(nuevaSolicitud)


  def hay_disponibilidad_camion(self):
    # Falta implementacion, aun no hay agente camion
    # Checar si camion sale en menos de 30 minutos y si Persona llega al camion a tiempo,
    return False


  def moverse_a_camion(self):
    # Falta implementacion
    pass