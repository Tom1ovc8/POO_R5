import math

class Coordenada:
    def __init__(self, x=0.0, y=0.0):
        self.x = x
        self.y = y

    def resetear(self):
        self.x = 0
        self.y = 0

    def __str__(self):
        return f"Coordenada({self.x}, {self.y})"

class Segmento:
    def __init__(self, punto_a=None, punto_b=None):
        self.origen = punto_a if punto_a else Coordenada()
        self.destino = punto_b if punto_b else Coordenada()

    def longitud(self):
        dx = self.destino.x - self.origen.x
        dy = self.destino.y - self.origen.y
        return math.hypot(dx, dy)

    def pendiente(self):
        if self.destino.x == self.origen.x:
            return float('inf')
        return (self.destino.y - self.origen.y) / (self.destino.x - self.origen.x)

    def __str__(self):
        return f"Segmento de {self.origen} a {self.destino}"

class Figura:
    def __init__(self, centro=None):
        self.centro = centro if centro else Coordenada()

    def area(self):
        raise NotImplementedError("Implementar en subclases")

    def perimetro(self):
        raise NotImplementedError("Implementar en subclases")

    def contiene_punto(self, punto):
        raise NotImplementedError("Implementar en subclases")

    def intersecta_segmento(self, segmento):
        raise NotImplementedError("Implementar en subclases")