import streamlit as st
import datetime
import pandas as pd
import random
import json
import time
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
import seaborn as sns
import os
import bcrypt
import numpy as np
from auth import register_user, check_login

# -------------------- PERSONALIZZAZIONE DELLO SFONDO --------------------
# -------------------- CARICAMENTO E CREAZIONE DEI FILE JSON --------------------
def carica_dati_json(file_path):
    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            return json.load(f)
    else:
        return []


def salva_dati_json(file_path, data):
    """Salva i dati nel file JSON"""
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=4)

# Percorsi dei file JSON
file_questionario = "questionario.json"
file_diario = "diario.json"
file_emozioni= "emozioni.json"
file_checkin = "checkin_pre.json"
file_checkout = "checkout_post.json"

# Carica i dati esistenti dai file JSON
dati_questionario = carica_dati_json(file_questionario)
dati_diario = carica_dati_json(file_diario)
dati_checkin = carica_dati_json(file_checkin)
dati_checkout = carica_dati_json(file_checkout)

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

# File per salvare i dati (senza cifratura complessa)
#LOGIN_FILE = 'login_data.json'

# Dizionari separati per giocatrici e allenatori (contenente hash delle password)
#passwords_giocatrici = {
#    "Giuli": None,
#    "Faccio": None,
#    "Babi": None,
#    "Cla": None,
#    "Mame": None,
#    "Marti Russo": None,
#    "Marti Casella": None,
#    "Cata": None,
#    "Ele": None
#}

#passwords_allenatori = {
#    "Marti": None,
#    "Elena": None,
#    "Giulia": None
#}

# Funzione per leggere i login dal file
#def leggi_login():
#    try:
#        with open(LOGIN_FILE, 'r') as file:
#            data = json.load(file)
#        return data
#    except FileNotFoundError:
#        return {}

# Funzione per scrivere i login nel file
#def scrivi_login(data):
#    with open(LOGIN_FILE, 'w') as file:
#        json.dump(data, file)

# Funzione per registrare la password in modo sicuro con bcrypt
#def registra_password(nome, ruolo, password):
#    hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
#    
#    if ruolo == "Giocatrice":
#       passwords_giocatrici[nome] = hashed_password
#    elif ruolo == "Allenatore":
#        passwords_allenatori[nome] = hashed_password

# Funzione di login
def login():
    st.title("🔐 Login - Mental Coach")

    tab1, tab2 = st.tabs(["Accedi", "Registrati"])

    # ---------------- LOGIN ----------------
    with tab1:
        nome = st.text_input("Nome")
        password = st.text_input("Password", type="password")

        if st.button("Accedi"):
            ok, ruolo = check_login(nome, password)
            if ok:
                st.session_state["nome"] = nome
                st.session_state["ruolo"] = ruolo
                st.success("Login effettuato con successo")
                st.rerun()
            else:
                st.error("Nome o password errati")

    # ---------------- REGISTRAZIONE ----------------
    with tab2:
        nome_r = st.text_input("Nuovo nome")
        ruolo_r = st.selectbox("Ruolo", ["Giocatrice", "Allenatore"])
        pw1 = st.text_input("Password", type="password", key="login_pw1")
        pw2 = st.text_input("Conferma password", type="password")

        if st.button("Registrati"):
            if pw1 != pw2:
                st.error("Le password non coincidono")
            elif len(pw1) < 4:
                st.error("Password troppo corta")
            else:
                ok, msg = register_user(nome_r, ruolo_r, pw1)
                if ok:
                    st.success("Registrazione completata, ora puoi accedere")
                else:
                    st.error(msg)

    return False


# Funzione per il reset della password
#def resetta_password(nome, ruolo):
    # Aggiungi la possibilità di resettare la password
#    st.write(f"Stai per resettare la password per {nome}.")
#    nuova_password = st.text_input("Inserisci una nuova password", type="password")
#    conferma_password = st.text_input("Conferma la nuova password", type="password")
#
#    if nuova_password and nuova_password == conferma_password:
#        registra_password(nome, ruolo, nuova_password)
#        st.success(f"La password per {nome} è stata aggiornata con successo!")

