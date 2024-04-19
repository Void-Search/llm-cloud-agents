# Makfile used to build, install and test ollama compose

all: build install

SETUP_DIRECTORY = $(shell pwd)/setup

build:
	@echo "Building ollama compose"
	$(SETUP_DIRECTORY)/ollama_options.sh --build

install:
	@echo "Installing ollama compose"
	$(SETUP_DIRECTORY)/ollama_options.sh -- install

test:
	@echo "Testing ollama compose"
	$(SETUP_DIRECTORY)/ollama.sh --test

clean:
	@echo "Cleaning ollama compose"
	$(SETUP_DIRECTORY)/ollama.sh --clean

documentation:
	@echo "Work in progress... function to review and improve the documentation"
	@echo "Generating ollama compose documentation"
	$(SETUP_DIRECTORY)/ollama.sh --documentation

pull_models:
	@echo "Pulling ollama compose models"
	$(SETUP_DIRECTORY)/ollama.sh --pull_models

pull_data:
	@echo "Work in progress... function to pull data for use in the compose"
	@echo "Pulling ollama compose data"
	$(SETUP_DIRECTORY)/ollama.sh --pull_data

local_workspace:
	@echo "Setting up local python workspace for ollama compose"
	$(SETUP_DIRECTORY)/ollama.sh --local_workspace


.phony: all build install test clean documentation pull_models pull_data local_workspace