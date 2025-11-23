import cv2
import numpy as np
import tensorflow as tf
import tkinter as tk
from tkinter import filedialog
import os

# ==========================================
# 1. CONFIGURACIÓN (INPUTS DEL SISTEMA)
# ==========================================

# Nombre del archivo del modelo entrenado
MODEL_PATH = 'modelo_fotos_dummy.keras'

# Tamaño de imagen (DEBE SER IGUAL AL USADO EN EL ENTRENAMIENTO)
IMG_SIZE = 128 

# Clases (DEBEN ESTAR EN EL MISMO ORDEN EXACTO QUE EN EL ENTRENAMIENTO)
# Ajusta esta lista si tu orden es diferente
CLASSES = ['Capacitor', 'Diodo', 'Fuente', 'Inductor', 'Resistencia']

# Colores para las gráficas (Formato BGR para OpenCV)
COLORS = {
    'Resistencia': (0, 255, 255), # Amarillo
    'Capacitor electrolitic':   (0, 255, 0),   # Verde
    'Capacitor ceramic':      (0, 0, 255),   # Rojo
    'Inductor':    (255, 100, 0), # Azul fuerte
    'Diodo':       (255, 0, 255)  # Magenta
}

# ==========================================
# 2. CARGA DEL MODELO
# ==========================================
print(f"--- Cargando modelo desde {MODEL_PATH} ---")
try:
    model = tf.keras.models.load_model(MODEL_PATH)
    print("¡Modelo cargado exitosamente!")
except Exception as e:
    print(f"\nERROR CRÍTICO: No se encontró el archivo '{MODEL_PATH}'.")
    print("Asegúrate de haber corrido el script de entrenamiento primero.")
    print(f"Detalles: {e}")
    exit()

def preprocess_image(filepath):
    """
    Toma la ruta de un archivo, la lee y la prepara para la Red Neuronal.
    Input: Ruta del archivo (str)
    Output: Tensor de imagen procesada y la imagen original para mostrar
    """
    # Leer imagen
    img_bgr = cv2.imread(filepath)
    if img_bgr is None: return None, None
    
    # Conversión de color (OpenCV usa BGR, Keras suele preferir RGB)
    img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
    
    # Redimensionar al tamaño de entrada de la red
    img_resized = cv2.resize(img_rgb, (IMG_SIZE, IMG_SIZE))
    
    # Normalizar (valores de 0 a 1)
    img_normalized = img_resized / 255.0
    
    # Expandir dimensiones: de (128, 128, 3) a (1, 128, 128, 3)
    # Esto es porque la red espera un "batch" de imágenes, aunque sea una sola.
    img_tensor = np.expand_dims(img_normalized, axis=0)
    
    return img_tensor, img_bgr

def create_dashboard(original_img, probs):
    """
    Crea una visualización bonita con la imagen y las barras de probabilidad.
    """
    # Redimensionar imagen original para que quepa bien en pantalla (alto fijo 500px)
    h, w = original_img.shape[:2]
    aspect_ratio = w / h
    display_h = 500
    display_w = int(display_h * aspect_ratio)
    img_display = cv2.resize(original_img, (display_w, display_h))
    
    # Crear panel lateral (Negro)
    panel_w = 350
    panel = np.zeros((display_h, panel_w, 3), dtype=np.uint8)
    panel[:] = (30, 30, 30) # Fondo gris oscuro
    
    # Título
    cv2.putText(panel, "ANALISIS IA", (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
    
    # Encontrar la predicción ganadora
    best_idx = np.argmax(probs)
    best_label = CLASSES[best_idx]
    best_prob = probs[best_idx]
    
    # Mostrar predicción principal
    cv2.putText(panel, f"Prediccion:", (20, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (200, 200, 200), 1)
    cv2.putText(panel, best_label.upper(), (20, 120), cv2.FONT_HERSHEY_SIMPLEX, 1.0, COLORS.get(best_label, (255,255,255)), 2)
    cv2.putText(panel, f"Confianza: {best_prob*100:.1f}%", (20, 150), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (200, 200, 200), 1)
    
    # Dibujar barras para todas las clases
    y_start = 200
    for i, class_name in enumerate(CLASSES):
        prob = probs[i]
        color = COLORS.get(class_name, (200, 200, 200))
        
        # Texto de la etiqueta
        cv2.putText(panel, class_name, (20, y_start), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        
        # Barra de fondo
        cv2.rectangle(panel, (120, y_start-10), (330, y_start), (60, 60, 60), -1)
        # Barra de valor
        bar_len = int(prob * 210) # 210 es el largo máximo
        cv2.rectangle(panel, (120, y_start-10), (120+bar_len, y_start), color, -1)
        
        # Texto de porcentaje
        cv2.putText(panel, f"{int(prob*100)}%", (290, y_start-15), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1)
        
        y_start += 50

    # Instrucciones
    cv2.putText(panel, "Presiona ESC para salir", (20, display_h - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (100, 100, 100), 1)
    
    # Unir imagen y panel
    dashboard = np.hstack((img_display, panel))
    return dashboard

# ==========================================
# 4. BLOQUE PRINCIPAL (SELECCIÓN DE ARCHIVO)
# ==========================================
def main():
    # Ocultar la ventana root de Tkinter (solo queremos el explorador de archivos)
    root = tk.Tk()
    root.withdraw()
    
    print("\n--- SISTEMA DE CLASIFICACIÓN LISTO ---")
    
    while True:
        print("\nAbriendo explorador de archivos...")
        # Input del Usuario: Selección del archivo
        file_path = filedialog.askopenfilename(
            title="Selecciona una imagen de componente",
            filetypes=[("Imagenes", "*.jpg *.jpeg *.png *.bmp")]
        )
        
        if not file_path:
            print("Selección cancelada. Saliendo...")
            break
            
        print(f"Procesando: {os.path.basename(file_path)}...")
        
        # Procesar Inputs
        tensor_input, original_img = preprocess_image(file_path)
        
        if tensor_input is None:
            print("Error: No se pudo leer la imagen.")
            continue
            
        # Predicción
        predictions = model.predict(tensor_input, verbose=0)
        probabilities = predictions[0] # Extraer el array de probabilidades
        
        # Generar Output Visual
        final_output = create_dashboard(original_img, probabilities)
        
        # Mostrar en ventana
        cv2.imshow("Clasificador de Componentes - Proyecto Final", final_output)
        
        print("Resultado mostrado en ventana. Presiona ESC para cerrar la imagen (o selecciona otra tras cerrar).")
        key = cv2.waitKey(0)
        cv2.destroyAllWindows()
        
        if key == 27: # Tecla ESC para salir del todo
            break

if __name__ == "__main__":
    main()