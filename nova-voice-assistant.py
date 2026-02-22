import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import speech_recognition as sr
import pyttsx3
import webbrowser
import threading
import queue
from datetime import datetime
import pywhatkit as kit
import wikipedia
import requests
import json
import os
from gtts import gTTS
import pygame
import tempfile
import time

# ================= ADVANCED VOICE ENGINE =================
class VoiceEngine:
    def __init__(self):
        # Initialize multiple TTS engines for better quality
        self.engine = pyttsx3.init()
        self.pygame_initialized = False
        self.setup_engine()
        
    def setup_engine(self):
        # Configure pyttsx3 engine
        self.engine.setProperty('rate', 175)  # Slightly faster
        self.engine.setProperty('volume', 0.9)
        voices = self.engine.getProperty('voices')
        
        # Try to find a good voice
        for voice in voices:
            if 'female' in voice.name.lower():
                self.engine.setProperty('voice', voice.id)
                break
        
    def speak(self, text):
        """Enhanced speech with better quality"""
        try:
            # Try using gTTS for better quality (requires internet)
            if check_internet():
                self.speak_with_gtts(text)
            else:
                # Fallback to pyttsx3
                self.engine.say(text)
                self.engine.runAndWait()
        except Exception as e:
            print(f"Speech error: {e}")
            # Final fallback
            self.engine.say(text)
            self.engine.runAndWait()
    
    def speak_with_gtts(self, text):
        """Use Google TTS for natural sounding voice"""
        try:
            if not self.pygame_initialized:
                pygame.mixer.init()
                self.pygame_initialized = True
                
            # Create temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as tmp_file:
                temp_path = tmp_file.name
            
            # Generate speech
            tts = gTTS(text=text, lang='en', slow=False)
            tts.save(temp_path)
            
            # Play audio
            pygame.mixer.music.load(temp_path)
            pygame.mixer.music.play()
            
            # Wait for playback to finish
            while pygame.mixer.music.get_busy():
                pygame.time.wait(100)
            
            # Cleanup
            pygame.mixer.music.unload()
            os.unlink(temp_path)
            
        except Exception as e:
            print(f"gTTS error: {e}")
            raise e

# ================= ADVANCED COMMAND PROCESSOR =================
class CommandProcessor:
    def __init__(self, voice_engine, ui_callback):
        self.engine = voice_engine
        self.update_ui = ui_callback
        self.is_listening = False
        
    def process(self, text):
        """Process voice commands with AI-like capabilities"""
        text = text.lower().strip()
        
        # Basic commands
        if any(word in text for word in ['hello', 'hi', 'hey']):
            response = f"Hello! How can I help you today?"
            self.engine.speak(response)
            return response
            
        # Time and date
        elif 'time' in text:
            current_time = datetime.now().strftime("%I:%M %p")
            response = f"The current time is {current_time}"
            self.engine.speak(response)
            return response
            
        elif 'date' in text or 'day' in text:
            current_date = datetime.now().strftime("%A, %B %d, %Y")
            response = f"Today is {current_date}"
            self.engine.speak(response)
            return response
            
        # Web browsing
        elif 'youtube' in text:
            response = "Opening YouTube"
            self.engine.speak(response)
            webbrowser.open("https://youtube.com")
            return response
            
        elif 'google' in text:
            search_term = text.replace('google', '').replace('search', '').strip()
            if search_term:
                response = f"Searching Google for {search_term}"
                webbrowser.open(f"https://www.google.com/search?q={search_term}")
            else:
                response = "Opening Google"
                webbrowser.open("https://google.com")
            self.engine.speak(response)
            return response
            
        elif 'wikipedia' in text or 'wiki' in text:
            try:
                search_term = text.replace('wikipedia', '').replace('wiki', '').strip()
                if search_term:
                    summary = wikipedia.summary(search_term, sentences=2)
                    response = f"According to Wikipedia: {summary}"
                else:
                    response = "What would you like to search on Wikipedia?"
                self.engine.speak(response)
                return response
            except:
                response = "Sorry, I couldn't find that on Wikipedia"
                self.engine.speak(response)
                return response
        
        # Music and entertainment
        elif 'play' in text:
            song = text.replace('play', '').strip()
            if song:
                response = f"Playing {song} on YouTube"
                kit.playonyt(song)
            else:
                response = "What song would you like to play?"
            self.engine.speak(response)
            return response
            
        # System commands
        elif 'screenshot' in text:
            response = "Taking screenshot"
            self.engine.speak(response)
            # Add screenshot functionality here
            return response
            
        # Weather (requires API key)
        elif 'weather' in text:
            response = "Weather feature coming soon!"
            self.engine.speak(response)
            return response
            
        # Default response
        else:
            response = "I'm not sure how to help with that. You can ask me about time, date, or to search Google or YouTube."
            self.engine.speak(response)
            return response

