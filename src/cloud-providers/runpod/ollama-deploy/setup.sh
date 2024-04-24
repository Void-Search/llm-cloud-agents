###
#
# in order to u
#
###


update_host() {
  echo "Updating host"
  apt-get update && apt-get upgrade -y && apt-get install -y pciutils
}

install_lspci() {
  echo "Installing lspci"
  apt-get install -y pciutils
}

install_ollama() {
  echo "Installing Ollama"
  (curl -fsSL https://ollama.com/install.sh | sh &&  OLLAMA_HOST=0.0.0.0:11434 ollama serve > ollama.log 2>&1) &
}

pull_model() {
  echo "Pulling model"
  ollama pull llama3
}

run_model() {
    echo "Running model"
    ollama run llama3
}

main() {
  update_host
  install_lspci
  install_ollama
  serve_ollama
  pull_model
  run_model
}