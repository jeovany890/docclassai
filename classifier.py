# ============================================================
# DocClassAI — Module Classification IA
# Comprend le texte et extrait les informations clés
# ============================================================

import json
import re
import requests
from config.settings import OLLAMA_MODEL, OLLAMA_HOST, PROMPT_CLASSIFICATION


def classifier_document(texte):
    """
    Envoie le texte extrait à Ollama (Qwen2.5:3b local)
    et retourne les informations structurées en JSON.
    """
    if not texte or len(texte.strip()) < 10:
        print("   ⚠️  Texte trop court ou vide")
        return _resultat_vide()

    prompt_complet = f"""{PROMPT_CLASSIFICATION}

TEXTE DU DOCUMENT :
\"\"\"
{texte[:3000]}
\"\"\"

JSON :"""

    try:
        response = requests.post(
            f"{OLLAMA_HOST}/api/generate",
            json={
                "model":  OLLAMA_MODEL,
                "prompt": prompt_complet,
                "stream": False,
                "options": {
                    "temperature": 0.1,   # très peu de créativité = plus précis
                    "top_p": 0.9,
                    "num_predict": 300,
                }
            },
            timeout=120
        )

        if response.status_code != 200:
            print(f"   ❌ Erreur Ollama : {response.status_code}")
            return _resultat_vide()

        reponse_texte = response.json().get("response", "")
        return _extraire_json(reponse_texte)

    except requests.exceptions.ConnectionError:
        print("   ❌ Ollama non démarré. Lance : ollama serve")
        return _resultat_vide()
    except Exception as e:
        print(f"   ❌ Erreur classification : {e}")
        return _resultat_vide()


def _extraire_json(texte):
    """
    Extrait le JSON de la réponse du modèle.
    Gère les cas où le modèle ajoute du texte autour.
    """
    # Chercher un bloc JSON dans la réponse
    match = re.search(r'\{[^{}]*\}', texte, re.DOTALL)
    if match:
        try:
            data = json.loads(match.group())
            return _valider_et_nettoyer(data)
        except json.JSONDecodeError:
            pass

    # Tentative de parsing direct
    try:
        data = json.loads(texte.strip())
        return _valider_et_nettoyer(data)
    except json.JSONDecodeError:
        pass

    print("   ⚠️  JSON non parseable, retour résultat vide")
    return _resultat_vide()


def _valider_et_nettoyer(data):
    """
    Valide et nettoie les données extraites par l'IA.
    """
    types_valides = [
        "facture", "recu", "bon_commande", "contrat",
        "bulletin_paie", "devis", "bon_livraison",
        "releve_bancaire", "autre"
    ]

    # Valider le type
    type_doc = str(data.get("type", "autre")).lower().strip()
    if type_doc not in types_valides:
        type_doc = "autre"

    # Valider la date
    date = data.get("date")
    if date and not re.match(r'\d{4}-\d{2}-\d{2}', str(date)):
        date = None

    # Nettoyer le fournisseur
    fournisseur = data.get("fournisseur")
    if fournisseur:
        fournisseur = str(fournisseur).strip()[:50]  # max 50 chars
        fournisseur = re.sub(r'[<>:"/\\|?*]', '', fournisseur)  # retirer chars interdits

    # Nettoyer le numéro
    numero = data.get("numero")
    if numero:
        numero = str(numero).strip()[:30]
        numero = re.sub(r'[<>:"/\\|?*\s]', '-', numero)

    # Valider confiance
    confiance = str(data.get("confiance", "faible")).lower()
    if confiance not in ["haute", "moyenne", "faible"]:
        confiance = "faible"

    return {
        "type":          type_doc,
        "date":          date,
        "fournisseur":   fournisseur,
        "destinataire":  data.get("destinataire"),
        "numero":        numero,
        "montant_total": data.get("montant_total"),
        "devise":        data.get("devise", "XOF"),
        "confiance":     confiance,
    }


def _resultat_vide():
    """Retourne un résultat par défaut en cas d'erreur."""
    return {
        "type":          "autre",
        "date":          None,
        "fournisseur":   None,
        "destinataire":  None,
        "numero":        None,
        "montant_total": None,
        "devise":        "XOF",
        "confiance":     "faible",
    }
