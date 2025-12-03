"""
JARVIS ELITE - Multi-Agent Voice Assistant
Fixed version with proper error handling and async support
"""

import speech_recognition as sr
import os
import webbrowser
import subprocess
import sys
import time
import asyncio
import platform
from dotenv import load_dotenv
from fastapi import FastAPI
from pydantic import BaseModel

# Import agents
from agents import planner, executor, ai_agent, parallel_run
from evaluation import run_evaluation

# ================= PLATFORM DETECTION =================

IS_WINDOWS = platform.system() == "Windows"
IS_MAC = platform.system() == "Darwin"
IS_LINUX = platform.system() == "Linux"
 
# Windows-specific imports
WINDOWS_FEATURES = False
if IS_WINDOWS:
    try:
        import win32com.client
        import pyautogui
        pyautogui.FAILSAFE = False
        WINDOWS_FEATURES = True
        print("✓ Windows automation features enabled")
    except ImportError:
        print("⚠️  Windows automation unavailable (install: pip install pywin32 pyautogui)")

load_dotenv()

# ================= FASTAPI SERVER =================

app = FastAPI(title="Jarvis Elite Multi-Agent Assistant")

class Query(BaseModel):
    query: str

@app.post("/ask")
async def ask(data: Query):
    """Handle API requests"""
    try:
        exec_output, ai_text = await parallel_run(data.query)
        result = {"response": ai_text}
        if exec_output:
            result["executor"] = exec_output
        return result
    except Exception as e:
        return {"error": str(e)}

@app.get("/")
def home():
    return {"status": "Jarvis Elite is running", "platform": platform.system()}

@app.get("/evaluate")
def evaluate():
    return run_evaluation()

@app.get("/health")
def health():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "platform": platform.system(),
        "windows_features": WINDOWS_FEATURES
    }

# ================= CONFIGURATION =================

WAKE_WORDS = ["hey jarvis", "ok jarvis", "wake up", "jarvis"]
EXIT_WORDS = ["exit", "goodbye", "shut down"]
GREETING = "Hello sir, how can I assist you?"

# Cross-platform application paths
ALLOWED_APPS = {
    "notepad": r"C:\Windows\System32\notepad.exe" if IS_WINDOWS else "open -a TextEdit" if IS_MAC else "gedit",
    "calculator": r"C:\Windows\System32\calc.exe" if IS_WINDOWS else "open -a Calculator" if IS_MAC else "gnome-calculator"
}

ALLOWED_WEBSITES = {
    "google": "https://www.google.com",
    "youtube": "https://www.youtube.com",
    "facebook": "https://www.facebook.com",
    "twitter": "https://www.twitter.com",
    "instagram": "https://www.instagram.com",
    "github": "https://www.github.com",
    "linkedin": "https://www.linkedin.com",
    "gmail": "https://mail.google.com",
    "amazon": "https://www.amazon.com",
    "netflix": "https://www.netflix.com",
    "stackoverflow": "https://stackoverflow.com",
    "chatgpt": "https://chat.openai.com",
    "reddit": "https://www.reddit.com"
}

# Cross-platform folders
FOLDERS = {
    "documents": os.path.expanduser("~/Documents"),
    "downloads": os.path.expanduser("~/Downloads"),
    "desktop": os.path.expanduser("~/Desktop"),
    "home": os.path.expanduser("~")
}

# ================= TEXT TO SPEECH =================

tts_engine = None
if WINDOWS_FEATURES:
    try:
        tts_engine = win32com.client.Dispatch("SAPI.SpVoice")
        print("✓ TTS engine initialized")
    except Exception as e:
        print(f"⚠️  TTS initialization failed: {e}")
        WINDOWS_FEATURES = False

# Global TTS control flags
GEMINI_MUTED = False
STOP_READING = False

def speak(text, is_gemini=False):
    """
    Text-to-speech with interrupt support
    """
    global GEMINI_MUTED, STOP_READING

    if not text or text.strip() == "":
        return

    print(f"\n🤖 Assistant: {text}")

    if not WINDOWS_FEATURES or not tts_engine:
        return

    if is_gemini and GEMINI_MUTED:
        print("🔇 (Gemini muted)")
        return

    STOP_READING = False

    try:
        sentences = text.split(". ")
        for sentence in sentences:
            if STOP_READING:
                tts_engine.Skip("Sentence", 999999)
                print("⏹️  Speech interrupted")
                break
            
            if sentence.strip():
                tts_engine.Speak(sentence + ".")
    
    except Exception as e:
        print(f"TTS Error: {e}")

