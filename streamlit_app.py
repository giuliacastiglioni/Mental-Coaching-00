import streamlit as st
import datetime
import pandas as pd
import random
import json
import time
import matplotlib.pyplot as plt
import seaborn as sns
import os

# -------------------- PERSONALIZZAZIONE DELLO SFONDO --------------------
# -------------------- CARICAMENTO E CREAZIONE DEI FILE JSON --------------------
def carica_dati_json(file_path):
    """Carica i dati da un file JSON, creando un file vuoto se non esiste"""
    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            return json.load(f)
    else:
        return {}

def salva_dati_json(file_path, data):
    """Salva i dati nel file JSON"""
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=4)

# Percorsi dei file JSON
file_questionario = "questionario.json"
file_diario = "diario.json"

# Carica i dati esistenti dai file JSON
dati_questionario = carica_dati_json(file_questionario)
dati_diario = carica_dati_json(file_diario)

# Funzione per aggiungere uno sfondo azzurro chiaro
def set_bg_color():
    st.markdown(
        """
        <style>
        .stApp {
            background-color: #a2c8f7;  /* Colore azzurro chiaro */
        }
        </style>
        """, unsafe_allow_html=True)

# Applicare il colore di sfondo azzurro chiaro
set_bg_color()


# -------------------- PERSONALIZZAZIONE DEI BOTTONI --------------------
def style_buttons():
    st.markdown("""
        <style>
        .stButton > button {
            background-color: #6c9e92;  /* Colore verde chiaro */
            color: white;
            border-radius: 8px;
            padding: 10px 20px;
            font-size: 16px;
            transition: background-color 0.3s ease;
        }
        .stButton > button:hover {
            background-color: #4a7366;  /* Colore verde più scuro per hover */
        }
        </style>
    """, unsafe_allow_html=True)

# Applica la personalizzazione dei bottoni
style_buttons()

# -------------------- LOGIN --------------------
def login():
    st.title("Login - Mental Coach per Calcio a 7 Femminile")

    # Dizionari dei codici personali
    codici_giocat = {
        "Giuli": "001",
        "Faccio": "001",
        "Babi": "001",
        "Cla": "001",
        "Mame": "001",
        "Marti Russo": "001",
        "Marti Casella": "001",
        "Cata": "001",
        "Ele": "001"
    }

    codici_allenatori = {
        "Marti": "1234",
        "Elena": "1234",
        "Giulia": "1234",
    }

    ruolo = st.radio("Seleziona il tuo ruolo", ("Giocatrice", "Allenatore"))

    if ruolo == "Giocatrice":
        nome = st.selectbox("Seleziona il tuo nome", list(codici_giocat.keys()))
        codice_inserito = st.text_input("Inserisci il tuo codice personale", type="password")
    else:
        nome = st.selectbox("Seleziona il tuo nome", list(codici_allenatori.keys()))
        codice_inserito = st.text_input("Inserisci il tuo codice personale", type="password")

    if st.button("Accedi"):
        if nome and codice_inserito:
            if ruolo == "Allenatore":
                codice_atteso = codici_allenatori.get(nome)
                if codice_inserito != codice_atteso:
                    st.error("Codice allenatore non valido!")
                    return False
            elif ruolo == "Giocatrice":
                codice_atteso = codici_giocat.get(nome)
                if codice_inserito != codice_atteso:
                    st.error("Codice personale errato!")
                    return False

            # Salva nella sessione
            st.session_state["nome"] = nome
            st.session_state["ruolo"] = ruolo
            st.session_state["codice"] = codice_inserito

            st.success(f"Benvenuta {nome}, sei loggata come {ruolo}")
            return True
        else:
            st.error("Compila tutti i campi!")

    return False

# Funzione di navigazione aggiornata
def navigazione():
    pagina = None  # Inizializza la variabile pagina

    if 'nome' not in st.session_state:
        st.warning("Devi prima effettuare il login.")
        return "login"  # Torna alla pagina di login

    # Navigazione basata sul ruolo dell'utente
    if st.session_state['ruolo'] == 'Giocatrice':
        st.sidebar.title(f"👋 Benvenuta {st.session_state['nome']}!")
        pagina = st.sidebar.radio("Scegli sezione", 
                                  ["🏠 Home", 
                                   "🧠 Questionario mentale", 
                                   "📓 Diario personale", 
                                   "🧘‍♀️ Esercizi Mentali & Risorse"])
    elif st.session_state['ruolo'] == 'Allenatore':
        st.sidebar.title(f"👋 Benvenuto {st.session_state['nome']} - Allenatore!")
        pagina = st.sidebar.radio("Scegli sezione", 
                                  ["🏠 Home", 
                                   "📊 Dashboard Allenatore"])
    
    # Aggiungi il pulsante di logout
    if st.sidebar.button("Logout"):
        st.session_state.clear()  # Resetta tutti i dati della sessione
        st.success("Sei stato disconnesso!")
        return "login"  # Torna alla pagina di login
    
    return pagina