# Funzione di navigazione aggiornata
def navigazione():
    pagina = None  # Inizializza la variabile pagina

    if 'nome' not in st.session_state:
        st.warning("Devi prima effettuare il login.")
        return "login"  # Torna alla pagina di login

    # Navigazione basata sul ruolo dell'utente
    if st.session_state['ruolo'] == 'Giocatrice':
        st.sidebar.title(f"👋 Benvenuta {st.session_state['nome']}!")
        
        # Menu principale in sidebar
        menu_principale = st.sidebar.radio("Seleziona una sezione:", 
                                            ["🏠 Home", "⚡ Allenamento", "🧘‍♀️ Esercizi Mentali & Risorse", 
                                            "🧠 Questionario mentale", "📓 Diario personale", "📝 Diario delle emozioni"])

        if menu_principale == "⚡ Allenamento":
            st.title("⚡ Allenamento")
            st.markdown("Seleziona un'opzione per gestire il tuo allenamento:")

            # Inizializza lo stato della pagina allenamento
            if 'allenamento_page' not in st.session_state:
                st.session_state['allenamento_page'] = None

            # Pulsanti nella pagina centrale
            col1, col2, col3 = st.columns(3)
            if col1.button("Check-in pre allenamento"):
                st.session_state['allenamento_page'] = "checkin"
            if col2.button("Check-out post allenamento"):
                st.session_state['allenamento_page'] = "checkout"
            if col3.button("Il mio andamento"):
                st.session_state['allenamento_page'] = "andamento"

            # Mostra la sezione selezionata
            if st.session_state['allenamento_page'] == "checkin":
                checkin_pre()
            elif st.session_state['allenamento_page'] == "checkout":
                checkout_post()
            elif st.session_state['allenamento_page'] == "andamento":
                andamento_atleta()

        else:
            # Selezione diretta per altre sezioni
            pagina = menu_principale


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

def checkin_pre():
    st.title("⚡ Check-in pre allenamento")

    nome = st.session_state.get("nome")

    energia = st.slider("Quanta energia hai?",1,5,3)
    umore = st.slider("Umore",1,5,3)
    stress = st.slider("Stress",1,5,3)
    focus = st.slider("Concentrazione",1,5,3)

    if st.button("Invia check-in"):
        nuovo = {
            "nome": nome,
            "data": datetime.now().isoformat(),
            "energia": energia,
            "umore": umore,
            "stress": stress,
            "focus": focus
        }

        dati = carica_dati_json(file_checkin)
        dati.append(nuovo)
        salva_dati_json(file_checkin, dati)

        st.success("Check-in salvato!")

        # feedback immediato
        indice = stress - energia

        if indice > 2:
            st.error("🔴 Attenzione: arrivi molto stanca/stressata")
            st.write("Parlane con l'allenatore prima di iniziare")
        elif indice > 0:
            st.warning("🟠 Giornata media")
        else:
            st.success("🟢 Pronta per allenarti!")

def checkout_post():
    st.title("🏁 Check-out post allenamento")

    nome = st.session_state.get("nome")

    fatica = st.slider("Quanto sei stanca?",1,5,3)
    soddisfazione = st.slider("Soddisfazione allenamento",1,5,3)
    prestazione = st.slider("Come ti sei sentita in campo?",1,5,3)
    emozione = st.text_input("Una parola sull'allenamento")

    if st.button("Invia check-out"):
        nuovo = {
            "nome": nome,
            "data": datetime.now().isoformat(),
            "fatica": fatica,
            "soddisfazione": soddisfazione,
            "prestazione": prestazione,
            "emozione": emozione
        }

        dati = carica_dati_json(file_checkout)
        dati.append(nuovo)
        salva_dati_json(file_checkout, dati)

        st.success("Check-out salvato!")

        if fatica > 4 and soddisfazione < 3:
            st.warning("Allenamento pesante oggi. Recupera bene 💧")
        elif soddisfazione > 4:
            st.success("Ottimo allenamento! 🔥")

def andamento_atleta():
    st.title("📈 Il mio andamento")

    nome = st.session_state.get("nome")

    if not os.path.exists("checkin_pre.json"):
        st.info("Nessun dato")
        return

    with open("checkin_pre.json") as f:
        dati = json.load(f)

    df = pd.DataFrame(dati)
    df = df[df["nome"]==nome]

    if df.empty:
        st.info("Ancora nessun dato")
        return

    df["data"] = pd.to_datetime(df["data"])

    import plotly.express as px
    fig = px.line(df, x="data", y=["energia","umore","stress","focus"], markers=True)
    st.plotly_chart(fig, use_container_width=True)

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

