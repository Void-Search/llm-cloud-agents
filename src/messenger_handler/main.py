'''
this program communicates to a remote pod that is running a LLM
and prints the response. The program is designed to handle both
single and multi prompts recieved either from the user or other files

'''

from requestbuilder import RequestBuilder
import sys
from messenger import Messenger
import argparse




def parse_args():
    """
    this function uses argsparse to parse the command line arguments


    arguemnts:
    --url: the url of the pod
    --model: the model to use
    --prompt: the prompt to send
    --format: the format of the response
    --backend: the backend to use
    """

    parser = argparse.ArgumentParser(description='Send a prompt to a pod and recieve a response')
    parser.add_argument('--backend', type=dict, help='the backend to use')
    parser.add_argument('--help', type=bool, help='print the help message')
    parser.add_argument('--multi_prompt', type=bool, help='use a multi prompt')

    args = parser.parse_args()

    return args
    



def read_prompt_from_terminal():
    '''
    reads a prompt from terminal and returns it as a string
    '''
    return input('Enter Prompt: ')

def handle_prompt(prompt, messenger):
    '''
    handles a single prompt and returns the response as a string
    '''
    response = messenger.send_request(prompt)
    return response

def handle_multi_prompt(prompt, messenger):
    '''
    handles a multi prompt and returns the response as a string
    
    '''
    while True:
        response = messenger.send_request(prompt)
        print(response)
        prompt = input('Enter Prompt: ')
        # handle exits like ctrl+c, ctrl+d, exit
        if not prompt or prompt == 'exit':
            break
        return response
        
def main():
    parse_args(sys.argv)
    

    

if __name__ == "__main__":
    main()