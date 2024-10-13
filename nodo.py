#classe che rappresenta ogni nodo
#y: int -> la y del nodo
#stato: str -> indica lo stato del nodo, questo stato verrà mostrato all'utente
#puntaA: dict[str : str] -> dizionario che indica per ogni carattere possibile a quale stato bisogna collegare il nodo

#ogni nodo sarà salvato in un dizionario con lo stato come chiave, e l'istanza come valore

class Nodo:
    x = 200
    def __init__(self, y: int = 0, stato: str = "", puntaA: dict[str, str] = {}, showNodeFunc = None, coord: tuple[int] = (0, 0), pen = None, brush = None, flag = None):
        self.x = Nodo.x
        self.y = y
        
        self.diametro: int = 100        
        Nodo.x += self.diametro*2
        
        self.stato = stato
        self.puntaA = puntaA    #{lettera : stato}
        
        self.showNode = showNodeFunc(self.x + coord[0], self.y + coord[1], self.diametro, self.diametro, pen, brush)
        self.showNode.setFlag(flag)