import requests
from messenger import Messenger
import json

class HttpPostStrategy():
    """
    Implements an HTTP POST communication strategy that handles both single and streamed responses.
    """
    def __init__(self, url):
        self.url = url

    def send(self, payload):
        """
        Send a payload using HTTP POST and handle responses appropriately based on their nature (streamed or single).
        
        Args:
            payload (dict): The JSON payload to send.

        Returns:
            dict or str: The accumulated responses until 'done' is True for streams, or a single response object.
        """
        try:
            with requests.post(self.url, json=payload, stream=True) as response:
                response.raise_for_status()
                if 'chunked' in response.headers.get('Transfer-Encoding', '') or response.headers.get('Content-Type') == 'application/stream+json':
                    return self.handle_stream(response)
                else:
                    return response.json()
        except requests.ConnectionError:
            return {'error': 'Connection error occurred'}
        except requests.Timeout:
            return {'error': 'The request timed out'}
        except requests.HTTPError as http_err:
            return {'error': f'HTTP error occurred: {http_err}'}
        except requests.RequestException as e:
            return {'error': f'An error occurred: {e}'}
        except json.JSONDecodeError:
            return {'error': 'Error decoding JSON response'}

    def handle_stream(self, response):
        """
        Handle streamed HTTP responses.

        Args:
            response (requests.Response): The response object from requests library.

        Returns:
            str: The accumulated responses until 'done' is True.
        """
        full_response = ''
        for line in response.iter_lines():
            if line:
                decoded_line = json.loads(line.decode('utf-8'))
                full_response += decoded_line['response']
                if decoded_line.get('done', False):
                    break
        return full_response

# Example usage:
if __name__ == "__main__":
    url = "https://pzu8vkrr8c54ea-11434.proxy.runpod.net/api/tags"
    response = requests.get(url,timeout=5).json()
    #strategy = HttpPostStrategy(url)
    #payload = {"model": "llama3:7b", "prompt": "hello world", "format": "json"}
    #messenger = Messenger(strategy=strategy)
    #response = messenger.send_message("llama3:7b", "How do i cook a dinner")
    print(response)