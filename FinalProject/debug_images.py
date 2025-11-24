import os
import tensorflow as tf
from pathlib import Path

# Tu ruta exacta
data_dir = r"c:/Users/enriq/Documents/UNAM/7mo semestre/IA/IAG08-Labs/FinalProject/dataSet"

print(f"🔍 Escaneando directorio: {data_dir}")

files_found = 0
files_corrupt = 0

# Recorremos todas las carpetas
for root, dirs, files in os.walk(data_dir):
    for filename in files:
        filepath = os.path.join(root, filename)
        files_found += 1
        
        # 1. Detectar y borrar Thumbs.db automáticamente
        if filename.lower() == "thumbs.db":
            print(f"❌ BORRANDO archivo de sistema: {filepath}")
            try:
                os.remove(filepath)
                files_corrupt += 1
            except:
                print("   (No se pudo borrar, ciérralo en el explorador)")
            continue

        # 2. Intentar decodificar con TensorFlow
        try:
            file_content = tf.io.read_file(filepath)
            # Intentamos decodificar como imagen. Si falla, salta al 'except'
            image = tf.io.decode_image(file_content, channels=3, expand_animations=False)
        except Exception as e:
            print(f"💀 ARCHIVO CORRUPTO DETECTADO: {filepath}")
            print(f"   Error: {e}")
            
            # Opcional: Borrarlo automáticamente
            os.remove(filepath) 
            print("   ---> Borrado.")
            
            files_corrupt += 1

print("-" * 30)
print(f"Escaneo terminado.")
print(f"Archivos revisados: {files_found}")
print(f"Archivos malos encontrados: {files_corrupt}")