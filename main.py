import tkinter as tk
import json
import os
import platform
import ctypes
import threading
import time

# load config
def load_config(filename='config.json'):
    if not os.path.exists(filename):
        return { "count": "Snowgraves", "countCol": "#ffcc00", "startNum": 0, 
                 "numCol": "#00ee00", "countKey": ["0"], "countSoundPath": "snow.wav" }
    with open(filename, 'r') as f:
        return json.load(f)

# mapper
def get_vk_code(key_str):
    key_str = key_str.upper()
    # nubers
    if len(key_str) == 1 and '0' <= key_str <= '9':
        return ord(key_str)
    # letters
    if len(key_str) == 1 and 'A' <= key_str <= 'Z':
        return ord(key_str)
    # special
    special_keys = {
        "SPACE": 0x20, "ENTER": 0x0D, "SHIFT": 0x10, "CTRL": 0x11, 
        "ALT": 0x12, "TAB": 0x09, "F1": 0x70, "F2": 0x71, "F3": 0x72
    }
    return special_keys.get(key_str, ord(key_str[0]))

class GlobalCounterApp:
    def __init__(self, root):
        self.root = root
        self.config = load_config()
        self.count = self.config['startNum']
        
        # get target
        self.target_vk = get_vk_code(self.config['countKey'][0])
        
        # set it up
        self.root.overrideredirect(True)
        self.root.geometry("+0+0")
        self.root.attributes("-topmost", True)
        self.root.configure(bg='black')
        self.frame = tk.Frame(root, bg='black', padx=20, pady=10)
        self.frame.pack()

        self.title_label = tk.Label(
            self.frame, text=f"{self.config['count']}: ", 
            font=("Arial", 40, "bold"), fg=self.config['countCol'], bg='black'
        )
        self.title_label.pack(side="left")

        self.value_label = tk.Label(
            self.frame, text=str(self.count), 
            font=("Arial", 40, "bold"), fg=self.config['numCol'], bg='black'
        )
        self.value_label.pack(side="left")

        # exit
        self.root.bind("<Escape>", self.close_and_save)
        
        # listening
        threading.Thread(target=self.start_global_listener, daemon=True).start()

    def play_sound(self):
        path = self.config['countSoundPath']
        if not os.path.exists(path): return
        if platform.system() == "Windows":
            import winsound
            winsound.PlaySound(path, winsound.SND_FILENAME | winsound.SND_ASYNC)
        else:
            cmd = "afplay" if platform.system() == "Darwin" else "aplay"
            os.system(f"{cmd} '{path}' &")

    def increment(self):
        self.count += 1
        self.root.after(0, lambda: self.value_label.config(text=str(self.count)))
        self.play_sound()

    def start_global_listener(self):
        if platform.system() != "Windows": return
        user32 = ctypes.windll.user32
        last_state = 0
        while True:
            state = user32.GetAsyncKeyState(self.target_vk)
            # 0x8000 checks if key is pressed
            if state & 0x8000 and not last_state & 0x8000:
                self.increment()
            last_state = state
            time.sleep(0.01)

    def close_and_save(self, event=None):
        # bye bye
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = GlobalCounterApp(root)
    root.mainloop()
