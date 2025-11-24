import cv2
import numpy as np
import tensorflow as tf
import tkinter as tk
from tkinter import filedialog
import os

MODEL_PATH = 'FinalProject/models_components.keras' #route to the trained model

IMG_SIZE = 128 # Size of input image for the model 

# Class names used in the model
#same order as in training
CLASSES = ['Ceramic Capacitor', 'Electrolytic Capacitor', 'Inductor', 'Leds', 'Resistor']

# colors for each class in the dashboard
COLORS = {
    'Resistor': (0, 255, 255), # yellow
    'Electrolytic Capacitor':   (0, 255, 0),   # green
    'Ceramic Capacitor':      (0, 0, 255),   # red
    'Inductor':    (255, 100, 0), # dark blue
    'Led':       (255, 0, 255)  # purple
}

#Charhing the trianed model
print(f"--- Charhing {MODEL_PATH} ---")
try:
    model = tf.keras.models.load_model(MODEL_PATH)
    print("SUCCESS: MODEL CHARGED CORRECTLY.")
except Exception as e:
    print(f"\nNOT FOUND MODEL '{MODEL_PATH}'.")
    print(f"{e}")
    exit()

def preprocess_image(filepath):
    """
    takes the imagge file path and processes it to be ready for model prediction.
    Input: route of the image file
    Output: tensor ready for the model, original image in BGR format
    """
    img_bgr = cv2.imread(filepath) #reading in BGR format
    if img_bgr is None: return None, None #error reading image
    
    img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)  # Convert BGR to RGB
    img_resized = cv2.resize(img_rgb, (IMG_SIZE, IMG_SIZE))# Resize to model input size
    img_normalized = img_resized / 255.0  # Convert BGR to RGB and normalize to [0, 1]
    
    #  expand from(128, 128, 3) to (1, 128, 128, 3)
    # rhis is needed for model input
    img_tensor = np.expand_dims(img_normalized, axis=0)
    
    return img_tensor, img_bgr

def create_dashboard(original_img, probs):
    # redimention the image for the panel
    h, w = original_img.shape[:2]
    aspect_ratio = w / h
    display_h = 500
    display_w = int(display_h * aspect_ratio)
    img_display = cv2.resize(original_img, (display_w, display_h))
    
    # lateral panel
    panel_w = 450
    panel = np.zeros((display_h, panel_w, 3), dtype=np.uint8)
    panel[:] = (60, 60, 60) #dark background
    #panel[:] = (30, 30, 30) #gray background
    
    # title
    cv2.putText(panel, "Akinelector", (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
    
    # Encontrar la predicción ganadora
    best_idx = np.argmax(probs)
    best_label = CLASSES[best_idx]
    best_prob = probs[best_idx]
    
    # Mostrar predicción principal
    cv2.putText(panel, f"Prediction:", (20, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (200, 200, 200), 1)
    cv2.putText(panel, best_label.upper(), (20, 120), cv2.FONT_HERSHEY_SIMPLEX, 1.0, COLORS.get(best_label, (255,255,255)), 2)
    cv2.putText(panel, f"Trust probability: {best_prob*100:.1f}%", (20, 150), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (200, 200, 200), 1)
    
    # draw bars for all classes
    y_start = 200
    for i, class_name in enumerate(CLASSES):
        prob = probs[i]
        color = COLORS.get(class_name, (200, 200, 200))
        
        # labels texts for each
        cv2.putText(panel, class_name, (20, y_start), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        
        # background bar
        cv2.rectangle(panel, (200, y_start-10), (410, y_start), (0, 0, 0), -1)
        # value bar
        bar_len = int(prob * 210) # 210 is the maxium length
        cv2.rectangle(panel, (200, y_start-10), (200+bar_len, y_start), color, -1)
        
        # passing the probability to porcentage text
        cv2.putText(panel, f"{int(prob*100)}%", (400, y_start-15), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1)
        
        y_start += 50

    # joining panel and image
    dashboard = np.hstack((img_display, panel))
    return dashboard

def main():
    root = tk.Tk()
    root.withdraw()
    
    print("\n--- Image Electronic Component Classifier ---")
    
    while True:
        print("\nOpening finder...")
        # Input del Usuario: Selección del archivo
        file_path = filedialog.askopenfilename(
            title="Select an image",
            filetypes=[("Images", "*.jpg *.jpeg *.png *.bmp")]
        )
        
        if not file_path:
            break
            
        print(f"Precossing: {os.path.basename(file_path)}...")
        
        # Procesar Inputs
        tensor_input, original_img = preprocess_image(file_path)
        
        if tensor_input is None:
            print("Error reading the image. Please select a valid image file.")
            continue
            
        predictions = model.predict(tensor_input, verbose=0)
        probabilities = predictions[0] # extract the array probabilities
        final_output = create_dashboard(original_img, probabilities)
        cv2.imshow("Clasificador de Componentes - Proyecto Final", final_output)#show the final output
        key = cv2.waitKey(0)
        cv2.destroyAllWindows()
        
        if key == 27 or key == ord('u') or key == ord('U'):
            break


if __name__ == "__main__":
    main()