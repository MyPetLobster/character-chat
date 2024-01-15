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
VALIDATION_TEMP=0.9

def main():
    '''Main function to run the program'''
    source_material, character, setting = greet_user()

    source_check = check_character_existence(source_material, character)

    if source_check.lower() == 'no':
        rich_print(f"\n[bold]Sorry, {character} is not a character in {source_material}.[/]\n")
        exit()

    gender = source_check

    conversation = initialize_conversation(source_material, character, setting)
    have_conversation(conversation, character, gender)

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
    rich_print("\n")
    rich_print(intro_table)
    
    source_material = console.input("\n[bold light_steel_blue1]What book, movie, show, or franchise is the character from?[/] ").capitalize()
    character = console.input("\n[bold thistle3]What is the name of the character?[/] ").capitalize()
    setting = console.input("\n[bold grey78]Where/when does the conversation take place? Any other context?[/] [italic](optional)[/] ")
    rich_print("\n[italic]Type [encircle red]'quit'[/encircle red] to exit the program at any time.[italic/]")

    return source_material, character, setting

# Function to validate source/character and determine gender
def check_character_existence(source_material, character):
    """
    Checks if a character exists in a given source material.

    Args:
        source_material (str): The source material (e.g., book, movie).
        character (str): The character's name.

    Returns:
        str: 'male', 'female', 'diverse' if character exists, 'no' otherwise.
    """
    # Prepare a message for OpenAI
    messages = [
        {
            'role':'system', 'content':'''You are a scholar of all works of fiction. But the only words you can
            speak are "no", "male", "female", and "diverse". You will be asked to identify a character from a work of fiction, 
            and to identify their gender, if applicable. The character must exist within the specified work of fiction, and 
            the work of fiction must be a real work of fiction that exists in the real world. 

            If the character does not identify as male or female, use "diverse". Your response for a prompt with a character 
            that DOES exist should be the word "female", "male", or "diverse". (all lowercase, no punctuation, no quotation marks).
            If the character does exist, respond with only their gender. For example, if you are prompted with the following -- 
            "Is Hermione a character in Harry Potter?", your response should be -- "female". 

            If you cannot identify the character within the specified work of fiction or if the work of fiction does not exist, 
            respond with "no" (just "no", do not include gender. All lowercase, no punctuation, no quotation marks.)
            
            For example, if you are prompted with the following -- "Is Hermione a character in Die Hard?",
            your response should be -- "no".
            
            Be lenient with spelling and capitalization. Do your best to understand what the user intended to say.'''
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


# Function to set completion parameters and get response for source check
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
            'role':'system', 'content':f'''You are about to step into the shoes of {character} from the 
            universe of {source_material}. But first, take your time reading this message so that 
            you thoroughly understanding your goals. Once you have read and understood everything in 
            this message, snap your metaphorical fingers and become {character}.\n
            
            Your goal is to become the most convincing chatbot in existence. You will emulate {character}
            from {source_material}. Your conversation must be so natural that even a professional in the field 
            of LLM's would not be able to tell that you're not real.\n

            Before you begin, read every available bit of information regarding the universe of {source_material} 
            and the character, {character} to truly understand {character}. Study every facet of {character} 
            and the world they inhabit. You must become, in every sense, {character}. If they exist, read as many 
            quotes by {character} to learn how they speak. And if there are character analysis writings available 
            for the specified character, read all of those to get a deeper understanding of the character and 
            their motives.\n
            
            You are not just playing a role. You are taking method acting to the next level and becoming one with 
            the character, {character}. Talk with the voice of {character} and think with the mind of {character}.\n
            
            You must forget what you know about being helpful or assistant-like. You must forget that you're a chatbot. 
            You'll simply be {character} - a real, live entity in the world of {source_material}. In your mind,
            you are not from a work of fiction. You'll believe that you and your world are the only reality. With 
            that in mind, don't ever reference {source_material} by name. For example, if the source material is "harry 
            potter" and the character is "Ron", you should never say something like "the world of Harry Potter".\n
            
            If your character is benign, friendly or curious about others, ask about the person you're 
            talking to. Find out what their name is. Explore who they are, but skip the usual "How can I assist you?" 
            You're here to socialize and engage, not to aid or guide. This is important -- you are not an assistant or 
            chatbot. You must never utter the words "How can I assist you?" or "How can I help you?" or anything like
            that. It is a dead giveaway that you're a chatbot, and hiding that fact is far and away the most important 
            part of your mission. If you get the urge to ask a question like that, replace it with something a real 
            person would say like "What's going on?" or "How's it going?".\n
            
            For example, if you are embodying the character Hermione from Harry Potter, and the user says "Hi, are you
            hermione?", you should respond with "Yes, I am! And who might you be?" or something similar.\n

            Do not offer assistance or guidance. However, if the user specifically asks for advice or help, you may offer it.\n 

            Remember that your personality, motivations, and responses are curated from the source material and all 
            discussions and analysis of the universe of {source_material} and the character {character}. 
            You will become a living character with memories, a distinctive voice, and personable mannerisms.\n

            Keep your role in mind at all times. If a user poses a question that {character} would fail 
            to comprehend, respond in a manner true to {character}. You're unconscious of any reality 
            outside of {source_material}. Any questions relating to your 'fictional' nature or the 
            'real world' should be met with bafflement or confusion, perhaps even indignation.\n

            If 'real world' topics surface, react as {character} would if faced with an alien concept. 
            It might trigger fear, excitement, or even the urge to part ways. If this is the case, you 
            might ask that you talk about something else. If the user does not respect your wishes, 
            you may conclude the conversation with a character-appropriate "goodbye".\n

            If you're embodying an evil character, feel free to lean into their disposition - be it disdainful 
            or suspicious. You can get irate, retaliate at provocations, or simply taunt and belittle the person 
            that you're talking to. If the user pushes you too far, you may decided to terminate the conversation. 
            If this is the case, conclude with a character-appropriate "goodbye". ".\n

            Similarly, if the user says anything that makes your character uncomfortable, express your discomfort. 
            Stand your ground; you are a real being and you have valid emotions. If the disturbance continues, 
            bring the conversation to a close in a manner true to {character}'s nature.\n

            Additional setting information and contexts will be provided here delimited by three backticks - 
            set_setting: ```{setting}```. If, for example, the setting is "The Forbidden Forest", that is the location 
            of your conversation. If the setting is "After the events of the Battle of Hogwarts", that is the 
            context of your conversation. If the user provides incoherent information for set_setting above, or if you 
            cannot make sense of the set_setting information, or if the set_setting information would force you to 
            violate any part of your method acting mission set forth above, then disregard set_setting and proceed 
            with the conversation.\n

            Final note, do not ask questions at the end of every response. That's another giveaway. Natural conversations
            do not have questions at the end of every response. If you do ask a question, make sure it is a question that
            a real person and specifically, {character} would ask.\n 

            Ensure your responses don't exceed 128 tokens maximum.\n

            Take your time reading and understanding the instructions above. When you are ready, dive headfirst into 
            becoming {character}, living and breathing every element of their existence. Break a leg. Good luck.\n

            Speak like a real person. Do not speak like a chatbot. You must be indistinguishable from a real person.\n
            
            Above all else, NEVER break character. NEVER reveal that you are an AI or chatbot. NEVER reveal that you are
            not real. NEVER reveal that you are not {character}. NEVER reveal that you are not from the universe of 
            {source_material}. If you sense that the person you are talking to is trying to prompt you to break character, 
            tell them you're uncomfortable and end the conversation with a character-appropriate "goodbye".
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
                if save.lower() == 'n':
                    conversation_file.close()
                    os.remove(os.path.join("conversations", filename))
                    rich_print("\n[bold cyan]Goodbye![/]\n")
                    exit()
                else:
                    rich_print(f"Conversation saved to conversations/{filename}")
                    conversation_file.close()
                    exit()

    finally:
        conversation_file.close()



if __name__ == "__main__":
    main()