# -------------------- PAGINE PRINCIPALI --------------------


def home():
    st.title("⚽ Mental Coach App - Vittoria Junior")
    st.markdown("Benvenuta nella tua area personale per migliorare il tuo benessere mentale nel calcio!")
    st.image("https://th.bing.com/th/id/OIP.Sz-ErltHiavXNHUAne6W_QHaE8?pid=ImgDet&w=184&h=122&c=7&dpr=1,3", use_container_width=True)
    st.markdown("Usa il menu a sinistra per iniziare ✨")

# -------------------- Esercizi Mentali & Risorse --------------------

# Definisci tutte le funzioni prima del blocco principale
def esercizio_respirazione():
    st.subheader("Esercizi di Respirazione")
    scelta = st.radio("Scegli il tipo di respirazione:", 
                      ["Quadrata (4-4-4-4)", "4-7-8", "Diaframmatica", "Narici Alternate"])
    
    if scelta == "Quadrata (4-4-4-4)":
        st.markdown("""
        **Istruzioni per la Respirazione Quadrata:**
        1. Inspira per 4 secondi.
        2. Trattieni il respiro per 4 secondi.
        3. Espira per 4 secondi.
        4. Trattieni il respiro per 4 secondi.
        Ripeti il ciclo per 3-5 minuti.
        """)
    elif scelta == "4-7-8":
        st.markdown("""
        **Istruzioni per la Respirazione 4-7-8:**
        1. Inspira lentamente per 4 secondi.
        2. Trattieni il respiro per 7 secondi.
        3. Espira lentamente per 8 secondi.
        Ripeti per 4-8 cicli.
        """)
    elif scelta == "Diaframmatica":
        st.markdown("""
        **Istruzioni per la Respirazione Diaframmatica:**
        1. Metti una mano sul petto e l'altra sull'addome.
        2. Inspira profondamente dal naso, espandendo soprattutto l'addome.
        3. Espira lentamente per 6-8 secondi, concentrandoti sulla contrazione dell'addome.
        Ripeti per alcuni minuti.
        """)
    elif scelta == "Narici Alternate":
        st.markdown("""
        **Istruzioni per la Respirazione a Narici Alternate:**
        1. Chiudi la narice destra e inspira lentamente attraverso quella sinistra per 4 secondi.
        2. Chiudi la narice sinistra, apri la destra ed espira lentamente per 4 secondi.
        3. Inspira attraverso la narice destra per 4 secondi, poi chiudi la destra e apri la sinistra per espirare per 4 secondi.
        Ripeti il ciclo per 3-5 minuti.
        """)
    st.button("Inizia esercizio")

def visualizzazione_pre_partita():
    st.subheader("Visualizzazione Pre-Partita")
    st.write("Immagina di entrare in campo, concentrata e pronta per dare il massimo.")
    st.write("Segui questi passaggi di visualizzazione per migliorare la tua preparazione mentale prima della partita:")
    st.markdown("""
    1. Trova un posto tranquillo dove puoi sederti o stare in piedi comodamente.
    2. Chiudi gli occhi e prendi un respiro profondo.
    3. Immagina di essere sul campo da gioco, guardando la tua squadra e l'avversario.
    4. Visualizza ogni movimento che farai durante la partita, dal riscaldamento fino al fischio finale.
    5. Concentrati sui tuoi obiettivi individuali e di squadra.
    6. Visualizza te stessa mentre esegui perfettamente ogni azione, sentendo la tua energia e determinazione crescere.
    7. Senti la fiducia crescere dentro di te, pronta a fare la tua parte per la squadra.
    8. Ora, prendi un altro respiro profondo e prepara la tua mente per la partita!
    """)
    st.button("Inizia esercizio")

def diario_emozioni():
    st.subheader("Diario delle Emozioni")
    emozioni = st.text_area("Come ti senti oggi?")
    if st.button("Salva emozioni"):
        st.success("Le tue emozioni sono state salvate!")

