### 
# This script is used to install the pre-requisites for the prompt processing

###

LOG_FILE="prompt_processing_pre_req.log"

# Function to log messages to the log file and console
log() {
    echo "$(date) - $1" | tee -a $LOG_FILE
}


# check if java is installed
if ! command -v java &> /dev/null
then
    log "java is not installed. Installing java..."
    pamac install jdk-openjdk --no-confirm
fi