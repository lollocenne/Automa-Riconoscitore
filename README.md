<h1>AUTOMA RICONOSCITORE</h1>
<h2>Stati</h2>
<p>
  In questo automa gli stati sono chiamati in base a quello che devono riconosciere:
  se la sequenza è "ABAB" allora gli stati saranno: "ABAB", "BAB", "AB", "B", "".
</p>
<h2>Nodi</h2>
<p>
  I nodi sono rappresentati da un dizionario che come chiave ha il suo stato e come valore ha un altro dizionario, 
  dove per ogni carattere possibile, indica un altro stato: {"ABAB": {"A": "BAB", "B": "ABAB"}}.
</p>
<h2>Come funziona</h2>
<p>
  Inizialmente con la funzione <code>creaNodi()</code> crea tutti i nodi partendo dall'ultimo e aggiungendo come valori iniziali
  solo i caratteri corrette e ogni carattere punta ad uno stato.
</p>
<p>
  Successivamente con la funzione <code>collegaNodi()</code> finisce di collegare i nodi con tutte le possibili combinazioni,
  per farlo controlla ogni stato e ogni carattere, se il carattere è già segnato per quello stato continua avanti,
  se invece non è già presente, cercherà a quale nodo sia meglio collegarsi.<br>
  Ecco i passaggi per farlo:
  <ol>
    <li>Prende la sequenza</li>
    <li>Elimina la chiave (lo stato) dalla sequenza e aggiunge il carattere da aggiungere</li>
    <li>Elimina la chiave (lo stato) dalla sequenza e aggiunge il carattere da aggiungere</li>
    <li>Cerca se questa parola + (le lettere mancanti della sequenza) è presente negli stati</li>
    <li>Se è presente allora lo stato a cui può puntare è le lettere mancanti della sequenza, se invece non è presente, bisogna levare la prima lettera e ricominciare il controllo</li>
  </ol>
  Tutti questi passaggi verranno effettuati su tutte le combinazioni che vanno riconosciute, quindi al passaggio 5 possono esistere più stati possibili ma interessa soltanto
  lo stato con la lunghezza minore.
</p>