# ================= INTERNET CHECK =================
def check_internet():
    try:
        requests.get("http://www.google.com", timeout=3)
        return True
    except:
        return False

# ================= MAIN APPLICATION =================
class NovaAssistant:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("NOVA - Advanced AI Voice Assistant")
        self.root.geometry("1200x700")
        self.root.configure(bg="#0a0a0f")
        
        # Initialize components
        self.voice_engine = VoiceEngine()
        self.command_processor = CommandProcessor(self.voice_engine, self.update_ui)
        
        # Variables
        self.current_mode = tk.StringVar(value="Voice Command")
        self.status = tk.StringVar(value="✨ Ready")
        self.is_recording = False
        self.message_queue = queue.Queue()
        
        # Setup UI
        self.setup_ui()
        self.process_queue()
        
    def update_ui(self, message, status=None):
        """Thread-safe UI updates"""
        self.message_queue.put(('update', message, status))
        
    def process_queue(self):
        """Process UI update queue"""
        try:
            while True:
                msg_type, message, status = self.message_queue.get_nowait()
                if msg_type == 'update':
                    self.output.insert(tk.END, f"\n> {message}")
                    self.output.see(tk.END)
                    if status:
                        self.status.set(status)
        except queue.Empty:
            pass
        finally:
            self.root.after(100, self.process_queue)
    
    def setup_ui(self):
        # Modern color scheme
        colors = {
            'bg': '#0a0a0f',
            'sidebar': '#111117',
            'accent': '#7c3aed',
            'accent_light': '#8b5cf6',
            'text': '#ffffff',
            'text_secondary': '#a0a0b0',
            'success': '#10b981',
            'error': '#ef4444'
        }
        
        # ================= SIDEBAR =================
        sidebar = tk.Frame(self.root, bg=colors['sidebar'], width=300)
        sidebar.pack(side=tk.LEFT, fill=tk.Y)
        sidebar.pack_propagate(False)
        
        # Logo and branding
        logo_frame = tk.Frame(sidebar, bg=colors['sidebar'])
        logo_frame.pack(pady=40)
        
        logo_label = tk.Label(logo_frame, text="NOVA", 
                              font=("Helvetica", 36, "bold"),
                              fg=colors['accent'], bg=colors['sidebar'])
        logo_label.pack()
        
        subtitle = tk.Label(logo_frame, text="Advanced AI Voice Assistant",
                           font=("Helvetica", 11),
                           fg=colors['text_secondary'], bg=colors['sidebar'])
        subtitle.pack(pady=5)
        
        # Mode selection with custom styling
        modes_frame = tk.Frame(sidebar, bg=colors['sidebar'])
        modes_frame.pack(pady=30, fill=tk.X, padx=20)
        
        modes_label = tk.Label(modes_frame, text="OPERATION MODE",
                              font=("Helvetica", 10, "bold"),
                              fg=colors['text_secondary'], bg=colors['sidebar'])
        modes_label.pack(anchor=tk.W, pady=(0, 10))
        
        modes = [
            ("🎤 Voice Command", "Voice Command"),
            ("📝 Speech to Text", "Speech to Text"),
            ("🔊 Text to Speech", "Text to Speech")
        ]
        
        for display_text, mode_value in modes:
            rb = tk.Radiobutton(modes_frame, text=display_text,
                               variable=self.current_mode, value=mode_value,
                               command=self.on_mode_change,
                               bg=colors['sidebar'], fg=colors['text'],
                               selectcolor=colors['sidebar'],
                               activebackground=colors['sidebar'],
                               activeforeground=colors['accent'],
                               font=("Helvetica", 11))
            rb.pack(anchor=tk.W, pady=8)
        
        # Status indicator
        status_frame = tk.Frame(sidebar, bg=colors['sidebar'])
        status_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=20, pady=20)
        
        tk.Label(status_frame, text="SYSTEM STATUS",
                font=("Helvetica", 10, "bold"),
                fg=colors['text_secondary'], bg=colors['sidebar']).pack(anchor=tk.W)
        
        self.status_indicator = tk.Canvas(status_frame, width=12, height=12,
                                         bg=colors['sidebar'], highlightthickness=0)
        self.status_indicator.pack(side=tk.LEFT, pady=10)
        self.indicator = self.status_indicator.create_oval(2, 2, 10, 10,
                                                          fill=colors['success'])
        
        self.status_label = tk.Label(status_frame, textvariable=self.status,
                                     font=("Helvetica", 10),
                                     fg=colors['text'], bg=colors['sidebar'])
        self.status_label.pack(side=tk.LEFT, padx=10)
        
        # ================= MAIN CONTENT =================
        main = tk.Frame(self.root, bg=colors['bg'])
        main.pack(expand=True, fill=tk.BOTH, padx=40, pady=40)
        
        # Header with animation effect
        header_frame = tk.Frame(main, bg=colors['bg'])
        header_frame.pack(fill=tk.X, pady=(0, 30))
        
        header = tk.Label(header_frame, text="How can I help you today?",
                         font=("Helvetica", 28, "bold"),
                         fg=colors['text'], bg=colors['bg'])
        header.pack(side=tk.LEFT)
        
        # Input area with modern styling
        input_frame = tk.Frame(main, bg=colors['bg'])
        input_frame.pack(fill=tk.X, pady=20)
        
        self.input_box = tk.Entry(input_frame,
                                  font=("Helvetica", 14),
                                  bg=colors['sidebar'],
                                  fg=colors['text'],
                                  insertbackground=colors['accent'],
                                  relief=tk.FLAT,
                                  bd=10)
        self.input_box.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=10)
        self.input_box.bind("<Return>", lambda e: self.execute())
        
        # Action button with hover effect
        self.action_btn = tk.Button(input_frame,
                                    text="ACTIVATE",
                                    font=("Helvetica", 12, "bold"),
                                    bg=colors['accent'],
                                    fg=colors['text'],
                                    activebackground=colors['accent_light'],
                                    activeforeground=colors['text'],
                                    relief=tk.FLAT,
                                    cursor="hand2",
                                    command=self.execute)
        self.action_btn.pack(side=tk.RIGHT, padx=(10, 0), ipadx=20, ipady=10)
        
        # Output area with scroll
        output_frame = tk.Frame(main, bg=colors['bg'])
        output_frame.pack(fill=tk.BOTH, expand=True, pady=20)
        
        # Custom styled scrolled text
        self.output = scrolledtext.ScrolledText(output_frame,
                                               font=("Consolas", 12),
                                               bg=colors['sidebar'],
                                               fg=colors['text'],
                                               insertbackground=colors['accent'],
                                               relief=tk.FLAT,
                                               height=15)
        self.output.pack(fill=tk.BOTH, expand=True)
        
        # Configure text tags for styling
        self.output.tag_config("user", foreground=colors['accent'])
        self.output.tag_config("assistant", foreground=colors['success'])
        self.output.tag_config("error", foreground=colors['error'])
        
        # Quick actions bar
        actions_frame = tk.Frame(main, bg=colors['bg'])
        actions_frame.pack(fill=tk.X, pady=10)
        
        quick_actions = [
            ("🎵 Play Music", lambda: self.quick_command("play music")),
            ("⏰ Time", lambda: self.quick_command("time")),
            ("📅 Date", lambda: self.quick_command("date")),
            ("🌐 YouTube", lambda: self.quick_command("open youtube")),
            ("🔍 Google", lambda: self.quick_command("google search"))
        ]
        
        for text, command in quick_actions:
            btn = tk.Button(actions_frame, text=text,
                          font=("Helvetica", 10),
                          bg=colors['sidebar'],
                          fg=colors['text'],
                          activebackground=colors['accent'],
                          activeforeground=colors['text'],
                          relief=tk.FLAT,
                          cursor="hand2",
                          command=command)
            btn.pack(side=tk.LEFT, padx=5, ipadx=10, ipady=5)
    
    def quick_command(self, command):
        self.input_box.delete(0, tk.END)
        self.input_box.insert(0, command)
        self.execute()
    
    def on_mode_change(self):
        self.output.delete(1.0, tk.END)
        mode = self.current_mode.get()
        self.status.set(f"🔄 Mode set to {mode}")
        
        # Update placeholder text based on mode
        if mode == "Text to Speech":
            self.input_box.delete(0, tk.END)
            self.input_box.insert(0, "Type something to speak...")
        elif mode == "Speech to Text":
            self.input_box.delete(0, tk.END)
            self.input_box.insert(0, "Click ACTIVATE and start speaking...")
        elif mode == "Voice Command":
            self.input_box.delete(0, tk.END)
            self.input_box.insert(0, "Say a command (e.g., 'time', 'play music')...")
    
    def listen(self, process_command=False):
        """Enhanced speech recognition"""
        r = sr.Recognizer()
        r.energy_threshold = 3000
        r.dynamic_energy_threshold = True
        
        try:
            self.status.set("🎤 Listening... Speak now")
            with sr.Microphone() as source:
                r.adjust_for_ambient_noise(source, duration=0.5)
                audio = r.listen(source, timeout=5, phrase_time_limit=10)
            
            self.status.set("⏳ Processing speech...")
            text = r.recognize_google(audio)
            
            # Update UI
            self.root.after(0, lambda: self.output.insert(tk.END, f"\nYou: {text}", "user"))
            self.root.after(0, lambda: self.output.see(tk.END))
            
            if process_command:
                # Process as command
                response = self.command_processor.process(text)
                if response:
                    self.root.after(0, lambda: self.output.insert(tk.END, f"\nNOVA: {response}", "assistant"))
            else:
                # Just display the text
                self.root.after(0, lambda: self.status.set("✅ Speech converted successfully"))
                
        except sr.WaitTimeoutError:
            self.root.after(0, lambda: self.status.set("⏰ No speech detected"))
        except sr.UnknownValueError:
            self.root.after(0, lambda: self.status.set("❌ Could not understand audio"))
        except sr.RequestError:
            self.root.after(0, lambda: self.status.set("🌐 Check internet connection"))
        except Exception as e:
            self.root.after(0, lambda: self.status.set(f"❌ Error: {str(e)[:30]}..."))
    
    def execute(self):
        """Execute based on current mode"""
        mode = self.current_mode.get()
        
        if mode == "Text to Speech":
            text = self.input_box.get().strip()
            if text and text != "Type something to speak...":
                self.output.insert(tk.END, f"\nYou: {text}", "user")
                self.status.set("🔊 Speaking...")
                
                def speak_thread():
                    self.voice_engine.speak(text)
                    self.root.after(0, lambda: self.status.set("✅ Finished speaking"))
                
                threading.Thread(target=speak_thread, daemon=True).start()
                self.input_box.delete(0, tk.END)
                
        elif mode == "Speech to Text":
            threading.Thread(target=self.listen, args=(False,), daemon=True).start()
            
        elif mode == "Voice Command":
            threading.Thread(target=self.listen, args=(True,), daemon=True).start()
    
    def run(self):
        self.root.mainloop()

# ================= MAIN =================
if __name__ == "__main__":
    # Install required packages if not present
    try:
        import pywhatkit
        import wikipedia
        import pygame
        from gtts import gTTS
    except ImportError:
        print("Installing required packages...")
        os.system("pip install pywhatkit wikipedia pygame gtts")
        print("Please restart the application")
        exit()
    
    # Create and run application
    app = NovaAssistant()
    app.run()