# ================= SPEECH RECOGNITION =================

def recognize_speech(recognizer, mic, timeout=6):
    """
    Recognize speech with error handling
    """
    try:
        with mic as source:
            recognizer.adjust_for_ambient_noise(source, duration=0.4)
            print("🎤 Listening...")
            audio = recognizer.listen(source, timeout=timeout, phrase_time_limit=8)
        
        text = recognizer.recognize_google(audio).lower()
        print(f"👤 You: {text}")
        return text
    
    except sr.WaitTimeoutError:
        print("⏱️  No speech detected")
        return ""
    
    except sr.UnknownValueError:
        print("❓ Could not understand audio")
        return ""
    
    except sr.RequestError as e:
        print(f"❌ Speech recognition error: {e}")
        return ""
    
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return ""

def detect_wake_word(text):
    """Check if wake word is present"""
    return any(word in text for word in WAKE_WORDS)

def detect_exit_word(text):
    """Check if exit word is present"""
    return any(word in text for word in EXIT_WORDS)

# ================= MEMORY =================

recent_searches = []

def add_recent_search(query):
    """Add search to history"""
    if query:
        recent_searches.append(query)
        if len(recent_searches) > 10:
            recent_searches.pop(0)

def show_recent_searches():
    """Display recent searches"""
    if not recent_searches:
        speak("No recent searches.")
        return

    speak("Here are your recent searches.")
    for i, query in enumerate(recent_searches[-5:], 1):
        speak(f"{i}. {query}")

# ================= AUTOMATION HELPERS =================

def safe_hotkey(*keys):
    """Execute hotkey safely"""
    if not WINDOWS_FEATURES:
        return
    try:
        import pyautogui
        pyautogui.hotkey(*keys)
        time.sleep(0.25)
    except Exception as e:
        print(f"Hotkey error: {e}")

def safe_type(text):
    """Type text safely"""
    if not WINDOWS_FEATURES:
        return
    try:
        import pyautogui
        pyautogui.typewrite(text, interval=0.03)
    except Exception as e:
        print(f"Type error: {e}")

def safe_click(x, y):
    """Click safely"""
    if not WINDOWS_FEATURES:
        return
    try:
        import pyautogui
        pyautogui.click(x, y)
    except Exception as e:
        print(f"Click error: {e}")

# ================= GOOGLE SEARCH =================

def perform_google_search(query):
    """Perform Google search"""
    try:
        search_url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
        webbrowser.open(search_url)
        add_recent_search(query)
        speak(f"Searching for {query}")
    except Exception as e:
        print(f"Search error: {e}")
        speak("Sorry, I couldn't perform the search.")

# ================= CONTROL MODES =================

def google_control_mode(recognizer, mic):
    """Google search voice control mode"""
    speak("Google mode activated. You can search multiple times. Say 'exit google' to leave.")

    while True:
        cmd = recognize_speech(recognizer, mic)

        if not cmd:
            continue

        if "exit google" in cmd or "stop google" in cmd:
            speak("Exiting Google mode.")
            break

        elif "search" in cmd or "search for" in cmd:
            query = cmd.replace("search for", "").replace("search", "").strip()
            if query:
                perform_google_search(query)
            else:
                speak("What would you like to search for?")

        elif "scroll down" in cmd:
            if WINDOWS_FEATURES:
                import pyautogui
                pyautogui.scroll(-700)
            speak("Scrolling down")

        elif "scroll up" in cmd:
            if WINDOWS_FEATURES:
                import pyautogui
                pyautogui.scroll(700)
            speak("Scrolling up")

        elif "go back" in cmd or "back" in cmd:
            safe_hotkey("alt", "left")
            speak("Going back")

        elif "forward" in cmd:
            safe_hotkey("alt", "right")
            speak("Going forward")

        elif "refresh" in cmd or "reload" in cmd:
            safe_hotkey("f5")
            speak("Refreshing page")

        elif "new tab" in cmd:
            safe_hotkey("ctrl", "t")
            speak("Opening new tab")

        elif "close tab" in cmd:
            safe_hotkey("ctrl", "w")
            speak("Closing tab")

