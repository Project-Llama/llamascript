import ollama

class llama:
    """
    The `llama` class represents a no-code AI chatbot.

    Attributes:
    - model: The model to be used for chatbot responses.
    - data: The prompt data to be used for chatbot conversations.

    Methods:
    - __init__(self, ignore=False): Initializes the `llama` object.
    - USE(self, line): Sets the model to be used for chatbot responses.
    - PROMPT(self, line): Sets the prompt data to be used for chatbot conversations.
    - CHAT(self): Initiates a chat with the AI chatbot.
    - read(self, filename): Reads and executes commands from a file.
    """

    def __init__(self):
        """
        Initializes the `llama` object.

        Parameters:
        - ignore (bool): If True, the initialization message will be ignored.
        """
        self.model = None
        self.data = None
        self.ignore = False
    
    def USE(self, line):
        """
        Sets the model to be used for chatbot responses.

        Parameters:
        - line (str): The command line containing the model name.
        """
        if line.split(' ')[0] == 'USE':
            self.model = line.split(' ')[1]
        else:
            raise ValueError('Invalid model')
    
    def PROMPT(self, line):
        """
        Sets the prompt data to be used for chatbot conversations.

        Parameters:
        - line (str): The command line containing the prompt data.
        """
        if line.split(' ')[0] == 'PROMPT':
            self.data = line.split(' ')[1]
        else:
            raise ValueError('Invalid data')
    
    def CHAT(self):
        """
        Initiates a chat with the AI chatbot.
        """
        print(ollama.chat(model=self.model, messages=[{'role': 'user', 'content': self.data}])['message']['content'])
    
    def read(self, filename):
        """
        Reads and executes commands from a file.

        Parameters:
        - filename (str): The path to the file containing the commands.
        """
        with open(filename, 'r') as file:
            for line in file:
                line = line.strip()
                if not line:
                    continue
                command = line.split(' ')[0]
                if command == 'IGNORE':
                    self.ignore = True
                elif command == 'USE':
                    self.USE(line)
                elif command == 'PROMPT':
                    self.PROMPT(line)
                elif command == 'CHAT':
                    if not self.ignore:
                        print('=================\nThanks for using llama, a no-code AI chatbot. Please ensure Ollama (https://ollama.com) is running. To get started, type "USE" followed by the model you want to use. Then, type "PROMPT" followed by the prompt you want to use. Finally, type "CHAT" to chat with the AI. To run a script, type "llamascript" to run your script. To ignore this message, add "IGNORE" to the beginning of your llama file.\n=================')
                        self.ignore = True
                    self.CHAT()
                else:
                    raise ValueError('Invalid command')
                

def run():
    try:
        l = llama()
        l.read('llama')
    except KeyboardInterrupt:
        pass
