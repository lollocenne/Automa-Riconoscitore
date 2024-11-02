from nodoAutoma import NodoAutoma

class AutomaRiconoscitore:
    def __init__(self, sequenze: list[str] = [], caratteri: list[str] = ()):
        self.sequenze = sequenze
        self.sequenze.sort(key=len, reverse=True)
        self.sequenzeSemplici = self.semplificaSequenze()
        self.caratteri = caratteri
        
        self.nodi: dict[str, dict[str,str]] = {}
    
    #dalle sequenze elimina quelle che sono gia contenute
    #all'inizio di un altra sequenza
    def semplificaSequenze(self) -> list[str]:
        res = []
        for seq in self.sequenze:
            if not any(seq != s and s.startswith(seq) for s in res):
                res.append(seq)
        return res
    
    #crea una lista di tutte le istanze di NodoAutoma create
    @staticmethod
    def creaListaNodi(head: NodoAutoma) -> list[NodoAutoma]:
        head.inizializza()
        head.calcolaPunta()
        visitati = set()
        def dfs(nodo: NodoAutoma):
            if nodo in visitati: return
            visitati.add(nodo)
            for successivo in nodo.puntaA.values():
                dfs(successivo)
        dfs(head)
        return list(visitati)
    
    def creaNodiAutoma(self) -> None:
        listaNodi = self.creaListaNodi(NodoAutoma(self.sequenze))
        listaNodi.sort(key=lambda n: int(n.stato[1:]))  #ordina in base allo stato (forse è inutile lol)
        for n in listaNodi:
            self.creaDizionarioStati(n)
    
    #trasforma la lista di NodoAutoma in un dizionario dove la chiave è
    #NodoAutoma.stato e il valore è NodoAutoma.puntaA
    def creaDizionarioStati(self, nodo: NodoAutoma) -> None:
        self.nodi[nodo.stato] = {key: punta.stato for key, punta in nodo.puntaA.items()}

    
    def __str__(self):
        return f"{'-'*15}modello{'-'*15}\n" + "\n".join([f"'{key}' : '{value}'" for key, value in self.nodi.items()]) + f"\n{'-'*37}"

if __name__ == "__main__":
    modello = AutomaRiconoscitore(["ABA", "ABB"], ("A", "B"))
    modello.creaNodiAutoma()
    print(modello)
