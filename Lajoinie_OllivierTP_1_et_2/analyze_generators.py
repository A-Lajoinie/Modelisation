import csv
import math

# Chargement des donnees
def charger_donnees(chemin):
    try:
        bits = ""
        with open(chemin, 'r', newline='', encoding='utf-8') as f:
            lecteur = csv.reader(f)
            next(lecteur, None) # On saute l'entete
            for ligne in lecteur:
                if len(ligne) >= 2:
                    bits += ligne[1].strip()
        return bits
    except Exception as e:
        print(f"Erreur de lecture: {e}")
        return None

# Test 1: Frequence (Monobit)
def test_frequence(donnees):
    n = len(donnees)
    n0 = donnees.count('0')
    n1 = donnees.count('1')
    
    print(f"  [Freq] Total: {n} bits")
    print(f"  [Freq] 0s: {n0}, 1s: {n1}")
    
    stat = ((n0 - n1) ** 2) / n
    ok = stat < 3.8415
    
    return "Monobit (Frequence)", stat, ok

# Test 2: Frequence par bloc
def test_freq_bloc(donnees, M=128):
    n = len(donnees)
    nb_blocs = n // M
    
    somme = 0
    for i in range(nb_blocs):
        bloc = donnees[i*M : (i+1)*M]
        prop = bloc.count('1') / M
        somme += (prop - 0.5) ** 2
        
    stat = 4 * M * somme
    z = (stat - nb_blocs) / math.sqrt(2 * nb_blocs)
    ok = abs(z) < 1.96 
    
    return f"Frequence Bloc (M={M})", stat, ok

# Test 3: Suites (Runs)
def test_suites(donnees):
    n = len(donnees)
    n0 = donnees.count('0')
    n1 = donnees.count('1')
    
    runs = 1
    for i in range(1, n):
        if donnees[i] != donnees[i-1]:
            runs += 1
            
    attendu = 1 + (2 * n0 * n1) / n
    var = (2 * n0 * n1 * (2 * n0 * n1 - n)) / (n * n * (n - 1))
    
    z = (runs - attendu) / math.sqrt(var)
    
    print(f"  [Suites] Runs: {runs}, Attendu: {attendu:.2f}")
    
    ok = abs(z) < 1.96
    
    return "Runs (Suites)", z, ok

# Test 4: Suite la plus longue
def test_longue_suite(donnees, M=128):
    n = len(donnees)
    nb_blocs = n // M
    
    # Valeurs pour M=8 (approximees ou calculees pour 8 bits)
    # Pour M=8, les classes sont souvent: <=1, 2, 3, >=4
    # Proba approx: 
    # v0 (<=1): 0.2148
    # v1 (2): 0.3672
    # v2 (3): 0.2305
    # v3 (>=4): 0.1875
    # (Ces valeurs sont des exemples pour illustrer la logique M=8, a verifier si precision critique)
    
    if M == 8:
        pi = [0.2148, 0.3672, 0.2305, 0.1875]
        K = 4
        seuil = 7.815 # Chi2 df=3 a 0.05
    elif M == 128:
        pi = [0.1174, 0.2430, 0.2493, 0.1752, 0.1027, 0.1124]
        K = 6
        seuil = 11.0705
    else:
        print(f"Attention: M={M} non supporte pour le calcul precis du Chi2.")
        return f"Longue Suite (M={M})", 0.0, False

    comptes = [0] * K
    
    for i in range(nb_blocs):
        bloc = donnees[i*M : (i+1)*M]
        
        max_run = 0
        curr = 0
        for b in bloc:
            if b == '1':
                curr += 1
                if curr > max_run: max_run = curr
            else:
                curr = 0
        
        # Binning
        if M == 128:
            if max_run <= 4: comptes[0] += 1
            elif max_run == 5: comptes[1] += 1
            elif max_run == 6: comptes[2] += 1
            elif max_run == 7: comptes[3] += 1
            elif max_run == 8: comptes[4] += 1
            else: comptes[5] += 1
        elif M == 8:
            if max_run <= 1: comptes[0] += 1
            elif max_run == 2: comptes[1] += 1
            elif max_run == 3: comptes[2] += 1
            else: comptes[3] += 1
            
    chi2 = 0
    for i in range(K):
        attendu = nb_blocs * pi[i]
        chi2 += ((comptes[i] - attendu) ** 2) / attendu
        
    ok = chi2 < seuil
    return f"Longue Suite (M={M})", chi2, ok

def analyse():
    fichiers = ["generator1.csv", "generator2.csv"]
    
    for f in fichiers:
        print(f"\n{'='*30}")
        print(f"Fichier: {f}")
        bits = charger_donnees(f)
        
        if not bits: continue
        
        res = []
        res.append(test_frequence(bits))
        res.append(test_freq_bloc(bits, 128))
        res.append(test_suites(bits))
        res.append(test_longue_suite(bits, 128))
        
        # Ajout du test M=8 demande
        res.append(test_longue_suite(bits, 8))
        
        print("-" * 20)
        tout_ok = True
        for nom, val, reussite in res:
            etat = "OK" if reussite else "KO"
            if not reussite: tout_ok = False
            print(f"{nom:<25} : {etat} (Stat: {val:.4f})")
            
        if tout_ok:
            print(">> CONCLUSION: Semble aleatoire.")
        else:
            print(">> CONCLUSION: Biais detecte (pas aleatoire).")

if __name__ == "__main__":
    analyse()
