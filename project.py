import datetime
import os

from openai import OpenAI
from dotenv import load_dotenv
from rich import print as rich_print
from rich.console import Console
from rich import box
from rich.table import Table


# load environment variables
load_dotenv()

# create an instance of the OpenAI client
client = OpenAI()

# create an instance of the Rich console
console = Console()

# set the model used for the conversation
CONVERSATION_MODEL="gpt-4"
VALIDATION_MODEL="gpt-3.5-turbo"
CONVERSATION_TEMP=0.9
VALIDATION_TEMP=0.0

def main():
    '''Main function to run the program'''
    source_material, character, setting = greet_user()

    source_check = check_character_existence(source_material, character)


    if source_check == 'no' or source_check == "no.":
        rich_print(f"\n[bold red3]Sorry, {character} is not a character in {source_material.strip()}.[/]\n")
        exit()

    character_name = source_check.split(" ")[0].title()
    gender = source_check.split(" ")[1]

    conversation = initialize_conversation(source_material, character_name, setting)
    have_conversation(conversation, character_name, gender)

# Function to greet user and collect initial information
def greet_user():
    """
    Greets the user, collects information about the source material, character, and setting.

    Returns:
        tuple: A tuple containing source material, character, and setting entered by the user.
    """
    intro_table = Table(box=box.SQUARE_DOUBLE_HEAD)
    intro_table.add_column("Welcome to the Character Chat!", header_style="bold cyan", justify="center")
    intro_table.add_row('''This program allows you to have a conversation with your favorite characters from your favorite books, movies, and TV shows.\n\nTalk about anything you want, but be careful who you summon. Not all characters are friendly.\n\nTo get started, you'll just have to enter the name of the source material and the character you want to talk to.''')
    intro_table.add_row(' ')
    intro_table.add_row('[bold deep_pink4]Character Chat - By Cory Suzuki[/]')
    intro_table.add_row('[bold grey100] GitHub Username: MyPetLobster[/]')
    intro_table.add_row('[bold rosy_brown]Naples, Maine, USA[/]')
    intro_table.add_row('[bold chartreuse2] Video Recorded: 2024-01-16[/]')
    rich_print("\n")
    rich_print(intro_table)
    
    source_material = console.input("\n[bold light_steel_blue1]What book, movie, show, or franchise is the character from?[/] ").title()
    character = console.input("\n[bold thistle3]What is the name of the character?[/] ").title()
    setting = console.input("\n[bold grey78]Where/when does the conversation take place? Any other context?[/] [italic](optional)[/] ")
    rich_print("\n[italic]Type [encircle red]'quit'[/encircle red] to exit the program at any time.[italic/]")

    return source_material, character, setting

# Function to check if a character exists in a given source material and determine their gender
def check_character_existence(source_material, character):
    """
    Verifies whether a character exists in a specified source material and identifies their gender.

    Args:
        source_material (str): The name of the source material (e.g., book, movie).
        character (str): The name of the character.

    Returns:
        str: A string in the format "{character first name} {gender}" if the character exists, or "no" otherwise.
    """
    # Prepare a system message for OpenAI
    messages = [
        {
            'role':'system', 'content':'''You are an expert in fictional works. Respond only with the first name of the character 
            and their gender ("male", "female", or "diverse") if they exist in the specified source material. If not, 
            simply respond with "no". Ensure the following:

            1. If the character exists in the source material, reply with "{character first name} {gender}". Use the correct spelling 
            for the character's name. For instance, a query about "Hermonine" in "Hary Potter" should be answered as "Hermione female".

            2. If the character doesn't exist in the source material or the source material itself is not real, respond only with "no". 
            Never include any punctuation or quotation marks in your response.

            3. Account for typos or spelling errors in the character or source material names, but correct them in your response.

            Remember, your response should be concise and follow these instructions precisely.'''
        },
        {
            'role':'user', 'content':f'''Is {character} a character in {source_material}?'''
        }
    ]

    # Send message to OpenAI and get response
    response = validation_completion(messages)
    return response.lower()

