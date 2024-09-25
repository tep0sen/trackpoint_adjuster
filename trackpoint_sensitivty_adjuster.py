import tkinter as tk
from tkinter import ttk
import subprocess
import os

def get_trackpoint_id():
    output = subprocess.check_output(["xinput", "list"]).decode()
    for line in output.split('\n'):
        if "TrackPoint" in line:
            return line.split('id=')[1].split()[0]
    return None

def get_current_sensitivity(trackpoint_id):
    output = subprocess.check_output(["xinput", "list-props", trackpoint_id]).decode()
    for line in output.split('\n'):
        if "libinput Accel Speed (" in line:
            return float(line.split(':')[1].strip())
    return 0

def set_sensitivity(value):
    subprocess.run(["xinput", "set-prop", trackpoint_id, "libinput Accel Speed", str(value)])

def update_sensitivity(event):
    value = float(sensitivity_scale.get())
    set_sensitivity(value)
    current_value.set(f"Current sensitivity: {value:.2f}")

def save_settings():
    value = float(sensitivity_scale.get())
    script_path = os.path.expanduser("~/.config/autostart-scripts/trackpoint-sensitivity.sh")
    
    # Create the autostart-scripts directory if it doesn't exist
    os.makedirs(os.path.dirname(script_path), exist_ok=True)
    
    with open(script_path, "w") as f:
        f.write("#!/bin/bash\n")
        f.write(f"xinput set-prop $(xinput list | grep -i 'trackpoint' | grep -o 'id=[0-9]*' | cut -d= -f2) 'libinput Accel Speed' {value}\n")
    
    # Make the script executable
    os.chmod(script_path, 0o755)
    
    save_status.set("Settings saved!")

trackpoint_id = get_trackpoint_id()
if trackpoint_id is None:
    print("TrackPoint not found")
    exit(1)

root = tk.Tk()
root.title("TrackPoint Sensitivity Adjuster")

current_sensitivity = get_current_sensitivity(trackpoint_id)

sensitivity_scale = ttk.Scale(root, from_=-1, to=1, orient='horizontal', length=200, value=current_sensitivity, command=update_sensitivity)
sensitivity_scale.pack(pady=20)

current_value = tk.StringVar()
current_value.set(f"Current sensitivity: {current_sensitivity:.2f}")
ttk.Label(root, textvariable=current_value).pack()

save_button = ttk.Button(root, text="Save Settings", command=save_settings)
save_button.pack(pady=10)

save_status = tk.StringVar()
save_status.set("")
ttk.Label(root, textvariable=save_status).pack()

root.mainloop()