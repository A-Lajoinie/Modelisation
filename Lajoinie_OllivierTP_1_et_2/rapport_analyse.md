# Rapport d'Analyse des Générateurs Pseudo-Aléatoires

**Auteurs :** [Vos Noms]
**Date :** 21 Novembre 2025

---

## 1. Introduction
Ce rapport présente l'analyse de deux jeux de données (`generator1.csv` et `generator2.csv`) issus de générateurs pseudo-aléatoires inconnus. L'objectif est de déterminer si ces générateurs sont biaisés en appliquant une batterie de tests statistiques.

## 2. Méthodologie
Les données ont été extraites des fichiers CSV fournis. Chaque fichier contient 200 lignes, et chaque ligne contient une séquence binaire de 128 bits.

**Traitement des données :**
Nous avons concaténé l'ensemble des séquences de 128 bits pour former une unique séquence binaire longue de **25 600 bits** ($200 \times 128$) pour chaque générateur.

**Tests implémentés (CM3) :**
Nous avons implémenté les 4 tests demandés :
1.  **Test 1 : Monobit (Fréquence)** : Vérifie l'équiprobabilité des 0 et des 1 sur l'ensemble de la séquence.
2.  **Test 2 : Fréquence par bloc** : Vérifie si la proportion de 1 dans des blocs de $M=128$ bits est proche de 1/2.
3.  **Test 3 : Suites de 0s et 1s (Runs)** : Vérifie le nombre total de changements de valeur (runs) dans la séquence.
4.  **Test 4 : La suite la plus longue par bloc** : Vérifie la distribution de la longueur de la plus longue suite de 1 consécutifs dans des blocs de $M=128$ bits.

Seuil de significativité ($\alpha$) : 0.05 (Niveau de confiance de 95%).

---

## 3. Résultats

### Générateur 1 (`generator1.csv`)

| Test | Statistique | Résultat | Détails |
| :--- | :--- | :--- | :--- |
| **1. Monobit** | 0.2256 | **PASSED** | 0s: 12838, 1s: 12762 |
| **2. Fréquence par bloc** | 190.5000 | **PASSED** | Z-score approx normal |
| **3. Runs** | -0.5486 | **PASSED** | Runs: 12757 (Attendu: ~12800) |
| **4. Suite la plus longue** | **32.9902** | **FAILED** | Seuil critique $\chi^2 \approx 11.07$ |

**Conclusion pour Générateur 1 :**
Le générateur 1 **échoue** au test de la **Suite la plus longue par bloc**. La statistique (32.99) est largement supérieure au seuil critique. Cela indique que la distribution des longueurs maximales de 1 dans les blocs de 128 bits ne correspond pas à celle d'une séquence aléatoire.

---

### Générateur 2 (`generator2.csv`)

| Test | Statistique | Résultat | Détails |
| :--- | :--- | :--- | :--- |
| **1. Monobit** | 0.0127 | **PASSED** | 0s: 12809, 1s: 12791 |
| **2. Fréquence par bloc** | 176.3438 | **PASSED** | Z-score approx normal |
| **3. Runs** | **-4.8125** | **FAILED** | Runs: **12416** (Attendu: ~12801) |
| **4. Suite la plus longue** | 5.1230 | **PASSED** | Seuil critique $\chi^2 \approx 11.07$ |

**Conclusion pour Générateur 2 :**
Le générateur 2 **échoue** significativement au **Test des Runs** (Suites de 0s et 1s). La statistique Z de -4.81 indique un écart très important par rapport à la normale.

---

## 4. Analyse des Biais (Bonus)

### Biais du Générateur 1 (Suite la plus longue)
Le générateur 1 produit des blocs où la longueur de la plus longue suite de 1 consécutifs est anormale.
Si l'on observe les données brutes (via le script), on pourrait voir une sur-représentation de suites très longues ou très courtes. Un échec à ce test suggère souvent un problème dans la complexité locale du générateur ; il peut "rester bloqué" sur des 1 un peu trop longtemps par moment, ou au contraire ne jamais produire de longues suites (ce qui est statistiquement improbable).

### Biais du Générateur 2 (Runs / Stickiness)
Le générateur 2 présente un nombre de "runs" (12416) significativement inférieur à la valeur attendue (12801).
**Interprétation :**
Un nombre de runs plus faible signifie que le générateur change de valeur moins souvent que prévu. Il a une tendance à la **répétition** (stickiness).
Estimation du biais :
$$ P(change) \approx \frac{12416}{25599} \approx 0.485 $$
Probabilité de répétition : $P(X_i = X_{i-1}) \approx 51.5\%$.
Ce générateur n'est pas parfaitement "sans mémoire" et dépend légèrement de l'état précédent.

---

## 5. Bibliographie
1.  NIST SP 800-22 Rev. 1a, *A Statistical Test Suite for Random and Pseudorandom Number Generators*.
2.  Knuth, D. E., *The Art of Computer Programming, Vol 2*.

---

## 6. Glossaire
*   **Monobit** : Test de fréquence simple.
*   **Runs** : Séquences ininterrompues de bits identiques.
*   **Block Frequency** : Test de fréquence locale.
*   **Longest Run** : Test sur la longueur maximale de 1 consécutifs dans un bloc.
