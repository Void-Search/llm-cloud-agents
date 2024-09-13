#!/bin/bash

# Split audio from video file into 5 minute segments with overlap using GNU Parallel

CHUNK_DURATION=300  # 5 minutes in seconds
OVERLAP=10  # 10 seconds overlap

# Process arguments
if [ $# -ne 2 ]; then
    echo "Usage: $0 <input_file> <output_directory>"
    exit 1
fi

# Check if GNU Parallel is installed
if ! command -v parallel &> /dev/null; then
    echo "GNU Parallel is not installed. Please install it and try again."
    exit 1
fi

# Variables
input_file=$1
output_directory=$2

# Function to determine the number of CPU threads and get thread list
get_cpu_info() {
    if [ "$(uname)" == "Darwin" ]; then
        # macOS
        total_threads=$(sysctl -n hw.logicalcpu)
        threads_to_use=$((total_threads - 2))
        threads_to_use=$((threads_to_use > 1 ? threads_to_use : 1))
        echo "$total_threads $threads_to_use"
    elif [ -f /proc/cpuinfo ]; then
        # Linux
        total_threads=$(nproc)
        threads_to_use=$((total_threads - 2))
        threads_to_use=$((threads_to_use > 1 ? threads_to_use : 1))
        thread_list=$(seq -s, 0 $((threads_to_use - 1)))
        echo "$total_threads $threads_to_use $thread_list"
    else
        # Default
        echo "4 2 0,1"
    fi
}

read total_threads threads_to_use thread_list <<< $(get_cpu_info)

echo "Total logical CPU threads: $total_threads"
echo "Using $threads_to_use threads for processing"
[ -n "$thread_list" ] && echo "Thread list: $thread_list"

# Check if output directory exists else create it
if [ ! -d "$output_directory" ]; then
    mkdir -p "$output_directory"
fi

# Check if input file exists
if [ ! -f "$input_file" ]; then
    echo "Input file does not exist"
    exit 1
fi

duration=$(ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 "$input_file")
duration=${duration%.*}  # Remove decimal part

echo "Duration: $duration seconds"

# Function to process a single chunk
process_chunk() {
    local start=$1
    local chunk_number=$2
    local output_file="${output_directory}/chunk_$(printf "%03d" $chunk_number).m4a"
    
    if [ "$(uname)" == "Linux" ] && [ -n "$thread_list" ]; then
        taskset -c $thread_list ffmpeg -i "$input_file" -ss $start -t $CHUNK_DURATION \
            -vn -c:a aac -b:a 192k \
            -avoid_negative_ts 1 -copyts \
            "$output_file"
    else
        ffmpeg -i "$input_file" -ss $start -t $CHUNK_DURATION \
            -vn -c:a aac -b:a 192k \
            -avoid_negative_ts 1 -copyts \
            "$output_file"
    fi
}

export -f process_chunk
export input_file output_directory CHUNK_DURATION thread_list

# Generate the list of start times and chunk numbers
seq 0 $((CHUNK_DURATION-OVERLAP)) $duration | \
    awk -v chunk=0 '{print $0, chunk++}' | \
    parallel -j $threads_to_use --colsep ' ' process_chunk {1} {2}

echo "Audio splitting completed"

exit 0