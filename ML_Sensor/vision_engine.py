import cv2
from ultralytics import YOLO
import threading
import time
import json
import csv
import os

class SmartFlowVision:
    def __init__(self, config_path='config.json'):
        # 1. Initialization Header
        print("\n" + "█"*60)
        print("  SMARTFLOW AI: SYSTEM INITIALIZING...")
        print("█"*60)
        
        # 2. Load Configuration
        if os.path.exists(config_path):
            with open(config_path, 'r') as f:
                self.config = json.load(f)
        else:
            self.config = {"multiplier": 1.5, "log_interval": 2}
        
        # 3. Initialize AI Model
        print("[ML_CORE] Loading YOLOv8n Neural Weights...")
        self.model = YOLO('yolov8n.pt')
        
        # 4. Data Storage Setup
        self.log_file = 'traffic_logs.csv'
        self._initialize_csv()
        
        # 5. Camera Setup
        self.cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        if not self.cap.isOpened():
            print("[CRITICAL] Could not access camera. Please check hardware.")
            exit()
            
        self.current_count = 0
        self.running = True

    def _initialize_csv(self):
        """Prepares the data persistence layer."""
        if not os.path.exists(self.log_file):
            with open(self.log_file, mode='w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(['Timestamp', 'Vehicle_Count', 'Lane_Pressure', 'Status'])
            print(f"[STORAGE] Created local database: {self.log_file}")

    def vision_loop(self):
        """Thread 1: Handles AI inference and Visual GUI."""
        print("[VISION] Video stream established.")
        print("\n" + "*"*60)
        print("  USER INSTRUCTION: CLICK THE VIDEO WINDOW AND PRESS 'Q' TO EXIT")
        print("*"*60 + "\n")
        
        while self.running:
            success, frame = self.cap.read()
            if not success: break

            # Perform AI Detection
            # Classes: 0:person, 2:car, 3:motorcycle, 5:bus, 7:truck
            results = self.model(frame, verbose=False)
            
            count = 0
            for r in results:
                for box in r.boxes:
                    if int(box.cls[0]) in [0, 2, 3, 5, 7]:
                        count += 1
            
            self.current_count = count

            # --- Visual HUD Rendering ---
            annotated_frame = results[0].plot()
            h, w, _ = annotated_frame.shape
            
            # Top Stats Banner
            cv2.rectangle(annotated_frame, (0, 0), (w, 60), (15, 23, 42), -1)
            cv2.putText(annotated_frame, f"SMARTFLOW AI | ACTIVE SENSORS: {count}", (20, 40), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
            
            # Bottom Exit Instruction (The "How to Quit" Cue)
            cv2.rectangle(annotated_frame, (0, h-40), (w, h), (0, 0, 0), -1)
            cv2.putText(annotated_frame, "COMMAND: PRESS [Q] ON KEYBOARD TO EXIT SYSTEM", (int(w/2) - 200, h - 12), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
            
            cv2.imshow("SmartFlow AI - Vision Dashboard", annotated_frame)
            
            # Key Listener
            if cv2.waitKey(1) & 0xFF == ord('q'):
                print("\n[SYSTEM] Shutdown command received.")
                self.running = False

    def logger_loop(self):
        """Thread 2: Handles CLI logging and CSV updates."""
        while self.running:
            timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
            multiplier = self.config.get('traffic_logic_parameters', {}).get('multiplier', 1.5)
            pressure = self.current_count * multiplier
            
            # 1. Professional Terminal Output
            print(f"[{timestamp}] DATA_FEED >> Count: {self.current_count} | Pressure: {pressure:.2f} | Status: OK")
            
            # 2. Permanent Data Persistence
            try:
                with open(self.log_file, mode='a', newline='') as f:
                    writer = csv.writer(f)
                    writer.writerow([timestamp, self.current_count, f"{pressure:.2f}", "ACTIVE"])
            except:
                pass # Silently fail if file is open in Excel

            time.sleep(self.config.get('traffic_logic_parameters', {}).get('log_interval', 2))

    def start(self):
        # Initialize Concurrent Processing
        t1 = threading.Thread(target=self.vision_loop)
        t2 = threading.Thread(target=self.logger_loop)
        
        t1.start()
        t2.start()
        
        t1.join()
        t2.join()
        
        # Cleanup Resources
        self.cap.release()
        cv2.destroyAllWindows()
        print("\n" + "█"*60)
        print("  SYSTEM OFFLINE: HARDWARE SAFELY DISCONNECTED")
        print("█"*60 + "\n")

if __name__ == "__main__":
    # Auto-detect config.json in the same directory
    sensor = SmartFlowVision()
    sensor.start()