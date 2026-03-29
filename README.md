# **SmartFlow AI: Edge Vision for Adaptive Traffic Management**

# 🌍 The Problem
Currently, over 80% of urban traffic signals operate on static, "dumb" fixed timers.
This outdated approach leads to:
**Massive Fuel Waste & Emissions:** Vehicles idle at red lights even when cross-traffic lanes are completely empty.
**Emergency Delays:** Ambulances and fire engines get trapped in artificial gridlock, losing the critical "Golden Hour. 
**"High Infrastructure Costs:** Traditional smart upgrades require digging up roads to install expensive inductive loops or LiDAR sensors.

# 💡 The ML Solution 
Neuro-Symbolic Architecture:

**The "Eyes" (Sub-symbolic):** A multi-threaded YOLOv8 engine processes raw video to detect cars, buses, and ambulances.

**The "Brain" (Symbolic):** A Prolog Knowledge Base applies formal traffic laws and safety heuristics to the data provided by the vision engine.

**The "Twin" (Cyber-Physical):** A high-fidelity Digital Twin simulation validates the logic and calculates sustainability impact (CO2 and Fuel savings).

# 📂 Repository Structure
SmartFlow_Project/
├── ML_Sensor/
│   ├── vision_engine.py    # Multi-threaded YOLOv8 Detection Engine
│   ├── train_model.py     # Transfer Learning/Training Pipeline
│   └── config.json         # System & Heuristic Parameters
├── Knowledge_Base/
│   └── traffic_rules.pl    # Prolog Symbolic Logic (The Reasoning Layer)
├── Digital_Twin/
│   └── index.html          # Interactive JS Simulation (The Digital Twin)
└── README.md


#  How to Run the Project
Execution Guide (CLI & GUI)

This project is fully executable via the command line to ensure compatibility with headless edge devices.

**1. Prerequisites**

Ensure you have Python 3.8+ and the required libraries:

pip install opencv-python ultralytics numpy


(Optional: Install SWI-Prolog to run the formal logic engine separately).

**2. Running the AI Vision Sensor (Python)**

Navigate to the ML_Sensor folder and run the multi-threaded engine:

python vision_engine.py


GUI View: A window will show the live camera feed with AI bounding boxes.

CLI View: The terminal will print real-time "Lane Pressure" logs every 2 seconds.

**3. Running the Logic Audit (Prolog CLI)**

To verify the symbolic reasoning layer without a GUI, execute the following command:

swipl -q -s traffic_rules.pl -g "run_logic_test(lane_a, emergency, 20, 5, 10)." -t halt


This simulates an emergency vehicle detection and returns the AI's formal decision.

**4. Launching the Digital Twin (Simulation)**

Open Digital_Twin/index.html in any modern web browser to visualize the system in action, including the Emergency Dispatch and Sustainability Dashboard.
*
**🛠️ Key Features Highlight**
*🚑 Emergency Green Corridor: The AI assigns an absolute priority score to ambulances, safely clearing the intersection without causing accidents.*
*🌍 Carbon Footprint Tracker: Calculates idle-time reduction, estimating real-world drops in kg CO2 per hour.*
*🛡️ Fail-Safe Protocol: If camera visibility drops (simulated via weather conditions), the system automatically gracefully degrades to a standard fixed-timer pattern.*
*⛈️ Weather-Adaptive Physics: Automatically adjusts "Yellow Light" timing based on road friction (configured in config.json).*