# Emozioni e relative frasi di supporto psicologico
emozioni = {
    "Felicità": "La felicità non è il risultato di eventi esterni, ma nasce dalla capacità di vivere in armonia con ciò che siamo e con ciò che abbiamo. La felicità è il frutto di una scelta consapevole di apprezzare ogni momento, anche nelle difficoltà. Non cercarla lontano, perché è già dentro di te, pronta a fiorire.",
    "Tristezza": "La tristezza è il linguaggio dell’anima che ha bisogno di essere ascoltata. Essa non è il nemico, ma un compagno che ci insegna la vulnerabilità e ci permette di ricostruire, più forti di prima. Non sfuggire ad essa, ma accoglila come un'opportunità di crescita interiore. Solo attraverso la tristezza possiamo apprezzare pienamente la gioia che verrà.",
    "Ansia": "L’ansia è la voce che ci ricorda quanto è importante il nostro benessere. Non è un segno di debolezza, ma un’indicazione che stiamo affrontando sfide significative. Piuttosto che lasciarla dominarci, possiamo usarla come una guida per fare un passo indietro, respirare profondamente e scegliere consapevolmente come affrontare la situazione.",
    "Rabbia": "La rabbia è una passione intensa che può consumarci se non la comprendiamo. Essa è una risposta a qualcosa che ci ferisce, ma è anche un’opportunità di introspezione. Invece di scagliarla verso l'esterno, chiediamoci: cosa sta cercando di insegnarmi? Quali confini voglio proteggere? Solo attraverso la riflessione possiamo trasformare la rabbia in azioni positive.",
    "Sorpresa": "La sorpresa è il messaggio dell’universo che ci invita a rimanere aperti e ricettivi al cambiamento. Le sorprese sono spesso momenti di disordine che ci spingono fuori dalla zona di comfort, ma è solo quando abbracciamo l'incertezza che possiamo scoprire nuove possibilità. Imparare a navigare nel caos è una delle abilità più potenti che possiamo sviluppare.",
    "Paura": "La paura è l’ombra che si forma quando ci avviciniamo a qualcosa che non conosciamo. Ma ciò che temiamo è raramente così grande o invincibile come sembra. La paura è solo un segnale che la nostra crescita sta per avvenire. Scegliere di affrontarla, passo dopo passo, è l'unico modo per superarla e scoprire una versione più forte di noi stessi.",
    "Calma": "La calma non è l'assenza di movimento, ma la presenza di un centro interiore solido che resiste al caos esterno. Quando sei calmo, puoi osservare le tue emozioni senza esserne sopraffatto. La calma è la forza silenziosa che ti permette di rispondere alle sfide con lucidità e fiducia. È la terra sotto i piedi quando il mondo sembra tremare.",
    "Speranza": "La speranza è la forza invisibile che ci spinge a guardare oltre le nuvole nere, a credere che, nonostante le difficoltà, c'è sempre una possibilità di miglioramento. Ogni passo verso il futuro è un atto di coraggio, ed è nella speranza che possiamo trovare la forza di trasformare i nostri sogni in realtà.",
    "Disperazione": "La disperazione può sembrare un abisso oscuro, ma in realtà è un'opportunità nascosta. In quei momenti in cui sembra che nulla abbia senso, possiamo scegliere di guardarci dentro e trovare la nostra luce. La disperazione è il momento in cui la nostra anima è più ricettiva al cambiamento, se solo ci fermiamo ad ascoltarla.",
    "Confusione": "La confusione è una nebbia che avvolge la nostra mente, ma è anche il primo passo verso la chiarezza. In quei momenti in cui non sappiamo cosa fare, possiamo scegliere di fermarci e osservare con calma. La chiarezza non arriva con la fretta, ma con la pazienza di lasciar fluire i pensieri senza giudizio.",
    "Gratitudine": "La gratitudine è la chiave che apre la porta alla felicità. Non si tratta di ignorare le difficoltà, ma di riconoscere il valore anche nei piccoli momenti di bellezza quotidiana. Quando siamo grati, il nostro cuore si espande e ci connettiamo a una forza più grande di noi stessi.",
    "Vergogna": "La vergogna è una pesantezza che portiamo dentro, ma non è una condanna permanente. È un segnale che ci invita a guardare dentro di noi, a perdonarci e a fare spazio alla crescita. La vergogna può diventare il terreno fertile da cui nascono la consapevolezza e la libertà.",
    "Amore": "L’amore non è solo un’emozione, ma una forza che trasforma il mondo. È la capacità di vedere l'altro con occhi pieni di comprensione, rispetto e cura. Amare non significa non soffrire mai, ma essere pronti a condividere i momenti di gioia e di dolore, sapendo che ogni emozione è parte di un legame più profondo.",
    "Solitudine": "La solitudine è spesso vista come un nemico, ma è in quei momenti di silenzio che possiamo riscoprire chi siamo veramente. La solitudine non significa isolamento, ma è un'opportunità di connessione con la nostra essenza, di ascoltare ciò che la vita ha da dirci senza distrazioni esterne.",
    "Rimpianto": "Il rimpianto è il peso del passato che ancora portiamo con noi. Tuttavia, ogni rimpianto è anche una lezione che ci invita a vivere con maggiore consapevolezza nel presente. Non permettere che i rimpianti definiscano chi sei, ma usali come un trampolino per diventare la persona che desideri essere.",
    "Indifferenza": "L'indifferenza è un muro che erigiamo intorno a noi per proteggere il nostro cuore. Ma questo muro non ci rende più forti, solo più isolati. L'indifferenza ci impedisce di vivere pienamente e di connetterci con gli altri. Scegli di abbattere quel muro e di tornare a sentire.",
    "Soddisfazione": "La soddisfazione non arriva da ciò che possediamo, ma dal riconoscimento del nostro cammino. Ogni piccolo traguardo che raggiungiamo è il frutto della nostra determinazione. La soddisfazione è un segno che stiamo crescendo, che siamo più forti di quanto pensavamo."
}

