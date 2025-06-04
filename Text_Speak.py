import tkinter as tk
from tkinter import ttk
import pyttsx3

class SpeechApp:
    def __init__(self, root):
        self.engine = pyttsx3.init()
        self.root = root
        self.root.title('Text to Speech')
        self.root.geometry("750x700")
        self.dark_mode = False

        self.create_ui()
        # Giving the colors for the desired figure
    def create_ui(self):
        self.bg_color = "#2e3f4f" if self.dark_mode else "#f0f0f0"
        self.fg_color = "white" if self.dark_mode else "black"
        self.main_bg = "#1f2a38" if self.dark_mode else "#4285F4"
        self.frame_bg = "#37474F" if self.dark_mode else "#e3f2fd"
        self.button_bg = "#66BB6A" if self.dark_mode else "#4CAF50"
        self.clear_bg = "#EF5350" if self.dark_mode else "#F44336"
        self.root.configure(bg=self.bg_color)

        for widget in self.root.winfo_children():
            widget.destroy()

        tk.Label(self.root, text='🎤 Text to Speech', bg=self.main_bg, fg='white',font=('Helvetica', 26, 'bold'), pady=20).pack(fill='x')

        mainFrame = tk.Frame(self.root, bg=self.frame_bg, bd=4, relief='ridge')
        mainFrame.place(relx=0.5, rely=0.52, anchor='center', width=650, height=570)

        tk.Label(mainFrame, text='Enter your text below:', bg=self.frame_bg,fg=self.fg_color, font=('Arial', 16, 'bold')).place(x=20, y=20)

        text_frame = tk.Frame(mainFrame)
        text_frame.place(x=20, y=60)
        self.text = tk.Text(text_frame, wrap='word', bd=2, relief='groove', width=58, height=5, font=('Arial', 13))
        scrollbar = tk.Scrollbar(text_frame, command=self.text.yview)
        self.text.config(yscrollcommand=scrollbar.set)
        self.text.pack(side='left')
        scrollbar.pack(side='right', fill='y')

        # For changing the voice creating voice selection
        tk.Label(mainFrame, text='Select Voice:', bg=self.frame_bg,fg=self.fg_color, font=('Arial', 13)).place(x=20, y=190)
        self.voice_var = tk.StringVar()
        self.voice_box = ttk.Combobox(mainFrame, textvariable=self.voice_var, state='readonly', width=30)
        self.voices = self.engine.getProperty('voices')
        self.voice_box['values'] = [voice.name for voice in self.voices]
        self.voice_box.current(0)
        self.voice_box.place(x=150, y=190)

        # Now Create the Speed Slider
        tk.Label(mainFrame, text='Speed:', bg=self.frame_bg, fg=self.fg_color, font=('Arial', 13)).place(x=20, y=240)
        self.speed = tk.Scale(mainFrame, from_=100, to=300, orient='horizontal',length=300, bg=self.frame_bg, fg=self.fg_color)
        self.speed.set(self.engine.getProperty('rate'))
        self.speed.place(x=100, y=230)

        # Creating the Volume Slider
        tk.Label(mainFrame, text='Volume:', bg=self.frame_bg,fg=self.fg_color, font=('Arial', 13)).place(x=20, y=300)
        self.volume = tk.Scale(mainFrame, from_=0, to=1, resolution=0.1,orient='horizontal', length=300,bg=self.frame_bg, fg=self.fg_color)
        self.volume.set(self.engine.getProperty('volume'))
        self.volume.place(x=100, y=290)

        # Creating the required Buttom
        btn_frame = tk.Frame(mainFrame, bg=self.frame_bg)
        btn_frame.place(x=100, y=370)

        speak_btn = tk.Button(btn_frame, text='🔊 Speak', command=self.speak,bg=self.button_bg, fg='white',font=('Arial', 14, 'bold'), width=12, bd=3, relief='raised')
        speak_btn.grid(row=0, column=0, padx=10)

        clear_btn = tk.Button(btn_frame, text='❌ Clear', command=self.clear_text, bg=self.clear_bg, fg='white',font=('Arial', 14, 'bold'), width=12, bd=3, relief='raised')
        clear_btn.grid(row=0, column=1, padx=10)

        # For changing the background mode given the Toggle Theme
        theme_btn = tk.Button(mainFrame, text='🌓 Toggle Theme', command=self.toggle_theme, bg='#607D8B', fg='white',font=('Arial', 12, 'bold'), width=20, bd=2)
        theme_btn.place(x=190, y=460)


    def speak(self):
        text = self.text.get("1.0", tk.END).strip()
        if not text:
            return

        selected_voice = self.voice_box.current()
        self.engine.setProperty('voice', self.voices[selected_voice].id)
        self.engine.setProperty('rate', self.speed.get())
        self.engine.setProperty('volume', self.volume.get())

        self.engine.say(text)
        self.engine.runAndWait()

    def clear_text(self):
        self.text.delete('1.0', tk.END)

    def toggle_theme(self):
        self.dark_mode = not self.dark_mode
        self.create_ui()

root = tk.Tk()
app = SpeechApp(root)
root.mainloop()