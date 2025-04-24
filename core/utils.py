import os
from PIL import Image
import pandas as pd
import re
from pdf2image import convert_from_path
from openai import OpenAI
from dotenv import load_dotenv

import pytesseract

# Establece la ruta al ejecutable de Tesseract
pytesseract.pytesseract.tesseract_cmd = '/opt/local/bin/tesseract'


# Cargar las variables de entorno
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def procesar_imagen_con_ocr(ruta_imagen):
    try:
        # Abrir la imagen y extraer texto usando Tesseract OCR
        imagen = Image.open(ruta_imagen)
        texto_extraido = pytesseract.image_to_string(imagen, config='--psm 6')

        # Intentar extraer datos financieros como texto
        descriptions = []
        amounts = []
        lines = texto_extraido.strip().split("\n")
        for line in lines:
            match = re.match(r"^(.*?)(\s+\$?[\d,]+(?:\.\d{2})?)$", line)
            if match:
                description = match.group(1).strip()
                amount = match.group(2).strip()
                descriptions.append(description)
                amounts.append(amount)

        # Si se encontraron descripciones y montos, formar un texto estructurado
        if descriptions and amounts:
            texto_estructurado = "\n".join(f"{desc} {amt}" for desc, amt in zip(descriptions, amounts))
            return texto_estructurado

        # Si no se encontraron datos estructurados, devolver el texto extraído como está
        return texto_extraido

    except Exception as e:
        return f"Error al procesar la imagen con OCR: {str(e)}"


def procesar_pdf_con_ocr(ruta_pdf):
    paginas = convert_from_path(ruta_pdf)
    texto_extraido = ""
    for i, pagina in enumerate(paginas):
        texto = pytesseract.image_to_string(pagina)
        texto_extraido += texto + "\n"
    return texto_extraido

def procesar_excel(ruta_excel):
    df = pd.read_excel(ruta_excel, engine='openpyxl')
    if 'Descripción' in df.columns and 'Monto' in df.columns:
        return df
    else:
        descriptions = []
        amounts = []
        
        for _, row in df.iterrows():
            line = " ".join(map(str, row.values))
            match = re.match(r"^(.*?)(\s+\$?[\d,]+(?:\.\d{2})?)$", line)
            if match:
                description = match.group(1).strip()
                amount = match.group(2).strip()
                descriptions.append(description)
                amounts.append(amount)
        
        df = pd.DataFrame({'Descripción': descriptions, 'Monto': amounts})
        return df

def obtener_respuesta_openai(texto, prompt):
    try:
        completion = client.completions.create(
            model="gpt-3.5-turbo-instruct",
            prompt=f"{prompt}: {texto}",
            max_tokens=300,
            temperature=0.1
        )
        bot_message = completion.choices[0].text.strip()
        return bot_message
    except Exception as e:
        return f"Error en la respuesta de OpenAI: {str(e)}"
