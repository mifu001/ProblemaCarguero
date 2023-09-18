class Contenedor:
    id = ""
    peso = 0
    puerto = 0
    peligroso = False

    def __init__(self, id:str, peso:int, puerto:int, peligroso:bool) -> None:
        self.id = id
        self.peso = peso
        self.puerto = puerto
        self.peligroso = peligroso
    def __gt__(self,other):
        return self.peso>other.peso
    def __eq__(self, other):
        return self.id==other.id       

class Compartimento:
    huecos = []
    alto = 0
    ancho = 0

    def __init__(self, ancho:int, alto:int) -> None:
        self.huecos = [None for i in range(alto*ancho)]
        self.alto = alto
        self.ancho = ancho
    
    def setContenedor(self, contenedor:Contenedor, fila:int, columna:int):
        self.huecos[fila][columna] = contenedor
    
    def toLlist(self) -> list[int]:
        lista = []
        [[lista.append(elemento) for elemento in fila] for fila in self.huecos]
        return lista

class Barco:
    compartimentos: list[Compartimento] = []

    def __init__(self, numCompartimentos:int, anchoComp:int, altoComp:int) -> None:
        self.compartimentos = [Compartimento(anchoComp, altoComp) for i in range(numCompartimentos)]

    