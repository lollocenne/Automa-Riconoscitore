#classe che rappresenta ogni nodo
#y: int -> la y del nodo
#stato: str -> indica lo stato del nodo, questo stato verrà mostrato all'utente
#puntaA: dict[str : str] -> dizionario che indica per ogni carattere possibile a quale stato bisogna collegare il nodo

#ogni nodo sarà salvato in un dizionario con lo stato come chiave, e l'istanza come valore

class Nodo:
    x = 30
    def __init__(self, y: int = 0, stato: str = "", puntaA: dict[str : str] = {}):
        self.x = Nodo.x
        self.y = y
        
        self.grandezza: int = 20        
        Nodo.x += self.grandezza*2
        
        self.stato = stato
        self.puntaA = puntaA    #{lettera : stato}