def youtube_control_mode(recognizer, mic):
    """YouTube voice control mode"""
    speak("YouTube control mode activated. Say 'exit youtube' to leave.")

    while True:
        cmd = recognize_speech(recognizer, mic)

        if not cmd:
            continue

        if "exit youtube" in cmd or "stop youtube" in cmd:
            speak("Exiting YouTube mode.")
            break

        elif "pause" in cmd or "resume" in cmd or "play" in cmd:
            safe_hotkey("k")

        elif "next video" in cmd or "skip" in cmd:
            safe_hotkey("shift", "n")

        elif "previous video" in cmd:
            safe_hotkey("shift", "p")

        elif "scroll down" in cmd:
            if WINDOWS_FEATURES:
                import pyautogui
                pyautogui.scroll(-700)
            speak("Scrolling down")

        elif "scroll up" in cmd:
            if WINDOWS_FEATURES:
                import pyautogui
                pyautogui.scroll(700)
            speak("Scrolling up")

        elif "full screen" in cmd:
            safe_hotkey("f")

def whatsapp_control_mode(recognizer, mic):
    """WhatsApp voice control mode"""
    speak("WhatsApp mode activated. Say 'exit whatsapp' to leave.")

    while True:
        cmd = recognize_speech(recognizer, mic)

        if not cmd:
            continue

        if "exit whatsapp" in cmd or "stop whatsapp" in cmd:
            speak("Leaving WhatsApp mode.")
            break

        elif "search" in cmd:
            name = cmd.replace("search", "").strip()
            speak(f"Searching for {name}")
            safe_hotkey("ctrl", "f")
            time.sleep(0.3)
            safe_type(name)
            time.sleep(0.5)
            if WINDOWS_FEATURES:
                import pyautogui
                pyautogui.press("enter")

        elif "message" in cmd or "send" in cmd:
            msg = cmd.replace("message", "").replace("send", "").strip()
            speak("Sending message.")
            safe_type(msg)
            if WINDOWS_FEATURES:
                import pyautogui
                pyautogui.press("enter")

# ================= APPLICATION LAUNCH =================

def open_whatsapp():
    """Open WhatsApp application"""
    if not IS_WINDOWS:
        speak("WhatsApp opening is only supported on Windows.")
        return False
    
    try:
        # Try desktop app first
        exe_path = os.path.expandvars(r"C:\Users\%USERNAME%\AppData\Local\WhatsApp\WhatsApp.exe")
        if os.path.exists(exe_path):
            subprocess.Popen(exe_path)
            return True
        
        # Try Microsoft Store version
        uwp_cmd = r"explorer.exe shell:appsFolder\5319275A.WhatsAppDesktop_cv1g1gvanyjgm!App"
        subprocess.Popen(uwp_cmd, shell=True)
        return True
    
    except Exception as e:
        print(f"WhatsApp open error: {e}")
        speak("Unable to open WhatsApp.")
        return False

def open_application(cmd, recognizer=None, mic=None):
    """Open applications or websites"""
    
    # WhatsApp
    if "whatsapp" in cmd:
        if open_whatsapp():
            time.sleep(5)
            if recognizer and mic:
                whatsapp_control_mode(recognizer, mic)
        return

    # Desktop applications
    for app, path in ALLOWED_APPS.items():
        if app in cmd:
            try:
                if IS_WINDOWS:
                    subprocess.Popen(path)
                else:
                    os.system(path)
                speak(f"Opening {app}")
            except Exception as e:
                print(f"App open error: {e}")
                speak(f"Sorry, I couldn't open {app}")
            return

    # Websites
    for site, url in ALLOWED_WEBSITES.items():
        if site in cmd:
            try:
                webbrowser.open(url)
                speak(f"Opening {site}")
                time.sleep(3)

                # Special control modes
                if site == "youtube" and recognizer and mic:
                    youtube_control_mode(recognizer, mic)
                elif site == "google" and recognizer and mic:
                    google_control_mode(recognizer, mic)
                
            except Exception as e:
                print(f"Website open error: {e}")
                speak(f"Sorry, I couldn't open {site}")
            return

    # Folders
    for name, path in FOLDERS.items():
        if name in cmd and os.path.exists(path):
            try:
                if IS_WINDOWS:
                    os.startfile(path)
                elif IS_MAC:
                    os.system(f"open '{path}'")
                else:
                    os.system(f"xdg-open '{path}'")
                speak(f"Opening {name} folder.")
            except Exception as e:
                print(f"Folder open error: {e}")
            return

