import customtkinter as ctk
import threading
import webbrowser
import speech_recognition as sr
import pyttsx3
import datetime
import wikipedia
import pyjokes

# Initialize
recognizer = sr.Recognizer()
engine = pyttsx3.init()
listening = False

# GUI Appearance
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# Speak Function
def speak(text):
    engine.say(text)
    engine.runAndWait()
    update_text_area(f"🤖 Jarvis: {text}")

# Listen Function
def listen():
    with sr.Microphone() as source:
        status_label.configure(text="🎙️ Listening...", text_color="green")
        try:
            audio = recognizer.listen(source)
            command = recognizer.recognize_google(audio).lower()
            update_text_area(f"🧑 You: {command}")
            return command
        except sr.UnknownValueError:
            update_text_area("🤖 Jarvis: Sorry, I couldn't understand that.")
            return ""
        except sr.RequestError:
            update_text_area("🤖 Jarvis: Network error.")
            return ""

# Command Execution
def execute_command(command):
    if "open google" in command:
        speak("Opening Google")
        webbrowser.open("https://www.google.com")

    elif "open linkedin" in command:
        speak("Opening LinkedIn")
        webbrowser.open("https://www.linkedin.com")

    elif "open facebook" in command:
        speak("Opening Facebook")
        webbrowser.open("https://www.facebook.com")

    elif "open instagram" in command:
        speak("Opening Instagram")
        webbrowser.open("https://www.instagram.com")

    elif "open youtube" in command:
        speak("Opening YouTube")
        webbrowser.open("https://www.youtube.com")

    elif "what's the time" in command or "what is the time" in command:
        now = datetime.datetime.now()
        speak(f"The current time is {now.strftime('%I:%M %p')}")

    elif "what's the date" in command or "what is the date" in command:
        today = datetime.date.today()
        speak(f"Today is {today.strftime('%B %d, %Y')}")

    elif "search wikipedia for" in command:
        topic = command.replace("search wikipedia for", "").strip()
        if topic:
            try:
                summary = wikipedia.summary(topic, sentences=2)
                speak(f"According to Wikipedia: {summary}")
            except wikipedia.exceptions.DisambiguationError:
                speak("There are multiple results, please be more specific.")
            except:
                speak("Sorry, I couldn’t fetch that from Wikipedia.")
        else:
            speak("What should I search on Wikipedia?")
            topic = listen()
            if topic:
                execute_command(f"search wikipedia for {topic}")

    elif "tell me a joke" in command:
        joke = pyjokes.get_joke()
        speak(joke)

    elif "exit" in command or "stop" in command:
        speak("Goodbye!")
        stop_listening()
        app.quit()
    else:
        speak("Sorry, I don't understand that command.")

def update_text_area(text):
    output_textbox.configure(state="normal")
    output_textbox.insert("end", text + "\n")
    output_textbox.see("end")
    output_textbox.configure(state="disabled")

# Voice Assistant Loop
def assistant_loop():
    global listening
    speak("Jarvis is ready.")
    while listening:
        command = listen()
        if "jarvis" in command:
            speak("Yes sir, how can I assist you?")
            while listening:
                user_command = listen()
                if "jarvis" in user_command:
                    speak("Yes sir?")
                    continue
                if user_command:
                    execute_command(user_command)

# Start/Stop Functions
def start_listening():
    global listening
    listening = True
    update_text_area("✅ Jarvis started.")
    threading.Thread(target=assistant_loop, daemon=True).start()
    status_label.configure(text="🎙️ Listening...", text_color="green")

def stop_listening():
    global listening
    listening = False
    status_label.configure(text="🔴 Jarvis has been stopped.", text_color="red")
    update_text_area("❌ Jarvis stopped.")

# GUI Setup
app = ctk.CTk()
app.title("🤖 Jarvis - Voice Assistant")
app.geometry("540x560")
app.resizable(False, False)

# Styling
title_label = ctk.CTkLabel(app, text="🤖 Jarvis Voice Assistant", font=ctk.CTkFont(size=26, weight="bold"))
title_label.pack(pady=10)

status_label = ctk.CTkLabel(app, text="Click 'Start Listening' to begin.", font=ctk.CTkFont(size=16))
status_label.pack(pady=5)

output_frame = ctk.CTkFrame(app, corner_radius=12)
output_frame.pack(padx=10, pady=10, fill="both", expand=True)

output_textbox = ctk.CTkTextbox(output_frame, height=280, width=500, corner_radius=10, wrap="word", font=("Consolas", 13))
output_textbox.pack(padx=10, pady=10, fill="both", expand=True)
output_textbox.configure(state="disabled")

btn_frame = ctk.CTkFrame(app, fg_color="transparent")
btn_frame.pack(pady=10)

start_btn = ctk.CTkButton(btn_frame, text="▶️ Start Listening", command=start_listening, fg_color="#22bb33", hover_color="#1eaa2a", width=180)
start_btn.grid(row=0, column=0, padx=10)

stop_btn = ctk.CTkButton(btn_frame, text="⛔ Stop / Exit", command=stop_listening, fg_color="#bb2222", hover_color="#aa1e1e", width=180)
stop_btn.grid(row=0, column=1, padx=10)

# Run App
app.mainloop()
