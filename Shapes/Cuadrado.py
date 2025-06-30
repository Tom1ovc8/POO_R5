from Shapes.Figura import Coordenada, Figura

class Rectangulo(Figura):
    def __init__(self, ancho, alto, centro=None):
        super().__init__(centro)
        self.ancho = ancho
        self.alto = alto

    def esquinas(self):
        mitad_ancho = self.ancho / 2
        mitad_alto = self.alto / 2
        return [
            Coordenada(self.centro.x + mitad_ancho, self.centro.y + mitad_alto),
            Coordenada(self.centro.x - mitad_ancho, self.centro.y + mitad_alto),
            Coordenada(self.centro.x - mitad_ancho, self.centro.y - mitad_alto),
            Coordenada(self.centro.x + mitad_ancho, self.centro.y - mitad_alto)
        ]

    def mostrar_esquinas(self):
        nombres = ["Superior derecha", "Superior izquierda", "Inferior izquierda", "Inferior derecha"]
        for etiqueta, esquina in zip(nombres, self.esquinas()):
            print(f"{etiqueta}: {esquina}")

    def area(self):
        return self.ancho * self.alto

    def perimetro(self):
        return 2 * (self.ancho + self.alto)

    def contiene_punto(self, punto):
        puntos = self.esquinas()
        min_x = min(p.x for p in puntos)
        max_x = max(p.x for p in puntos)
        min_y = min(p.y for p in puntos)
        max_y = max(p.y for p in puntos)
        return min_x <= punto.x <= max_x and min_y <= punto.y <= max_y

    def intersecta_segmento(self, segmento):
        return self.contiene_punto(segmento.origen) or self.contiene_punto(segmento.destino)

class Cuadrado(Rectangulo):
    def __init__(self, lado, centro=None):
        super().__init__(lado, lado, centro)
        self.lado = lado

    def establecer_lado(self, longitud):
        if longitud <= 0:
            raise ValueError("El lado debe ser positivo")
        self.lado = longitud
        self.ancho = longitud
        self.alto = longitud