# Funzione per visualizzare il grafico delle emozioni selezionate con intensità personalizzate
def visualizza_emozioni(emozioni_selezionate):
    # Creare un dizionario per memorizzare l'intensità delle emozioni selezionate
    emozioni_count = {}
    
    # Chiedere l'intensità per ogni emozione selezionata
    for emozione in emozioni_selezionate:
        intensita = st.slider(f"Seleziona l'intensità per l'emozione {emozione}:", min_value=0, max_value=10, value=5)
        emozioni_count[emozione] = intensita
    
    # Creare un DataFrame per il grafico
    df = pd.DataFrame(list(emozioni_count.items()), columns=["Emozione", "Intensità"])
    
    # Visualizzare il grafico a barre
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(x="Emozione", y="Intensità", data=df, palette="Blues_d")
    ax.set_title("Intensità delle Emozioni Selezionate", fontsize=16)
    ax.set_xlabel('Emozioni')
    ax.set_ylabel('Intensità (0-10)')
    plt.xticks(rotation=45)
    st.pyplot(fig)
    
# Funzione per l'area del diario emozioni
def diario_emozioni():
    st.title("Diario delle Emozioni")

    st.write("Oggi, come ti senti? Seleziona le emozioni che ti rappresentano oggi.")

    # Seleziona più emozioni
    emozioni_selezionate = st.multiselect("Seleziona le emozioni che stai provando:", list(emozioni.keys()))

    # Visualizza la frase di supporto per ciascuna emozione selezionata
    if emozioni_selezionate:
        st.write("**Frasi di supporto per le emozioni selezionate:**")
        for emozione in emozioni_selezionate:
            st.write(f"**{emozione}:**")
            st.write(f"'{emozioni[emozione]}'")

        # Visualizza il grafico delle emozioni selezionate
        visualizza_emozioni(emozioni_selezionate)

        # Aggiungi un'area di riflessione per ciascuna emozione
        riflessioni = {}
        for emozione in emozioni_selezionate:
            riflessioni[emozione] = st.text_area(f"Come ti senti riguardo a '{emozione}'?", "")

        # Salva nel file specifico per le emozioni
        if st.button('Salva Emozioni'):
            if 'nome' in st.session_state:
                nome = st.session_state['nome']
                oggi = datetime.date.today().isoformat()

                # Crea un oggetto per le emozioni selezionate e le riflessioni
                emozioni_data = {
                    "nome": nome,
                    "data": oggi,
                    "emozioni_selezionate": emozioni_selezionate,
                    "riflessioni": riflessioni
                }

                try:
                    # Crea il file delle emozioni se non esiste
                    if not os.path.exists("emozioni.json"):
                        with open("emozioni.json", "w") as f:
                            json.dump([], f)

                    with open("emozioni.json", "r+") as f:
                        data = json.load(f)
                        data.append(emozioni_data)
                        f.seek(0)
                        json.dump(data, f, ensure_ascii=False, indent=2)

                    st.success("✅ Le tue emozioni e riflessioni sono state salvate correttamente!")

                except Exception as e:
                    st.error(f"❌ Errore durante il salvataggio: {e}")
            else:
                st.error("❌ Devi essere loggato per salvare nel diario.")
    else:
        st.write("Non hai selezionato nessuna emozione.")
