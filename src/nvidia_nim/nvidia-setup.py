from openai import OpenAI
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

client = OpenAI(
  base_url = "https://integrate.api.nvidia.com/v1",
  api_key = "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"
)


def get_user_input() -> str:
    """
    Prompts the user to enter a question. If the user types 'quit', the function
    returns None to indicate the desire to exit the program.

    Returns:
    - str: The user input, or None if the user wants to exit the program.

    Handles:
    - KeyboardInterrupt: If the user interrupts the program (Ctrl+C).
    - EOFError: If the user interrupts the program (Ctrl+D).
    """
    try:
        user_input = input("\nAsk a question: ").strip()
        
        if user_input.lower() == "quit":
            return None

    except KeyboardInterrupt:
        print("\nExiting program due to user interruption...")
        exit(0)
    except EOFError:
        print("\nExiting program due to user interruption...")
        exit(0)
    return user_input

def process_input(input_str: str) -> str:
    """
    Processes the input string by trimming leading and trailing whitespace.
    
    Parameters:
    - input_str (str): The input string to be processed.
    
    Returns:
    - str: The processed input string.
    
    Raises:
    - TypeError: If the input is not a string.
    - ValueError: If the input string is empty after trimming.
    """
    if not isinstance(input_str, str):
        logging.error("The input is not a string. Please provide a valid input.")
        processed_input = None
    else:
        processed_input = input_str.strip()
    
    if not processed_input:
        logging.warning("The input string is empty after trimming. Please provide a valid input.")
        processed_input = None
    
    return processed_input


def send_question_to_model(input):
    """
    Sends a question to an AI model and retrieves the response.

    Parameters:
    - input (str): The question to send to the model.

    Returns:
    - Optional[Any]: The model's response or None if an error occurs.

    Raises:
    - ValueError: If the input is invalid.
    """    

    print("\n")
    print("Asking the model for a response to the question...")
    completion = client.chat.completions.create(
        model="mistralai/mixtral-8x7b-instruct-v0.1",
        messages=[{"role": "user", "content": input}],
        temperature=0.71,
        top_p=1,
        max_tokens=1024,
        stream=True
    )
    return completion

def generate_question(input_str: str = None) -> str:
    """
    Generates a question either by processing the provided input string or by prompting the user for input.

    Parameters:
    - input_str (str, optional): The input string to process. If None, the user will be prompted for input.

    Returns:
    - str: The processed question.
    """
    if input_str is None or input_str == "":
        input_from_user = get_user_input()  
        processed_input = process_input(input_from_user)  
    else:
        processed_input = process_input(input_str)  

    return processed_input

def parse_completion(completion):
    """
    Iterates through a sequence of completion chunks, printing the content of each chunk. 
    If a chunk contains no content, it prints "No response from model".

    Parameters:
    - completion (Iterable): An iterable sequence of completion chunks.
    """
    combined_content = ""
    for chunk in completion:
        try:
            content = chunk.choices[0].delta.content
            if content is not None:
                # Concatenate the content of each chunk
                combined_content += content
            else:
                # If there is no content, log a message
                logging.info("No response from model\n")
        except AttributeError:
            # Log an error if the expected structure is not found
            logging.error("Invalid completion format encountered.")

    # Print the entire combined content after processing all chunks
    print(combined_content)
    

if __name__ == "__main__":
    # Main loop
    while True:
        # handle user input or provided input in generate_question
        question = generate_question(input_str="")
        if question is not None:
            # We have a question
            # send the question to the model
            completion = send_question_to_model(question)
            parse_completion(completion)
        