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
   
## 5. Security Note
   
secrets.py (containing WiFi credentials and Google API URLs) is excluded from this repository for security reasons. Please use secrets_template.py as a reference.