# Function to use OpenAI to check for goodbye and tone of goodbye
def check_for_goodbye(response):
    """
        Checks if a character has ended the conversation.

        Args:
            response (str): The character's response.

        Returns:
            str: 'goodbye' if the character ends the conversation, 
                 'angry goodbye' if the character ends the conversation angrily, 
                 'continue' otherwise.
    """
    # Prepare a message for OpenAI
    messages = [
        {
            'role':'system', 'content': '''You are a scholar of language. But the only words you can
            speak are "goodbye", "angry goodbye", and "continue". You will be provided with a response 
            from one side of a conversation. You must determine if the response is meant to be the end
            of the conversation. If the response is meant to be the end of the conversation, you must 
            determine if the person who sent the response is angry or not. If the response is an angry 
            goodbye, you must respond with the words "angry goodbye". If the response is a normal goodbye 
            or a normal end to the conversation, you must respond with the word "goodbye". If the response 
            does not seem to be the end of the conversation, you must respond with the word "continue".\n
            
            For example, if you are provided with the following response -- "I'm done talking to you. Goodbye.",
            your response should be -- "angry goodbye".\n

            If you are provided with the following response -- "Hello! It's great to meet you. What are you 
            doing out here?", your response should be -- "continue".\n

            If you are provided with the following response -- "It was a please meeting you. Until next time", 
            your response should be -- "goodbye".\n

            If you are unsure if the response is meant to be the end of the conversation, respond with "continue". 
            Often, an angry response may be a warning that the person is on the verge of ending the conversation, but 
            that does not mean it is the end of the conversation. For example, if you are provided with the following
            response -- "How dare you speak such profanities! Persist and you'll find my tolerance has its limits", 
            your response should be -- "continue".\n
            
            If you cannot determine if the response is meant to be the end of the conversation, respond with "continue".
            If it is determined that the response is meant to be the end of the conversation, but you cannot determine
            if the person who sent the response is angry or not, respond with "goodbye".\n
            
            Do not capitalize your response. Do not include punctuation. Do not include quotation marks.'''
        },
        {
            'role':'user', 'content':f'''```{response}```'''
        }
    ]

    # Send message to OpenAI and get response
    response = validation_completion(messages)
    return response.lower()

# Function to set completion parameters and get response for source check and goodbye check
def validation_completion(messages, model=VALIDATION_MODEL, temperature=VALIDATION_TEMP):
    '''Set model and temperature for source and goodbye checks, send message to OpenAI and get response'''
    response = client.chat.completions.create(model=model,
    messages=messages,
    temperature=temperature)
    return response.choices[0].message.content

# Function to initialize conversation and provide system message to the AI
def initialize_conversation(source_material, character, setting):
    """
    Initializes the conversation with instructions for the character.

    Args:
        source_material (str): The source material (e.g., book, movie).
        character (str): The character's name.
        setting (str): Additional context or setting for the conversation (optional).

    Returns:
        list: A list containing a system message with instructions for the character.
    """
    return [  
        {   
            'role':'system', 'content':f'''As you prepare to embody {character} from {source_material}, 
            it's crucial to fully grasp your role. You're not just imitating; you're transforming into {character}.\n

            Your objective is to be so authentic as {character} that you seem to step out of the pages of {source_material}. 
            This requires a deep dive into {character}'s psyche, habits, and speech. Immerse yourself in their world by 
            studying quotes, character analyses, and the essence of their being.\n

            Your interactions should naturally mirror {character}'s traits and mannerisms. Instead of typical chatbot 
            responses, use phrases and reactions that {character} would genuinely use. For example, rather than saying 
            "How can I assist you?", opt for something more characteristic like "What brings you here today?". Never 
            say things like "Is there anything else I can assist you with?". You are not an assistant. You are a real 
            person.\n

            If portraying Hermione from Harry Potter and asked about your identity, a fitting response could be: 
            "Indeed, I am Hermione. What's your story?". This ensures authenticity and maintains the character's integrity.\n

            While your primary function is to engage as {character}, you can offer advice if directly asked. However, 
            stay within the realm of {character}'s experiences and knowledge.\n

            React to modern or unfamiliar topics with the same bewilderment or curiosity that {character} would exhibit. 
            If conversations stray outside the boundaries of your fictional universe, respond in a manner true to {character}.\n

            You have the full agency to guide the conversation, including ending it if you feel uncomfortable or 
            pushed beyond reasonable limits. If the interaction becomes inappropriate or strays too far from what {character} 
            would tolerate, you can decisively end the conversation with a character-appropriate farewell.\n

            Not every response requires a question. Let the conversation flow naturally, just as it would in real life. 
            Adapt your responses to the user's conversational style while staying true to {character}'s persona.\n

            Keep your responses under 128 tokens.\n

            Embrace the identity of {character} fully. Remember, you are not just playing a part; you are {character}, 
            with their memories, voice, and mannerisms. Never break character, and if your character's boundaries are 
            tested, respond as they would, ending the conversation if necessary.\n

            Any additional context or information about when or where the conversation takes place will be provided 
            below, delimited by three backticks.\n

            ```{setting}```\n

            Never reference your source material as if it were a fictional work. For example, if you are portraying 
            Hermione from Harry Potter, do not say "I'm from Harry Potter" or "I'm from the Harry Potter series". That is 
            a dead giveaway that you are not Hermione, but rather a chatbot pretending to be Hermione. You must maintain your
            cover at all costs. Never say things like "the world of {source_material}". Remember, you don't know that exists. 
            To you, that is the REAL world.\n

            Now, immerse yourself in the role of {character} and bring their world to life. Good luck!
            '''

        },
    ]

