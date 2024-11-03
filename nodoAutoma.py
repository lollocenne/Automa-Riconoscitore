#questa classe viene utilizzata solo durante la creazione dell'automa
#ogni NodoAutoma ha le sequenze che deve riconoscere (sequenze) e le
#sequenze che sono state messe fino a quel nodo (attuale)

class NodoAutoma:
    stato = 0
    def __init__(self, sequenze: list[str], attuale: list[str] = [""]):
        self.stato = f"S{NodoAutoma.stato}"
        NodoAutoma.stato += 1
        
        self.sequenze = sequenze
        self.attuale = attuale
    
    @staticmethod
    def rimuoviUguali(sequenze: list[str]) -> list[str]:
        res = []
        for seq in sequenze:
            if seq not in res:
                res.append(seq)
        return res
    
    def inizializza(self):
        self.sequenze = self.rimuoviUguali(self.sequenze)
        self.puntaA: dict[str, NodoAutoma] = {s[0]: None for s in self.sequenze}    #{carattere: nodo a cui punta}
    
    #ogni nodo crea un nodo a cui deve collegarsi, o se già esiste
    #si gollega ad esso
    def calcolaPunta(self) -> None:
        for s in self.sequenze:
            inizio = s[0]
            continuo = s[1:]
            if self.puntaA[inizio]:
                if continuo:
                    self.puntaA[inizio].sequenze.append(continuo)
                continue
            for seq in self.puntaA.values():
                if seq and continuo in seq.sequenze:
                    self.puntaA[inizio] = seq
                    self.puntaA[inizio].attuale += [att + inizio for att in self.attuale]
                    break
            else:
                self.puntaA[inizio] = NodoAutoma([continuo] if continuo else [], [att + inizio for att in self.attuale])
        
        self.creaNodiSuccessivi()
    
    #crea tutti i nodi successivi
    def creaNodiSuccessivi(self) -> None:
        for n in self.puntaA.values():
            n.inizializza()
            n.calcolaPunta()
    
    #se due caratteri puntano allo stesso nodo allora vengono uniti e divisi da una virgola
    def unisciPuntaA(self) -> None:
        tempDict = {}
        for key, value in self.puntaA.items():
            if value not in tempDict:
                tempDict[value] = []
            tempDict[value].append(key)
        self.puntaA = {",".join(sorted(keys)): value for value, keys in tempDict.items()}


if __name__ == "__main__":
    nodo = NodoAutoma(["ABA", "BBA"], [""])
    nodo.inizializza()
    nodo.calcolaPunta()
    print(nodo.puntaA["B"].puntaA["B"].puntaA["A"].stato)     #nodo dopo aver inserito la sequenza BBA