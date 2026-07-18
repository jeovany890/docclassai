# ============================================================
# DocClassAI — Module Sauvegarde et Classement
# Renomme et classe chaque document dans le bon dossier
# ============================================================

import os
import re
import fitz
from datetime import datetime
from config.settings import OUTPUT_DIR, FORMAT_NOM, STRUCTURE_DOSSIERS


def construire_nom_fichier(infos, index):
    """
    Construit le nom du fichier à partir des infos extraites.
    Exemple : facture_ORANGE-BENIN_2024-06-15_F-0042.pdf
    """
    type_doc    = infos.get("type")    or "document"
    date        = infos.get("date")    or datetime.now().strftime("%Y-%m-%d")
    fournisseur = infos.get("fournisseur") or "inconnu"
    numero      = infos.get("numero")  or f"p{index+1:03d}"

    # Nettoyer le fournisseur pour le nom de fichier
    fournisseur = fournisseur.upper()
    fournisseur = re.sub(r'\s+', '-', fournisseur)
    fournisseur = re.sub(r'[^\w\-]', '', fournisseur)
    fournisseur = fournisseur[:30]  # limiter la longueur

    # Nettoyer le numéro
    numero = re.sub(r'\s+', '-', str(numero))
    numero = re.sub(r'[^\w\-]', '', numero)

    nom = FORMAT_NOM.format(
        type=type_doc,
        fournisseur=fournisseur,
        date=date,
        numero=numero,
    )

    return f"{nom}.pdf"


def determiner_dossier(type_doc, date):
    """
    Détermine le dossier de destination selon le type et la date.
    Crée la structure : OUTPUT/Type/Annee/
    """
    dossier_type = STRUCTURE_DOSSIERS.get(type_doc, "Autres")

    # Extraire l'année depuis la date
    annee = "Inconnue"
    if date and re.match(r'\d{4}', str(date)):
        annee = str(date)[:4]

    chemin = os.path.join(OUTPUT_DIR, dossier_type, annee)
    os.makedirs(chemin, exist_ok=True)
    return chemin


def extraire_et_sauvegarder_page(pdf_source_path, page_index, nom_fichier, dossier_dest):
    """
    Extrait une seule page du PDF source et la sauvegarde
    dans le dossier de destination sous le nom donné.
    """
    chemin_final = os.path.join(dossier_dest, nom_fichier)

    # Gérer les doublons de noms
    compteur = 1
    base, ext = os.path.splitext(chemin_final)
    while os.path.exists(chemin_final):
        chemin_final = f"{base}_{compteur}{ext}"
        compteur += 1

    # Extraire la page
    doc_source  = fitz.open(pdf_source_path)
    doc_nouveau = fitz.open()
    doc_nouveau.insert_pdf(doc_source, from_page=page_index, to_page=page_index)
    doc_nouveau.save(chemin_final)
    doc_nouveau.close()
    doc_source.close()

    return chemin_final


def sauvegarder_document(pdf_source_path, page_index, infos):
    """
    Fonction principale : construit le nom, détermine le dossier,
    extrait et sauvegarde la page.
    Retourne le chemin du fichier créé.
    """
    nom      = construire_nom_fichier(infos, page_index)
    dossier  = determiner_dossier(infos.get("type"), infos.get("date"))
    chemin   = extraire_et_sauvegarder_page(pdf_source_path, page_index, nom, dossier)

    return chemin, nom
