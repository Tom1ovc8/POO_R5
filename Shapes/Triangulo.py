import math
from Shapes.Figura import Coordenada, Figura, Segmento

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
