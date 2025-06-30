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

class Triangulo(Figura):
    def __init__(self, v1, v2, v3):
        centro = self._calcular_centroide([v1, v2, v3])
        super().__init__(centro)
        self.vertices = [v1, v2, v3]
        self.lados = [Segmento(v1, v2), Segmento(v2, v3), Segmento(v3, v1)]
        self.longitudes = [lado.longitud() for lado in self.lados]
        self.clasificacion = self._tipo_triangulo()

    def _tipo_triangulo(self):
        a, b, c = sorted(self.longitudes)
        if a + b <= c:
            raise ValueError("Triángulo inválido")
        if math.isclose(a, b) and math.isclose(b, c):
            return "equilátero"
        if math.isclose(a**2 + b**2, c**2):
            return "rectángulo isósceles" if math.isclose(a, b) else "rectángulo"
        if math.isclose(a, b) or math.isclose(b, c) or math.isclose(a, c):
            return "isósceles"
        return "escaleno"

    def _calcular_centroide(self, puntos):
        x_prom = sum(p.x for p in puntos) / 3
        y_prom = sum(p.y for p in puntos) / 3
        return Coordenada(x_prom, y_prom)

    def perimetro(self):
        return sum(self.longitudes)

    def area(self):
        s = self.perimetro() / 2
        a, b, c = self.longitudes
        return math.sqrt(s * (s - a) * (s - b) * (s - c))

    def contiene_punto(self, punto):
        def signo(pa, pb, pc):
            return (pa.x - pc.x) * (pb.y - pc.y) - (pb.x - pc.x) * (pa.y - pc.y)

        d1 = signo(punto, self.vertices[0], self.vertices[1])
        d2 = signo(punto, self.vertices[1], self.vertices[2])
        d3 = signo(punto, self.vertices[2], self.vertices[0])

        tiene_neg = d1 < 0 or d2 < 0 or d3 < 0
        tiene_pos = d1 > 0 or d2 > 0 or d3 > 0

        return not (tiene_neg and tiene_pos)

class TrianguloEquilatero(Triangulo):
    def __init__(self, centro, longitud):
        h = (math.sqrt(3) / 2) * longitud
        a = Coordenada(centro.x, centro.y + (2 / 3) * h)
        b = Coordenada(centro.x - longitud / 2, centro.y - (1 / 3) * h)
        c = Coordenada(centro.x + longitud / 2, centro.y - (1 / 3) * h)
        super().__init__(a, b, c)
        self.lado = longitud

class TrianguloIsosceles(Triangulo):
    def __init__(self, centro_base, base, altura):
        a = Coordenada(centro_base.x - base / 2, centro_base.y - altura / 2)
        b = Coordenada(centro_base.x + base / 2, centro_base.y - altura / 2)
        c = Coordenada(centro_base.x, centro_base.y + altura / 2)
        super().__init__(a, b, c)
        self.base = base
        self.altura = altura

class TrianguloRecto(Triangulo):
    def __init__(self, punto_recto, cateto1, cateto2):
        a = punto_recto
        b = Coordenada(a.x + cateto1, a.y)
        c = Coordenada(a.x, a.y + cateto2)
        super().__init__(a, b, c)
        self.cateto1 = cateto1
        self.cateto2 = cateto2

class TrianguloEscaleno(Triangulo):
    def __init__(self, a, b, c):
        super().__init__(a, b, c)
        if self.clasificacion in ("equilátero", "isósceles"):
            raise ValueError("Debe ser un triángulo escaleno")

if __name__ == "__main__":
    pass
