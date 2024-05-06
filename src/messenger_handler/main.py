from configuration_manager import ConfigurationManager

def handle_single_prompt():
    pass

def handle_multi_prompt():
    pass

def main():
    config_manager = ConfigurationManager()
    settings = config_manager.configure()

    print(f"Using model: {settings['model']}")
    print(f"Using prompt: {settings['prompt']}")

    if settings['multi_prompt']:
        handle_multi_prompt()
    else:
        handle_single_prompt()

    # Here, you could continue to integrate with other parts of your system
    # For instance, initializing a RequestBuilder and sending a request to a service

if __name__ == "__main__":
    main()