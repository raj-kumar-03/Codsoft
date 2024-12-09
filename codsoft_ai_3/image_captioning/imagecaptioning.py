'''
Image captioning model with LLM
BY RAJKUMAR
Codsoft_UID: CS24NY339750
'''


import os
from dotenv import find_dotenv, load_dotenv
from transformers import pipeline
import streamlit as st

# Load environment variables
load_dotenv(find_dotenv())


# 1. Image to text implementation (Image Captioning) with HuggingFace
def image_to_text(image_path):
    # Load the image-to-text model
    pipe = pipeline(
        "image-to-text",
        model="Salesforce/blip-image-captioning-large",
        max_new_tokens=1000,
    )
    # Generate caption
    text = pipe(image_path)[0]["generated_text"]
    return text


# Streamlit app for image captioning
def main():
    st.title("Image Captioning 🖼️")
    st.header("Upload an image and get its caption")

    # Upload image
    upload_file = st.file_uploader("Choose an image:", type=["jpg", "png"])

    if upload_file is not None:
        # Display the uploaded image
        st.image(
            upload_file,
            caption="Uploaded Image",
            use_column_width=True
        )

        # Save the image temporarily
        file_bytes = upload_file.getvalue()
        temp_image_path = f"temp_{upload_file.name}"
        with open(temp_image_path, "wb") as file:
            file.write(file_bytes)

        # Perform image captioning
        st.write("Generating caption...")
        caption = image_to_text(temp_image_path)
        st.success("Caption generated!")

        # Display the caption
        st.subheader("Caption")
        st.write(caption)


# Invoking main function
if __name__ == "__main__":
    main()
