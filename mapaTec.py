from mesa.space import MultiGrid
from celdaMapa import CeldaMapa
from enum import Enum

class MapaTec():
    MAP_WIDTH = 20
    MAP_HEIGHT = 22
    entidades_ciudad = Enum("Entidades_Ciudad", ["inhabitable", "calle", "casa", "estacion_camion", "edificio-residencia", "tec"])
    casas = [
            (1, 0), (6, 0), (7, 0), (14, 0), (20, 0), (1, 3),
            (2, 3), (7, 3), (20, 3), (13, 12), (16, 12), (16, 15),
            (16, 18), (16 , 19), (19, 18), (20, 18), (21, 18)
        ]
    edificios = [
            (17, 6), (19, 6), (21, 12), (21, 15)
        ]

    def __init__(self, schedule, model):
        self.mesagrid = MultiGrid(self.MAP_WIDTH, self.MAP_HEIGHT, False)
        self.schedule = schedule
        self.model = model

        self.llenar_inhabitables()
        self.llenar_tec()
        self.llenar_estacion_camiones()
        self.llenar_calles()
        self.llenar_casas()
        self.llenar_edificios()


    def llenar_tec(self):
        self.llenar_multiples_celdas(5, 0, 9, 12, 20)


    def llenar_estacion_camiones(self):
        self.llenar_multiples_celdas(3, 13, 17, 3, 8)


    def llenar_casas(self):
        for casa in self.casas:
            self.asignar_celda(2, casa[0], casa[1])

    def llenar_edificios(self):
        for edificio in self.edificios:
            self.asignar_celda(4, edificio[0], edificio[1])

    
    def llenar_inhabitables(self):
        self.llenar_multiples_celdas(0, 0, self.MAP_HEIGHT, 0, self.MAP_WIDTH)


    def llenar_calles(self):
        # Llenar calle principal horizontal
        self.llenar_multiples_celdas(1, 9, 13, 0, 20)
        
        # Llenar calle principal vertical superior
        self.llenar_multiples_celdas(1, 0, 9, 8, 12)

        # Llenar calle principal vertical inferior
        self.llenar_multiples_celdas(1, 13, 22, 8, 12)

        # Calles no-principales bloque izquierdo superior
        self.llenar_multiples_celdas(1, 0, 9, 1, 3)
        self.llenar_multiples_celdas(1, 0, 9, 4, 6)
        self.llenar_multiples_celdas(1, 4, 6, 0, 6)

        # Calles bloque izquierdo inferior
        self.llenar_multiples_celdas(1, 13, 22, 1, 3)
        self.llenar_multiples_celdas(1, 17, 19, 0, 6)
        self.llenar_multiples_celdas(1, 19, 22, 4, 6)

        # Calles bloque derecho inferior
        self.llenar_multiples_celdas(1, 14, 16, 12, 18)
        self.llenar_multiples_celdas(1, 17, 19, 12, 20)
        self.llenar_multiples_celdas(1, 13, 22, 13, 15)
        self.llenar_multiples_celdas(1, 15, 22, 16, 18)

        # Calle del Tec
        self.llenar_multiples_celdas(1, 1, 2, 12, 18)


    def llenar_multiples_celdas(self, contenido, y_start, y_end, x_start, x_end):
        for y in range(y_start, y_end):
            for x in range(x_start, x_end):
                self.asignar_celda(contenido, y, x)


    def asignar_celda(self, contenido, y, x):
        x_pos = x
        # Mesa empieza (0, 0) en la esquina inferior izquierda, se tiene que "traducir" la coordenada y
        y_pos = self.MAP_HEIGHT - y - 1

        # Eliminar celdas previamente agregadas por default
        if not self.mesagrid.is_cell_empty((x_pos, y_pos)):
            agent = self.mesagrid.get_cell_list_contents([(x_pos, y_pos)])[0]
            self.mesagrid.remove_agent(agent)
            self.schedule.remove(agent)

        # Agregar agente
        celdaMapa = CeldaMapa((x_pos, y_pos), self.model, contenido)
        self.schedule.add(celdaMapa)
        self.mesagrid.place_agent(celdaMapa, (x_pos, y_pos))