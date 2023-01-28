# Algoritmo obtenido de: https://www.geeksforgeeks.org/find-whether-path-two-cells-matrix/


class PathGenerator():
    def __init__(self, matriz, origen, destino, altura, largo):
        self.matriz = matriz
        self.origen = origen
        self.destino = destino
        self.camino = []
        self.altura = altura
        self.largo = largo

    def return_path(self):
        if self.get_path():
            self.camino.reverse()
            return self.camino

    def get_path(self):
        visitados = [[False for x in range(self.largo)]
               for y in range(self.altura)]
    
        for i in range(self.altura):
            for j in range(self.largo):
                if ([i, j] == self.origen and not visitados[i][j]):
                    return self.find_path(i, j, visitados)

        return False

    def is_safe(self, i, j):
        if (i >= 0 and i < self.altura and
                j >= 0 and j < self.largo):
            return True
        return False

    def find_path(self, i, j, visitados):
        if (self.is_safe(i, j) and self.matriz[i][j][0].contenido in [1, 100] and not visitados[i][j]):
            visitados[i][j] = True
            
            if [i, j] == self.destino:
                self.camino.append([i, j])
                return True
                
            left = self.find_path(i, j - 1, visitados)
            if left:
                self.camino.append([i, j])
                return True
    
            right = self.find_path(i, j + 1, visitados)
            if right:
                self.camino.append([i, j])
                return True
                
            # Traverse up
            up = self.find_path(i - 1, j, visitados)
            if up:
                self.camino.append([i, j])
                return True
                
            down = self.find_path(i + 1, j, visitados)
            if down:
                self.camino.append([i, j])
                return True