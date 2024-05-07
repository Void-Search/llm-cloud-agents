import argparse
import json
import os
import yaml


class ApiConfigManager:
    def __init__(self, config_file='config.ini'):
        self.config_file = config_file
        self.configure()

    def parse_arguments(self):
        parser = argparse.ArgumentParser(description="Configure API request settings.")
        parser.add_argument('--backend', help='the backend to use, e.g., ollama, openai, etc', type=str)
        parser.add_argument('--multi_prompt', help='use a multi prompt, default is False', action='store_true')
        parser.add_argument('--prompt', help='the prompt to send, if not provided will be read from terminal', type=str)
        parser.add_argument('--model', help='the model to use, e.g., llama3, gpt3, etc', type=str)
        parser.add_argument('--url', help='the URL of the pod, e.g., http://localhost:8000', type=str)
        parser.add_argument('--stream', help='stream the response, default is False', action='store_true')
        parser.add_argument('--raw', help='raw text, default is False', action='store_true')
        parser.add_argument('--context', help='the context to use, default is None', type=json.loads)
        parser.add_argument('--system', help='the system prompt to use, default is None', type=str)
        parser.add_argument('--response', help='the response format, default is json', type=str)
        parser.add_argument('--images', help='a list of base64 encoded images, default is None', type=json.loads)
        parser.add_argument('--config_file', help='the path to a configuration file', default='config.ini', type=str)
        parser.add_argument('--create_system_prompt', help='create a system prompt', default=False, action='store_true')
        return parser.parse_args()

    def parse_config_file(self):
        # check if file exists
        if not os.path.exists(os.path.join("config", self.config_file)):
            print(f"Configuration file {self.config_file} not found.")
            return 0
        with open(os.path.join("config", self.config_file), 'r') as file:
            config = yaml.safe_load(file)
        return config
    
    def configure(self):
        # parse arguments
        args = self.parse_arguments()
        # parse config file
        config = self.parse_config_file()
        # merge arguments with config file
        settings = vars(args)
        if config:
            settings.update(config)
        self.verify_config(settings)
        return settings
    
    def verify_config(self, settings):
        # verify that the configuration is valid
        if settings['backend'] is None:
            raise ValueError("Backend must be provided.")
        if settings['model'] is None and settings['prompt'] is None:
            raise ValueError("Model and prompt must be provided.")
        
    
def main():
    config_manager = ApiConfigManager()
    settings = config_manager.configure()

    print(f"Using model: {settings['model']}")
    print(f"Using prompt: {settings['prompt']}")
    print(f"Using backend: {settings['backend']}")

    # Here, you could continue to integrate with other parts of your system
    # For instance, initializing a RequestBuilder and sending a request to a service
    
if __name__ == "__main__":
    main()
    

