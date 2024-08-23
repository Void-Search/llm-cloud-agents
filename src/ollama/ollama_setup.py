import ollama
from helper_functions.timing_functions import monitor_function
import os
import sys
import pprint
import logging

sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..")))


logging.basicConfig(level=logging.INFO)


# Define a ollama class that can take in arguments
class ollama_handler:
    def __init__(
        self,
        mode_type,
        model_file,
        name,
    ):
        if not isinstance(mode_type, str):
            raise TypeError("model_type must be a string")
        if not isinstance(model_file, str):
            raise TypeError("model_file must be a string")
        if not isinstance(name, str):
            raise TypeError("name must be a string")

        self.model_type = mode_type
        self.model_file = model_file
        self.name = name

    def create_model(self, model_file_path="", stream=True):
        if not self.verify_ollama_online():
            raise ConnectionError("Ollama is not running")
        if os.path.exists(model_file_path):
            model_path = model_file_path
        else:
            raise FileNotFoundError(f"File not found at {model_file_path}")
        try:
            ollama.create(
                model=self.model_type,
                path=model_path,
                model_file=self.model_file,
                name=self.name,
            )
            return True
        except ollama.ResponseError as e:
            print(f"Error creating model: {e}")
            return False

    def verify_ollama_online(self):
        if ollama.list():
            print("Ollama is running")
            return True
        else:
            print("Ollama is not running")
            return False


# Monitor how long the following command takes to run and the system resources used
response = monitor_function(
    ollama.chat,
    model="phi",
    messages=[{"role": "user", "content": "Why is the sky blue?"}],
)

# pass to another model for review
response = monitor_function(
    ollama.chat,
    model="phi",
    messages=[
        {
            "role": "user",
            "content": """Please provide a brief review of the text provided.
                          Present only the final,
                          revised output starting adding in anything that was
                          missed and respond with ANSWER <output>: """
            + response.get("message").get("content"),
        }
    ],
)

print("Response from ollama:")
pprint.pprint(response.get("message").get("content"))
