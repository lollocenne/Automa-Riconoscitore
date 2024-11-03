from nodoAutoma import NodoAutoma

class AutomaRiconoscitore:
    def __init__(self, sequenze: list[str] = [], caratteri: list[str] = ()):
        self.sequenze = sequenze
        self.sequenze.sort(key=len, reverse=True)
        self.sequenzeSemplici = self.lunghezzaUguale(self.semplificaSequenze(self.sequenze))
        self.caratteri = caratteri
        self.nodi: dict[str, dict[str,str]] = {}    #{stato: {carattere: stato2}}
    
    #da sequenze elimina quelle che sono gia contenute
    #all'inizio di un altra sequenza
    @staticmethod
    def semplificaSequenze(sequenze) -> list[str]:
        res = []
        for seq in sequenze:
            if not any(seq != s and s.startswith(seq) for s in res):
                res.append(seq)
        return res
    
    @staticmethod
    def lunghezzaUguale(sequenze):
        if not sequenze: return []
        lenTarget = len(sequenze[0])
        nuoveSequenze = []
        for seq in sequenze:
            nuovaSequenza = sequenze[0][:(lenTarget - len(seq))] + seq
            if nuovaSequenza not in nuoveSequenze:
                nuoveSequenze.append(nuovaSequenza)
        return nuoveSequenze
    
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
        self.listaNodi = self.creaListaNodi(NodoAutoma(self.sequenzeSemplici))
        self.listaNodi.sort(key=lambda n: int(n.stato[1:]))  #ordina in base allo stato (forse è inutile lol)
        self.connettiNodi(self.listaNodi)
        for n in self.listaNodi:
            self.creaDizionarioStati(n)
    
    #connette i nodi con i caratteri rimasti
    def connettiNodi(self, listaNodi: list[NodoAutoma]) -> None:
        for nodo in listaNodi:
            for c in self.caratteri:
                if any(c in chiave.split(',') for chiave in nodo.puntaA): continue
                idx = 0
                while c not in nodo.puntaA:
                    for seq in nodo.attuale:
                        seq += c
                        for nodoDestinazione in listaNodi:
                            for seq2 in nodoDestinazione.sequenze:
                                if seq[idx:] + seq2 in self.sequenze:
                                    nodo.puntaA[c] = nodoDestinazione
                    idx += 1
    
    #se una sequenze di nodo.attuale è in sequenze allora è uno stato finale
    def getFinali(self) -> list[str]:
        sequenzeSet = set(self.sequenze)
        return [nodo.stato for nodo in self.listaNodi if set(nodo.attuale) & sequenzeSet]
    
    #trasforma la lista di NodoAutoma in un dizionario dove la chiave è
    #NodoAutoma.stato e il valore è NodoAutoma.puntaA
    def creaDizionarioStati(self, nodo: NodoAutoma) -> None:
        self.nodi[nodo.stato] = {key: punta.stato for key, punta in nodo.puntaA.items()}
    
    
    def __str__(self):
        return f"{'-'*15}modello{'-'*15}\n" + "\n".join([f"'{key}' : '{value}'" for key, value in self.nodi.items()]) + f"\n{'-'*37}"

if __name__ == "__main__":
    modello = AutomaRiconoscitore(["ABA", "BBA"], ("A", "B"))
    modello.creaNodiAutoma()
    print(modello)