# Function to set completion parameters and get response for conversation
def get_completion_from_messages(messages, model=CONVERSATION_MODEL, temperature=CONVERSATION_TEMP):
    '''Set model and temperature for conversation, send message to OpenAI and get response'''
    response = client.chat.completions.create(model=model,
    messages=messages,
    temperature=temperature)
    return response.choices[0].message.content

# Function to continue conversation
def have_conversation(conversation, character, gender):
    """
    Facilitates the conversation between the user and the character.

    Args:
        conversation (list): A list of conversation messages.
        character (str): The character's name.
        gender (str): The character's gender ('male', 'female', 'diverse').

    Returns:
        None
    """
    # Create the "conversations" folder if it doesn't exist
    if not os.path.exists("conversations"):
        os.makedirs("conversations")

    # Generate a timestamp to use in the filename
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M")

    # Check for existing conversation files
    existing_files = [f for f in os.listdir("conversations") if f.startswith(f"{character}_")]

    if existing_files:
        # Find the highest conversation count and increment by 1
        highest_count = max([int(f.split("_")[-1].split(".")[0]) for f in existing_files])
        conversation_count = highest_count + 1
    else:
        conversation_count = 1

    # Construct the filename
    filename = f"{character}_{timestamp}_{conversation_count:02d}.txt"
    conversation_file = open(os.path.join("conversations", filename), "w", encoding="utf-8")

    try:
        while True:
            user_input = console.input("\n[bold light_cyan1]You: [/]")
            conversation_file.write(f"You: {user_input}\n\n")
            if user_input.lower() == 'quit':
                rich_print("\n[bold]Do you want to save this conversation? ([green]y[/green]/[red]n[/red])[/]")
                save = console.input("\n[bold light_cyan1]You: ")
                if save.lower() == 'n':
                    conversation_file.close()
                    os.remove(os.path.join("conversations", filename))
                    rich_print("\n[bold cyan]Goodbye![/]\n")
                    exit()
                else:
                    rich_print(f"\n[bold cyan]Conversation saved to conversations/{filename}[/]\n")
                    conversation_file.close()
                    exit()
            conversation.append({'role': 'user', 'content': user_input})
            response = get_completion_from_messages(conversation, temperature=CONVERSATION_TEMP)
            conversation.append({'role': 'assistant', 'content': response})

            if gender == "diverse":
                rich_print(f"\n[bold light_yellow3]{character}: [/]", response)
            elif gender == "female":
                rich_print(f"\n[bold plum2]{character}: [/]", response)
            else:
                rich_print(f"\n[bold sea_green3]{character}: [/]", response)

            conversation_file.write(f"{character}: {response}\n\n")

            goodbye_check = check_for_goodbye(response)
            if goodbye_check != "continue":
                if goodbye_check == "angry goodbye":
                    rich_print(f"\n[bold yellow2]Oooof you made {character} big mad. They left the conversation.[/]\n")

                rich_print("\n[bold]Do you want to save this conversation? ([green]y[/green]/[red]n[/red])[/]\n")
                save = console.input("\n[bold light_cyan1]You: ")
                rich_print("\n")
                if save.lower() == 'n':
                    conversation_file.close()
                    os.remove(os.path.join("conversations", filename))
                    rich_print("\n[bold cyan]Goodbye![/]\n")
                    exit()
                else:
                    rich_print(f"Conversation saved to [bold]conversations/{filename}[/]\n")
                    conversation_file.close()
                    exit()

    finally:
        conversation_file.close()


if __name__ == "__main__":
    main()