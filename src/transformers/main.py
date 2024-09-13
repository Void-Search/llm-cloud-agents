import torch
from transformers import AutoModelForSpeechSeq2Seq, AutoProcessor, pipeline
from datasets import load_from_disk
import pydub
import os
from pathlib import Path

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"Using device: {device}")
torch_dtype = torch.float16 if torch.cuda.is_available() else torch.float32


model_id = "openai/whisper-large-v3"

# Load the model
model = AutoModelForSpeechSeq2Seq.from_pretrained(model_id, torch_dtype=torch_dtype)

model.to(device=device)

processor = AutoProcessor.from_pretrained(model_id)


# Create the pipeline
pipe = pipeline(
    "automatic-speech-recognition",
    model=model,
    device=device,
    torch_dtype=torch_dtype,
    feature_extractor=processor.feature_extractor,
    tokenizer=processor.tokenizer,
)


# Transcribe an audio file
# lotr_dataset = load_from_disk("/workspaces/llm-cloud-agents/The.Lord.of.the.Rings.The.Two.Towers.2002.EXTENDED.REMASTERED.1080p.BluRay.x264.TrueHD.7.1.Atmos-FGT.mkv")
# dataset = load_dataset("/workspaces/llm-cloud-agents/The.Lord.of.the.Rings.The.Two.Towers.2002.EXTENDED.REMASTERED.1080p.BluRay.x264.TrueHD.7.1.Atmos-FGT.mkv", "clean", split="validation")

# sample = lotr_dataset[0]["audio"]


def slice_audio_file(
    audio_file_path, output_directory, chunk_length_minutes=5, overlap_seconds=10
):

    print("Loading audio file...")
    audio = pydub.AudioSegment.from_file(audio_file_path)

    chunk_length = chunk_length_minutes * 60 * 1000
    overlap_length_ms = overlap_seconds * 1000
    chunk_dir = output_directory

    os.makedirs(chunk_dir, exist_ok=True)

    start_time = 0
    chunk_number = 1

    while start_time < len(audio):
        end_time = start_time + overlap_length_ms

        chunk = audio[start_time:end_time]

        output_path = os.path.join(chunk_dir, f"chunk_{chunk_number}.wav")
        with open(output_path, "wb") as f:
            chunk.export(f, format="wav")
        start_time += chunk_length - overlap_length_ms
        print(f"Saved chunk {chunk_number} to {output_path}")
        chunk_number += 1


slice_audio_file(
    "/workspaces/llm-cloud-agents/The.Lord.of.the.Rings.The.Two.Towers.2002.EXTENDED.REMASTERED.1080p.BluRay.x264.TrueHD.7.1.Atmos-FGT.mkv",
    "/workspaces/llm-cloud-agents/chunks",
)
# slice the audio file to 5 minutes
# sample = sample[:5*60*16000]
result = pipe(
    "/workspaces/llm-cloud-agents/The.Lord.of.the.Rings.The.Two.Towers.2002.EXTENDED.REMASTERED.1080p.BluRay.x264.TrueHD.7.1.Atmos-FGT.mkv"
)

print(result["text"])
