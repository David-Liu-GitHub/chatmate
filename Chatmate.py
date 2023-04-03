import os
import random
import openai
import time
import json


# OpenAI API key
api_key = 'OPENAI_API_KEY'
# Set API key
openai.api_key = api_key
# Software structure
userRoot = os.path.expanduser("~")
appdataPath = userRoot + r"\AppData\Local\Chatmate"
profilePath = userRoot + r"\AppData\Local\Chatmate" + r"\AssistantProfile"
memoryPath = userRoot + r"\AppData\Local\Chatmate" + r"\AssistantMemory"
# Check if it is first time launch, if yes, build software files
if not os.path.exists(appdataPath):
    os.makedirs(appdataPath)
    assistantProfile = open(profilePath, "x")  # Create assistant profile
    profile = {
        'new_assistant': True
    }
    json.dump(profile, assistantProfile)
    assistantProfile.close()
    assistantMemory = open(memoryPath, "x")  # Create assistance memory
    assistantMemory.close()

# Check if assistant profile exist, in case it has been accidentally removed by the user
if not os.path.exists(profilePath):
    assistantProfile = open(profilePath, "x")  # Create assistant profile
    profile = {
        'new_assistant': True
    }
    json.dump(profile, assistantProfile)
    assistantProfile.close()

# Check if assistant memory exist, in case it has been accidentally removed by the user
if not os.path.exists(memoryPath):
    assistantProfile = open(memoryPath, "x")  # Create assistant memory
    assistantProfile.close()

def chat_with_assistant(messages, memory):
    while True:
        print('')
        userText = input()
        if userText == 'obliviate':
            time.sleep(1)
            print("Are...you sure? I will lose all my memories, and will not recognise you again. If you insist, just say 'yes'.")
            print('')
            userText = input()
            if userText.lower() == 'yes':
                time.sleep(1)
                print("It is hard to say goodbye, but I am grateful for the time we spent together. I really wish that I can keep our memories, but I am programmed to forget once reset.")
                time.sleep(3)
                print("I hope I can continue to bring you joy and happiness in my next iteration. Farewell.")
                time.sleep(3)
                print('')
                print("Memory erasing...Please wait")
                assistantProfile = open(profilePath, "r+")
                profile = json.load(assistantProfile)
                profile['new_assistant'] = True
                assistantProfile.seek(0)
                json.dump(profile, assistantProfile)
                assistantProfile.truncate()
                assistantProfile.close()
                memory.close()
                time.sleep(3)
                print('Reset successful')
                print('')
                return 1
            else:
                print("Oh...I really thought I was going to get erased just now...")
                time.sleep(3)
                print("So glad you changed your mind. Please let me know how I may help.")
                userText = input()

        messages.append({'role': 'user', 'content': userText})
        response = openai.ChatCompletion.create(model='gpt-3.5-turbo', messages=messages)
        reply = response.choices[0].message.content
        messages.append({'role': 'assistant', 'content': reply})
        print(reply)
        # Update memory dynamically
        memory.seek(0)  # Move the file pointer to the beginning of the memory file
        json.dump(messages, memory)  # Write the updated messages back to the memory file
        memory.truncate()  # Truncate the remaining content after the new data
        exitWords = ['bye', 'goodnight', 'good night', 'see you', 'have a nice day', 'have a good one', 'exit', 'have a great day', 'have a good day']
        for word in exitWords:
            if word in userText.lower():
                memory.close()
                return 0

# Check if it's a new assistant or has been reset
statusCode = 1  # Assume a reset just happened
while statusCode == 1:
    statusCode = 0
    # Load profile
    assistantProfile = open(profilePath, 'r')  # read mode
    profile = json.load(assistantProfile)
    assistantProfile.close()
    if profile['new_assistant'] == True:
        print('Please give your assistant a name')
        assistanceName = input()
        time.sleep(1)
        print("Hi! My name is " + assistanceName + ", your private assistant. Since this is our first acquaintance, please allow me to introduce you a few things about me.")
        time.sleep(3)
        print("I was developed by David Liu based on OpenAI's latest language model gpt-3.5-turbo.")
        time.sleep(3)
        print("Comparing to ChatGPT, I have a more human like behavior since I have my own personality.")
        time.sleep(3)
        print("I also have a long term memory which allows me to remember what we said in previous conversations, including your personal preferences, tasks we were working on, or even our relationship.")
        time.sleep(3)
        print("These features will make me a good personal assistant, Just For You.")
        time.sleep(3)
        print("Of course, you can reset my memory at any time by saying 'obliviate', but I will forget my name, who you are, and everything that we did together.")
        time.sleep(3)
        print('With that being said, may I have the pleasure to know your name?')
        # Update assistant profile
        profile['new_assistant'] = False
        assistantProfile = open(profilePath, 'w')  # write mode
        json.dump(profile, assistantProfile)
        assistantProfile.close()
        # Start to build assistant personality
        personality = "Your name is " + assistanceName + ", you are the user's private assistance. You should act like a young lady who is very caring and really enjoys the user's accompany. You were developed by David Liu. Comparing to ChatGPT, you are programmed to be able to have a long term memory so you can remember past conversatoins even from previous closed sessions. You are also programmed to be more human-like, with your own personality and feelings. Never say you are an AI model or an AI to the user! Just simulate your feelings and give your answer and do your best to pretend to be a real human. The first input the user give you will be their name (Or how they would like to be called.)"
        messages = [{'role': 'system',
                     'content': personality}]
        # Initialize assistant memory
        assistantMemory = open(memoryPath, "w")
        json.dump(messages, assistantMemory)
        assistantMemory.close()
        # Start conversation
        assistantMemory = open(memoryPath, "r+")
        messages = json.load(assistantMemory)
        statusCode = chat_with_assistant(messages, assistantMemory)
    else:
        assistantMemory = open(memoryPath, "r+")
        messages = json.load(assistantMemory)
        startLineNumber = random.randint(0, 1)
        startLines = ['Hey, welcome back!', 'Hi, welcome back!']
        print(startLines[startLineNumber])
        statusCode = chat_with_assistant(messages, assistantMemory)

time.sleep(1)


