# Visualizza le note precedenti
    if os.path.exists("emozioni.json"):
        with open("emozioni.json", "r") as f:
            tutte_le_note = json.load(f)

        if 'nome' in st.session_state:
            nome = st.session_state['nome']

            # Filtra le note per il nome dell'utente
            emozioni_data = [r for r in tutte_le_note if r["nome"] == nome]

            if emozioni_data:
                for riga in sorted(emozioni_data, key=lambda x: x["data"], reverse=True):
                    st.markdown(f"**{riga['data']}**")

                    # Visualizza le emozioni e le riflessioni per ciascuna
                    for emozione in riga['emozioni_selezionate']:
                        riflessione = riga['riflessioni'].get(emozione, "Nessuna riflessione salvata.")
                        st.markdown(f"**{emozione}:** {riflessione}")
                    
                    st.markdown("---")
            else:
                st.info("📝 Nessun appunto trovato.")
        else:
            st.info("📝 Devi essere loggato per visualizzare gli appunti.")
    else:
        st.info("📝 Nessun appunto trovato.")

def frasi_motivazionali():
    # Frasi motivazionali estratte da calciatori famosi
    frasi = [
        "Be curious, not judgmental. (Sii curioso, non giudicante.)",
        "I believe in hope. I believe in believe. (Io credo nella speranza. Io credo nel credere.)",
        "Taking on a challenge is a lot like riding a horse, isn’t it? If you’re comfortable while you’re doing it, you’re probably doing it wrong. (Affrontare una sfida è un po' come andare a cavallo, no? Se ti senti a tuo agio mentre lo fai, probabilmente lo stai facendo male.)",
        "Doing the right thing is never the wrong thing. (Fare la cosa giusta non è mai sbagliato.)",
        "Believe in yourself and be the best version of you. (Credi in te stesso e sii la migliore versione di te.)",
        "I think that you might be so sure that you’re one in a million, that sometimes you forget that out there, you’re just one of eleven. (Penso che a volte sei così sicuro di essere uno su un milione, che ti dimentichi che là fuori sei solo uno di undici.)",
        "Success is not about wins and losses, it’s about helping these young fellas be the best versions of themselves. (Il successo non riguarda vittorie e sconfitte, ma aiutare questi giovani a essere la migliore versione di se stessi.)",
        "It’s the lack of hope that kills you. (È la mancanza di speranza che ti uccide.)",
        "If the plan doesn’t work, change the plan, but never the goal. (Se il piano non funziona, cambia il piano, ma mai l’obiettivo.)",
        "Smells like potential. (Sa di potenziale.)",
        "You know what the happiest animal on Earth is? It’s a goldfish. You know why? It’s got a ten-second memory. Be a goldfish. (Sai qual è l'animale più felice sulla Terra? È un pesce rosso. Sai perché? Ha una memoria di dieci secondi. Sii un pesce rosso.)",
        "I promise you, there is something worse out there than being sad, and that’s being alone and being sad. (Vi assicuro, c’è qualcosa di peggio che essere tristi, ed è essere soli e tristi.)",
        "Just listen to your gut, and on the way down to your gut, check in with your heart. Between those two things, they’ll let you know what’s what. (Ascolta semplicemente il tuo istinto, e lungo la strada verso il tuo istinto, consulta anche il tuo cuore. Tra queste due cose, ti diranno cosa fare.)",
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
        "La disciplina è il ponte tra gli obiettivi e i risultati. - Jim Rohn",
        "Il vero fallimento non è cadere, ma rimanere a terra. - Mary Pickford",
        "Quando tutto sembra andare male, ricorda: il tramonto è solo il preludio all'alba. - Unknown",
        "Se vuoi qualcosa che non hai mai avuto, devi fare qualcosa che non hai mai fatto. - Thomas Jefferson",
        "Le persone che riescono sono quelle che non mollano mai. - Winston Churchill",
        "Non limitarti. Il mondo è tuo. - Unknown",
        "Solo quelli che osano fallire grandemente possono mai ottenere grandi successi. - Robert F. Kennedy",
        "Sii il cambiamento che vuoi vedere nel mondo. - Mahatma Gandhi",
        "La passione è l'energia. Sentirete il potere che deriva dal concentrarvi su ciò che vi entusiasma. - Oprah Winfrey",
        "L'unico modo per fare un ottimo lavoro è amare quello che fai. - Steve Jobs",
        "Non aspettare il momento perfetto. Crea il momento perfetto. - Unknown",
        "Se non sei disposto a rischiare, non sarai mai in grado di ottenere ciò che desideri. - Unknown",
        "In sostanza, o sei uno che si assume rischi o non lo sei, e se non corri rischi, non vincerai mai in grande. - Geno Auriemma"
        "Ci saranno giorni buoni e giorni cattivi, ma il mio amore assoluto per il gioco e la forza che viene da Dio mi riporteranno dove devo essere. - Paige Bueckers"
    ]
    st.subheader("Frase motivazionale del giorno")
    st.write(random.choice(frasi))

