# PicoW-Mood-Tracker: OOP-based IoT Logger

![Hardware Setup](./images/IMG_1025.jpeg)

IoT mood tracking system built with Raspberry Pi Pico W. This project demonstrates the integration of hardware sensors, local data persistence, and cloud synchronization using an Object-Oriented Programming (OOP) approach.

## 1.  Key Features
- OOP Architecture: Modular design with dedicated managers for Display, WiFi, Logging, and Cloud Uploading.
- Hardware Integration: Real-time feedback via SH1106 OLED and precise timekeeping with DS3231 RTC.
- Data Resilience: Local CSV logging ensures no data loss during network outages.
- Cloud Sync: Seamless data transmission to Google Sheets via REST API.
- Reliability: Memory management and hardware debouncing for stable long-term operation.

## 2.  Tech Stack

![Schematic](./images/IMG_0002.jpeg)
- Language: MicroPython
- Hardware: Raspberry Pi Pico W, SH1106 OLED, DS3231 RTC, Tactile Buttons
- Cloud: Google Apps Script (Web App)
- Concepts: Encapsulation, Modularization, System Integration, API Communication

## 3. Project Journey: From Script to System

This project evolved through a rigorous refactoring process.
(1) Monolithic Script: Initial proof-of-concept.
(2) Refactoring (OOP): Transitioned to class-based design for better encapsulation.
(3) Modularization: Decoupled components into 5 distinct modules for professional maintenance and scalability.

## 4. Project Structure

- **main.py** : Central controller. Must be saved directly to Pico.
- **lib/** : Containing functional modules.
  - **display_manager.py** : Handles I2C for SH1106 OLED & DS3231 RTC.
  - **wifi_manager.py** : Manage Pico W's wireless connectivity.
  - **local_logger.py** : Provides persistent CSV logging (offline storage).
  - **google_uploader.py** : Syncs data with Google Sheets API.
- **images/** : Contain hardware schematics and project photos.
- **secrets_template.py** : Template for environment variables (wifi / API).

## 5. How to Install & Run

This project uses **Thonny IDE** to upload and run code on the Raspberry Pi Pico W.

### 1) Prerequisites
* Install [Thonny IDE](https://thonny.org/).
* Connect your Pico W to your computer via USB.
* Ensure MicroPython firmware is installed on your Pico W.

### 2) Setup Secrets
1. Locate `secrets_template.py` in this repository.
2. Rename it to `secrets.py`.
3. Open `secrets.py` and enter your WiFi SSID, Password, and your Google Apps Script URL.

### 3) Upload Files to Pico W
1. Open Thonny IDE.
2. Go to **File > Open...** and select all files from the `lib/` folder and the `main.py` file from your local machine.
3. For each file, go to **File > Save as...** and select **Raspberry Pi Pico**.
4. **Important:** * Save the contents of the `lib/` folder (e.g., `display_manager.py`, `wifi_manager.py`, etc.) into a folder named `lib` on the Pico.
   * Save `main.py` and `secrets.py` directly in the root directory of the Pico.

### 4) Run
1. Disconnect and reconnect the USB, or simply press the **Run** button in Thonny.
2. Your Pico W will now start tracking your mood!

   
## 6. Security Note
   
secrets.py (containing WiFi credentials and Google API URLs) is excluded from this repository for security reasons. Please use secrets_template.py as a reference.
