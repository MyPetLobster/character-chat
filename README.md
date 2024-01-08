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
    </li>
    <ul>
        <li>python3 -m venv .venv</li>
        <li>source .venv/bin/activate</li>
        <li>Install dependencies -- openai, python-dotenv</li>
        <li>create .env file and add OPENAI_API_KEY</li>
        <li>create requirements.txt file</li>
        <li>create .gitignore file and add .venv and .env</li>
    </ul>
    <h2>LLM Research</h2>
    <li> Once I had my project directory setup, I started reading about LLMs in general as well as specific LLMs that I could use to create my chatbot. I found several viable options, but decided to go with OpenAI's GPT. The main reason -- I already purchased $10 worth of credits for OpenAI's API weeks ago for another project I never started. I have also primarily used ChatGPT for my own personal use, so I feel like I have a good baseline understanding of how it works and what kinds of responses I can expect and generate.
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
    <li>Next step was to provide a way for the user to select what character they want to talk to. I created a function called "character" that would take the user's input and return a prompt based on the character they chose.  I also added a function called "restart" that would allow the user to restart the chat with a different character.</li>
