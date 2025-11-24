import cv2
import numpy as np
import tensorflow as tf
import tkinter as tk
from tkinter import filedialog
import os

MODEL_PATH = 'FinalProject/models_components_250.keras' 

IMG_SIZE = 150 

# Class names used in the model
# Same order as in training
CLASSES = ['Ceramic Capacitor', 'Electrolytic Capacitor', 'Inductor', 'Leds', 'Resistor']

COLORS = {
    'Resistor': (0, 255, 255), # yellow
    'Electrolytic Capacitor':   (0, 255, 0),   # green
    'Ceramic Capacitor':      (0, 0, 255),   # red
    'Inductor':    (255, 100, 0), # dark blue
    'Leds':       (255, 0, 255)  # purple
}

# Loading the trained model
print(f"--- Loading {MODEL_PATH} ---")
try:
    model = tf.keras.models.load_model(MODEL_PATH)
    print("SUCCESS: MODEL LOADED CORRECTLY.")
except Exception as e:
    print(f"\nNOT FOUND MODEL '{MODEL_PATH}'.")
    print(f"{e}")
    exit()

def preprocess_image(filepath):
    """
    Takes the image file path and processes it to be ready for model prediction.
    Input: route of the image file
    Output: tensor ready for the model, original image in BGR format
    """
    img_bgr = cv2.imread(filepath) # Reading in BGR format
    if img_bgr is None: return None, None # Error reading image
    
    img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)  # Convert BGR to RGB
    img_resized = cv2.resize(img_rgb, (IMG_SIZE, IMG_SIZE))
    
    # We pass values 0-255 directly to the model.
    img_tensor = np.array(img_resized).astype('float32')
    
    # Expand from (150, 150, 3) to (1, 150, 150, 3)
    # This is needed for model input (Batch size)
    img_tensor = np.expand_dims(img_tensor, axis=0)
    
    return img_tensor, img_bgr

def create_dashboard(original_img, probs):
    # Redimension the image for the panel
    h, w = original_img.shape[:2]
    aspect_ratio = w / h
    display_h = 500
    display_w = int(display_h * aspect_ratio)
    img_display = cv2.resize(original_img, (display_w, display_h))
    
    # Lateral panel
    panel_w = 450
    panel = np.zeros((display_h, panel_w, 3), dtype=np.uint8)
    panel[:] = (60, 60, 60) # Dark background
    
    # Title (Added cv2.LINE_AA for smooth text)
    cv2.putText(panel, "Akinelector", (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2, cv2.LINE_AA)
    
    # Find the winning prediction
    best_idx = np.argmax(probs)
    
    # Safety check for index
    if best_idx < len(CLASSES):
        best_label = CLASSES[best_idx]
    else:
        best_label = "Unknown"

    best_prob = probs[best_idx]
    
    # Show main prediction
    cv2.putText(panel, f"Prediction:", (20, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (200, 200, 200), 1, cv2.LINE_AA)
    cv2.putText(panel, best_label.upper(), (20, 120), cv2.FONT_HERSHEY_SIMPLEX, 1.0, COLORS.get(best_label, (255,255,255)), 2, cv2.LINE_AA)
    cv2.putText(panel, f"Trust probability: {best_prob*100:.1f}%", (20, 150), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (200, 200, 200), 1, cv2.LINE_AA)
    
    # Draw bars for all classes
    y_start = 200
    for i, class_name in enumerate(CLASSES):
        if i >= len(probs): break
        
        prob = probs[i]
        color = COLORS.get(class_name, (200, 200, 200))
        
        # Label texts for each
        cv2.putText(panel, class_name, (20, y_start), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1, cv2.LINE_AA)
        
        # Background bar
        cv2.rectangle(panel, (200, y_start-10), (410, y_start), (0, 0, 0), -1)
        # Value bar
        bar_len = int(prob * 210) # 210 is the maximum length
        cv2.rectangle(panel, (200, y_start-10), (200+bar_len, y_start), color, -1)
        
        # Passing the probability to percentage text
        cv2.putText(panel, f"{int(prob*100)}%", (415, y_start-3), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1, cv2.LINE_AA)
        
        y_start += 50

    #joining panel and image
    dashboard = np.hstack((img_display, panel))
    return dashboard

def main():
    root = tk.Tk()
    root.withdraw()
    
    print("\n--- Image Electronic Component Classifier ---")
    
    while True:
        print("\nOpening finder...")
        # User Input: File selection
        file_path = filedialog.askopenfilename(
            title="Select an image",
            filetypes=[("Images", "*.jpg *.jpeg *.png *.bmp")]
        )
        
        if not file_path:
            print("No file selected. Exiting.")
            break
            
        print(f"Processing: {os.path.basename(file_path)}...")
        
        # Process Inputs
        tensor_input, original_img = preprocess_image(file_path)
        
        if tensor_input is None:
            print("Error reading the image. Please select a valid image file.")
            continue
        
        try:
            predictions = model.predict(tensor_input, verbose=0)
            probabilities = predictions[0] # Extract the array probabilities
            
            final_output = create_dashboard(original_img, probabilities)
            
            # Show the final output
            cv2.imshow("Eletronic components classifier", final_output)
            
            print("Press ESC or 'U' to exit, any other key to try another image.")
            key = cv2.waitKey(0)
            cv2.destroyAllWindows()
            
            if key == 27 or key == ord('u') or key == ord('U'):
                break
                
        except Exception as e:
            print(f"Error during prediction: {e}")


if __name__ == "__main__":
    main()