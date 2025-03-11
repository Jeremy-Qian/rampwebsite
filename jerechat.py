import requests
import random
from deep_translator import GoogleTranslator

# List of responses for 'Bye'
ERROR = ["Sorry. I didn't get that."]
bye_responses = [
    "再见！保重！",  # "Goodbye! Take care!"
    "下次见！",  # "See you next time!"
    "回头见！",  # "Catch you later!"
    "祝你一切顺利，告别！",  # "Farewell! Wish you all the best!"
    "拜拜！保持精彩！"  # "Bye! Stay awesome!"
]

class JereChat_Model2_0:
    """
    This class defines a chatbot model that:
    1. Communicates with an external API to generate conversational responses based on user input.
    2. Optionally translates the chatbot's responses into the specified target language (e.g., 'en' for English, 'zh' for Chinese).
    3. Can handle specific keywords like goodbye ("再见" or "拜拜") and respond with a random farewell message from a predefined list.
    
    Attributes:
    - company (str): The name of the chatbot company.
    - version (str): The version of the chatbot model.
    - language (str): The target language for the responses (e.g., 'en' for English).
    - translator (GoogleTranslator): A translation object to translate responses to the target language.
    - mode (str): The operational mode of the chatbot ('chat' or 'debug').
    - api (str): The URL for the external API to fetch chatbot responses.
    """
    
    def __init__(self, companyname="JereChat", version="2.0", language="en", mode="chat"):
        """
        Initialize the chatbot with the following parameters:
        - companyname: The name of the company or bot.
        - version: The version number of the chatbot.
        - language: The target language for the responses (default is 'en' for English).
        - mode: The operation mode ('chat' for normal operation, 'debug' for debugging).
        """
        self.company = companyname
        self.version = version
        self.language = language  # Target language for translation (e.g., 'en' for English)
        self.translator = GoogleTranslator(source='auto', target=language)  # Translator instance for language conversion
        self.mode = mode
        self.api = 'https://api.ownthink.com/bot?appid=9ffcb5785ad9617bf4e64178ac64f7b1&spoken=%s'

    def generate_response(self, data):
        """
        This method interacts with the external API to generate a response based on the user's input. 
        It also handles the translation of the response into the target language if necessary.
        
        Steps:
        1. Make an API call to retrieve the chatbot's response based on the user input.
        2. Extract the relevant text from the API's response.
        3. If the response contains a goodbye message ("再见" or "拜拜"), randomly select a farewell message.
        4. Translate the response text into the target language (if applicable).
        
        Parameters:
        - data (str): The user's input to be processed.
        
        Returns:
        - str: The translated chatbot response.
        """
        response_url = self.api % data  # Prepare the API URL with the user's input
        try:
            # Send the GET request to the API
            response = requests.get(response_url).json()
            if self.mode == "debug":
                print("API Response:", response)  # Debugging: Print API response if in debug mode

            # Extract the actual response text from the API's nested JSON structure
            if (
                response.get("data") 
                and isinstance(response["data"], dict)
                and response["data"].get("info")
                and isinstance(response["data"]["info"], dict)
                and "text" in response["data"]["info"]
            ):
                text_to_translate = response["data"]["info"]["text"]  # Extract the chatbot's message
            else:
                return random.choice(ERROR)  # Return an error message if the response structure is invalid
        except Exception as e:
            return random.choice(ERROR)  # Return an error if the API request fails

        # If the response contains "goodbye" messages, randomly pick a farewell message
        if not isinstance(text_to_translate, str):
            return random.choice(ERROR)  # Ensure the response text is a string
        if "再见" in text_to_translate or "拜拜" in text_to_translate:
            text_to_translate = random.choice(bye_responses)  # Select a random goodbye message from the list
        
        # Translate the response text to the target language (e.g., 'en' or 'zh')
        translated_response = self.translate(text_to_translate)
        return translated_response

    def translate(self, data):
        """
        This method translates the given text into the target language using the GoogleTranslator API.
        
        Parameters:
        - data (str): The text to be translated.
        
        Returns:
        - str: The translated text.
        """
        try:
            translated = self.translator.translate(data)  # Translate the text
            return translated  # Return the translated text
        except Exception as e:
            print(f"Translation error: {e}")  # Print any errors encountered during translation
            return "Translation failed."  # Return a failure message if translation fails

# Main execution loop for user interaction
if __name__ == "__main__":
    """
    This is the main execution block for the chatbot. It continuously asks the user for input, 
    processes the input using the generate_response() method, and displays the response.
    The loop ends when the user types 'q' to quit.
    """
    chat = JereChat_Model2_0(mode="debug")  # Initialize the chatbot in 'debug' mode
    while True:
        # Continuously prompt the user for input and provide the chatbot's response
        a = input("You: ")
        if a.lower() == "q":  # Exit loop if the user types 'q'
            break
        print("Bot:", chat.generate_response(a))  # Display the generated response from the chatbot
