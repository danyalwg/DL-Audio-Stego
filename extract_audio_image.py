import torch
import torchvision.transforms as transforms
from PIL import Image
import matplotlib.pyplot as plt

from models.RevealNet import RevealNet  # Import the Reveal model

def load_reveal_model():
    model = RevealNet(output_function=torch.nn.Sigmoid)
    model.load_state_dict(torch.load("./checkPoint/netR_epoch_73,sumloss=0.000447,Rloss=0.000252.pth", map_location="cpu"))
    model.eval()
    return model

reveal_model = load_reveal_model()

# Image transformation
transform = transforms.Compose([
    transforms.Resize((256, 256)),
    transforms.ToTensor()
])

def extract_image(stego_img_path, extracted_audio_img_path):
    """
    Takes a stego image and extracts the hidden spectrogram (audio image).
    """
    container_img = Image.open(stego_img_path).convert("RGB")
    container_tensor = transform(container_img).unsqueeze(0)

    with torch.no_grad():
        revealed_tensor = reveal_model(container_tensor)

    revealed_img = transforms.ToPILImage()(revealed_tensor.squeeze(0))
    revealed_img.save(extracted_audio_img_path)
    # Do not call plt.show() in non-interactive environments
    return extracted_audio_img_path
