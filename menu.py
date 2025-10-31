
# menu.py
import pandas as pd
from modules.plots.time_series import plot_time_series, plot_time_series_multi

def lancer_nettoyage():
    print("Nettoyage: en attente de branchement au module cleaning.")

def menu_graphiques():
    print("\n=== MENU GRAPHIQUES ===")
    print("1. Histogramme")
    print("2. Box Plot")
    print("3. Nuage de points")
    print("4. Courbes")
    print("0. Retour")
    choix = input("Votre choix: ").strip()

    if choix == "1":
        print("Histogramme: en attente de branchement.")
    elif choix == "2":
        print("Box Plot: en attente de branchement.")
    elif choix == "3":
        print("Nuage de points: en attente de branchement.")
    elif choix == "4":
        print("Courbes: en attente de branchement.")
    elif choix == "0":
        return
    else:
        print("Choix invalide.")

def menu_timeseries():
    print("\n=== MENU TIME SERIES ===")
    print("1. Séries temporelles simples")
    print("2. Séries multiples")
    print("0. Retour")
    choix = input("Votre choix: ").strip()

    if choix == "1":
        try:
            df = pd.read_csv("covid_19_clean_complete.csv")
            cols = {c.lower(): c for c in df.columns}
            date_col = cols.get("date", "Date" if "Date" in df.columns else None)
            confirmed_col = cols.get("confirmed", "Confirmed" if "Confirmed" in df.columns else None)

            if date_col is None or confirmed_col is None:
                print("Colonnes 'Date' et 'Confirmed' introuvables. Vérifie les en-têtes du CSV.")
                return

            fig = plot_time_series(df, date_col, confirmed_col, title="COVID-19 Confirmed Cases")
            fig.show()
            print("Série temporelle affichée.")
        except Exception as e:
            print(f"Erreur lors du tracé de la série temporelle: {e}")

    elif choix == "2":
        try:
            df = pd.read_csv("covid_19_clean_complete.csv")
            cols = {c.lower(): c for c in df.columns}
            date_col = cols.get("date", "Date" if "Date" in df.columns else None)
            y_cols = [c for c in df.columns if c.lower() in ["confirmed", "deaths", "recovered"]]

            if date_col is None or not y_cols:
                print("Colonnes 'Date' et/ou séries multiples introuvables. Vérifie les en-têtes du CSV.")
                return

            fig = plot_time_series_multi(df, date_col, y_cols, title="COVID-19: Confirmed vs Deaths vs Recovered")
            fig.show()
            print("Séries multiples affichées.")
        except Exception as e:
            print(f"Erreur lors du tracé des séries multiples: {e}")

    elif choix == "0":
        return
    else:
        print("Choix invalide.")

def lancer_export():
    print("Export: en attente de branchement.")

def menu_parametres():
    print("Paramètres: en attente de configuration.")

def menu_principal():
    while True:
        print("\n=== MENU PRINCIPAL ===")
        print("1. Nettoyage des données")
        print("2. Graphiques")
        print("3. TimeSeries")
        print("4. Export / Sauvegarde")
        print("5. Paramètres")
        print("0. Quitter")

        choix = input("Votre choix: ").strip()

        if choix == "1":
            lancer_nettoyage()
        elif choix == "2":
            menu_graphiques()
        elif choix == "3":
            menu_timeseries()
        elif choix == "4":
            lancer_export()
        elif choix == "5":
            menu_parametres()
        elif choix == "0":
            print("Au revoir 👋")
            break
        else:
            print("Choix invalide, réessayez.")

def main():
    menu_principal()

if __name__ == "__main__":
    main()
