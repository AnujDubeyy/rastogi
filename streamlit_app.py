import webbrowser
import datetime
import wikipedia
import streamlit as st
from transformers import BlenderbotTokenizer, BlenderbotForConditionalGeneration

# Initialize Chatbot Model
model_name = "facebook/blenderbot-400M-distill"
tokenizer = BlenderbotTokenizer.from_pretrained(model_name)
model = BlenderbotForConditionalGeneration.from_pretrained(model_name)

def chatbot_response(text):
    inputs = tokenizer(text, return_tensors="pt")
    reply_ids = model.generate(**inputs)
    return tokenizer.decode(reply_ids[0], skip_special_tokens=True)

def wiki_search(query):
    try:
        result = wikipedia.summary(query, sentences=2)
        return result
    except wikipedia.exceptions.DisambiguationError:
        return "The query is ambiguous. Please be more specific."
    except wikipedia.exceptions.PageError:
        return "Page doesn't exist."
    except Exception:
        return "An error occurred while searching Wikipedia."

st.title("Rastogi-V1 Chatbot")
st.write("Hello ji, Rastogi here. How can I help you ji?")

query = st.text_input("Enter your command or message:")

if st.button("Submit"):
    if query:
        if "open youtube" in query.lower():
            st.write("Opening YouTube...")
            webbrowser.open("https://www.youtube.com/")
        elif "open spotify" in query.lower():
            st.write("Opening Spotify...")
            webbrowser.open("https://open.spotify.com/")
        elif "the time" in query.lower():
            strfTime = datetime.datetime.now().strftime("%H:%M:%S")
            st.write(f"Bhai, the time is {strfTime}")
        elif "wiki" in query.lower():
            search_query = query.replace("wiki", "").replace("wikipedia", "").strip()
            st.write(f"Searching Wikipedia for: {search_query}")
            result = wiki_search(search_query)
            st.write(result)
        elif "talk to me" in query.lower():
            st.write("Sure! Let's chat. Type 'exit' to stop.")
            user_input = ""
            while user_input.lower() not in ["exit", "quit"]:
                user_input = st.text_input("You:")
                if user_input.lower() in ["exit", "quit"]:
                    st.write("Goodbye!")
                    break
                bot_reply = chatbot_response(user_input)
                st.write(f"Rastogi: {bot_reply}")
        elif "quit" in query.lower() or "exit" in query.lower():
            st.write("Goodbye!")
        else:
            bot_reply = chatbot_response(query)
            st.write(f"Rastogi: {bot_reply}")
