from mesa import Agent
from enum import Enum
from pathGenerator import PathGenerator

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
    # Llego a su destino
    self.estado = Carro.estados.estacionado
    for solicitud in self.solicitudesAceptadas:
      if self.destino == self.model.grid.coordenadasTec:
        # TODO: Mover agentes
        self.origen = self.model.grid.coordenadasTec
        self.destino = self.coordenadasCasa
        solicitud.persona.origen = self.model.grid.coordenadasTec
        solicitud.persona.destino = solicitud.persona.coordenadasCasa
      solicitud.persona.setEstado("en_pausa")
      solicitud.persona.solicitudActual = None
      self.ruta = []
      self.solicitudesAceptadas = []
      self.asientosOcupados = 1


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
      self.ruta = self.generar_ruta()

      tempPasajeros = []
      for solicitud in self.solicitudesAceptadas:
        tempPasajeros.append(solicitud.persona.unique_id)
      print("    Voy a llevar a", tempPasajeros)


  def stage_3(self):
    # Ir por personas
    # TODO: mover agentes

    if self.horaDeIda == self.model.horaActual:
      self.model.grid.mesagrid.move_agent(self, self.model.grid.coordenadasTec) 
    elif self.horaDeRegreso == self.model.horaActual:
      self.model.grid.mesagrid.move_agent(self, self.coordenadasCasa)

    # Marcar como recogidas


  def aceptar_solicitudes(self):
    if self.destino == self.model.grid.coordenadasTec:
      # Desde punto de origen hacia el Tec
      self.aceptar_solicitudes_cuadrante()
    elif self.origen == self.model.grid.coordenadasTec:
      # Desde el Tec hacia las casas
      self.aceptar_solicitudes_en_tec()
    

  def aceptar_solicitudes_cuadrante(self):
    cuadranteCarro = self.get_cuadrante(self.pos)
    for solicitud in self.model.solicitudesCarpool:
        if not self.hay_espacio_en_carro():
          break
        if solicitud.destino == self.model.grid.coordenadasTec and cuadranteCarro == self.get_cuadrante(solicitud.origen):
          self.aceptar_solicitud(solicitud)


  def aceptar_solicitudes_en_tec(self):
    cuadranteCarro = self.get_cuadrante(self.coordenadasCasa)
    for solicitud in self.model.solicitudesCarpool:
        if not self.hay_espacio_en_carro():
          break
        if solicitud.origen == self.model.grid.coordenadasTec and self.get_cuadrante(solicitud.destino) == cuadranteCarro:
          self.aceptar_solicitud(solicitud)
          

  def aceptar_solicitud(self, solicitud):
    self.solicitudesAceptadas.append(solicitud)
    self.asientosOcupados += 1
    self.model.solicitudesCarpool.remove(solicitud)
    solicitud.persona.setEstado("esperando_pickup")


  def generar_ruta(self):
    ruta = []
    if self.destino == self.model.grid.coordenadasTec:
      cuadrante = self.get_cuadrante(self.pos)
      # Generar rutas desde poisicion original hacia otros pasajeros desde origen
      origen_mini_ruta = self.origen
      for solicitud in self.solicitudesAceptadas:
        ruta += self.crear_ruta(origen_mini_ruta, solicitud.origen)
        origen_mini_ruta = solicitud.origen

      # Escoger ruta predefinida desde cuadrante hacia rotonda
      if cuadrante == 1 or cuadrante == 2:
        calle_izquierda_hacia_Tec = [
          (1, 9), (2, 9), (3, 9), (4, 9), (5, 9), (6, 9), (7, 9), (8, 9), (9, 9), (10, 9), (11, 9),
          (11, 10), (11, 11), (11, 12)
        ]

        # Agregar coordenadas de ultimo pasajero a inicio de ruta final
        ruta += self.crear_ruta(origen_mini_ruta, calle_izquierda_hacia_Tec[0])

        # Agregar desde calle hasta el centro de la rotonda
        ruta += calle_izquierda_hacia_Tec[1:]

      elif cuadrante == 3:
        calle_derecha_hacia_Tec = [
          (14, 12), (13, 12), (12, 12), (11, 12)
        ]

        # Agregar coordenadas de ultimo pasajero a inicio de ruta final
        ruta += self.crear_ruta(origen_mini_ruta, calle_derecha_hacia_Tec[0])

        # Agregar desde calle hasta el centro de la rotonda
        ruta += calle_derecha_hacia_Tec[1:]

      # Agregar waypoints desde rotonda hacia tec
      despues_rotonda_hacia_Tec = [
        (11, 13), (11, 14), (11, 15), (11, 16), (11, 17), (11, 18), (11, 19), (11, 20),
        (12, 20), (13, 20), (14, 20), (15, 20), (16, 20), (17, 20)
      ]
      ruta += despues_rotonda_hacia_Tec

    else:
      cuadrante = self.get_cuadrante(self.coordenadasCasa)
      desde_tec_hacia_rotonda = [
        (17, 20), (16, 20), (15, 20), (14, 20), (13, 20), (12, 20), (11, 20), (10, 20), (9, 20), (8, 20),
        (8, 19), (8, 18), (8, 17), (8, 16), (8, 15), (8, 14), (8, 13), (8, 12)
      ]
      ruta += desde_tec_hacia_rotonda

      if cuadrante == 1:
        desde_tec_hacia_cuadrante1 = [
          (7, 12), (6, 12), (5, 12), (4, 12), (3, 12), (2, 12), (2, 13)
        ]
        ruta += desde_tec_hacia_cuadrante1
      elif cuadrante == 2:
        desde_tec_hacia_cuadrante2 = [
          (7, 12), (6, 12), (5, 12), (4, 12), (3, 12), (2, 12), (1, 12),
          (1, 11), (1, 10), (1, 9), (1, 8)
        ]
        ruta += desde_tec_hacia_cuadrante2
      elif cuadrante == 3:
        desde_tec_hacia_cuadrante3 = [
          (8, 11), (8, 10), (8, 9), (9, 9), (10, 9), (11, 9), (12, 9), (13, 9), (13, 8)
        ]
        ruta += desde_tec_hacia_cuadrante3

      # Generar rutas desde inicio de cuadrante a las casas de los pasajeros
      origen_mini_ruta = ruta[-1]
      for solicitud in self.solicitudesAceptadas:
        ruta += self.crear_ruta(origen_mini_ruta, solicitud.persona.coordenadasCasa)
        origen_mini_ruta = solicitud.persona.coordenadasCasa
      ruta += self.crear_ruta(origen_mini_ruta, self.coordenadasCasa)
    
    return ruta


  def get_cuadrante(self, posicion):
    # Izquierda superior = 1
    # Izquierda inferior = 2
    # Derecha inferior = 3
    # Derecha superior = 4
    x = posicion[0]
    y = posicion[1]

    if x < 8 and y > 12:
      return 1
    elif x < 8 and y < 9:
      return 2
    elif x > 11 and y < 9: 
      return 3
    elif x > 11 and y > 12:
      return 4

    return -1 # Fuera de los cuadrantes 


  def hay_espacio_en_carro(self):
    return len(self.solicitudesAceptadas) < 4


  def crear_ruta(self, desde, hacia):
    # Valores especiales para no confundir las otras casas
    self.model.grid.mesagrid[desde[0]][desde[1]][0].contenido = 100
    self.model.grid.mesagrid[hacia[0]][hacia[1]][0].contenido = 100

    camino = PathGenerator(self.model.grid.mesagrid, list(desde), list(hacia),
                           self.model.grid.MAP_WIDTH,
                           self.model.grid.MAP_HEIGHT).return_path()

    # Regresar valores originales
    self.model.grid.mesagrid[desde[0]][desde[1]][0].contenido = 2
    self.model.grid.mesagrid[hacia[0]][hacia[1]][0].contenido = 2

    return camino


  def get_datos_pasajeros(self):
    pasajeros = []
    for solicitud in self.solicitudesAceptadas:
      datos = {
        "id" : solicitud.persona.unique_id,
        "coordenadasCasa" : solicitud.persona.coordenadasCasa
      }
      pasajeros.append(datos)
    return pasajeros