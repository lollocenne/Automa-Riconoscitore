class AutomaRiconoscitore:
    def __init__(self, sequenze: list[str] = [], caratteri: list[str] = []):
        self.sequenze = sequenze
        self.caratteri = caratteri
        
        #ogni nodo è un dizionario dove la chiave è la sequenza che
        #deve riconoscere, il valore è invece un dizionario che come 
        #chiave ha quale carattere è stato inserito, come valore ha a 
        #quale nodo con una sequenza deve puntare:
        #nodi = {sequenza : {carattere1 : sequenzaNodo1, carattere2 : sequenzaNodo2}}
        #invece degli stati (s1,s2,s3) abbiamo quindi quale sequenza deve riconoscere (aba,ba,a)
        self.nodi: dict[str : dict[str : dict]] = {}
    
    #crea e collega i nodi, conta solo i caratteri che fanno parte della sequenza giusta,
    def creaNodi(self, sequenza: str):
        self.nodi[""] = {}
        for i in range(len(sequenza)-1, -1, -1):
            if sequenza[i:] in self.nodi:
                continue
            self.nodi[sequenza[i:]] = {sequenza[i]: sequenza[i+1:]}
    
    #trova quale lettere se aggiunte a "parola" fanno "sequenza",
    #se non lo fanno allora la prima lettera di "parola" viene tolta,
    #se ancora non si trova ritorna la sequenza
    def trovaCollegamento(self, sequenza: str, parola: str) -> str:
        lenParola = len(parola)
        while parola:
            if parola + sequenza[lenParola:] in self.nodi:
                return sequenza[lenParola:]
            parola = parola[1:]
            lenParola -= 1
        return sequenza
    
    #finisce di collegare tutti i nodi
    def collegaNodi(self, sequenza: str):
        for key, value in self.nodi.items():
            for carattere in self.caratteri:
                if carattere in value:
                    continue
                value[carattere] = self.trovaCollegamento(sequenza, sequenza[:len(key)] + carattere)
        
    #crea tutti i nodi con tutti i collegamenti
    def creaNodiAutoma(self):
        self.__init__(self.sequenze, self.caratteri) #inizializza la classe
        for seq in self.sequenze:
            self.creaNodi(seq) #crea i nodi
        for seq in self.sequenze:
            self.collegaNodi(seq) #collega i nodi
    
    def __str__(self):
        return "\n".join([f"'{key}' : '{value}'" for key, value in self.nodi.items()])



if __name__ == "__main__":
    modello = AutomaRiconoscitore(["ABA"], ["A", "B"])
    modello.creaNodiAutoma()
    print(modello)