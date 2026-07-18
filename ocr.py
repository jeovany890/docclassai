# ============================================================
# DocClassAI — Module OCR (Tesseract)
# Lit le texte sur les pages scannées
# Fonctionne sur Python 3.14+ et PC faibles
# ============================================================

import fitz  # PyMuPDF
import os
from PIL import Image
import pytesseract
import io

def pdf_en_images(pdf_path, dpi=200):
    """
    Convertit chaque page d'un PDF en image PIL.
    Retourne une liste de (index, image_PIL)
    """
    doc   = fitz.open(pdf_path)
    pages = []
    zoom  = dpi / 72
    mat   = fitz.Matrix(zoom, zoom)

    for i, page in enumerate(doc):
        pix = page.get_pixmap(matrix=mat)
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        pages.append((i, img))
        print(f"   📄 Page {i+1}/{len(doc)} convertie")

    doc.close()
    return pages


def extraire_texte_image(image_pil):
    """
    Extrait le texte d'une image PIL via Tesseract OCR.
    Supporte le français et l'anglais.
    """
    try:
        # Configuration Tesseract : français + anglais
        config = "--oem 3 --psm 6"
        texte  = pytesseract.image_to_string(
            image_pil,
            lang="fra+eng",
            config=config
        )
        return texte.strip()

    except pytesseract.TesseractNotFoundError:
        print("   ❌ Tesseract non installé. Lance : sudo apt install tesseract-ocr tesseract-ocr-fra")
        return ""
    except Exception as e:
        print(f"   ⚠️  Erreur OCR : {e}")
        return ""


def lire_pdf_complet(pdf_path, dpi=200):
    """
    Lit toutes les pages d'un PDF.
    Retourne une liste de dicts : {index, image, texte}
    """
    print(f"\n🔍 Lecture OCR de : {os.path.basename(pdf_path)}")
    pages_images = pdf_en_images(pdf_path, dpi=dpi)
    resultats    = []

    for index, image in pages_images:
        print(f"\n   🔤 Extraction texte page {index+1}...")
        texte = extraire_texte_image(image)
        mots  = len(texte.split())
        print(f"   ✅ {mots} mots extraits")

        resultats.append({
            "index": index,
            "image": image,
            "texte": texte,
        })

    return resultats
