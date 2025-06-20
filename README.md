# 🔐 Keylogger Enable in Network Domain under Network Security. 

## 📌 Project Overview

This project is a **network-enabled keylogger** designed for use in organizational environments to monitor system activity, **detect insider threats**, and ensure **compliance with security policies**. It actively tracks keystrokes, monitors USB activity, and allows centralized control of endpoint systems by an administrator.

> ⚠️ **Disclaimer:** This project is strictly for educational and ethical research purposes. Do not use it without proper authorization in any live environment.

---

## 🚀 Features

### 🎯 Keylogger Client (Agent)
- Monitors and records all **keystrokes**.
- Logs detailed metadata: **IP address**, **MAC address**, **username**, **timestamp**.
- Detects usage of **restricted keywords** and sends real-time alerts.
- Monitors **USB device insertion/removal** events.
- Sends all logs securely to a centralized **database**.

### 🛠️ Admin Dashboard
- Real-time **activity monitoring** of all connected systems.
- View and filter logs based on **date/time**, **device**, or **keywords**.
- **Receive alerts** for suspicious activity.
- **Block/unblock** specific client systems remotely.

---

## 🧰 Tech Stack

- **Programming Language:** Python
- **Database:** Firebase Realtime DB / SQLite
- **UI (Admin Panel):** Tkinter / Web-based (Optional)
- **Networking:** Socket, psutil, getmac
- **System Monitoring:** `keyboard`, `os`, `shutil`, `datetime`

---

## 📁 Project Structure keylogger_project/ │ ├── client/                 # Keylogger client-side script │   ├── keylogger.py │   └── usb_monitor.py │ ├── admin_panel/            # Admin dashboard for monitoring & control │   └── admin_gui.py │ ├── database/               # Firebase configuration │   └── db_config.json │ └── README.md

---

## ⚙️ How It Works

1. **Client** script runs silently on each endpoint system.
2. Captures keystrokes and system events (like USB insertions).
3. Sends all activity logs to a **central database** in real-time.
4. **Admin Dashboard** fetches and displays the logs, alerts, and provides control options.

---

## 🛡️ Use Cases

- Corporate environments to **monitor employee compliance**.
- Educational research in **insider threat detection**.
- Demonstrating endpoint security solutions in **cybersecurity projects**.

---

## 📌 Important Notes

- Ensure **administrative privileges** are granted to run keylogger and USB monitoring modules.
- This project is meant to simulate real-world scenarios for **training and research**.
- Never deploy on a live network without **legal and ethical clearance**.

---

## 🤝 Acknowledgements

- Inspired by real-world cybersecurity monitoring tools.
- Built as part of a cybersecurity-focused academic project.

---

## 🙋‍♂️ Author

**[Your Name]**  
Cybersecurity Enthusiast | Python Programmer  
[LinkedIn](#) • [Email](#) • [GitHub](https://github.com/yourusername)
