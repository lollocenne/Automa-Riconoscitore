<h1>AUTOMA RICONOSCITORE</h1>
<h2>Stati</h2>
<p>
  Gli stati sono indicati con una S e un numero, gli stati finali hanno scritto < finale> e il numero
</p>
<h2>Nodi</h2>
<p>
  I nodi sono rappresentati da un dizionario che come chiave ha il suo stato e come valore ha un altro dizionario, 
  dove per ogni carattere possibile, indica un altro stato: {"S1": {"A": "S1", "B": "S2"}}.
</p>
<h2>Come funziona</h2>
<p>
  L'algoritmo segue questi step:
  <ol>
    <li>
      <b>Ordinamento sequenze</b><br>
      Le sequenze che sono già contenute all'inizio di un altra sequenza verranno eliminate (verranno comunque onservate per capire quali stati sono finali)
    </li>
    <li>
      <b>Creazione nodi iniziali</b><br>
      Inizialmente vengono creati tutti i nodi necessari per la creazione, vedendo quali nodi servono se si inseriscono solo caratteri "giusti".<br>
      Ogni nodo contiene una lista <code>sequenze</code>, che indica quali sequenze quel nodo deve riconoscere, una lista <code>attuale</code>, che indica quali sequenze sono state inserite fino al quel nodo, un dizionario <code>puntaA</code>, dove la chiave è il carattere e il valore è a quale nodo punta.
      <ol type="1">
        <li>
          Per ogni sequenza S in <code>sequenze</code> controlla se esiste già un collegamento per la prima lettera di S, se esiste allora deve     soltanto aggiungere S senza la prima lettera nella lista <code>sequenze</code> del secondo nodo.
        </li>
        <li>
          Se non esiste allora controlla se esiste già un nodo dove nella sua lista <code>sequenze</code> esiste S senza la prima lettera,
          se esiste allora la prima lettera di S deve puntare a quel nodo, inoltre deve aggiungere ad <code>attuale</code> del secondo nodo, ogni elemento di <code>attuale</code> di questo nodo + la prima lettera di S.
        </li>
        <li>Se non esiste allora deve craere un nuovo nodo.</li>
      </ol>
    </li>
    <li>
      <b>Creare tutti i collegamenti</b><br>
      Adesso per ogni nodo bisogna controllare se manca un carattere.
      Se manca un carattere allora si cerca a quale nodo bisogna collegarlo in questo modo:
      <ol type="1">
        <li>
          Itera per ogni sequenza in <code>attuale</code> e ci aggiunge il carattere mancante (creando S).
        </li>
        <li>
          Itera per ogni nodo e cerca quale ha una sequenza in <code>sequenze</code> che se aggiunta a S crea una sequenza da riconoscere.
        </li>
        <li>
          Se la trova allora si collega a quel nodo.
        </li>
        <li>
          Se non lo trova allora leva la prima lettera di S e ricomincia dal punto 2.
        </li>
      </ol>
    </li>
    <li>
      <b>Definire nodi finali</b><br>
      I nodi finali sono tutti i nodi che nella loro lista <code>sequenze</code> contengono una sequenza da riconoscere.
    </li>
  </ol>
</p>