def frasi_motivazionali():
    # Frasi motivazionali estratte da calciatori famosi
    frasi = [
        "Devi lottare per raggiungere il tuo sogno. Devi sacrificarti e lavorare sodo per farlo. - Lionel Messi",
        "Il successo non è un caso. È il risultato di perseveranza, determinazione e duro lavoro. - Cristiano Ronaldo",
        "Il calcio è una questione di orgoglio e spirito di squadra, e il duro lavoro batte il talento quando il talento non lavora duro. - Andrea Pirlo",
        "Non puoi battere il duro lavoro. - Zinedine Zidane",
        "La vittoria è solo un altro passo. La cosa importante è continuare a migliorarsi. - Michael Jordan",
        "Il più grande errore che puoi fare nella vita è avere paura di fare errori. - Elbert Hubbard",
        "Il successo appartiene a coloro che sono abbastanza audaci da credere in sé stessi. - Coco Chanel",
        "Non misurare mai il tuo progresso con quello degli altri. Abbi fede nel tuo percorso. - Unknown",
        "La forza non arriva dalle capacità fisiche. Arriva dalla volontà indomabile. - Mahatma Gandhi",
        "Non importa quanto lento tu vada, l'importante è non fermarti. - Confucio",
        "Ogni grande sogno inizia con un sognatore. - Harriet Tubman",
        "Cadi sette volte, rialzati otto. - Giappone proverbio",
        "La disciplina è il ponte tra gli obiettivi e i risultati. - Jim Rohn",
        "Il vero fallimento non è cadere, ma rimanere a terra. - Mary Pickford",
        "Quando tutto sembra andare male, ricorda: il tramonto è solo il preludio all'alba. - Unknown",
        "Se vuoi qualcosa che non hai mai avuto, devi fare qualcosa che non hai mai fatto. - Thomas Jefferson",
        "Le persone che riescono sono quelle che non mollano mai. - Winston Churchill",
        "Non limitarti. Il mondo è tuo. - Unknown",
        "Solo quelli che osano fallire grandemente possono mai ottenere grandi successi. - Robert F. Kennedy",
        "Sii il cambiamento che vuoi vedere nel mondo. - Mahatma Gandhi",
        "La passione è l'energia. Sentirete il potere che deriva dal concentrarvi su ciò che vi entusiasma. - Oprah Winfrey",
        "Non è la forza fisica che conta, ma la forza di volontà. - Unknown",
        "L'unico modo per fare un ottimo lavoro è amare quello che fai. - Steve Jobs",
        "Non aspettare il momento perfetto. Crea il momento perfetto. - Unknown",
        "La perseveranza è la chiave di ogni successo. - Unknown",
        "Se non sei disposto a rischiare, non sarai mai in grado di ottenere ciò che desideri. - Unknown",
        "Ogni passo che fai ti avvicina di più al successo. - Unknown"
    ]
    st.subheader("Frase motivazionale del giorno")
    st.write(random.choice(frasi))

def audio_mindfulness():
    st.subheader("Audio Brevi per Mindfulness")
    st.audio("https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3")
    st.button("Inizia audio mindfulness")

# -------------------- QUESTIONARIO --------------------
def questionario_mentale():
    st.title("🧠 Come ti senti oggi?")
    oggi = datetime.date.today().isoformat()

    # Domande originali
    motivazione = st.slider("Motivazione (quanto ti senti ispirata per allenarti?)", 1, 5, 3, step=1)
    ansia = st.slider("Ansia (quanto ti senti preoccupata o tesa?)", 1, 5, 3, step=1)
    concentrazione = st.slider("Concentrazione (quanto riesci a mantenere l'attenzione?)", 1, 5, 3, step=1)
    autostima = st.slider("Autostima (quanto credi in te stessa?)", 1, 5, 3, step=1)

    st.markdown("---")
    st.subheader("Ulteriori aspetti da valutare:")

    # Nuove domande aggiunte:
    st.markdown("**Stanchezza Mentale:**")
    st.markdown("Valuta quanto ti senti mentalmente affaticata oggi.")
    stanchezza = st.slider("Stanchezza Mentale", 1, 5, 3, step=1)

    st.markdown("**Livello di Stress:**")
    st.markdown("Quanto senti il carico dello stress nella giornata odierna?")
    stress = st.slider("Stress", 1, 5, 3, step=1)

    st.markdown("**Senso di Supporto:**")
    st.markdown("Quanto ti senti supportata dalla squadra e dagli allenatori?")
    supporto = st.slider("Senso di Supporto", 1, 5, 3, step=1)

    st.markdown("**Soddisfazione Personale:**")
    st.markdown("Quanto sei soddisfatta della tua performance recente?")
    soddisfazione = st.slider("Soddisfazione Personale", 1, 5, 3, step=1)

    # Verifica che il nome sia stato inserito nella homepage
    if 'nome' not in st.session_state:
        st.error("⚠️ Inserisci prima il tuo nome nella homepage.")
    else:
        nome = st.session_state['nome']
        if st.button("Salva risposte"):
            risposta = {
                "nome": nome,
                "data": oggi,
                "motivazione": motivazione,
                "ansia": ansia,
                "concentrazione": concentrazione,
                "autostima": autostima,
                "stanchezza": stanchezza,
                "stress": stress,
                "supporto": supporto,
                "soddisfazione": soddisfazione
            }

            try:
                # Percorso per il salvataggio su file JSON
                if not os.path.exists("questionario_mentale.json"):
                    with open("questionario_mentale.json", "w") as f:
                        json.dump([], f)

                with open("questionario_mentale.json", "r+") as f:
                    data = json.load(f)
                    data.append(risposta)
                    f.seek(0)
                    json.dump(data, f, indent=4)

                st.success("✅ Risposte salvate con successo!")

            except Exception as e:
                st.error(f"❌ Errore durante il salvataggio: {e}")

