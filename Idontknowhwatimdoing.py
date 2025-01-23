import time
import random
import speech_recognition as sr
import pyttsx3
import spacy
from textblob import TextBlob

# Load the English language model from spaCy
nlp = spacy.load('en_core_web_sm')

# Initialize text-to-speech engine
engine = pyttsx3.init()

# IELTS Speaking Test Parts (simplified)
part_1_questions = [
    "Can you tell me your full name, please?",
    "Where are you from?",
    "What do you do? Do you work or are you a student?",
    "What are your hobbies?",
    "Do you enjoy traveling?"
]
part_2_prompt = "Describe a place you have visited that you would like to go back to. You should say: where it is, why you went there, what you did there, and why you want to go back."

part_3_questions = [
    "What are the benefits of traveling abroad?",
    "How do you think tourism affects the local economy?",
    "Do you think international tourism has a positive or negative impact on culture?",
    "What are some ways countries can improve their tourism industry?"
]


# Timer Function
def timer(seconds):
    for i in range(seconds, 0, -1):
        print(f"Time remaining: {i} seconds")
        time.sleep(1)
    print("Time's up!")


# Function to give feedback based on text analysis
def assess_response(response):
    doc = nlp(response)
    blob = TextBlob(response)

    # Analyze fluency: Check the number of sentences
    sentence_count = len(blob.sentences)
    fluency_score = min(sentence_count, 5)

    # Analyze grammar: Check for simple grammatical errors using TextBlob
    grammar_score = 0
    for sentence in blob.sentences:
        if sentence.correct() != sentence:
            grammar_score += 1

    # Vocabulary: Check for word complexity
    vocabulary_score = len(set(doc))  # Unique words
    vocabulary_score = min(vocabulary_score, 5)

    # Simple pronunciation analysis (based on fluency and text quality for now)
    pronunciation_score = fluency_score

    # Provide feedback based on these metrics
    feedback = f"Fluency: {fluency_score}/5\nGrammar: {5 - grammar_score}/5\nVocabulary: {vocabulary_score}/5\nPronunciation: {pronunciation_score}/5"
    return feedback


# Speech recognition function to capture spoken responses
def listen_to_speech(prompt):
    # Initialize recognizer
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print(prompt)
        audio = recognizer.listen(source)

    try:
        print("Processing your response...")
        response = recognizer.recognize_google(audio)
        print(f"You said: {response}")
        return response
    except sr.UnknownValueError:
        print("Sorry, I could not understand your speech. Please try again.")
        return listen_to_speech(prompt)
    except sr.RequestError:
        print("Error with the speech recognition service.")
        return None


# Simulate Part 1
def part_1():
    print("Part 1: Introduction and Interview\n")
    for question in part_1_questions:
        print(question)
        response = listen_to_speech("Please speak your response.")
        feedback = assess_response(response)
        print(f"Feedback: \n{feedback}\n")


# Simulate Part 2 (Long Turn)
def part_2():
    print("Part 2: Long Turn\n")
    print(f"Your topic: {part_2_prompt}")
    print("You have 1 minute to prepare. Please use the time wisely.")
    timer(60)
    print("Now, speak for 1-2 minutes on the topic.")
    response = listen_to_speech("Please speak your response.")
    feedback = assess_response(response)
    print(f"Feedback: \n{feedback}\n")
    timer(120)


# Simulate Part 3 (Discussion)
def part_3():
    print("Part 3: Discussion\n")
    print("Let's discuss some more complex questions related to your topic.")
    for question in random.sample(part_3_questions, len(part_3_questions)):
        print(question)
        response = listen_to_speech("Please speak your response.")
        feedback = assess_response(response)
        print(f"Feedback: \n{feedback}\n")


# Main function to start the simulation
def start_test():
    print("Welcome to the IELTS Speaking Test Simulation!")
    input("Press Enter to start the test.")

    part_1()
    input("Press Enter to proceed to Part 2.")
    part_2()
    input("Press Enter to proceed to Part 3.")
    part_3()

    print("Test complete! Thank you for participating.")


if __name__ == "__main__":
    start_test()