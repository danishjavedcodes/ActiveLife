import tkinter as tk
from tkinter import messagebox
import subprocess

class ScriptRunnerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Script Runner")

        self.label = tk.Label(root, text="Click Start to run the script")
        self.label.pack()

        self.start_button = tk.Button(root, text="Start", command=self.start_script)
        self.start_button.pack(pady=10)

        self.stop_button = tk.Button(root, text="Stop", command=self.stop_script, state=tk.DISABLED)
        self.stop_button.pack(pady=5)

        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def start_script(self):
        self.process = subprocess.Popen(["python", "script.py"])
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        self.label.config(text="Script is running...")

    def stop_script(self):
        if self.process.poll() is None:
            self.process.terminate()
            self.start_button.config(state=tk.NORMAL)
            self.stop_button.config(state=tk.DISABLED)
            self.label.config(text="Script stopped")
        else:
            messagebox.showinfo("Info", "Script is not running.")

    def on_closing(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            if hasattr(self, 'process') and self.process.poll() is None:
                self.process.terminate()
            self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = ScriptRunnerApp(root)
    root.mainloop()