# ================= AI RESPONSE =================

def respond_to_conversation(cmd):
    """Get AI response with async support"""
    try:
        exec_result, ai_text = asyncio.run(parallel_run(cmd))
        
        if exec_result:
            speak(exec_result)
        
        speak(ai_text, is_gemini=True)
    
    except Exception as e:
        print(f"AI response error: {e}")
        speak("Sorry, I encountered an error processing your request.")

# ================= MAIN LOOP =================

def main_loop():
    """Main voice assistant loop"""
    global GEMINI_MUTED, STOP_READING

    print("\n" + "="*60)
    print("🤖 JARVIS ELITE - Multi-Agent Voice Assistant")
    print("="*60)
    print(f"Platform: {platform.system()}")
    print(f"Windows Features: {'Enabled' if WINDOWS_FEATURES else 'Disabled'}")
    print("="*60 + "\n")

    recognizer = sr.Recognizer()
    
    # Try to get microphone
    try:
        mic = sr.Microphone()
        print("✓ Microphone initialized")
    except Exception as e:
        print(f"❌ Microphone error: {e}")
        print("Please check your microphone connection.")
        return

    speak("Jarvis Elite activated.")
    speak("Say a wake word to begin.")

    try:
        while True:
            # Wait for wake word
            wake = recognize_speech(recognizer, mic, timeout=10)
            
            if not wake:
                continue
            
            if not detect_wake_word(wake):
                continue

            speak(GREETING)

            # Active listening mode
            while True:
                cmd = recognize_speech(recognizer, mic)

                if not cmd:
                    continue

                # ========== GLOBAL CONTROLS ==========

                if detect_exit_word(cmd):
                    STOP_READING = True
                    if tts_engine:
                        tts_engine.Skip("Sentence", 999999)
                    speak("Goodbye sir. Shutting down.")
                    return

                elif "stop reading" in cmd or "stop talking" in cmd:
                    STOP_READING = True
                    if tts_engine:
                        tts_engine.Skip("Sentence", 999999)
                    print("⏹️  Stopped reading")

                elif "mute gemini" in cmd or "mute ai" in cmd:
                    GEMINI_MUTED = True
                    speak("Gemini responses muted.")

                elif "unmute gemini" in cmd or "unmute ai" in cmd:
                    GEMINI_MUTED = False
                    speak("Gemini responses unmuted.")

                # ========== SEARCH ==========

                elif "recent searches" in cmd or "search history" in cmd:
                    show_recent_searches()

                elif "google search" in cmd or "search for" in cmd:
                    query = cmd.replace("google search", "").replace("search for", "").strip()
                    if query:
                        perform_google_search(query)

                # ========== APPLICATION CONTROL ==========

                elif "open" in cmd:
                    open_application(cmd, recognizer, mic)

                # ========== SLEEP MODE ==========

                elif "sleep" in cmd or "go to sleep" in cmd:
                    speak("Going to sleep. Say a wake word to wake me up.")
                    break

                # ========== DEFAULT AI ==========

                else:
                    respond_to_conversation(cmd)

    except KeyboardInterrupt:
        print("\n\n⚠️  Interrupted by user")
        speak("Shutting down.")
    
    except Exception as e:
        print(f"\n\n❌ Fatal error: {e}")
        import traceback
        traceback.print_exc()
        speak("A critical error occurred. Shutting down.")

# ================= START =================

if __name__ == "__main__":
    try:
        main_loop()
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
    except Exception as e:
        print(f"\n❌ Fatal error: {e}")
        import traceback
        traceback.print_exc()