#!/usr/bin/env python3
# ============================================================
# DocClassAI — Programme Principal
# Usage : python3 main.py chemin/vers/fichier.pdf
# ============================================================

import os
import sys
import time

# Ajouter le dossier du projet au path Python
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ocr        import lire_pdf_complet
from classifier import classifier_document
from sauvegarde import sauvegarder_document
from rapport    import generer_rapport
from config.settings import INPUT_DIR, OUTPUT_DIR


def afficher_banniere():
    print("""
╔══════════════════════════════════════════════╗
║          DocClassAI — v1.0                   ║
║   Système de Classification de Documents     ║
║   100%% Local | Zéro Internet | Zéro Coût    ║
╚══════════════════════════════════════════════╝
""")


def traiter_pdf(pdf_path):
    """
    Fonction principale : traite un PDF complet.
    1. Lit toutes les pages (OCR)
    2. Classifie chaque page (IA locale)
    3. Sauvegarde chaque page dans le bon dossier
    4. Génère le rapport
    """
    debut = time.time()

    # Vérifier que le fichier existe
    if not os.path.exists(pdf_path):
        print(f"❌ Fichier introuvable : {pdf_path}")
        sys.exit(1)

    print(f"📂 Fichier : {os.path.basename(pdf_path)}")
    print(f"📁 Sortie  : {OUTPUT_DIR}")

    # ── ÉTAPE 1 : OCR ─────────────────────────────────────
    print("\n🔍 ÉTAPE 1/3 — Lecture OCR des pages...")
    pages = lire_pdf_complet(pdf_path)
    print(f"✅ {len(pages)} page(s) lue(s)")

    # ── ÉTAPE 2 : CLASSIFICATION ───────────────────────────
    print("\n🤖 ÉTAPE 2/3 — Classification IA...")
    resultats = []

    for page in pages:
        index = page["index"]
        texte = page["texte"]

        print(f"\n   📊 Classification page {index+1}/{len(pages)}...")
        infos = classifier_document(texte)

        print(f"   Type        : {infos['type']}")
        print(f"   Fournisseur : {infos.get('fournisseur') or '?'}")
        print(f"   Date        : {infos.get('date') or '?'}")
        print(f"   Numéro      : {infos.get('numero') or '?'}")
        print(f"   Montant     : {infos.get('montant_total') or '?'} {infos.get('devise','')}")
        print(f"   Confiance   : {infos['confiance']}")

        # ── ÉTAPE 3 : SAUVEGARDE ──────────────────────────
        chemin, nom = sauvegarder_document(pdf_path, index, infos)
        dossier     = os.path.dirname(chemin)

        print(f"   💾 Sauvegardé : {nom}")
        print(f"   📁 Dans       : {dossier}")

        resultats.append({
            "page":        index + 1,
            "nom_fichier": nom,
            "chemin":      chemin,
            "dossier":     dossier,
            "infos":       infos,
        })

    # ── RAPPORT FINAL ──────────────────────────────────────
    print("\n📋 ÉTAPE 3/3 — Génération du rapport...")
    duree = time.time() - debut
    generer_rapport(resultats, pdf_path, duree)

    return resultats


def traiter_dossier(dossier_path):
    """
    Traite tous les PDF d'un dossier.
    """
    pdfs = [
        os.path.join(dossier_path, f)
        for f in os.listdir(dossier_path)
        if f.lower().endswith(".pdf")
    ]

    if not pdfs:
        print(f"❌ Aucun PDF trouvé dans : {dossier_path}")
        sys.exit(1)

    print(f"📂 {len(pdfs)} PDF trouvé(s) dans le dossier")
    for pdf in pdfs:
        print(f"\n{'='*50}")
        traiter_pdf(pdf)


# ── POINT D'ENTRÉE ────────────────────────────────────────
if __name__ == "__main__":
    afficher_banniere()

    if len(sys.argv) < 2:
        print("📖 USAGE :")
        print("   python3 main.py fichier.pdf          → traite un PDF")
        print("   python3 main.py dossier/             → traite tous les PDF du dossier")
        print(f"\n💡 Mets tes fichiers dans : {INPUT_DIR}")
        sys.exit(0)

    cible = sys.argv[1]

    if os.path.isdir(cible):
        traiter_dossier(cible)
    elif os.path.isfile(cible):
        traiter_pdf(cible)
    else:
        print(f"❌ Chemin invalide : {cible}")
        sys.exit(1)
