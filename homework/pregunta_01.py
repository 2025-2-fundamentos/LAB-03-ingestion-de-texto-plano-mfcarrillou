"""
Escriba el codigo que ejecute la accion solicitada en cada pregunta.
"""

# pylint: disable=import-outside-toplevel

import re
import pandas as pd

def pregunta_01():
    """
    Construya y retorne un dataframe de Pandas a partir del archivo
    'files/input/clusters_report.txt'. Los requierimientos son los siguientes:

    - El dataframe tiene la misma estructura que el archivo original.
    - Los nombres de las columnas deben ser en minusculas, reemplazando los
      espacios por guiones bajos.
    - Las palabras clave deben estar separadas por coma y con un solo
      espacio entre palabra y palabra.


    """
    # Leer archivo y limpiar líneas vacías o separadores
    with open("files/input/clusters_report.txt", "r") as f:
      lines = f.readlines()

    lines = [line.strip() for line in lines if line.strip() and "----" not in line]
    
    # Obtener nombre de columnas
    line_1 = re.findall(r'\S+(?: \S+)*', lines[0])
    line_2 = re.findall(r'\S+(?: \S+)*', lines[1])

    column_names = []
    column_names.append(line_1[0]) # Primera columna
    for i in range(len(line_2)):
      column_names.append(f"{line_1[i+1]} {line_2[i]}")
    column_names.append(line_1[-1]) # Ultima columna

    # Convertir nombres de columnas en minusculas y con guiones bajos
    column_names = [col.lower().replace(" ", "_") for col in column_names]

    # Extraer registros
    rows = []
    cluster = quantity = percentage = None
    keywords = []

    for line in lines[2:]:
      # Detectar el inicio de un nuevo cluster
      match = re.match(r'^\s*(\d+)\s+(\d+)\s+([\d,]+)\s*%\s*(.*)', line)
      if match:
          # Guardar fila anterior si existe
          if cluster is not None:
              keywords_str = re.sub(r'\s+', ' ', " ".join(keywords)).strip().rstrip('.')
              rows.append([cluster, quantity, percentage, keywords_str])
              keywords = []

          # Capturar valores
          cluster = int(match.group(1))
          quantity = int(match.group(2))
          percentage = float(match.group(3).replace(",", "."))
          keywords.append(match.group(4))
      else:
          # Línea de continuación de palabras clave
          keywords.append(line)

    # Guardar el último cluster
    keywords_str = re.sub(r'\s+', ' ', " ".join(keywords)).strip().rstrip('.')
    rows.append([cluster, quantity, percentage, keywords_str])

    # Crear DataFrame
    df = pd.DataFrame(rows, columns=column_names)

    return df