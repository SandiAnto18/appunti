
#SIMULAZIONE D'ESAME 26-27/05/2026
# menu a tendina(voto da: a: ) + pulsante crea grafo +pulsante trova cammino


# ============================================================
# SCHEMA ESAME - POPOLARE UN MENU A TENDINA
# ============================================================
#
# FLUSSO:
#
# DATABASE
#    ↓
# DAO
#    ↓
# MODEL
#    ↓
# CONTROLLER
#    ↓
# VIEW / DROPDOWN
#
# MEMORIA:
# DAO = recupera
# MODEL = passa
# CONTROLLER = riempie
# VIEW = inizializza e mostra
#
# ============================================================


# ============================================================
# 1. DAO
# ============================================================
# Nel DAO definisco il metodo che recupera i dati dal database.
#
# Ricordare:
# - connessione
# - cursor
# - query
# - execute
# - for sulle righe
# - results.append(...)
# - return results
#
# ============================================================

@staticmethod
def getAllCountries():

    conn = DBConnect.get_connection()

    results = []

    cursor = conn.cursor(dictionary=True)

    query = """
        SELECT DISTINCT country
        FROM customer
    """

    cursor.execute(query)

    for row in cursor:
        results.append(row["country"])

    cursor.close()
    conn.close()

    return results


# ============================================================
# 2. MODEL
# ============================================================
# Nel Model richiamo il metodo del DAO.
#
# Il Model fa da PONTE:
#
# DAO → MODEL → CONTROLLER
#
# IMPORTANTE:
# from database.DAO import DAO
#
# NON:
# from database import DAO
#
# ============================================================

from database.DAO import DAO


class Model:

    def getCountry(self):

        return DAO.getAllCountries()


# ============================================================
# 3. CONTROLLER
# ============================================================
# Nel Controller definisco il metodo per POPOLARE
# il menu a tendina.
#
# SCHEMA DA RICORDARE:
#
# 1. Prendo la lista dal Model
# 2. Faccio il for
# 3. Creo una Option
# 4. La aggiungo al Dropdown
# 5. Aggiorno la pagina
#
# MEMORIA:
#
# LISTA → FOR → OPTION → UPDATE
#
# ============================================================

def fillDDCountry(self):

    # 1. Prendo i dati dal Model
    countries = self._model.getCountry()

    # 2. Ciclo sulla lista
    for c in countries:

        # 3-4. Creo l'Option e la aggiungo al Dropdown
        self._view._ddCountry.options.append(
            ft.dropdown.Option(c)
        )

    # 5. Aggiorno la pagina
    self._view.update_page()


# ============================================================
# 4. VIEW
# ============================================================
# Nella View devo:
#
# A) INIZIALIZZARE il Dropdown
# B) eventualmente RICHIAMARE il metodo del Controller
#
# ============================================================


# A) INIZIALIZZO IL DROPDOWN

self._ddCountry = ft.Dropdown(
    label="Country"
)


# B) RICHIAMO IL METODO DEL CONTROLLER
# per popolare il Dropdown

self._controller.fillDDCountry()


# ============================================================
# SCHEMA VISIVO FINALE
# ============================================================
#
# DAO
# │
# │ getAllCountries()
# ↓
# lista countries
# │
# ↓
# MODEL
# │
# │ getCountry()
# │ DAO.getAllCountries()
# ↓
# CONTROLLER
# │
# │ fillDDCountry()
# │ countries = model.getCountry()
# │ for c in countries
# │ Dropdown.Option(c)
# │ update_page()
# ↓
# VIEW
# │
# │ _ddCountry = ft.Dropdown()
# ↓
# MENU A TENDINA
#
#
# ============================================================
# FRASE DA RICORDARE
# ============================================================
#
# DAO = RECUPERA
# MODEL = PASSA
# CONTROLLER = RIEMPIE
# VIEW = INIZIALIZZA / MOSTRA
#
# ============================================================

# ============================================================
# CREAZIONE GRAFO (pulsante crea grafo)
# ============================================================

# Grafo non orientato
self._graph = nx.Graph()

# Grafo orientato
self._graph = nx.DiGraph()

# ============================================================
# DAO - recupero Customer di un paese con almeno una Invoice
# ============================================================

@staticmethod
def getCustomerByCountry(country):
    conn = DBConnect.get_connection()
    results = []
    cursor = conn.cursor(dictionary=True)

    query = """
        SELECT DISTINCT c.CustomerId AS cliente
        FROM customer c, invoice i
        WHERE country = %s
        AND c.CustomerId = i.CustomerId
    """

    cursor.execute(query, (country,))

    for row in cursor:
        results.append(row["cliente"])

    cursor.close()
    conn.close()

    return results

# ============================================================
# MODEL - creo i vertici del grafo
# ============================================================

def buildGraph(self, country):
    self._graph.clear()

    customers = DAO.getCustomerByCountry(country)

    self._graph.add_nodes_from(customers)


# ============================================================
# MODEL - restituisco il numero di nodi
# ============================================================

def getNumNodi(self):
    return len(self._graph.nodes())

# ============================================================
# CONTROLLER - pulsante Crea grafo
# ============================================================

def handleCreaGrafo(self, e):
    country = self._view._ddCountry.value

    self._model.buildGraph(country)

    # Svuoto i risultati precedenti
    self._view._txt_result.controls.clear()

    # Mostro numero di nodi e archi
    self._view._txt_result.controls.append(
        ft.Text("Grafo correttamente creato:")
    )

    self._view._txt_result.controls.append(
        ft.Text(f"Numero di nodi: {self._model.getNumNodi()}")
    )


