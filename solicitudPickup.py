class SolicitudPickup():
  def __init__(self, idPersona, origenDeSolicitud, destino):
    self.idPersona = idPersona
    self.origenDeSolicitud = origenDeSolicitud
    self.destino = destino
    self.carro = None