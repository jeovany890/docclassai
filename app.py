#!/usr/bin/env python3
# ============================================================
# DocClassAI — Interface Web (Flask)
# Lance : python3 app.py
# Ouvre : http://localhost:5000
# ============================================================

import os
import sys
import threading
import time
from flask import Flask, render_template, request, jsonify, send_file

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ocr        import lire_pdf_complet
from classifier import classifier_document
from sauvegarde import sauvegarder_document
from rapport    import generer_rapport
from config.settings import INPUT_DIR, OUTPUT_DIR, LOGS_DIR

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # 100MB max

# État global du traitement
etat = {
    "en_cours":   False,
    "progression": 0,
    "total":       0,
    "message":    "",
    "resultats":  [],
    "erreur":     None,
    "termine":    False,
}


def traiter_pdf_async(pdf_path):
    """Traite le PDF en arrière-plan."""
    global etat
    debut = time.time()

    try:
        etat["message"]    = "Lecture OCR des pages..."
        etat["progression"] = 5

        pages = lire_pdf_complet(pdf_path)
        total = len(pages)
        etat["total"]   = total
        etat["message"] = f"{total} page(s) détectée(s). Classification en cours..."

        resultats = []

        for i, page in enumerate(pages):
            etat["progression"] = int(10 + (i / total) * 80)
            etat["message"]     = f"Classification page {i+1}/{total}..."

            infos = classifier_document(page["texte"])
            chemin, nom = sauvegarder_document(pdf_path, page["index"], infos)

            resultats.append({
                "page":        page["index"] + 1,
                "nom_fichier": nom,
                "chemin":      chemin,
                "dossier":     os.path.dirname(chemin),
                "infos":       infos,
            })

        etat["message"]    = "Génération du rapport..."
        etat["progression"] = 95

        duree = time.time() - debut
        generer_rapport(resultats, pdf_path, duree)

        etat["resultats"]  = resultats
        etat["progression"] = 100
        etat["message"]    = f"✅ Terminé ! {total} document(s) classé(s) en {duree:.1f}s"
        etat["termine"]    = True

    except Exception as e:
        etat["erreur"]  = str(e)
        etat["message"] = f"❌ Erreur : {e}"
    finally:
        etat["en_cours"] = False


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/upload", methods=["POST"])
def upload():
    global etat

    if etat["en_cours"]:
        return jsonify({"erreur": "Un traitement est déjà en cours."}), 400

    if "fichier" not in request.files:
        return jsonify({"erreur": "Aucun fichier reçu."}), 400

    fichier = request.files["fichier"]
    if not fichier.filename.lower().endswith(".pdf"):
        return jsonify({"erreur": "Seuls les fichiers PDF sont acceptés."}), 400

    # Sauvegarder le fichier uploadé
    os.makedirs(INPUT_DIR, exist_ok=True)
    chemin_pdf = os.path.join(INPUT_DIR, fichier.filename)
    fichier.save(chemin_pdf)

    # Réinitialiser l'état
    etat.update({
        "en_cours":    True,
        "progression": 0,
        "total":       0,
        "message":    "Démarrage...",
        "resultats":  [],
        "erreur":     None,
        "termine":    False,
    })

    # Lancer le traitement en arrière-plan
    t = threading.Thread(target=traiter_pdf_async, args=(chemin_pdf,))
    t.daemon = True
    t.start()

    return jsonify({"succes": True, "fichier": fichier.filename})


@app.route("/progression")
def progression():
    return jsonify(etat)


@app.route("/resultats")
def resultats():
    return jsonify(etat["resultats"])


if __name__ == "__main__":
    os.makedirs(INPUT_DIR,  exist_ok=True)
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    os.makedirs(LOGS_DIR,   exist_ok=True)

    print("""
╔══════════════════════════════════════════════╗
║          DocClassAI — Interface Web          ║
║   Ouvre ton navigateur sur :                 ║
║   http://localhost:5000                      ║
╚══════════════════════════════════════════════╝
""")
    app.run(host="0.0.0.0", port=5000, debug=False)
