import messenger 
import os

class RequestBuilder:
    """
    A builder class for constructing a request payload for API interactions, primarily used
    for configuring the properties of a request to a model.

    This class allows setting various attributes like model name, prompt, images, format,
    and others through a fluent interface.
    """
    def __init__(self):
        """
        Initializes a new RequestBuilder instance with an empty payload.
        """
        self.payload = {}

    def add_model(self, model):
        """
        Adds a model identifier to the payload.

        Parameters:
        model (str): The name of the model to be used.

        Returns:
        self (RequestBuilder): Enables method chaining.

        Raises:
        ValueError: If 'model' is not a string or is empty.
        """
        if not model or not isinstance(model, str):
            raise ValueError('model must be a string')
        self.payload['model'] = model
        return self

    def add_prompt(self, prompt):
        """
        Adds a prompt to the payload to be sent to the model.

        Parameters:
        prompt (str): The prompt text.

        Returns:
        self (RequestBuilder): Enables method chaining.

        Raises:
        ValueError: If 'prompt' is not a string or is empty.
        """
        if not prompt or not isinstance(prompt, str):
            raise ValueError('prompt must be a string')
        self.payload['prompt'] = prompt
        return self


    def add_option(self, key, value, version='v1'):
        """
        Adds an optional key-value pair to the payload for settings like temperature.

        Parameters:
        key (str): The option key.
        value (str): The option value.

        Returns:
        self (RequestBuilder): Enables method chaining.

        Raises:
        ValueError: If the key is not a valid option or the value is of the wrong type.
        """
        if version == 'v1':
            self.check_known_option_v1(key, value)
        else:
            # otherwise, add the key-value pair to the payload
            # if the key is not recognized as an option
            self.payload[key] = value
        return self
    
    def check_known_option_v1(self, key, value):
        # Sets a keep alive duration for the model session.
        if key == 'keep_all': 
            if not isinstance(value, str):
                raise ValueError('keep_all must be a string')
            self.payload[key] = value
        # Specifies whether the output should be raw text.
        elif key == 'raw':
            if not isinstance(value, bool):
                raise ValueError('raw must be a boolean')
            self.payload[key] = value
        # Sets whether the response should be streamed or received as a single payload.
        elif key == "stream":
            if not isinstance(value, bool):
                raise ValueError('stream must be a boolean')
            self.payload[key] = value
        # Adds a previous conversation context for the model to utilize.
        elif key == "context": 
            if not isinstance(value, dict):
                raise ValueError('context must be a dictionary')
            self.payload[key] = value
        # Adds a system prompt for the model to use.
        elif key == "system": 
            if not isinstance(value, str):
                raise ValueError('system must be a string')
            self.payload[key] = value
        # Sets the response format of the model output.
        elif key == "response": 
            if not value not in ['json']:
                raise ValueError('format must be of json')
            self.payload[key] = value
        # Adds a list of base64 encoded images to the payload.
        elif key == "images":
            if not all([isinstance(image, str) and image.startswith('data:image') for image in value]):
                raise ValueError('images must be base64 encoded list')
            self.payload[key] = value
        # Adds a prompt to the payload to be sent to the model.
        elif key == "prompt":
            if not isinstance(value, str):
                raise ValueError('prompt must be a string')
            self.payload[key] = value
        else:
            # otherwise, add the key-value pair to the payload
            # if the key is not recognized as an option
            self.payload[key] = value


    def create_system_prompt(self):
        if self.payload.get('prompt') and self.payload.get('model'):
            # we want to generate a dyname system prompt
            with open(os.path.join("prompts", "system_prompt_generator.txt"), 'r') as file:
                temp_system_prompt = f"{file.read()}" 
                self.payload['system'] = temp_system_prompt
            response = messenger.Messenger().send_message(self.payload)
            return response
            
    def build(self):
        """
        Finalizes and returns the constructed payload.

        Returns:
        dict: The fully constructed payload.
        """
        return self.payload
