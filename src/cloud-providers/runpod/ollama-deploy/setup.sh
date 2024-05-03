# This script is used to setup the Ollama server on the host machine
# It installs lspci and Ollama and pulls the models from the Ollama server
# It also starts the Ollama server
LOG_FILE="ollama_install.log"

logger() {
  # log echo data to file including date
  echo "$(date) $1" >> $LOG_FILE  
}

update_host() {
  logger "Updating host"
  apt-get update && apt-get upgrade -y && apt-get install -y pciutils
}

install_lspci() {
  logger "Installing lspci"
  apt-get install -y pciutils
}

install_ollama() {
  logger "Installing Ollama"
  (curl -fsSL https://ollama.com/install.sh | sh &&  OLLAMA_HOST=0.0.0.0:11434 ollama serve > ollama.log 2>&1) &
}

pull_model() {
  # check if model list is defined in dir then pull all models in list
  # else use llama3 as default model
  if [ -f models_list ]; then
    while read -r line; do
      logger "Pulling model : $line"
      ollama pull $line
    done < models_list
  else
    ollama pull $1
  fi
}

main() {
  update_host
  install_lspci
  install_ollama
  serve_ollama
  pull_model "llama3"
  logger "Ollama setup complete"
}