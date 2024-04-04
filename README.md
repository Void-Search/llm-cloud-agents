
# Ollama LLM Workspace

This workspace contains the source code for a Python project that uses the Ollama LLM (Language Learning Model).

## Directory Structure

- [`src/`](command:_github.copilot.openRelativePath?%5B%22src%2F%22%5D "src/"): Contains the main source code of the project.
  - `main.py`: The main entry point of the application.
  - `helper_functions/`: Contains helper functions used across the project.
    - `terminal_output.py`: Contains functions for terminal output.
    - `timing_functions.py`: Contains functions for timing and monitoring.
  - `ollama_llm/`: Contains files related to the Ollama LLM.
    - `Dockerfile`: Defines the Docker image for the project.
    - `ollama_install.sh`: A shell script to install Ollama.
    - `ollama-setup.py`: A Python script to set up Ollama.
    - `requirements.txt`: Lists the Python dependencies for the project.

- [`.gitignore`](command:_github.copilot.openRelativePath?%5B%22.gitignore%22%5D ".gitignore"): Specifies files and directories that Git should ignore.
- [`.vscode/settings.json`](command:_github.copilot.openRelativePath?%5B%22.vscode%2Fsettings.json%22%5D ".vscode/settings.json"): Contains settings for the Visual Studio Code editor.
- [`LICENSE`](command:_github.copilot.openRelativePath?%5B%22LICENSE%22%5D "LICENSE"): The license for the project.
- [`README.md`](command:_github.copilot.openRelativePath?%5B%22README.md%22%5D "README.md"): This file.

## Building and Running the Project

The project is containerized using Docker. To build the Docker image, run the following command in the terminal:

```sh
docker build -t ollama_llm:latest .
```

To run the Docker container, use the following command:

```sh
docker run -it --rm ollama_llm:latest
```

## Contributing

Please see the [`LICENSE`](command:_github.copilot.openRelativePath?%5B%22LICENSE%22%5D "LICENSE") file for details on how the code in this project is licensed. Contributions are welcome. Please submit a pull request with your proposed changes.

## Contact

For any questions or concerns, please open an issue on the project's GitHub page.