def audio_mindfulness():
    st.subheader("Audio Brevi per Mindfulness e Motivazione")

    # Lista di audio (aggiungi tutti gli URL che vuoi)
    audio_list = [
        {"titolo": "Believe - Ted Lasso", "url": "/workspaces/Mental-Coaching-00/Believe - Ted Lasso _ Powerful Motivational Speech [ZPGBceVfV60].mp3"},
        {"titolo": "Kobe Bryant's Greatest Speech", "url": "/workspaces/Mental-Coaching-00/Kobe Bryant's Greatest Speech _ BEST Motivation Ever [dTRBnHtHehQ].mp3"},
        {"titolo": "Be Curious Not Judgemental - Ted Lasso", "url": "/workspaces/Mental-Coaching-00/Ted Lasso Darts Scene - Be Curious Not Judgemental [DWLoasvaFb8].mp3"},
        {"titolo": "You'll never walk alone - Ted Lasso", "url": "/workspaces/Mental-Coaching-00/Ted Lasso, You'll never walk alone (ending of S01) [HA3HWP1OcL4].mp3"}    
    ]

    for audio in audio_list:
        st.markdown(f"**{audio['titolo']}**")
        st.audio(audio["url"])


# Funzione per ripulire il file JSON
def pulire_file_json():
    try:
        # Carica i dati dal file JSON
        with open("questionario_mentale.json", "r") as f:
            dati = json.load(f)

        # Pulisce tutti i dati nel file JSON
        dati.clear()

        # Scrive il file vuoto nel file JSON
        with open("questionario_mentale.json", "w") as f:
            json.dump(dati, f, indent=4)
        
        st.success("File JSON ripulito con successo!")  # Messaggio di successo
    except FileNotFoundError:
        st.warning("⚠️ Il file non è stato trovato.")
    except json.JSONDecodeError:
        st.warning("⚠️ Errore nella lettura del file JSON.")
    except Exception as e:
        st.error(f"❌ Errore: {e}")
