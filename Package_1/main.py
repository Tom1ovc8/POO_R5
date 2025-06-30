from Package_1.Shapes import Coordenada, Rectangulo, Triangulo

def main():

    point1 = Coordenada(0, 0)
    point2 = Coordenada(1, 0)
    point3 = Coordenada(0, 2)
    triangle = Triangulo(point1, point2, point3)
    print("El area del triángulo es:", triangle.area())
    print("El perímetro del triángulo es:", triangle.perimetro())

    alto = Coordenada(0, 0)
    ancho = Coordenada(2, 2)
    centro = Coordenada(1, 1)
    rectangle = Rectangulo(ancho, alto, centro)
    print("El area del rectangulo es:", rectangle.area())
    print("El perímetro del rectangulo es:", rectangle.perimetro())

if __name__ == "__main__":
    main() 