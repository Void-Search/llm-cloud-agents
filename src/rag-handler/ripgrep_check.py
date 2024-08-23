import os
import subprocess
import json
import re
from typing import List, Dict, Any

class LocalSearch:
    def __init__(self, path: str, rg_options: Dict[str, Any] = None, config_file: str = None):
        self.path = os.path.abspath(path)
        self.is_directory = os.path.isdir(self.path)
        self.rg_options = rg_options or {}
        self.config_file = config_file

    def _validate_path(self) -> bool:
        if not os.path.exists(self.path):
            raise ValueError(f"Path '{self.path}' does not exist")
        if self.is_directory and not any(os.path.isfile(os.path.join(self.path, f)) for f in os.listdir(self.path)):
            raise ValueError(f"Directory '{self.path}' does not contain any files")
        return True

    def _get_searchable_files(self) -> List[str]:
        if not self.is_directory:
            return [self.path]

        searchable_files = []
        for root, _, files in os.walk(self.path):
            for file in files:
                file_path = os.path.join(root, file)
                if self._is_searchable_file(file_path):
                    searchable_files.append(file_path)
        return searchable_files

    def _is_searchable_file(self, file_path: str) -> bool:
        return not os.path.basename(file_path).startswith('.') and os.path.splitext(file_path)[1] in ['.txt', '.md', '.py', '.js', '.html', '.css']

    def search(self, prompt: str, max_results: int = 10) -> List[Dict[str, Any]]:
        self._validate_path()
        searchable_files = self._get_searchable_files()
        results = self._execute_ripgrep(prompt, searchable_files)
        ranked_results = self._rank_results(results, prompt)
        return ranked_results[:max_results]

    def _execute_ripgrep(self, prompt: str, files: List[str]) -> List[Dict[str, Any]]:
        prompt_words = prompt.lower().split()
        rg_cmd = ['rg', '-i', '--json']

        if self.config_file:
            rg_cmd.extend(['--config', self.config_file])

        for option, value in self.rg_options.items():
            if value is True:
                rg_cmd.append(f'--{option}')
            elif value is not False:
                rg_cmd.extend([f'--{option}', str(value)])

        # Use word boundaries and OR condition for each word in the prompt
        search_pattern = '\\b(' + '|'.join(map(re.escape, prompt_words)) + ')\\b'
        rg_cmd.extend([search_pattern, *files])

        result = subprocess.run(rg_cmd, check=True, capture_output=True, text=True)
        output = []
        for line in result.stdout.splitlines():
            try:
                data = json.loads(line)
                if data['type'] == 'match':
                    output.append({
                        'file': data['data']['path']['text'],
                        'content': data['data']['lines']['text'],
                        'line_number': data['data']['line_number']
                    })
            except json.JSONDecodeError:
                continue
        return output

    def _rank_results(self, results: List[Dict[str, Any]], prompt: str) -> List[Dict[str, Any]]:
        prompt_words = set(prompt.lower().split())
        for result in results:
            content_words = set(result['content'].lower().split())
            matching_words = prompt_words.intersection(content_words)
            result['match_score'] = len(matching_words)
            result['matching_words'] = list(matching_words)

        return sorted(results, key=lambda x: x['match_score'], reverse=True)

def main():
    # Example usage
    search_path = '/home/developer/Documents/llm-cloud-agents'
    rg_options = {'word-regexp': True, 'ignore-case': True}
    #config_file = '/path/to/your/ripgrep.conf'  # Optional

    local_search = LocalSearch(search_path, rg_options)

    prompt = "run ollama locally"
    results = local_search.search(prompt, max_results=5)

    print(f"Top 5 search results for '{prompt}':")
    for result in results:
        print(f"File: {result['file']}")
        print(f"Content: {result['content']}")
        print(f"Line number: {result['line_number']}")
        print(f"Match score: {result['match_score']}")
        print(f"Matching words: {', '.join(result['matching_words'])}")
        print("---")

if __name__ == "__main__":
    main()