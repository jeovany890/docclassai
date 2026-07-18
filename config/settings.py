# ============================================================
# DocClassAI — Configuration principale
# ============================================================

import os

# Chemins
BASE_DIR     = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INPUT_DIR    = os.path.join(BASE_DIR, "input")
OUTPUT_DIR   = os.path.join(BASE_DIR, "output")
LOGS_DIR     = os.path.join(BASE_DIR, "logs")

# Modèle IA local (via Ollama)
OLLAMA_MODEL = "qwen2.5:3b"
OLLAMA_HOST  = "http://localhost:11434"

# OCR
OCR_LANGUE   = "fr"          # français
OCR_USE_GPU  = False         # CPU uniquement (compatible tous PC)
OCR_DPI      = 200           # résolution scan

# Classification
TYPES_DOCUMENTS = [
    "facture",
    "recu",
    "bon_commande",
    "contrat",
    "bulletin_paie",
    "devis",
    "bon_livraison",
    "releve_bancaire",
    "autre"
]

# Format du nom de fichier généré
# Disponible : {type} {fournisseur} {date} {numero} {destinataire}
FORMAT_NOM = "{type}_{fournisseur}_{date}_{numero}"

# Structure des dossiers de sortie
STRUCTURE_DOSSIERS = {
    "facture":          "Factures",
    "recu":             "Recus",
    "bon_commande":     "Bons_de_commande",
    "contrat":          "Contrats",
    "bulletin_paie":    "Bulletins_de_paie",
    "devis":            "Devis",
    "bon_livraison":    "Bons_de_livraison",
    "releve_bancaire":  "Releves_bancaires",
    "autre":            "Autres",
}

# Seuil de confiance (en dessous = vérification manuelle requise)
SEUIL_CONFIANCE = "moyenne"

# Prompt IA — règles de classification
PROMPT_CLASSIFICATION = """
Tu es un expert en analyse de documents d'entreprise africaine et française.
Tu analyses le texte extrait d'un document scanné.

MISSION : Extraire les informations clés et classifier le document.

TYPES POSSIBLES :
- facture       → montants, numéro facture, TVA, mentions "facture"
- recu          → preuve paiement, tampon, "reçu", "acquitté"
- bon_commande  → liste articles commandés, "bon de commande"
- contrat       → clauses, signatures, durée, "convention"
- bulletin_paie → salaire, employé, cotisations, "bulletin"
- devis         → prix estimatifs, "devis", "pro forma"
- bon_livraison → livraison, quantités livrées, "bon de livraison"
- releve_bancaire → opérations bancaires, solde, "relevé"
- autre         → aucun type ci-dessus ne correspond

RÈGLES STRICTES :
- Si information absente ou illisible → null
- Date toujours au format YYYY-MM-DD
- Si seulement l'année → YYYY-01-01
- Montant : chiffres uniquement, sans symbole
- Devise : XOF, EUR, USD, GNF, XAF selon le document
- Ne jamais inventer une information non visible
- Si document illisible → type = "autre", confiance = "faible"

NIVEAUX DE CONFIANCE :
- haute   → toutes les infos clairement lisibles
- moyenne → certaines infos partiellement lisibles
- faible  → document flou, beaucoup d'infos manquantes

RÉPONDS UNIQUEMENT EN JSON, rien d'autre :
{
  "type": "facture",
  "date": "2024-06-15",
  "fournisseur": "ORANGE BENIN",
  "destinataire": "ENTREPRISE ABC",
  "numero": "F-2024-0042",
  "montant_total": "150000",
  "devise": "XOF",
  "confiance": "haute"
}
"""