# -------------------- DIARIO --------------------
def diario_personale():
    st.title("📓 Diario personale")
    oggi = datetime.date.today().isoformat()

    testo = st.text_area("Scrivi qui il tuo pensiero di oggi")
    if 'nome' in st.session_state:
        nome = st.session_state['nome']

    if st.button("Salva nel diario"):
        nuova_entry = {
            "nome": nome,
            "data": oggi,
            "testo": testo
        }

        try:
            # Crea il file se non esiste
            if not os.path.exists("diario_personale.json"):
                with open("diario_personale.json", "w") as f:
                    json.dump([], f)

            with open("diario_personale.json", "r+") as f:
                data = json.load(f)
                data.append(nuova_entry)
                f.seek(0)
                json.dump(data, f, ensure_ascii=False, indent=2)

            st.success("✅ Salvato nel diario!")

        except Exception as e:
            st.error(f"❌ Errore durante il salvataggio: {e}")

    st.markdown("---")
    st.subheader("📖 I tuoi appunti passati")

    if os.path.exists("diario_personale.json"):
        with open("diario_personale.json", "r") as f:
            tutte_le_note = json.load(f)

        diario_nome = [r for r in tutte_le_note if r["nome"] == nome]

        if diario_nome:
            for riga in sorted(diario_nome, key=lambda x: x["data"], reverse=True):
                st.markdown(f"**{riga['data']}**")
                st.markdown(f"> {riga['testo']}")
                st.markdown("---")
        else:
            st.info("📝 Nessun appunto trovato.")
    else:
        st.info("📝 Nessun appunto trovato.")

# Funzione principale dell'app
def main():
    if 'nome' not in st.session_state:
        if not login():
            return

    pagina = navigazione()
    
    if pagina is None:
        return

    if pagina == "🏠 Home":
        home()

    if pagina == "🧠 Questionario mentale":
        questionario_mentale()

    elif pagina == "📓 Diario personale":
        diario_personale()

    elif pagina == "🧘‍♀️ Esercizi Mentali & Risorse":
        st.title("🧘‍♀️ Esercizi Mentali & Risorse")
        
        esercizio = st.radio("Scegli un esercizio mentale da fare:", 
                                ["Respirazione quadrata", 
                                "Visualizzazione positiva pre-partita", 
                                "Diario delle emozioni", 
                                "Frasi motivazionali", 
                                "Audio brevi (mindfulness)"])
        
        if esercizio == "Respirazione quadrata":
            esercizio_respirazione()
        elif esercizio == "Visualizzazione positiva pre-partita":
            visualizzazione_pre_partita()
        elif esercizio == "Diario delle emozioni":
            diario_emozioni()
        elif esercizio == "Frasi motivazionali":
            frasi_motivazionali()
        elif esercizio == "Audio brevi (mindfulness)":
            audio_mindfulness()

    elif pagina == "📊 Dashboard Allenatore":
        st.title("📊 Dashboard Allenatore - Stato Mentale delle Giocatrici")

        try:
            with open("questionario_mentale.json", "r") as f:
                dati = json.load(f)
            df_stato_mentale = pd.DataFrame(dati)

            # Mostra la tabella dei dati
            st.subheader("📋 Risposte raccolte")
            st.dataframe(df_stato_mentale)

            # Grafici delle medie per ogni parametro mentale
            st.subheader("📊 Medie per parametro psicologico")

            for colonna in ["motivazione", "ansia", "concentrazione", "autostima", "stanchezza", "stress", "supporto", "soddisfazione"]:
                media = df_stato_mentale.groupby("nome")[colonna].mean().sort_values(ascending=False)
                st.write(f"**{colonna.capitalize()} media**")
                st.bar_chart(media)

        except FileNotFoundError:
            st.warning("⚠️ Nessun dato disponibile. Le giocatrici devono prima compilare il questionario.")
        except Exception as e:
            st.error(f"❌ Errore durante la lettura dei dati: {e}")
            
# Aggiungi la chiamata alla funzione principale
if __name__ == "__main__":
    main()
