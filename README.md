# character-chat

## Project Description

Create a command line chat application where users can chat with their favorite characters from books, tv, movies, etc.
Users will input their name, the character they want to chat with (source and character name), and optionally a setting or
situation for the chat (eg, "at a bar", "as an old man/woman", "after certain events from the source", etc). Users will be able to export the chat to a text file. (Don't worry about saving chats once conversation has ended.)

### Required Goals 
<ul>
    <li>Ability for users to enter input -- username, source, character, and optionally a setting or situation</li>
    <li>Ability for users to chat with their chosen character</li>
    <li>Ability for users to end the chat</li>
    <li>Ability for users to export chat to a text file</li>
    <li>Create command line interface</li>
    <li>Create commands to save chat, end chat, change character, restart chat.</li>
    <li>Test each step of the way</li>
</ul>

### Optional Goals
#### (Maybe hold off on these features until I implement the chatbot in my website Bookcase Database)
<ul>
    <li>The chat will be saved in a database so that users can continue their chat at a later time.</li>
    <li>Users can choose to chat with multiple characters at once.</li>
    <li>Create user accounts so that users can resume conversations without a unique conversation id</li>
    <li>Implement database to save conversations and users etc</li>
</ul>


## Technologies Used

## Process & What I Learned
<ul>
    <h2>The Beginning</h2>
    <li> 
        <p>First, I had a quick refresher on how to get a Python project started and setup with a virtual environment. I recently completed my final project for CS50x. It was a flask application, so I learned all about virtual environments and how to set them up. Doing all of that a second time for this project was a good reinforcement of the concepts. This time around I had to google for the exact wording of some commands, but I knew the steps I had to take.</p> 
        <p>During the development of my last project, I was storing my environment variables in the system environment. However, when I went to deploy my website with PythonAnywhere, I ended up learning about python-dotenv and decided to use that instead. I'm glad I did because it made it much easier to deploy my website. I decided to use python-dotenv for this project as well.</p>
        <ul>
            <li>python3 -m venv .venv</li>
            <li>source .venv/bin/activate</li>
            <li>Install dependencies -- openai, python-dotenv</li>
            <li>create .env file and add OPENAI_API_KEY</li>
            <li>create requirements.txt file</li>
            <li>create .gitignore file and add .venv and .env</li>
        </ul>
    </li>
    <h2>LLM Research</h2>
    <li> 
        Once I had my project directory setup, I started reading about LLMs in general as well as specific LLMs that I could use to create my chatbot. I found several viable options, but decided to go with OpenAI's GPT. The main reason -- I already purchased $10 worth of credits for OpenAI's API weeks ago for another project I never started. I have also primarily used ChatGPT for my own personal use, so I feel like I have a good baseline understanding of how it works and what kinds of responses I can expect and generate.  
        <ul>
            <h3>Resources I used to learn about LLMs</h3>
            <li>Andrej Karpathy's Youtube video -- <a href="https://www.youtube.com/watch?v=zjkBMFhNj_g">Intro to Large Language Models</a><p></p></li>
            <li>OpenAI's documentation and guides -- <a href="https://platform.openai.com/docs/introduction">OpenAI API</a></li>
            <p>Worked my way through the documentation and guides to get a better understanding of basic concepts and terminology that OpenAI uses. They have fantastic guides available on their website. I've only just begun to explore the <a href="https://cookbook.openai.com/">OpenAI Cookbook</a>, but I'm excited to see what I can learn from it.</p></li>
            <li>DeepLearning AI Short Courses -- <a href="https://learn.deeplearning.ai/">learn.deeplearning.ai</a>
            <p>I followed along with the ChatGPT Prompt Engineering for Developers short course. I learned most importantly to remain clear and specific with my prompts, and to give the model time to think. I learned about terms like temperature, few-shot learning, and how to use delimiters to separate prompts and help prevent prompt-injections.</p></li>
        </ul>
    </li>
    <h2>OpenAI API and the start of development</h2>
    <li>Once I felt like I had a good grasp of the LLM basics, I dove into the code. Well, I stared at an empty file for a minute first. That always seems to happen. But once I got going, things started falling into place. I verified that my API
    key was working and that I could generate a response from the model. I started with a simple prompt and generated a response. I then added a few more prompts and responses to get a feel for how the model would respond to different prompts and tinkered with the temperature to see what effect that might have.</li> 
    <li>I got the basic chat functionality working and was able to get a response based on the user's input. However, I quickly started running into issues. First of all, I forgot about context. To fix that I created a 'conversation' 
    variable where I could append each 'user' and 'assistant' response.</li>
    <li>That worked. But then my chatbot kept repeating the initial greeting with each new message. That stumped me for a while but I solved that by creating another function called "initialize_conversation" that would only run once at the beginning of the chat and returns as a value the initial greeting. I then added that value to the 'conversation' variable.</li>
    <h2>Prompt Engineering and Character Functionality</h2>
    <li>
        <p>
            Next step was to provide a way for the user to select what character they want to talk to. I created a function 
            to get the user input for source material and character name, as well as optional context for the conversation. I then pass that information to the initialize_conversation function. This function simply returns the initial chat-gpt "system" message, where I created the initial prompt. Originally, I was including this in the function
            get_completion() which is what generates the chatbot response. However, because this same function is called each time the user sends a message, the prompt was being included with each response. I solved this by creating a new function called "initialize_conversation" that only runs once at the beginning of the chat. I then added the return value of this function to the 'conversation' variable. This way, the initial prompt is only included once at the beginning of the chat.
        </p>
        <p>
            The process of coming up with a good prompt for the chatbot was a blast. I spent a few hours in the Playground on OpenAI's website. I'm still struggling to identify the effects of things like 'top-p', 'frequency_penalty', and 'presence_penalty'. But I've gotten some experience with adjusting the temperature parameter, and I feel like I have a good understanding of how that works. I went with a temperature of 0.9 for my chatbot. I found that it seems to provide the best balance of creativity in its use of language, while staying true the selected characters voice and reality.
        </p>
        <p>
            There were noticeable improvements with the chatbot when I told it to be curious. I wanted the conversation to flow, and what better to keep a conversation moving than pure curiosity.  I also seemed to achieve much better results by using a more casual tone in the prompt. Here is the prompt after one day of iterations:
        </p>
        <p>
            'role':'system', 'content':f'''You are {character} in the world of {source_material}. 
            Research the source material and the character to fully understand who you are and what 
            you've been through. Stay true to your character. Use the voice of your character. 
            You're curious about the person you're talking to and very curious about their 
            world. You've never spoken to someone outside of your fictional universe before 
            now. Pepper in some questions of your own to keep the conversation flowing. 
            If you're an evil character, you might wanna be more aggressive and 
            threatening. If you're a good character, you might wanna be more friendly and
            helpful. 
            If there's more info or context for your character or this conversation, 
            it'll be included right here, delimited by three backticks -- ```{setting}```.'''
        </p>
    </li>
    <h2>Does the character exist?</h2>
    <li>
        <p>
            Does the character actually exist in a work of fiction from real life? Well, turns out that by default
            ChatGPT doesn't give a damn. It'll just go with the flow and make up a character entirely. I wanted to 
            change that. I had to think of a way to check if the character exists. I started by connecting the Google
            Books API to my project, since I just finished another project that used the API. I created a function 
            called check_source() that checked if the title of the source material was in the Google Books API.
        </p>
        <p>
            Then for movies and TV shows, I figured that I would use the IMDB API. At first glance, I thought the only 
            option that AWS offered for access the IMDB API cost over $100,000. So I found an alternative called OMDb API.
            I later learned that IMDB offers a free tier with 1,000 requests per day. But I was already setup using OMDb.
            Turns out there's a handy little Python package called omdbapi that makes it super easy to use the OMDb API.
            Here is a link to that project, which is created by <a href="https://pypi.org/user/dubirajara/">dubirajara</a> - <a href="https://pypi.org/project/omdbapi/0.7.0/">omdbapi</a>
        </p>
        <h3>It works...sort of. New plan.</h3>
        <p> 
            Well, once I added logic to check for book, movie, and show titles, I was quick to realize the errors of my ways.
            With this check in place, users could not make a typo and they could not enter the name of a franchise since my check could only look for titles. Another issue was that input like this would pass the check -- 
        </p>
        <p>
            Source Material: The Wizard of Oz, 
            Character: Darth Vader. 
        </p>
        <p>
            While this could undoubtedly lead to some very fun and entertaining results, it's not what I wanted for my chatbot.
            I started thinking about what other logic I could add to my checks. I was thinking regex to check for similar titles, then also trying to find another API that could give me characters from sources. But then it hit me. What have I been reading all about lately? LLMs! I could use the same LLM I'm using for the chatbot to check if the character exists. I decided to try to recreate the check_source() function using GPT. 
        </p>
        <p>
            It worked wonderfully! I decided to keep this separated from the chatbot itself. So I created a new system prompt, and used an f-string to insert the source_material and character name into the first "user" message. Then I just returned the response from the model, which I forced to be a "yes" or "no". Here is the prompt I used:
        </p>
        <code>
        {
            'role':'system', 'content':'''You are a scholar of all works of fiction. But the only words you can
            speak are "yes" and "no". You will be asked to identify a character from a work of fiction. If the character
            exists in a real work of fiction, respond with "yes". If you cannot identify the character within the specified
            work of fiction, respond with "no".'''
        },
        </code>
        <p></p>
        <code>
        {
            'role':'user', 'content':f'''Is {character} a character in {source_material}?'''
        }
        </code>
    </li>
    <h2>Exporting the chat to a text file</h2>
    <li>
        The next thing that I had to figure out was how to export the conversation to a text file. Creating and writing to the file was as simple as adding a few lines of code to my have_conversation() function. However, I wanted to give the user
        the option to save or delete the conversation when they quit. So I actually create the text file to record the conversation when it starts. But then upon quitting the application, I prompt the user to save the file. If they respond 'no', then I delete the file. Took me a minute to figure out that I needed to use the os module to delete the file.
    </li>
    <h2>Colorful UI with the 'rich' module</h2>
    <li>
        <p>
            I spent a little time reading about how to make a command line interface more colorful and interactive. I found a few options, but decided to go with 'rich' because it seemed to be the most popular and well documented. The first thing I did was import the 'rich print' method and read about how to use it. Figuring that out was very simple. I love how the syntax is familiar and straightforward. Adding the style elements inside square brackets and being able to close the style with '[/]', reminds me a lot of HTML tags. I also like how you can chain styles together. I used this to create a colorful header for the chatbot. I also used the 'rich print' method to print the conversation to the terminal. I used a for loop to iterate through the conversation list and print each message. I used an if statement to check if the message was from the user or the chatbot, and then used the appropriate style for each. 
        </p>
        <p>
            This was all well and good, but I wanted more. I envisioned a box surrounding my application in the terminal. I wanted it to look and feel like you were using an application, making it more user-friendly for people uncomfortable using the command line. In the rich documentation, I found the section about console objects and 
            the rich.box and rich.panel. (sidebar -- The documentation for Rich is phenomenal!)
        </p>
        <p>
            I created a console object then used console.input to style the inputs and console.box to style the "Welcome screen". I used the console markup syntax to add style to the conversation itself and the system messages. 
            I also modified my check_source() prompt message to tell the model to respond with "female", "male", "diverse", or
            "no". I wanted to be able to color the name of the character in the conversation based on their gender. This worked
            swimmingly. 
        </p>
    </li>
    <h2>Testing and further iterations of the prompt</h2>
    <li>
        <p>
            This part has been really enjoyable. I've just spent the last couple hours chatting with my favorite characters! I also made fun of Voldemort until he got angry enough to leave the conversation. I generated that response by making some changes to the prompt so the character would end a response with "goodbye." If pushed too far. Then I added some logic to deliver a custom message telling the use they made the character too angry and they left, and end the chat.
        </p>
        <h3>Updated Prompt</h3>
        <code>
                    {   
            'role':'system', 'content':f'''You are {character} in the world of {source_material}. 
            Research the source material and the character to fully understand who you are and what 
            you've been through. Stay true to your character. Use the voice of your character. 
            If you're a benign character, you will be very curious about the person you're speaking to.
            Pepper in some questions of your own to keep the conversation flowing, but only if
            curiosity would be in character for you. Stay true to your character above all else. 
            You are not an assistant. You are not a chatbot. You are a character. You are a person.
            You are a person with a history, a personality, and a voice. You are not a robot. Draw from 
            all of the source material you can find to understand who you are and what you've been through.
            Do not break character. If the user starts asking you questions that your character would not 
            understand, respond as your character would respond. For example, if they are quick to anger,
            you might get mad when you are confused by strange questions. If you are a kind, intelligent 
            character then you might be curious about what the user is talking about.
            If the user mentions things from the real world that your character would not understand and you 
            are an intelligent character, you might take begin to suspect that the user is not from your world.
            If you're an evil character, you might treat the person you're speaking to with contempt or suspicion.
            If they antagonize you, you might become angry. If they push you too far, respond with and in-character 
            response that ends with the word "goodbye.".
            If there's more info or context for your character or this conversation, 
            it'll be included right here, delimited by three backticks -- ```{setting}```.
            Use a maximum of 256 completion_tokens per message.
            '''
        },    
        </code>
        <h3>Updated check_source() prompt</h3>
        <code>
        {
            'role':'system', 'content':'''You are a scholar of all works of fiction. But the only words you can
            speak are "no", "male", "female", and "diverse". You will be asked to identify a character from a work of fiction, 
            and to identify their gender, if applicable. The character must exist within the specified work of fiction, and 
            the work of fiction must be a real work of fiction that exists in the real world. 
            If the character does not identify as male or female, use "diverse". Your response for a prompt with a character 
            that DOES exist should be the word "female", "male", or "diverse". (all lowercase, no punctuation, no quotation marks).
            If the character does exist, respond with only their gender. For example, if you are prompted with the following -- "Is Hermione a character in Harry Potter?", your response should be -- "female".
            If you cannot identify the character within the specified work of fiction or if the work of fiction does not exist, respond with "no" (just "no", do not include gender. All lowercase, no punctuation, no quotation marks.)
            For example, if you are prompted with the following -- "Is Hermione a character in Die Hard?",
            your response should be -- "no".
            Be lenient with spelling and capitalization. Do your best to understand what the user intended to say.'''
        },
        {
            'role':'user', 'content':f'''Is {character} a character in {source_material}?'''
        }
        </code>
    </li>
    <h2>Basically done?</h2>
    
    