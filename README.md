# Saudi Pumps Project | Smart Pumping Digital Twin V1.0

![Status](https://img.shields.io/badge/Status-Live-brightgreen)
![Field](https://img.shields.io/badge/Field-Mechanical%20Engineering-blue)
![Tech](https://img.shields.io/badge/Tech-Python%20%7C%20IoT%20%7C%20Streamlit-orange)

**Live Deployment:** [sap-project.streamlit.app](https://sap-project.streamlit.app/)

---

## Project Concept
**Saudi Pumps** is an advanced industrial Digital Twin platform designed to monitor and simulate smart water pumping stations. The project addresses a critical industrial challenge: **maintaining continuous flow during line obstructions.** It integrates mechanical hydraulic principles with modern software control to create a resilient, self-healing pumping system.

### The Challenge & Solution
* **The Challenge:** In conventional systems, a blockage in the main pipeline leads to immediate supply failure and potential pump damage due to excessive backpressure (Overpressure).
* **The Smart Solution:** This system utilizes real-time sensor data to detect flow drops. It programmatically triggers an **Interlock Switch-over**, activating a **Bypass Line** to ensure uninterrupted water delivery while protecting the pump's mechanical integrity.

---

## 📐 Engineering P&ID (Piping & Instrumentation Diagram)
The system is built on a professional P&ID architecture, ensuring all components adhere to industrial standards:

1.  **Pump (P-101):** The primary mover (Centrifugal Pump) responsible for hydraulic energy transfer.
2.  **Gate Valve (GV-01):** An isolation valve located upstream for maintenance and source control.
3.  **Non-Return Valve (NRV):** Protects the pump from backflow and "Water Hammer" effects.
4.  **Globe Valves (GLV-01/02):** Precision throttling valves used in both the main and bypass lines for accurate flow and pressure management.
5.  **Level Indicating Transmitters (LIT):** Dual ultrasonic sensors providing high-accuracy real-time tank level telemetry.



---

## Technical Excellence
* **Blueprint UI/UX:** A high-fidelity engineering interface designed with a "Blueprint" theme, mimicking professional SCADA and industrial control room environments.
* **Dynamic Hydraulic Simulation:** A real-time physics engine that simulates fluid velocity, pressure drops, and tank filling rates based on valve positions.
* **Interlock Control Logic:** A robust programmatic link between instrumentation and actuators; enabling automatic switching to the bypass route when the main line is compromised.



---

## Tech Stack & Components
* **Software Framework:** Python & Streamlit for the Digital Twin dashboard.
* **Visualization:** Scalable Vector Graphics (SVG) with Neon-Glow particle animation.
* **Hardware (Integration Ready):** * **Controller:** ESP32-WROOM-32.
    * **Sensors:** HC-SR04 Ultrasonic & YF-S201 Flow Sensor.
    * **Actuators:** 12V DC Pump & Solenoid/Globe Valves.

---

## Installation & Usage
To run the Digital Twin locally:

1.  **Clone the Repository:**
    ```bash
    git clone https://github.com/f9-o/Saudi-Pumps.git
    ```
2.  **Install Dependencies:**
    ```bash
    pip install streamlit
    ```
3.  **Launch the Dashboard:**
    ```bash
    streamlit run app.py
    ```

---
## 📄 License
This project is open-source and licensed under the **MIT License**.
