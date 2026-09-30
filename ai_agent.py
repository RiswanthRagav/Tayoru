from ollama import chat


class AIAgent:

    def __init__(self):
        self.model = "gemma3:1b"

    def send_message(self, message):

        response = chat(
            model=self.model,
            messages=[
                {
                    "role":"user",
                    "content": message
                }
            ]
        )

        return response.message.content