import speech_recognition as sr
import os
import re

def fix_speech_to_filename(words):
    """
    Converts a list of words from speech recognition into a valid filename.
    - Replaces "dot" with "." only when it's between words.
    """
    corrected_words = []
    
    for i in range(len(words)):
        if words[i] == "dot" and i > 0 and i < len(words) - 1:
            corrected_words.append(".")  # Convert "dot" to "."
        else:
            corrected_words.append(words[i])

    return "".join(corrected_words)  # Join without spaces to form a filename

def clean_command(command):
    """ Fix common misinterpretations in speech recognition """
    command = command.lower()  # Convert to lowercase
    command = command.replace(" folder ", " older ")  # Fix "folder" → "older" issue
    return command

def rename_file_from_voice_command(command):
    command = clean_command(command)
    words = command.split()

    if "rename" in words and "to" in words:
        try:
            rename_index = words.index("rename")
            to_index = words.index("to")
            
            if rename_index + 1 < to_index and to_index + 1 < len(words):
                old_name = fix_speech_to_filename(words[rename_index + 1:to_index])  # Process old filename
                new_name = fix_speech_to_filename(words[to_index + 1:])  # Process new filename
                
                os.rename(old_name, new_name)
                print(f"File renamed from {old_name} to {new_name}")
            else:
                print("Invalid command format. Please say: 'Rename [old_filename] to [new_filename]'.")
        except Exception as e:
            print(f"Error: {e}")
    else:
        print("Invalid command format. Please say: 'Rename [old_filename] to [new_filename]'.")

def listen_for_command():
    recognizer = sr.Recognizer()
    
    try:
        with sr.Microphone() as source:
            recognizer.adjust_for_ambient_noise(source)
            print("Listening for command to rename a file...")
            audio = recognizer.listen(source)

        command = recognizer.recognize_google(audio)
        print(f"Command received: {command}")
        rename_file_from_voice_command(command)

    except sr.UnknownValueError:
        print("Sorry, I couldn't understand the command.")
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")
    except Exception as e:
        print(f"Microphone error: {e}")

if __name__ == "__main__":
    listen_for_command()

