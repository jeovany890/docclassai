Le problème résolu
Dans les PME, mairies et institutions africaines, des milliers de documents papier sont scannés puis classés manuellement — un travail long, répétitif et source d'erreurs.
DocClassAI automatise entièrement ce processus.

Vous déposez un PDF contenant 100 factures scannées → le système ressort 100 fichiers classés et renommés automatiquement.

Fonctionnalités


-Séparation automatique d'un PDF multi-pages en fichiers individuels
- OCR intégré pour lire le texte des documents scannés (Tesseract)
-IA locale pour comprendre et classifier chaque document (Ollama + Qwen2.5)
-Classement automatique dans des dossiers organisés par type et année
-Renommage intelligent basé sur le contenu (fournisseur, date, numéro)
-Rapport de traitement détaillé après chaque session
-Interface web simple et moderne accessible depuis le navigateur
-100% local — aucune donnée envoyée sur internet

->Types de documents supportés

TypeExempleFacturefacture_ORANGE-BENIN_2024-06-15_F-0042.pdfReçurecu_CABINET-AGOSSOU_2024-06-20_R-087.pdfBon de commandebon_commande_SONAEC_2024-06-25_BC-015.pdfContratcontrat_ENTREPRISE-ABC_2024-01-01_C-001.pdfBulletin de paiebulletin_paie_EMPLOYE-NOM_2024-06-01_null.pdfDevisdevis_FOURNISSEUR_2024-05-10_D-003.pdfBon de livraisonbon_livraison_SONAEC_2024-06-30_BL-012.pdfRelevé bancairereleve_bancaire_SGBBE_2024-06-30_null.pdf

Architecture

PDF multi-pages (input)
        ↓
PyMuPDF — séparation des pages
        ↓
Tesseract OCR — extraction du texte
        ↓
Qwen2.5:3b via Ollama — classification IA locale
        ↓
Fichiers renommés + classés (output/)
        ↓
Rapport de traitement (logs/)

⚙️ Installation

Prérequis


Linux (Ubuntu 20.04+)
Python 3.10+
8 Go RAM minimum (16 Go recommandé)
10 Go d'espace disque libre


Étape 1 — Cloner le projet

bashgit clone https://github.com/jeovany890/docclassai.git
cd docclassai

Étape 2 — Installer les dépendances Python

bashpip3 install -r requirements.txt --break-system-packages

Étape 3 — Installer Tesseract OCR

bashsudo apt install tesseract-ocr tesseract-ocr-fra -y

Étape 4 — Installer Ollama et le modèle IA

bash# Installer Ollama
curl -fsSL https://ollama.com/install.sh | sh

# Télécharger le modèle (2 Go)
ollama pull qwen2.5:3b

Étape 5 — Vérifier l'installation

bashpython3 test_installation.py


🚀 Utilisation

Interface Web (recommandé)

bashpython3 app.py

Ouvre ton navigateur sur http://localhost:5000, glisse ton PDF et laisse le système travailler.

Ligne de commande

bash# Traiter un seul PDF
python3 main.py input/mon_fichier.pdf

# Traiter tous les PDF d'un dossier
python3 main.py input/

⚙️ Configuration

Tu peux personnaliser les règles de classement dans config/settings.py :

python# Format du nom de fichier
FORMAT_NOM = "{type}_{fournisseur}_{date}_{numero}"

# Structure des dossiers de sortie
STRUCTURE_DOSSIERS = {
    "facture":       "Factures",
    "recu":          "Recus",
    "bon_commande":  "Bons_de_commande",
    # Ajoute tes propres types ici...
}

# Modèle IA utilisé
OLLAMA_MODEL = "qwen2.5:3b"


💻 Configuration matérielle recommandée

RAMVitesse de traitement8 Go~30-60 sec / page16 Go~15-30 sec / page32 Go~5-10 sec / page


🔒 Souveraineté des données
DocClassAI a été conçu avec la confidentialité comme priorité absolue :
✅ Aucune donnée envoyée sur internet
✅ Modèle IA tournant entièrement en local
✅ Déployable sur serveur interne d'entreprise
✅ Compatible avec les exigences RGPD et de souveraineté numérique

🗺️ Roadmap
 Pipeline OCR + IA + classement
 Interface web
 Rapport de traitement
 Script d'installation automatique (install.sh)
 Support Windows
 Interface de correction manuelle
 Export Excel des métadonnées
 Multi-utilisateurs
 Support des langues locales africaines

👨‍💻 Auteur

WOROU Jeovany —Technicien en Audit de la Sécurité des Systèmes et Réseaux Informatiques

📄 Licence

MIT License — libre d'utilisation, modification et distribution.

"La souveraineté des données ne consiste pas seulement à les stocker localement : c'est aussi leur permettre d'être traitées de manière sécurisée, sans dépendre de services externes."
