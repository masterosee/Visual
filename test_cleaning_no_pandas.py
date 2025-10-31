
import csv

def lire_csv(path):
    with open(path, encoding="latin1") as f:
        reader = csv.reader(f, delimiter=",", skipinitialspace=True)
        

        rows = [ [cell.strip() for cell in row] for row in reader ]
    return rows

def nettoyer_colonnes(header):
    return [col.strip().lower().replace(" ", "_").replace("(", "").replace(")", "").replace("$", "") 
            for col in header]

def convertir_text_en_nombre(val):
    mapping = {"vingt": 20, "trente": 30, "quarante": 40}
    if not val:
        return None
    val = val.strip().lower()
    if val.isdigit():
        return int(val)
    return mapping.get(val, None)

def nettoyer_donnees(rows):
    header = nettoyer_colonnes(rows[0])
    data = []
    for row in rows[1:]:
        if len(row) < 4:  # ligne incomplète
            continue
        nom, age, ville, revenu = [cell.strip() for cell in row]

        age = convertir_text_en_nombre(age)
        revenu = int(revenu) if revenu.isdigit() else None

        data.append({
            "nom": nom,
            "age": age,
            "ville": ville if ville else None,
            "revenu": revenu
        })
    return header, data

# Exemple d’utilisation
if __name__ == "__main__":
    rows = lire_csv("dataset_sale.csv")
    header, data = nettoyer_donnees(rows)

    print("Colonnes :", header)
    for ligne in data:
        print(ligne)