# -------------------- QUESTIONARIO --------------------
def questionario_mentale():
    st.title("🧠 Come ti senti oggi?")
    oggi = datetime.date.today().isoformat()

    # Domande originali
    motivazione = st.slider("Motivazione", 1, 5, 3, step=1)
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

    # Aggiungi un'area di testo per scrivere il pensiero del giorno
    testo = st.text_area("Scrivi qui il tuo pensiero di oggi")
    
    if 'nome' in st.session_state:
        nome = st.session_state['nome']
    
    # Controllo se il campo "testo" non è vuoto prima di salvare
    if st.button("Salva nel diario"):
        if testo.strip() == "":
            st.error("❌ Il pensiero di oggi non può essere vuoto.")
        else:
            nuova_entry = {
                "nome": nome,
                "data": oggi,
                "testo": testo,
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

    # Visualizza le note precedenti
    if os.path.exists("diario_personale.json"):
        with open("diario_personale.json", "r") as f:
            tutte_le_note = json.load(f)

        diario_nome = [r for r in tutte_le_note if r["nome"] == nome]

        if diario_nome:
            for riga in sorted(diario_nome, key=lambda x: x["data"], reverse=True):
                # Controlliamo se la chiave 'testo' esiste nella riga
                if 'testo' in riga:
                    st.markdown(f"**{riga['data']}**")
                    st.markdown(f"> {riga['testo']}")
                    st.markdown("---")
                else:
                    st.warning(f"⚠️ Non ci sono appunti per la data {riga['data']}.")
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

    elif pagina == "checkin":
        checkin_pre()
    elif pagina == "checkout":
        checkout_post()
    elif pagina == "andamento":
        andamento_atleta()

    elif pagina == "🧠 Questionario mentale":
        questionario_mentale()

    elif pagina == "📓 Diario personale":
        diario_personale()

    elif pagina == "📝 Diario delle emozioni":
        diario_emozioni()

    elif pagina == "🧘‍♀️ Esercizi Mentali & Risorse":
        st.title("🧘‍♀️ Esercizi Mentali & Risorse")
        st.markdown("Seleziona un esercizio mentale da fare:")

        # Creiamo 4 colonne per i pulsanti
        col1, col2, col3, col4 = st.columns(4)

        if col1.button("Respirazione"):
            esercizio_respirazione()
        if col2.button("Visualizzazione pre-partita"):
            visualizzazione_pre_partita()
        if col3.button("Frasi motivazionali"):
            frasi_motivazionali()
        if col4.button("Audio motivazionali"):
            audio_mindfulness()


    elif pagina == "📊 Dashboard Allenatore":
        st.title("📊 Dashboard Allenatore")

        try:
            # Carica dati questionario mentale
            with open("questionario_mentale.json", "r") as f:
                dati = json.load(f)
            df = pd.DataFrame(dati)

            if df.empty:
                st.warning("Nessun dato disponibile")
            else:
                parametri = ["motivazione","ansia","concentrazione","autostima",
                            "stanchezza","stress","supporto","soddisfazione"]

                # Assicura numeri
                for col in parametri:
                    df[col] = pd.to_numeric(df[col], errors="coerce")
                df["data"] = pd.to_datetime(df["data"])

                # Crea le tab
                tab_mentale, tab_allenamento, tab_carico, tab_alert = st.tabs(
                    ["🧠 Mentale", "⚡ Allenamento", "📊 Carico", "🚨 Alert"]
                )

                # =====================================================
                # 🧠 TAB MENTALE
                # =====================================================
                with tab_mentale:
                    st.subheader("🧠 Indice rischio mentale squadra")
                    df["indice_rischio"] = (
                        df["ansia"]*0.3 +
                        df["stress"]*0.3 +
                        df["stanchezza"]*0.2 -
                        df["motivazione"]*0.1 -
                        df["autostima"]*0.1
                    )

                    rischio_squadra = df["indice_rischio"].mean()
                    col1, col2, col3 = st.columns(3)
                    col1.metric("Rischio medio squadra", round(rischio_squadra,2))
                    col2.metric("Motivazione media", round(df["motivazione"].mean(),2))
                    col3.metric("Stress medio", round(df["stress"].mean(),2))

                    # Semaforo giocatrici
                    ultimo = df.sort_values("data").groupby("nome").last().reset_index()
                    def semaforo(v):
                        if v > 3.5:
                            return "🔴 Alto"
                        elif v > 2.5:
                            return "🟠 Medio"
                        else:
                            return "🟢 OK"
                    ultimo["stato"] = ultimo["indice_rischio"].apply(semaforo)
                    st.subheader("🚦 Stato giocatrici")
                    st.dataframe(ultimo[["nome","indice_rischio","stato"]])

                    # Classifica mentale
                    st.subheader("🏆 Classifica mentale")
                    classifica = df.groupby("nome")[parametri].mean()
                    classifica["score"] = (
                        classifica["motivazione"] +
                        classifica["concentrazione"] +
                        classifica["autostima"] +
                        classifica["supporto"] -
                        classifica["ansia"] -
                        classifica["stress"] -
                        classifica["stanchezza"]
                    )
                    classifica = classifica.sort_values("score", ascending=False)
                    st.dataframe(classifica)
                    fig = px.bar(classifica, y=classifica.index, x="score", orientation="h",
                                title="Classifica mentale squadra")
                    st.plotly_chart(fig, use_container_width=True)

                    # Andamento parametro
                    st.subheader("📈 Andamento nel tempo")
                    parametro_sel = st.selectbox("Scegli parametro", parametri, key="grafico_param")
                    fig = px.line(df, x="data", y=parametro_sel, color="nome", markers=True)
                    st.plotly_chart(fig, use_container_width=True)

                    # Radar atleta
                    st.subheader("🧍 Scheda atleta")
                    atleta = st.selectbox("Seleziona atleta", df["nome"].unique(), key="radar")
                    df_atleta = df[df["nome"]==atleta]
                    medie = df_atleta[parametri].mean()
                    fig = go.Figure()
                    fig.add_trace(go.Scatterpolar(r=medie.values, theta=parametri, fill='toself'))
                    fig.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0,5])),
                                    showlegend=False)
                    st.plotly_chart(fig)

                # =====================================================
                # ⚡ TAB ALLENAMENTO
                # =====================================================
                with tab_allenamento:
                    st.header("⚡ Check-in e post allenamento")
                    
                    # Check-in pre
                    try:
                        with open("checkin_pre.json","r") as f:
                            df_check = pd.DataFrame(json.load(f))
                        if not df_check.empty:
                            df_check["data"] = pd.to_datetime(df_check["data"])
                            oggi = df_check[df_check["data"].dt.date == datetime.now().date()]
                            if not oggi.empty:
                                col1, col2, col3 = st.columns(3)
                                col1.metric("Energia media", round(oggi["energia"].mean(),2))
                                col2.metric("Stress medio", round(oggi["stress"].mean(),2))
                                col3.metric("Umore medio", round(oggi["umore"].mean(),2))
                                st.subheader("Stato giocatrici oggi")
                                fig = px.bar(oggi, x="nome", y="energia", color="stress", title="Energia vs Stress")
                                st.plotly_chart(fig, use_container_width=True)
                            else:
                                st.info("Nessun check-in oggi")
                    except:
                        st.info("Nessun dato check-in disponibile")

                    # Post allenamento
                    try:
                        with open("checkout_post.json","r") as f:
                            df_out = pd.DataFrame(json.load(f))
                        if not df_out.empty:
                            df_out["data"] = pd.to_datetime(df_out["data"])
                            oggi_out = df_out[df_out["data"].dt.date == datetime.now().date()]
                            if not oggi_out.empty:
                                col1, col2 = st.columns(2)
                                col1.metric("Fatica media", round(oggi_out["fatica"].mean(),2))
                                col2.metric("Soddisfazione media", round(oggi_out["soddisfazione"].mean(),2))
                                fig = px.bar(oggi_out, x="nome", y="fatica", color="soddisfazione",
                                            title="Fatica vs Soddisfazione")
                                st.plotly_chart(fig, use_container_width=True)
                    except:
                        st.info("Nessun dato post allenamento")

                # =====================================================
                # 📊 TAB CARICO
                # =====================================================
                with tab_carico:
                    try:
                        if not df.empty and 'df_check' in locals() and not df_check.empty:
                            ultimo_check = df_check.sort_values("data").groupby("nome").last()
                            ultimo_mentale = df.sort_values("data").groupby("nome").last()
                            merged = ultimo_check.join(ultimo_mentale, lsuffix="_check", rsuffix="_ment")
                            merged["carico_totale"] = merged["stress"] + merged["stanchezza"] + merged["ansia"]
                            fig = px.bar(merged, x=merged.index, y="carico_totale", title="Carico totale per atleta")
                            st.plotly_chart(fig, use_container_width=True)
                    except:
                        st.info("Nessun dato carico disponibile")

                # =====================================================
                # 🚨 TAB ALERT
                # =====================================================
                with tab_alert:
                    alert = ultimo[(ultimo["ansia"]>4) | (ultimo["stress"]>4) | (ultimo["stanchezza"]>4)]
                    st.header("Giocatrici da monitorare")
                    if alert.empty:
                        st.success("Nessun alert")
                    else:
                        st.error("Attenzione")
                        st.dataframe(alert[["nome","ansia","stress","stanchezza"]])

        except:
            st.warning("Nessun dato disponibile")

        if st.button("Ripulisci dati", key="pulisci"):
            pulire_file_json()
            st.success("Dati eliminati")


# Aggiungi la chiamata alla funzione principale
if __name__ == "__main__":
    main()
