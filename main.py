import customtkinter as ctk
import threading
import webbrowser
import speech_recognition as sr
import pyttsx3

# Initialize modules
recognizer = sr.Recognizer()
engine = pyttsx3.init()
listening = False

# Text-to-speech
def speak(text):
    engine.say(text)
    engine.runAndWait()
    update_text_area(f"Jarvis: {text}")

# Voice recognition
def listen():
    with sr.Microphone() as source:
        status_label.configure(text="🎙️ Listening...", text_color="green")
        try:
            audio = recognizer.listen(source)
            command = recognizer.recognize_google(audio).lower()
            update_text_area(f"You: {command}")
            return command
        except sr.UnknownValueError:
            update_text_area("Jarvis: Sorry, I couldn't understand that.")
            return ""
        except sr.RequestError:
            update_text_area("Jarvis: Network error.")
            return ""

# Command execution
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

    elif "play music" in command:
        speak("Which song do you want to play?")
        song = listen().strip().lower()
        music_lower = {key.lower(): value for key, value in music.music.items()}
        if song in music_lower:
            speak(f"Playing {song}")
            webbrowser.open(music_lower[song])
        else:
            speak("Sorry, I don't have that song in my library.")

    elif "exit" in command or "stop" in command:
        speak("Goodbye!")
        stop_listening()
        app.quit()

    else:
        speak("Sorry, I don't understand that command.")

# Update text area in GUI
def update_text_area(text):
    output_textbox.configure(state="normal")
    output_textbox.insert("end", text + "\n")
    output_textbox.see("end")
    output_textbox.configure(state="disabled")

# Background loop for voice assistant
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

# Start and Stop functions
def start_listening():
    global listening
    listening = True
    update_text_area("Jarvis started.")
    threading.Thread(target=assistant_loop, daemon=True).start()
    status_label.configure(text="🎙️ Listening...", text_color="green")

def stop_listening():
    global listening
    listening = False
    status_label.configure(text="Jarvis has been stopped.", text_color="red")
    update_text_area("Jarvis stopped.")

# GUI Setup
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("Jarvis Voice Assistant")
app.geometry("500x450")

title_label = ctk.CTkLabel(app, text="🤖 Jarvis", font=ctk.CTkFont(size=24, weight="bold"))
title_label.pack(pady=10)

status_label = ctk.CTkLabel(app, text="Click 'Start Listening' to begin.", font=ctk.CTkFont(size=16))
status_label.pack(pady=5)

output_textbox = ctk.CTkTextbox(app, height=200, width=460, corner_radius=8)
output_textbox.pack(padx=10, pady=10)
output_textbox.configure(state="disabled")

start_btn = ctk.CTkButton(app, text="Start Listening", command=start_listening, fg_color="green", hover_color="#0f0")
start_btn.pack(pady=5)

stop_btn = ctk.CTkButton(app, text="Stop / Exit", command=stop_listening, fg_color="red", hover_color="#f00")
stop_btn.pack(pady=5)

app.mainloop()
