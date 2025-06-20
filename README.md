
# M.I.N.D 🚀

**HackPrix 2025 entry by shuj4**

A Brain-Computer Interface (BCI) that enables cursor control using EEG brainwaves, powered by Arduino and a Python-based system.

---

## 🧠 Project Overview

M.I.N.D (Mental Interface for Neural Direction) is a brain-controlled interface designed to interpret EEG signals and translate them into real-time cursor movements. Developed during HackPrix 2025, the system bridges hardware and software using:

- **Arduino** to capture and transmit EEG brainwave signals
- **Python-based GUI and scripts** to process signals and control the cursor
- Real-time interaction loop between brain input and system output

---

## 🗂️ Repository Contents

- **Hackcode.ino** – Arduino firmware for signal reading
- **cursor.py** – Python script for cursor movement logic
- **cursor_control.py** – Converts signal data into actionable movement
- **gui.py** – Basic interface for monitoring status and signal flow

---

## ⚙️ Key Features

- Real-time cursor movement through EEG brainwave input
- Seamless hardware-software communication using serial data
- Designed for minimal user intervention post-setup
- Fully Python-driven interaction system

---

## 🚀 Getting Started

### 1. Requirements

- **Arduino IDE**
- **Python 3.7+**
- Install dependencies:
  ```bash
  pip install pyserial PySimpleGUI pyautogui
  ```

### 2. Setup

1. Upload `Hackcode.ino` to your Arduino
2. Connect your EEG input device to the board
3. Run the GUI:
   ```bash
   python gui.py
   ```

The system will begin reading EEG data and translating it into cursor movements automatically.

---

## 🧩 Architecture Diagram

```
[EEG Headset] → Arduino (Hackcode.ino) → Serial → Python (cursor_control)
        └─> cursor_control → cursor.py → moves cursor
                          └─> gui.py ← monitors system
```

---

## 📋 Future Roadmap

- Control car stereo and smart systems via thought
- Applications for physically challenged individuals, especially paralysis patients

---

## 🛡️ License

This project is for demonstration and research purposes only.  
**Use and reproduction are not permitted without explicit consent from the creator.**

---

## 📞 Contact

For queries, collaborations, or further details:
- Open an issue
- Tag @shuj4 on GitHub
