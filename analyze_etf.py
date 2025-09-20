import pandas as pd

# Charger les données ETF
df = pd.read_excel('data/etf_base_assets.xlsx')

print("=== ANALYSE DU FICHIER ETF ===")
print(f"Total ETF: {len(df)}")
print(f"Total colonnes: {len(df.columns)}")

print("\n=== PROVIDERS ===")
print(f"Nombre de providers: {df['PROVIDER'].nunique()}")
print("Top providers:", df['PROVIDER'].value_counts().head())

print("\n=== CLASSIFICATION ===")
print("CLASSE 1 (Types principaux):")
print(df['CLASSE 1'].value_counts())

print("\nCLASSE 2 (Sous-catégories):")
print(f"Nombre unique: {df['CLASSE 2'].nunique()}")
print(df['CLASSE 2'].value_counts().head(10))

print("\nCLASSE 3 (Régions):")
print(f"Nombre unique: {df['CLASSE 3'].nunique()}")
print(df['CLASSE 3'].value_counts().head(10))

print("\n=== COURTIERS ===")
brokers = ['XTB', 'ING', 'SCALABLE', 'EASYBOURSE', 'BOURSO', 'BOURSEDIRECT', 'ETORO']
for broker in brokers:
    if broker in df.columns:
        count = df[broker].sum() if df[broker].dtype == 'bool' else (df[broker] == True).sum()
        print(f"{broker}: {count} ETF disponibles")

print("\n=== ÉLIGIBILITÉS ===")
if 'PEA' in df.columns:
    pea_count = df['PEA'].sum() if df['PEA'].dtype == 'bool' else (df['PEA'] == True).sum()
    print(f"PEA éligibles: {pea_count}")

if 'ASSVIE' in df.columns:
    assvie_count = df['ASSVIE'].sum() if df['ASSVIE'].dtype == 'bool' else (df['ASSVIE'] == True).sum()
    print(f"Assurance vie éligibles: {assvie_count}")

if 'HEDGED' in df.columns:
    hedged_count = df['HEDGED'].sum() if df['HEDGED'].dtype == 'bool' else (df['HEDGED'] == True).sum()
    print(f"ETF hedgés: {hedged_count}")

print("\n=== FRAIS ===")
if 'FRAIS DE GESTION' in df.columns:
    frais_stats = df['FRAIS DE GESTION'].describe()
    print("Statistiques frais de gestion:")
    print(frais_stats)

print("\n=== RENDEMENTS ATTENDUS ===")
if 'EXP_MACRO_RETURN' in df.columns:
    return_stats = df['EXP_MACRO_RETURN'].describe()
    print("Statistiques rendements espérés:")
    print(return_stats)

print("\n=== EXEMPLES D'ETF ===")
print("5 premiers ETF:")
cols_display = ['NOM', 'ISIN', 'PROVIDER', 'CLASSE 1', 'CLASSE 2', 'FRAIS DE GESTION', 'PEA']
available_cols = [col for col in cols_display if col in df.columns]
print(df[available_cols].head())