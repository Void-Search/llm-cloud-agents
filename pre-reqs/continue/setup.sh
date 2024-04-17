# setup continue

CONTINUE_VERSION="0.9.112"

# parse arguments
while getopts ":v:" opt; do
    case ${opt} in
        v )
            CONTINUE_VERSION=$OPTARG
            ;;
        \? )
            echo "Usage: setup.sh [-v <version>]"
            exit 1
            ;;
    esac
done


# check if linux and wget is installed
if [ "$(uname)" != "Linux" ]; then
    echo "This script is for Linux only."
    exit 1
fi

# check if vscode is installed
if ! which code
then
    echo "Unable to find VSCode. Please install it first."
    exit 1
fi

# check if the extension is installed
rm -rf "continue-${CONTINUE_VERSION}.vsix"
if ping -c 1 www.marketplace.visualstudio.com; then
    echo "Network connection is good."
    curl -O "https://marketplace.visualstudio.com/_apis/public/gallery/publishers/Continue/vsextensions/continue/${CONTINUE_VERSION}/vspackage?targetPlatform=linux-x64"
else
    echo "Network connection is bad. Trying to install locally."
    if [ -f "continue-${CONTINUE_VERSION}.vsix" ]; then
        echo "Local vsix file found install manually in vscode gui..."
        code
    else
        echo "Continue not found locally."
        exit 1
    fi
fi
