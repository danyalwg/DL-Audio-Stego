# DL Techniques for Generation of Steganographic Images with Hidden Audio

Welcome, Mr. Danyal, to the repository for the **Deep Learning-Based Audio Steganography System**. This project combines state-of-the-art deep learning techniques to securely hide audio within images and subsequently reveal it with exceptional fidelity. By integrating an advanced audio-to-image conversion process with a powerful deep learning model originally designed for image steganography, this system provides a robust, high-capacity solution for secure audio transmission, watermarking, and covert communications—all while preserving the visual quality of the cover image.

---

## Table of Contents
- [Overview](#overview)
- [Process Flow](#process-flow)
- [Key Features](#key-features)
- [System Architecture](#system-architecture)
- [Deep Learning Model Reference](#deep-learning-model-reference)
- [Installation](#installation)
- [Usage](#usage)
- [Code Structure](#code-structure)
- [Repository Layout](#repository-layout)
- [Contributing](#contributing)
- [License](#license)
- [Acknowledgements](#acknowledgements)

---

## Overview

This repository extends the concepts of deep image steganography to audio data. The system first converts an audio signal into a 256×256 RGB image, then leverages an advanced deep learning framework to embed this audio image into a cover image without compromising its visual quality. On the extraction side, the system recovers the hidden audio image from the stego-image and reconstructs the original audio waveform with minimal loss. This unique integration ensures that high-fidelity audio is securely concealed and later retrieved, making it an ideal tool for secure communications and digital watermarking.

---

## Process Flow

### 1️⃣ Image Embedding Phase (Audio Hiding)

- **Step 1: Audio-to-Image Conversion**  
  - **Normalization:** Audio samples are normalized from a range of [-1, 1] to [0, 1].  
  - **Reshaping:** Data is padded or truncated to exactly 196,608 values (to form a 256×256×3 array).  
  - **Scaling:** Each normalized sample is scaled to an 8-bit intensity value (0–255), resulting in an image that encodes the audio waveform.

- **Step 2: Deep Learning-Based Audio Image Embedding**  
  - A specialized deep learning model seamlessly embeds the generated audio image into a cover image using multi-layer feature fusion.
  - The resulting stego-image is visually indistinguishable from the original cover image while securely containing the hidden audio data.

### 2️⃣ Image Extraction Phase (Audio Recovery)

- **Step 3: Deep Learning-Based Audio Image Extraction**  
  - The stego-image is processed through a trained reveal model that accurately recovers the embedded audio image.

- **Step 4: Image-to-Audio Conversion**  
  - The recovered audio image is converted back into an audio waveform, preserving essential frequency and time-domain characteristics.

- **Step 5: Post-Processing and Audio Enhancement**  
  - Advanced post-processing techniques (adaptive filtering, spectral rebalancing, and harmonic correction) are applied to remove noise and enhance audio clarity.
  - A transmission degradation simulation is included to emulate real-world conditions and ensure robustness.

---

## Key Features

- **High-Fidelity Audio Recovery:** Retains complete audio information for lossless reconstruction.
- **Imperceptible Embedding:** The stego-image is visually identical to the cover image.
- **Robust Deep Learning Models:** Utilizes advanced neural networks for both embedding and extraction.
- **Sophisticated Post-Processing:** Enhances recovered audio by mitigating noise and distortions.
- **User-Friendly Interface:** A Streamlit-based GUI enables real-time interaction for seamless operation.

---

## System Architecture

The system is divided into two primary components:

1. **Image Embedding Phase:**  
   - Converts the audio signal into an image representation.  
   - Embeds the audio image into a cover image using a deep learning model.

2. **Image Extraction Phase:**  
   - Extracts the hidden audio image from the stego-image.  
   - Reconstructs the original audio waveform with advanced post-processing enhancements.

---

## Deep Learning Model Reference

This project incorporates the powerful deep learning model from the repository [arnoweng/PyTorch-Deep-Image-Steganography](https://github.com/arnoweng/PyTorch-Deep-Image-Steganography). The original implementation is a PyTorch-based solution for image steganography, inspired by the paper *"Hiding Images in Plain Sight: Deep Steganography"*. Key highlights of the original model include:

- **Hiding Network (H-net):**  
  - An U-net structured convolutional network that takes a 6-channel tensor (concatenation of cover and secret images) and outputs a container image.  
  - Ensures that the container image is nearly identical to the cover image, with minimal perceptible differences.

- **Revealing Network (R-net):**  
  - A convolutional network with six layers (each using a 3×3 kernel, followed by batch normalization and ReLU activations, except the last layer) designed to recover the hidden secret image from the container image.
  - Achieves impressive recovery quality, with very low averaged pixel-wise discrepancies (APD) between the secret and the revealed secret.

**Integration in Our Project:**  
In our adaptation, we extend this deep learning framework to handle audio data. The audio signal is first converted into an image, then processed by the H-net and R-net to embed and extract the hidden audio information. This integration not only preserves the high-fidelity nature of the original model but also introduces the capability to securely hide and reveal audio within images.

---

## Installation

### Step 1: Install PyTorch

Visit the official [PyTorch website](https://pytorch.org/get-started/locally/) to choose the version that matches your hardware. For example, for CUDA 11.8:

```bash
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

> **Important:** Always verify compatibility on the official site before installation.

### Step 2: Install Additional Dependencies

Install the remaining libraries using pip:

```bash
pip install numpy librosa matplotlib soundfile torchvision pillow structlog streamlit
```

#### Dependency Breakdown

| Library     | Purpose                                          |
|-------------|--------------------------------------------------|
| numpy       | Numerical computations                           |
| librosa     | Audio processing and transformation            |
| matplotlib  | Visualization and spectrogram display           |
| soundfile   | Audio file handling                              |
| torchvision | Image transformations using PyTorch            |
| Pillow      | Image processing and conversions               |
| structlog   | Structured logging for debugging               |
| streamlit   | GUI framework for real-time interaction        |


### Additional Notes

- For CPU-only systems, install PyTorch with:

```bash
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
```

- Verify your installation with:

```bash
python3 -c "import torch; print('PyTorch Version:', torch.__version__)"
```

---

## Usage

### Cloning & Setup

Clone the repository and navigate to the project directory:

```bash
git clone https://github.com/danyalwg/DL-Audio-Stego.git
cd DL-Audio-Stego
```
### Download Pre-trained Checkpoints

Download the zipped checkpoint files from [google.com](google.com) and extract them into the `checkPoint` folder.

### Running the Application

Launch the Streamlit GUI to begin the embedding and extraction process:

```bash
streamlit run streamlit_app.py
```

This web-based interface provides an intuitive and interactive environment for processing audio steganography in real time.

---

## Code Structure

| File Name                | Functionality                                                       |
|--------------------------|---------------------------------------------------------------------|
| `convert_to_image.py`    | Converts an audio file into a 256×256 RGB image representation.     |
| `embed_audio_image.py`   | Embeds the audio image into a cover image using the deep learning model.|
| `extract_audio_image.py` | Extracts the hidden audio image from the stego-image.               |
| `convert_to_audio.py`    | Reconstructs the audio waveform from the recovered image.           |
| `audio_processing.py`    | Applies post-processing to enhance the recovered audio quality.       |
| `streamlit_app.py`       | Provides the GUI for user interaction with the system.              |

---

## Repository Layout

```plaintext
DL-Audio-Stego/
│   audio_processing.py
│   convert_to_audio.py
│   convert_to_image.py
│   embed_audio_image.py
│   extract_audio_image.py
│   streamlit_app.py
│   README.md
│   requirements.txt
│
├───checkPoint
│       netH_epoch_73,sumloss=0.000447,Hloss=0.000258.pth
│       netR_epoch_73,sumloss=0.000447,Rloss=0.000252.pth
│
├───models
│       HidingUNet.py
│       RevealNet.py
│       __init__.py
│       __pycache__/
│
├───utils
│       transformed.py
│       __pycache__/
│
└───__pycache__/
```

---

## Contributing

Contributions are highly welcome, Mr. Danyal! To contribute:

1. Fork the repository.
2. Create a new branch:

```bash
git checkout -b feature/YourFeature
```

3. Commit your changes:

```bash
git commit -m "Add new feature"
```

4. Push the branch:

```bash
git push origin feature/YourFeature
```

5. Open a pull request with detailed descriptions of your changes.

Please ensure that your contributions adhere to the project’s coding standards and that all documentation is kept up-to-date.

---

## License

This project is licensed under the MIT License. For full details, please refer to the [LICENSE](LICENSE) file.

---

## Acknowledgements

We extend our sincere gratitude to the open-source community and especially to the maintainers of [arnoweng/PyTorch-Deep-Image-Steganography](https://github.com/arnoweng/PyTorch-Deep-Image-Steganography) for their pioneering work. Their innovative approach to deep learning-based steganography has been instrumental in the development of this audio steganography system.

