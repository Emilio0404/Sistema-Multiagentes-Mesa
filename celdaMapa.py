"""
    Agente que representa el contenido de una celda en el mapa.

    0 = parque, locales, etc. (no hay personas que recoger)
    1 = calle
    2 = casa
    3 = estacion
    4 = edificio
    5 = Tec
"""

from mesa import Agent

class CeldaMapa(Agent):
    def __init__(self, unique_id, model, contenido):
        super().__init__(unique_id, model)
        self.contenido = contenido

    def stage_1(self):
        # Clase únicamente se usa para crear celdas, no es necesario implementar
        pass

    def stage_2(self):
        # Clase únicamente se usa para crear celdas, no es necesario implementar
        pass

    def stage_3(self):
        # Clase únicamente se usa para crear celdas, no es necesario implementar
        pass