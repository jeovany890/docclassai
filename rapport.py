# ============================================================
# DocClassAI — Module Rapport
# Génère un rapport texte après chaque traitement
# ============================================================

import os
from datetime import datetime
from config.settings import LOGS_DIR


def generer_rapport(resultats, pdf_source, duree_secondes):
    """
    Génère un rapport complet du traitement.
    Sauvegarde dans logs/ et affiche dans le terminal.
    """
    now       = datetime.now()
    horodatage = now.strftime("%Y%m%d_%H%M%S")
    nom_rapport = f"rapport_{horodatage}.txt"
    chemin_rapport = os.path.join(LOGS_DIR, nom_rapport)

    # Statistiques
    total       = len(resultats)
    haute       = sum(1 for r in resultats if r["infos"]["confiance"] == "haute")
    moyenne     = sum(1 for r in resultats if r["infos"]["confiance"] == "moyenne")
    faible      = sum(1 for r in resultats if r["infos"]["confiance"] == "faible")
    a_verifier  = [r for r in resultats if r["infos"]["confiance"] != "haute"]

    # Compter par type
    types_count = {}
    for r in resultats:
        t = r["infos"]["type"]
        types_count[t] = types_count.get(t, 0) + 1

    # Construire le rapport
    lignes = [
        "=" * 60,
        "         RAPPORT DE TRAITEMENT — DocClassAI",
        "=" * 60,
        f"Date          : {now.strftime('%d/%m/%Y à %H:%M:%S')}",
        f"Fichier source: {os.path.basename(pdf_source)}",
        f"Durée totale  : {duree_secondes:.1f} secondes",
        f"Pages traitées: {total}",
        "",
        "─" * 60,
        "RÉSULTATS PAR CONFIANCE",
        "─" * 60,
        f"✅ Haute confiance   : {haute} document(s)",
        f"⚠️  Moyenne confiance : {moyenne} document(s)",
        f"❌ Faible confiance  : {faible} document(s)",
        "",
        "─" * 60,
        "RÉSULTATS PAR TYPE",
        "─" * 60,
    ]

    for type_doc, count in sorted(types_count.items()):
        lignes.append(f"   {type_doc:<20} : {count} document(s)")

    lignes += [
        "",
        "─" * 60,
        "DÉTAIL DES FICHIERS CRÉÉS",
        "─" * 60,
    ]

    for r in resultats:
        infos     = r["infos"]
        confiance = infos["confiance"]
        emoji     = "✅" if confiance == "haute" else "⚠️ " if confiance == "moyenne" else "❌"
        lignes.append(f"{emoji} Page {r['page']:03d} → {r['nom_fichier']}")
        lignes.append(f"         Type: {infos['type']} | Date: {infos.get('date','?')} | Fournisseur: {infos.get('fournisseur','?')}")
        lignes.append(f"         Dossier: {r['dossier']}")
        lignes.append("")

    if a_verifier:
        lignes += [
            "─" * 60,
            "⚠️  DOCUMENTS À VÉRIFIER MANUELLEMENT",
            "─" * 60,
        ]
        for r in a_verifier:
            lignes.append(f"   → {r['nom_fichier']} (confiance: {r['infos']['confiance']})")

    lignes += [
        "",
        "=" * 60,
        "FIN DU RAPPORT",
        "=" * 60,
    ]

    contenu = "\n".join(lignes)

    # Afficher dans le terminal
    print("\n" + contenu)

    # Sauvegarder dans logs/
    os.makedirs(LOGS_DIR, exist_ok=True)
    with open(chemin_rapport, "w", encoding="utf-8") as f:
        f.write(contenu)

    print(f"\n📄 Rapport sauvegardé : {chemin_rapport}")
    return chemin_rapport
