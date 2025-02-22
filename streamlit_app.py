import os
# Disable the file watcher for torch to avoid the RuntimeError
os.environ["STREAMLIT_SERVER_FILEWATCHER_TYPE"] = "none"

import streamlit as st
import tempfile
import struct
from PIL import Image
import librosa
import torch
import torchvision.transforms as transforms

# Import visual presentation functions (for the illusion)
from embed_audio_image import audio_to_image as generate_spectrogram
from embed_audio_image import embed_image as create_container_image
from extract_audio_image import extract_image as recover_spectrogram

# Binary integration functions (actual embedding/extraction)
def integrate_audio_into_container(cover_path, audio_path, output_path):
    """
    Integrate the audio file into the container image.
    """
    with open(cover_path, "rb") as f:
        cover_data = f.read()
    with open(audio_path, "rb") as f:
        audio_data = f.read()
    marker = b"IMGAUDIO"
    packed_length = struct.pack(">Q", len(audio_data))
    combined_data = cover_data + audio_data + marker + packed_length
    with open(output_path, "wb") as f:
        f.write(combined_data)
    return output_path

def retrieve_audio_from_container(container_path, output_audio_path):
    """
    Retrieve the hidden audio from the container image.
    """
    with open(container_path, "rb") as f:
        data = f.read()
    marker = b"IMGAUDIO"
    marker_len = len(marker)
    length_field_size = 8
    tail_len = marker_len + length_field_size
    if len(data) < tail_len:
        st.error("The selected file is too small to contain embedded audio.")
        return None
    tail = data[-tail_len:]
    if tail[:marker_len] != marker:
        st.error("No embedded audio was found in the image.")
        return None
    audio_length = struct.unpack(">Q", tail[marker_len:])[0]
    audio_start = len(data) - tail_len - audio_length
    audio_data = data[audio_start : audio_start + audio_length]
    with open(output_audio_path, "wb") as f:
        f.write(audio_data)
    return output_audio_path

# Import and alias the audio processing function (your updated version)
from audio_processing import enhance_audio_clarity as refine_audio

def finalize_audio(input_audio_path, output_audio_path):
    """
    Finalize the audio processing step.
    """
    import soundfile as sf
    y, sr = librosa.load(input_audio_path, sr=None)
    processed_audio, new_sr = refine_audio(y, sr)
    sf.write(output_audio_path, processed_audio, new_sr)
    return output_audio_path

def main():
    st.title("Steganography Application")
    st.write("Embed an audio file within an image and later extract the hidden audio.")

    tabs = st.tabs(["Embedding Mode", "Extraction Mode"])

    # --- Embedding Mode ---
    with tabs[0]:
        st.header("Embedding Mode")
        uploaded_image = st.file_uploader("Select a Cover Image", type=["png", "jpg", "jpeg"], key="cover_img")
        uploaded_audio = st.file_uploader("Select an Audio File", type=["wav", "mp3", "ogg"], key="audio_file")

        if uploaded_image and uploaded_audio:
            # Save uploads to temporary files
            with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as temp_img:
                temp_img.write(uploaded_image.read())
                cover_image_path = temp_img.name
            with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_audio:
                temp_audio.write(uploaded_audio.read())
                audio_file_path = temp_audio.name

            st.subheader("Cover Image:")
            st.image(cover_image_path, caption="Cover Image", use_container_width=True)

            # Generate presentation visuals (for the illusion)
            with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as temp_spec:
                spectrogram_path = temp_spec.name
            try:
                generate_spectrogram(audio_file_path, spectrogram_path)
                st.subheader("Generated Spectrogram:")
                st.image(spectrogram_path, caption="Spectrogram", use_container_width=True)
            except Exception as e:
                st.error(f"Error generating spectrogram: {e}")

            with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as temp_container:
                container_image_path = temp_container.name
            try:
                create_container_image(cover_image_path, spectrogram_path, container_image_path)
                st.subheader("Container Image:")
                st.image(container_image_path, caption="Container Image", use_container_width=True)
            except Exception as e:
                st.error(f"Error creating container image: {e}")

            # Integrate the audio file into the container image
            with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as temp_stego:
                stego_image_path = temp_stego.name
            try:
                integrate_audio_into_container(container_image_path, audio_file_path, stego_image_path)
                st.success("Audio embedding completed successfully.")
                st.subheader("Final Stego Image:")
                st.image(stego_image_path, caption="Stego Image", use_container_width=True)
                with open(stego_image_path, "rb") as f:
                    st.download_button(label="Save Stego Image", data=f, file_name="stego_image.png", mime="image/png")
            except Exception as e:
                st.error(f"Error during embedding: {e}")

    # --- Extraction Mode ---
    with tabs[1]:
        st.header("Extraction Mode")
        uploaded_stego = st.file_uploader("Select the Stego Image", type=["png", "jpg", "jpeg"], key="stego_img")
        if uploaded_stego:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as temp_stego:
                temp_stego.write(uploaded_stego.read())
                stego_path = temp_stego.name

            st.subheader("Stego Image:")
            st.image(stego_path, caption="Stego Image", use_container_width=True)

            # Recover the presentation spectrogram
            with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as temp_recovered_spec:
                recovered_spec_path = temp_recovered_spec.name
            try:
                recover_spectrogram(stego_path, recovered_spec_path)
                st.subheader("Recovered Spectrogram:")
                st.image(recovered_spec_path, caption="Recovered Spectrogram", use_container_width=True)
            except Exception as e:
                st.error(f"Error recovering spectrogram: {e}")

            # Retrieve the embedded audio
            with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_extracted_audio:
                extracted_audio_path = temp_extracted_audio.name
            try:
                result = retrieve_audio_from_container(stego_path, extracted_audio_path)
                if result:
                    st.success("Audio extraction completed successfully.")
                    # Finalize the audio processing step
                    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_final_audio:
                        final_audio_path = temp_final_audio.name
                    try:
                        finalize_audio(extracted_audio_path, final_audio_path)
                        st.audio(final_audio_path, format="audio/wav")
                        with open(final_audio_path, "rb") as f:
                            st.download_button(label="Save Audio", data=f, file_name="final_audio.wav", mime="audio/wav")
                    except Exception as e:
                        st.error(f"Error finalizing audio: {e}")
            except Exception as e:
                st.error(f"Error retrieving audio: {e}")

if __name__ == "__main__":
    main()
