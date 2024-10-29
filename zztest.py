class AutomaRiconoscitore:
    def __init__(self, sequenze: list[str] = [], caratteri: list[str] = []):
        self.sequenze = sequenze
        self.caratteri = caratteri
        
        self.sequenzeOttimizzate = self.ottimizzaSequenze(self.sequenze)
        
        #ogni nodo è un dizionario dove la chiave è la sequenza che
        #deve riconoscere, il valore è invece un dizionario che come 
        #chiave ha quale carattere è stato inserito, come valore ha a 
        #quale nodo con una sequenza deve puntare:
        #nodi = {sequenza : {carattere1 : sequenzaNodo1, carattere2 : sequenzaNodo2}}
        #invece degli stati (s1,s2,s3) abbiamo quindi quale sequenza deve riconoscere (aba,ba,a)
        self.nodi: dict[str, dict[str, dict]] = {}
    
    @staticmethod
    def ottimizzaSequenze(sequenze: list[str]) -> list[str]:
        def accorciaSequenze(seqe: list[str]) -> list[str]:
            res = []
            for s in seqe:
                maxIdx = 0
                n = len(s)
                for s2 in res:
                    if n > len(s2): continue
                    for i in range(maxIdx, n+1):
                        if s[:i] == s2[:i]:
                            maxIdx = i
                s = s[maxIdx:]
                if s and s not in res:
                    res.append(s)
            return res
        
        def rimuoviSimili(seqe: list[str]) -> list[str]:
            res = []
            for s in seqe:
                if s[1:] not in [seq[1:] for seq in res]:
                    res.append(s)
            return res
        
        return accorciaSequenze(rimuoviSimili(sequenze))
    
    #crea e collega i nodi, conta solo i caratteri che fanno parte della sequenza giusta
    def creaNodi(self, sequenza: str) -> None:
        self.nodi[""] = {}
        for i in range(len(sequenza)-1, -1, -1):
            if sequenza[i:] not in self.nodi:
                self.nodi[sequenza[i:]] = {sequenza[i]: sequenza[i+1:]}
    
    #trova quale lettere se aggiunte a "parola" fanno "sequenza",
    #se non lo fanno allora la prima lettera di "parola" viene tolta,
    #se ancora non si trova ritorna la sequenza
    def trovaCollegamento(self, sequenza: str, parola: str) -> str:
        lenParola = len(parola)
        while parola:
            if parola == sequenza[:lenParola]:
                return sequenza[lenParola:]
            parola = parola[1:]
            lenParola -= 1
        return sequenza
    
    #richiama la funzione "trovaCollegamento()" per ogni sequenza
    #e ritorna il collegamento con la lunghezza minore
    def trovaCollegamentoCorto(self, key: str, carattere: str) -> str:
        seqPossibili = []
        for seq in self.sequenze:
            seqPossibili.append(self.trovaCollegamento(seq, (seq[:-len(key)] if len(key) > 0 else seq) + carattere))
        return min(seqPossibili, key=len)
    
    #finisce di collegare tutti i nodi controllando
    #cosa deve succede quando inserisci un carattere sbagliato
    def collegaNodi(self) -> None:
        for key, value in self.nodi.items():
            for carattere in self.caratteri:
                if carattere not in value:
                    value[carattere] = self.trovaCollegamentoCorto(key, carattere)
    
    #crea tutti i nodi con tutti i collegamenti
    def creaNodiAutoma(self) -> None:
        self.__init__(self.sequenze, self.caratteri)    #inizializza la classe
        for seq in self.sequenzeOttimizzate:
            self.creaNodi(seq)  #crea i nodi
        self.collegaNodi()  #collega i nodi
        self.miglioraCollegamenti()
        self.nodi = self.miglioraStati(self.nodi)
    
    def miglioraCollegamenti(self) -> None:
        for key1, value1 in self.nodi.items():
            collegamentiNuovi = {}
            for key2, value2 in value1.items():
                if value2 in collegamentiNuovi:
                    collegamentiNuovi[value2] += "," + key2
                else:
                    collegamentiNuovi[value2] = key2
            self.nodi[key1] = {chiavi: value2 for value2, chiavi in collegamentiNuovi.items()}
    
    @staticmethod
    def miglioraStati(stati: dict[str, dict[str, dict]]) -> dict[str, dict[str, dict]]:
        nuoviStati = stati.copy()
        statiDaSostituire = {}
        chiavi = list(stati.keys())
        for i in range(len(chiavi)):
            n = len(chiavi[i])
            s1 = chiavi[i][1:]
            for j in range(i + 1, len(chiavi)):
                if n != len(chiavi[j]): continue
                
                s2 = chiavi[j][1:]
                if s1 == s2:
                    statiDaSostituire[chiavi[j]] = chiavi[i]
                    nuoviStati.pop(chiavi[j], None)
        
        
        for outerKey, innerDict in nuoviStati.items():
            for innerKey, innerValue in innerDict.items():
                if innerValue in statiDaSostituire:
                    nuoviStati[outerKey][innerKey] = statiDaSostituire[innerValue]
        return nuoviStati
    
    def __str__(self):
        return f"{'-'*15}modello{'-'*15}\n" + "\n".join([f"'{key}' : '{value}'" for key, value in self.nodi.items()]) + f"\n{'-'*37}"



if __name__ == "__main__":
    modello = AutomaRiconoscitore(["BBA", "ABB"], ["A", "B"])
    modello.creaNodiAutoma()
    print(modello)



"""
!Se i due stati, sono della stessa lunghezza, e iniziano uguali, vanno fatti diventare uno solo:
    !Se uno stato s1 e uno stato s2 hanno questa caratteristica, allora lo stato s2 deve essere eliminato,
    !ma adesso, bisogna cambiare ogni s2 in s1, anche nei collegamenti degli altri nodi

*esempi di sequenze sbagliate: [ABA, ABB]
*    nodi che si possono unire:
*        ABB-AAB
*        BB-AB
"""