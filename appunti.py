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