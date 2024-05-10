from lang import llama


class LlamaScriptRunner:
    def __init__(self):
        self.llama = llama()

    def use(self, model):
        try:
            self.llama.USE(f"USE {model}")
            return True
        except ValueError:
            return False

    def prompt(self, prompt):
        self.llama.PROMPT(f"PROMPT {prompt}")
        return True

    def system(self, system_prompt):
        self.llama.SYSTEM(f"SYSTEM {system_prompt}")
        return True

    def chat(self, stream=False):
        try:
            self.llama.CHAT(stream)
            return True
        except ValueError:
            return False

    def input(self, command):
        try:
            self.llama.INPUT(command)
            return True
        except ValueError:
            return False

    def create_model(self, filename, parameters, model_name):
        try:
            self.llama.CREATE_MODEL(filename, parameters, model_name)
            return True
        except Exception:
            return False

    async def read(self, filename):
        try:
            await self.llama.read(filename)
            return True
        except FileNotFoundError:
            return False
