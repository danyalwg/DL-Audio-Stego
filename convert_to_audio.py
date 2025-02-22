import struct

def convert_image_to_audio(image_path, audio_output_path):
    """Converts an image-like file back into an audio file by extracting the embedded audio data."""

    with open(image_path, "rb") as file:
        data = file.read()

    # Define the marker and its length
    marker = b"IMGAUDIO"
    marker_len = len(marker)
    length_field_size = 8
    tail_len = marker_len + length_field_size

    # Ensure the file is large enough to contain embedded audio
    if len(data) < tail_len:
        raise ValueError("The file is too small to contain audio data.")

    # Retrieve the tail data where marker and length are stored
    tail = data[-tail_len:]

    # Check if the marker exists
    if tail[:marker_len] != marker:
        raise ValueError("No audio data found in the image.")

    # Extract the audio length
    audio_length = struct.unpack(">Q", tail[marker_len:])[0]

    # Compute the starting position of the embedded audio
    audio_start = len(data) - tail_len - audio_length

    # Extract the audio data
    audio_data = data[audio_start:audio_start + audio_length]

    # Save the extracted audio
    with open(audio_output_path, "wb") as audio_file:
        audio_file.write(audio_data)

    print(f"Image successfully converted back to audio: {audio_output_path}")


if __name__ == "__main__":
    convert_image_to_audio("converted_image.png", "restored_audio.wav")  # Example usage
