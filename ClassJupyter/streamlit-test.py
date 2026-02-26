import streamlit as st
import torch
import torchvision.models as models
import torchvision.transforms as transforms
from PIL import Image
import json
import requests

st.title("PyTorch ResNet18 Image Classification")
st.write("Upload an image for classification using a pre-trained ResNet18 model.")

# Load ImageNet class names
@st.cache_resource
def load_classes():
    # Attempt to download the ImageNet class labels file if it doesn't exist
    try:
        with open('imagenet_classes.txt', 'r') as f:
            classes = [line.strip() for line in f.readlines()]
    except FileNotFoundError:
        st.error("imagenet_classes.txt not found. Please ensure it is available.")
        # You would typically download this file from a source like the PyTorch examples repo
        # For this example, we assume the file is present in the same directory
        classes = None
    return classes

# Load the pre-trained PyTorch model
@st.cache_resource
def load_model():
    # Load ResNet18 model and set to evaluation mode
    resnet18 = models.resnet18(weights=models.ResNet18_Weights.DEFAULT)
    resnet18.eval() # Set model to evaluation mode
    return resnet18

model = load_model()
classes = load_classes()

# Define image transformations
transform = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])

uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file).convert('RGB')
    st.image(image, caption='Uploaded Image', use_column_width=True)
    st.write("")
    st.write("Classifying...")

    # Preprocess the image
    img_t = transform(image)
    batch_t = torch.unsqueeze(img_t, 0)

    # Perform inference
    with torch.no_grad():
        outputs = model(batch_t)

    # Get probabilities and predicted class
    probabilities = torch.nn.functional.softmax(outputs, dim=1)[0] * 100
    top5_prob, top5_indices = torch.topk(probabilities, 5)

    if classes is not None:
        st.write("### Top 5 Predictions:")
        for i in range(top5_prob.size(0)):
            st.write(f"- **{classes[top5_indices[i]]}**: {top5_prob[i].item():.2f}%")
    else:
        st.write("Predictions could not be displayed due to missing class labels file.")

