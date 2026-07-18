#!/usr/bin/env python3
# ============================================================
# DocClassAI — Test d'installation v2
# Compatible Python 3.14+
# ============================================================

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

print("🔍 Vérification de l'installation DocClassAI...\n")

erreurs = []

# Test 1 — PyMuPDF
try:
    import fitz
    print(f"✅ PyMuPDF           : {fitz.version[0]}")
except ImportError as e:
    print(f"❌ PyMuPDF           : NON INSTALLÉ — pip3 install pymupdf")
    erreurs.append("pymupdf")

# Test 2 — Pillow
try:
    from PIL import Image
    import PIL
    print(f"✅ Pillow            : {PIL.__version__}")
except ImportError:
    print(f"❌ Pillow            : NON INSTALLÉ — pip3 install pillow")
    erreurs.append("pillow")

# Test 3 — Pytesseract
try:
    import pytesseract
    print(f"✅ Pytesseract       : installé")
except ImportError:
    print(f"❌ Pytesseract       : NON INSTALLÉ — pip3 install pytesseract")
    erreurs.append("pytesseract")

# Test 4 — Tesseract binaire
try:
    import pytesseract
    ver = pytesseract.get_tesseract_version()
    print(f"✅ Tesseract OCR     : {ver}")
except Exception:
    print(f"❌ Tesseract OCR     : NON INSTALLÉ — sudo apt install tesseract-ocr tesseract-ocr-fra")
    erreurs.append("tesseract-ocr")

# Test 5 — Requests
try:
    import requests
    print(f"✅ Requests          : {requests.__version__}")
except ImportError:
    print(f"❌ Requests          : NON INSTALLÉ — pip3 install requests")
    erreurs.append("requests")

# Test 6 — Ollama en cours
try:
    import requests
    r = requests.get("http://localhost:11434", timeout=3)
    print(f"✅ Ollama            : en cours d'exécution")
except Exception:
    print(f"⚠️  Ollama            : NON DÉMARRÉ — lance : ollama serve")

# Test 7 — Modèle qwen2.5:3b
try:
    import requests
    r = requests.get("http://localhost:11434/api/tags", timeout=3)
    if r.status_code == 200:
        modeles = [m["name"] for m in r.json().get("models", [])]
        if any("qwen2.5" in m for m in modeles):
            print(f"✅ Qwen2.5:3b        : disponible")
        else:
            print(f"⚠️  Qwen2.5:3b        : NON TÉLÉCHARGÉ — ollama pull qwen2.5:3b")
except Exception:
    print(f"⚠️  Modèles Ollama    : impossible de vérifier")

# Test 8 — Structure dossiers
dossiers = ["input", "output", "logs", "config"]
manquants = [d for d in dossiers if not os.path.exists(d)]
if not manquants:
    print(f"✅ Structure projet  : OK")
else:
    print(f"❌ Dossiers manquants : {manquants}")
    for d in manquants:
        os.makedirs(d, exist_ok=True)
    print(f"   ✅ Dossiers créés automatiquement")

# Test 9 — Config
try:
    from config.settings import OLLAMA_MODEL, PROMPT_CLASSIFICATION
    print(f"✅ Configuration     : OK (modèle: {OLLAMA_MODEL})")
except Exception as e:
    print(f"❌ Configuration     : ERREUR ({e})")
    erreurs.append("config")

# Résumé final
print("\n" + "="*50)
if not erreurs:
    print("🎉 INSTALLATION COMPLÈTE — DocClassAI est prêt !")
    print("\n📖 Pour lancer :")
    print("   python3 main.py input/ton_fichier.pdf")
else:
    print(f"⚠️  {len(erreurs)} problème(s) : {', '.join(erreurs)}")
    print("Résous les erreurs ci-dessus et relance ce test.")
print("="*50)
