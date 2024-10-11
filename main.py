class AutomaRiconoscitore:
    def __init__(self, sequenza: str = "", caratteri: list[str] = []):
        self.sequenza = sequenza
        self.caratteri = caratteri
        
        #ogni nodo è un dizionario dove la chiave è la sequenza che
        #deve riconoscere, il valore è invece un dizionario che come 
        #chiave ha quale carattere è stato inserito, come valore ha a 
        #quale nodo con una sequenza deve puntare:
        #nodi = {sequenza : {carattere1 : sequenzaNodo1, carattere2 : sequenzaNodo2}}
        #invece degli stati (s1,s2,s3) abbiamo quindi quale sequenza deve riconoscere (aba,ba,a)
        self.nodi: dict[str : dict[str : dict]] = {}
    
    #crea e collega i nodi, conta solo i caratteri che fanno parte della sequenza giusta,
    def creaNodi(self):
        self.nodi[""] = {}
        for i in range(len(self.sequenza)-1, -1, -1):
            if self.sequenza[i:] in self.nodi:
                continue
            self.nodi[self.sequenza[i:]] = {self.sequenza[i]: self.sequenza[i+1:]}
    
    #trova quale lettere se aggiunte a "parola" fanno "sequenza",
    #se non lo fanno allora la prima lettera di "parola" viene tolta,
    #se ancora non si trova ritorna la sequenza
    def trovaCollegamento(self, parola: str) -> str:
        lenParola = len(parola)
        while parola:
            if parola + self.sequenza[lenParola:] in self.nodi:
                return self.sequenza[lenParola:]
            parola = parola[1:]
            lenParola -= 1
        return self.sequenza
    
    #finisce di collegare tutti i nodi
    def collegaNodi(self):
        for key, value in self.nodi.items():
            for carattere in self.caratteri:
                if carattere in value:
                    continue
                value[carattere] = self.trovaCollegamento(self.sequenza[:len(key)] + carattere)
        
    #crea tutti i nodi con tutti i collegamenti
    def creaNodiAutoma(self):
        self.__init__(self.sequenza, self.caratteri) #inizializza la classe
        self.creaNodi() #crea i nodi
        self.collegaNodi() #collega i nodi
    
    def __str__(self):
        return "\n".join([f"'{key}' : '{value}'" for key, value in self.nodi.items()])



if __name__ == "__main__":
    modello = AutomaRiconoscitore("ABAB", ["A", "B"])
    modello.creaNodiAutoma()
    print(modello)
    print(modello)
    print(modello)