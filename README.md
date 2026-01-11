# Python Keyboard Controller for Raspberry Pi (UDP)

This project provides a real-time remote control interface for a Raspberry Pi-based robotic system. It captures local keyboard inputs and transmits serialized command packets over a low-latency UDP network connection.

**Collaboration Note:** This codebase was developed in collaboration with AI to optimize real-time performance, multi-threaded input handling, and protocol reliability.

## 🚀 Features
* **Low-Latency Control:** Utilizes UDP socket programming for high-speed communication between the host and the robot.
* **Multi-Threaded Input Handling:** Employs the `pynput` library to monitor key states asynchronously, preventing control lag.
* **Heartbeat Mechanism:** Sends a periodic "stay-alive" packet every 0.5s if no input changes are detected, ensuring the robot remains connected.
* **Fail-Safe Protocols:** Automatically transmits a sequence of "STOP" packets upon script exit or interruption to prevent uncontrolled movement.
* **Custom Packet Serialization:** Implements a 9-byte binary protocol to efficiently map driving and auxiliary commands.



## 🛠 Technical Specifications
* **Protocol:** UDP (User Datagram Protocol).
* **Polling Rate:** 50Hz (20ms interval) for responsive motor control.
* **Language:** Python 3.x.
* **Dependencies:** `pynput`, `socket`, `threading`.

## 🎮 Controls
| Key | Action |
| :--- | :--- |
| **Arrow Up/Down** | Forward / Reverse Drivetrain |
| **Arrow Left/Right** | Turn Left / Right |
| **W/A/S/D** | Arm / Auxiliary Controls |
| **Esc** | Safety Stop & Exit |