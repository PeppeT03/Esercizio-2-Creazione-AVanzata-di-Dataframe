import pandas as pd
import sqlite3

# ==========================================
# STEP 1: Lettura dei dati dai Negozi (JSONL)
# ==========================================
# Leggiamo il file JSON Lines (JSONL) con le informazioni sui negozi.
# Usiamo 'lines=True' perché ogni riga del file è un oggetto JSON indipendente.
df_store = pd.read_json("stores.jsonl", lines=True)


# ==========================================
# STEP 2: Lettura delle Promozioni (Database SQL)
# ==========================================
# 1. Apriamo la connessione al database SQLite dove risiede la tabella promozioni.
conn = sqlite3.connect("example.db")

# 2. Eseguiamo la query SQL per estrarre tutta la tabella 'promotions' e caricarla in un DataFrame.
df_promo = pd.read_sql("SELECT * FROM promotions", conn)

# 3. Chiudiamo sempre la connessione al DB per liberare le risorse di sistema.
conn.close()


# ==========================================
# STEP 3: Lettura delle Vendite (CSV)
# ==========================================
# Carichiamo il file CSV principale che contiene lo storico delle transazioni/vendite.
df_sales = pd.read_csv("sales.csv")


# ==========================================
# STEP 4: Unione Progressiva delle Fonti (Merge)
# ==========================================
# 1. Primo Merge: Uniamo le vendite (df_sales) con le info sui negozi (df_store)
#    usando la colonna chiave 'store_id'. Salviamo il risultato in 'df_totale'.
df_totale = df_sales.merge(df_store, on="store_id")

# 2. Secondo Merge: Prendiamo 'df_totale' (che ha già 'region') e gli colleghiamo
#    le promozioni (df_promo) sempre sulla colonna chiave 'store_id'.
#    Ricorda: dobbiamo fare il merge su 'df_totale' e NON su 'df_sales',
#    altrimenti perderemmo la colonna 'region' aggiunta al passaggio precedente!
df_totale = df_totale.merge(df_promo, on="store_id")

print("--- DATI COMPLETI UNITI ---")
print(df_totale)
print("\n")


# ==========================================
# STEP 5: Filtro Vettorizzato (Senza cicli for)
# ==========================================
# Invece di scorrere riga per riga con un ciclo 'for' e un 'if', in Pandas creiamo
# una maschera booleana (True/False) per filtrare solo i negozi con promozioni attive (1).
filtro_promo = df_totale[df_totale['promo_flag'] == 1]

print("--- SOLO VENDITE CON PROMOZIONE ATTIVA ---")
print(filtro_promo)

df_gerarchico = df_totale.set_index(['region', 'store_id'])
print(df_gerarchico)


solo_nord = df_gerarchico.loc['Nord']
print("--- VENDITE SOLO REGIONE NORD ---")
print(solo_nord)

solo_nords1 = df_gerarchico.loc['Nord','S1']
print("--- VENDITE SOLO REGIONE NORD S1 ---")
print(solo_nords1)

vendite_s2 = df_gerarchico.xs('S2',level='store_id')
print("--- VENDITE SOLO  S2 ---")
print(vendite_s2)

sommatotale = df_gerarchico.groupby(level='region')['qty'].sum()
print("--- VENDITE TOTALI ---")
print(sommatotale)

somma_regione_promo = df_gerarchico.groupby(['region','promo_flag'])['qty'].sum()
print("--- VENDITE PER REGIONE E PROMOZIONE ---")
print(somma_regione_promo)

df_gerarchico['date']= pd.to_datetime(df_gerarchico['date'])

df_gerarchico['month'] = df_gerarchico['date'].dt.month
df_gerarchico['day_name'] = df_gerarchico['date'].dt.day_name()
print(df_gerarchico[['date','month','day_name']])

df_gerarchico['is_weekend']=df_gerarchico['date'].dt.day_name().isin(['Saturday','Sunday'])
print(df_gerarchico[['day_name', 'is_weekend']])

df_gerarchico['totale_incasso'] = df_gerarchico['qty'] * 15.0

print(df_gerarchico[['qty', 'totale_incasso']])

griglia = df_gerarchico.reset_index().pivot_table(index='region',columns='promo_flag',values='qty',aggfunc='sum',fill_value=0,margins=True)
print("stampo griglia")
print(griglia)

griglia.to_csv("report_vendite.csv",index=True)