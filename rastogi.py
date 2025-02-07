import win32com.client
import webbrowser
import datetime
import wikipedia
import sys
import speech_recognition as sr
from transformers import BlenderbotTokenizer, BlenderbotForConditionalGeneration
import streamlit as st
# Wikipedia search function
def wiki(query):
    global result
    try:
        result = wikipedia.summary(query, sentences=2)
        st.write(result)
        say(result)
    except wikipedia.exceptions.DisambiguationError:
        st.write("The query is ambiguous. Please be more specific.")
        say("The query is ambiguous. Please be more specific.")
    except wikipedia.exceptions.PageError:
        st.write("Page doesn't exist.")
        say("Page doesn't exist.")
    except Exception as e:
        st.write("An error occurred while searching Wikipedia.")
        say("An error occurred while searching Wikipedia.")

# Text-to-Speech setup
speaker = win32com.client.Dispatch("SAPI.SpVoice")

def say(s):
    speaker.Speak(s)

# Speech Recognition setup
recognizer = sr.Recognizer()

def takeCommand():
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source, duration=1)
        print("Listening...")
        st.write("Listening...")
        try:
            audio = recognizer.listen(source, timeout=5)
            query = recognizer.recognize_google(audio, language='en-in')
            print(f"You said: {query}")
            st.write(f"You said: {query}")
            return query
        except sr.UnknownValueError:
            print("Sorry, I didn't understand.")
            st.write("Sorry, I didn't understand.")
            return None
        except sr.RequestError as e:
            print(f"Could not request results; {e}")
            st.write("Sorry, I didn't understand.")
            return None
        except sr.exceptions.WaitTimeoutError as e:
            print(f"Could not request results; {e}")
            st.write("Sorry, I didn't understand.")
            takeCommand()
            return None


# Initialize Chatbot Model
model_name = "facebook/blenderbot-400M-distill"
tokenizer = BlenderbotTokenizer.from_pretrained(model_name)
model = BlenderbotForConditionalGeneration.from_pretrained(model_name)

# Function for chatbot's response
def chatbot_response(text):
    inputs = tokenizer(text, return_tensors="pt")
    reply_ids = model.generate(**inputs)
    return tokenizer.decode(reply_ids[0], skip_special_tokens=True)

if __name__ == "__main__":
    st.title("Rastogi-V1 powered by Blenderbot")
    print("Hello ji, Rastogi here. How can I help you ji?")
    st.write("Hello ji, Rastogi here. How can I help you ji?")
    say("Hello ji, Rastogi here. How can I help you ji?")

    while True:
        query = takeCommand()
        if query is None:
            continue
        say(query)

        # Custom Commands
        if "rastogi play my favourite song" in query.lower():
            st.write("I got you. Playing Shaktimaan title track.")
            say("I got you. Playing Shaktimaan title track.")
            webbrowser.open("https://youtu.be/J4gJNVdu8to?feature=shared")
        elif "rastogi cook something changa" in query.lower():
            st.write("I got you sir.")
            say("I got you, sir.")
            webbrowser.open("https://open.spotify.com/track/7iW9pTNgp2HtlRJinoYuiA?si=4604e97e0f6c4e6c")
        elif "rastogi play something changa" in query.lower():
            st.write("I got you sir.")
            say("I got you, sir.")
            webbrowser.open("https://open.spotify.com/track/7iW9pTNgp2HtlRJinoYuiA?si=4604e97e0f6c4e6c")

        # Opening websites based on voice command
        sites = [
            ["youtube", "https://www.youtube.com/"],
            ["spotify", "https://open.spotify.com/playlist/6rfZGZHrbD7HWtR2GBCnJF"],
            ["meet", "https://meet.google.com/landing?pli=1"],
            ["gpt", "https://chatgpt.com"]
        ]
        for site in sites:
            if f"open {site[0]}" in query.lower():
                say(f"Opening {site[0]}, sir.")
                st.write(f"Opening {site[0]}, sir.")
                webbrowser.open(site[1])

        # Time functionality
        if "the time" in query.lower():
            strfTime = datetime.datetime.now().strftime("%H:%M:%S")
            print(f"Bhai, the time is {strfTime}")
            st.write(f"Bhai, the time is {strfTime}")
            say(f"Bhai, the time is {strfTime}")

        # Wikipedia search functionality
        if "wiki" in query.lower():
            search_query = query.replace("wiki", "").replace("wikipedia", "").strip()
            st.write(f"Searching Wikipedia: {search_query}")
            print(f"Searching Wikipedia for {search_query}")
            say(f"Searching Wikipedia for {search_query}")
            wiki(search_query)

        # Quit functionality
        if "quit" in query.lower():
            say("Goodbye!")
            print("Goodbye!")
            st.write("Goodbye!")
            sys.exit()

        # "Talk to me" mode
        if "rastogi talk to me" in query.lower():
            st.write("Rastogi: Let's talk, say 'exit' to stop.")
            say("Sure! Let's talk. Say 'exit' to stop.")
            st.write("Connecting to blenderbot...")
            say("Connecting to blenderbot...")
            print("Rastogi: Let's chat, say 'exit' to stop.")

            while True:
                user_input = takeCommand()
                if user_input is None:
                    continue
                if user_input.lower() in ["exit", "quit"]:
                    print("Rastogi: Goodbye!")
                    st.write("Rastogi: Goodbye!")
                    say("Goodbye!")
                    break

                # Generate AI response
                bot_reply = chatbot_response(user_input)
                print(f"Rastogi: {bot_reply}")
                st.write(f"Rastogi: {bot_reply}")
                say(bot_reply)

        else:
            print(f"what i heard: {query}")
            st.write(f"what i heard: {query}")
            say(f"what i heard: {query}")
