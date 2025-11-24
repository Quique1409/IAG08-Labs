import tensorflow as tf
import numpy as np
import os

# --- CONFIGURACIÓN ---
# Asegúrate de que este nombre coincida con cómo guardaste tu modelo (.h5 o .keras)
MODEL_NAME = 'models_components.keras' 

# Dimensiones (Deben ser IGUALES a las del entrenamiento)
IMG_HEIGHT = 150
IMG_WIDTH = 150

# Clases (En orden alfabético, tal como lo hizo TensorFlow)
class_names = ['ceramicCapacitor', 'electrolyticCapacitor', 'inductors', 'leds', 'resistors']

# --- CARGAR MODELO ---
base_dir = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(base_dir, MODEL_NAME)

if os.path.exists(model_path):
    print(f"🔄 Cargando modelo desde: {model_path}...")
    model = tf.keras.models.load_model(model_path)
    print("✅ Modelo cargado correctamente.")
else:
    print(f"❌ ERROR: No se encuentra el archivo '{MODEL_NAME}'.")
    print(f"   Buscado en: {base_dir}")
    print("   Asegúrate de haber corrido train.py y que se haya creado el archivo.")
    exit()

# --- FUNCIÓN DE PREDICCIÓN ---
def predecir_imagen(ruta_imagen):
    # Limpiar comillas por si copias la ruta en Windows como "C:\ruta..."
    ruta_imagen = ruta_imagen.strip('"').strip("'")

    if not os.path.exists(ruta_imagen):
        print("❌ La ruta de la imagen no existe. Intenta de nuevo.")
        return

    try:
        # 1. Cargar la imagen y cambiarle el tamaño a 150x150
        img = tf.keras.utils.load_img(ruta_imagen, target_size=(IMG_HEIGHT, IMG_WIDTH))
        
        # 2. Convertir a arreglo de números
        img_array = tf.keras.utils.img_to_array(img)
        
        # 3. Agregar una dimensión extra (porque el modelo espera un lote de imágenes, no una sola)
        img_array = tf.expand_dims(img_array, 0) 

        # 4. Hacemos la predicción
        predictions = model.predict(img_array, verbose=0)
        score = tf.nn.softmax(predictions[0]) # Convertir a porcentajes

        # 5. Obtener el resultado más alto
        clase_ganadora = class_names[np.argmax(score)]
        confianza = 100 * np.max(score)

        print("\n" + "="*30)
        print(f"🔎 Resultado: {clase_ganadora.upper()}")
        print(f"📊 Confianza: {confianza:.2f}%")
        print("="*30 + "\n")

    except Exception as e:
        print(f"❌ Error al procesar la imagen: {e}")

# --- BUCLE PRINCIPAL ---
print("\n--- TEST DE COMPONENTES ELECTRÓNICOS ---")
while True:
    entrada = input("🖼️  Pega la ruta de tu imagen (o escribe 'salir'): ")
    
    if entrada.lower() in ['salir', 'exit', 'q']:
        break
    
    if entrada.strip() == "":
        continue

    predecir_imagen(entrada)