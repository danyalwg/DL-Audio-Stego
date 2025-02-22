import struct

def convert_audio_to_image(audio_path, image_output_path):
    """Converts an audio file into an image-like binary format."""

    # Read the audio file
    with open(audio_path, "rb") as aud_file:
        audio_data = aud_file.read()

    # Create a unique marker and append the length of the audio data
    marker = b"IMGAUDIO"
    packed_length = struct.pack(">Q", len(audio_data))

    # Create an image-like binary by appending the audio data and marker
    image_data = audio_data + marker + packed_length

    # Save the resulting "image"
    with open(image_output_path, "wb") as output_file:
        output_file.write(image_data)

    print(f"Audio successfully converted to an image-like format: {image_output_path}")


if __name__ == "__main__":
    convert_audio_to_image("example_audio.wav", "converted_image.png")  # Example usage
