import pyttsx3
import speech_recognition as sr
import time
import os
from gtts import gTTS

def text_to_speech_mac(text, rate=150, volume=1.0, save_file=False, lang='en'):
    """
    Converts text to speech with customizable parameters.

    Parameters:
    - text: The text to convert to speech.
    - rate: Speech rate (words per minute).
    - volume: Volume level (0.0 to 1.0).
    - save_file: Save the speech to an audio file if True.
    - lang: Language for speech (default 'en' for English).
    """
    engine = pyttsx3.init()
    engine.setProperty('rate', rate)   # Speed of speech
    engine.setProperty('volume', volume)  # Volume level (0.0 to 1.0)
    
    if save_file:
        # Save the speech to a file using gTTS (Google Text-to-Speech)
        tts = gTTS(text, lang=lang)
        filename = "speech_output.mp3"
        tts.save(filename)
        print(f"Audio saved as {filename}")
        os.system(f"start {filename}")  # Plays the saved audio file
    else:
        engine.say(text)
        engine.runAndWait()

def speech_to_text_mac(language='en-US', timeout=30, phrase_time_limit=30):
    """
    Converts speech to text using Google Speech API.
    
    Parameters:
    - language: The language code for recognition (default 'en-US' for English).
    - timeout: Time to wait for speech input (in seconds).
    - phrase_time_limit: Time limit for recording a single phrase.
    
    Returns:
    - The recognized speech as text or None if no speech is detected.
    """
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print(f"Listening for speech in {language}... (Timeout: {timeout}s, Phrase time limit: {phrase_time_limit}s)")
        try:
            recognizer.adjust_for_ambient_noise(source)  # Adjust for background noise
            # Listen for speech within the specified timeout and phrase time limit
            audio = recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
            text = recognizer.recognize_google(audio, language=language)
            print(f"You said: {text}")
            return text
        except sr.UnknownValueError:
            print("Sorry, I could not understand the audio.")
        except sr.RequestError as e:
            print(f"Could not request results; {e}")
        except sr.WaitTimeoutError:
            print("Listening timed out. No speech detected.")
        return None

def interactive_conversation():
    """
    An interactive conversation loop where the program listens to the user, converts speech to text, and
    provides text-to-speech feedback.
    """
    print("Starting interactive conversation...")
    while True:
        user_text = speech_to_text_mac()
        if user_text:
            print(f"You said: {user_text}")
            if "goodbye" in user_text.lower() or "quit" in user_text.lower():
                print("Goodbye!")
                text_to_speech_mac("Goodbye!", rate=130, volume=0.9)
                break
            elif "hello" in user_text.lower():
                text_to_speech_mac("Hello! How can I help you?", rate=150, volume=1.0)
            elif "what is your name" in user_text.lower():
                text_to_speech_mac("I am your assistant.", rate=150, volume=1.0)
            elif "be my boyfriend" in user_text.lower():
                text_to_speech_mac("shut the fuck up, you already have a very handsome boyfriend", rate=150, volume=1.0)
            else:
                text_to_speech_mac(f"You said: {user_text}", rate=150, volume=1.0)
        else:
            print("No input detected, trying again...")
            text_to_speech_mac("Sorry, I couldn't hear anything. Please try again.", rate=150, volume=1.0)

def save_audio_response(text, filename="response.mp3"):
    """
    Save the spoken response to a file.
    
    Parameters:
    - text: The text to convert to speech and save as an audio file.
    - filename: The name of the output audio file (default: 'response.mp3').
    """
    tts = gTTS(text)
    tts.save(filename)
    print(f"Audio response saved as {filename}")
    os.system(f"start {filename}")  # Play the saved file on Windows (use appropriate command on other OS)

def speech_recognition_demo():
    """
    Demonstrates the usage of speech recognition with speech-to-text and feedback using text-to-speech.
    """
    print("Welcome to the Speech Recognition Demo!")
    text_to_speech_mac("Welcome to the speech recognition demo! Please speak into the microphone.", rate=140, volume=1.0)
    
    user_input = speech_to_text_mac(language='en-US', timeout=10, phrase_time_limit=20)
    if user_input:
        print(f"Recognized Speech: {user_input}")
        text_to_speech_mac(f"You said: {user_input}", rate=150, volume=1.0)
    else:
        print("No speech recognized. Please try again.")
        text_to_speech_mac("No speech recognized. Please try again.", rate=150, volume=1.0)

if __name__ == "__main__":
    # Start an interactive conversation loop
    interactive_conversation()
    # Optionally, you can run speech recognition demos or other features
    # speech_recognition_demo()
