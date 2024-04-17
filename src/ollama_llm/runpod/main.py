'''
this program communicates to a remote pod that is running a LLM
and prints the response. The program is designed to handle both
single and multi prompts recieved either from the user or other files

'''

from requestbuilder import RequestBuilder
import json
import os
import sys
from messenger import Messenger



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




def main():
    parse_args(sys.argv)

    

if __name__ == "__main__":
    main()