# utils/donut_extractor.py

from transformers import DonutProcessor, VisionEncoderDecoderModel
from PIL import Image
import torch
import re

# Load pretrained Donut model
processor = DonutProcessor.from_pretrained("naver-clova-ix/donut-base")
model = VisionEncoderDecoderModel.from_pretrained("naver-clova-ix/donut-base")

# Use GPU if available
device = "cuda" if torch.cuda.is_available() else "cpu"
model.to(device)

def extract_fields(image_path):
    """
    Takes invoice image path
    Returns structured extracted fields
    """

    image = Image.open(image_path).convert("RGB")

    pixel_values = processor(image, return_tensors="pt").pixel_values
    pixel_values = pixel_values.to(device)

    # Generate text from Donut
    outputs = model.generate(pixel_values, max_length=512)
    decoded = processor.batch_decode(outputs, skip_special_tokens=True)[0]

    # Clean output
    decoded = decoded.replace("<s>", "").replace("</s>", "").strip()

    # Simple regex-based post parsing
    fields = {
        "raw_text": decoded
    }

    return fields
