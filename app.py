import streamlit as st
from PIL import Image, ImageDraw, ImageFont
from google import genai
import os
from pathlib import Path
import io # For in-memory file handling

# --- 1. CONFIGURATION ---

# Set your model name (ensure you have the GEMINI_API_KEY set as a secret on Streamlit Cloud)
MODEL_NAME = 'gemini-2.5-flash'


# If the font is not found, the script will automatically use the default bitmap font.
# If you uploaded a font (e.g., 'Impact.ttf'), change the line below.
# 1. Define the font filename
FONT_FILENAME = "Impact.ttf"

# 2. Get the absolute path to the font file
# os.path.dirname(__file__) gets the directory of the current script (app.py)
# Path combines this directory with the font filename
FONT_PATH = str(Path(os.path.dirname(os.path.abspath(__file__))) / FONT_FILENAME)


# --- 2. GENERATIVE AI FUNCTION ---

def generate_caption(topic):
    """Generates a caption using the Gemini API."""
    
    # 1. EXPLICITLY CHECK FOR THE API KEY IN STREAMLIT SECRETS
    if "GEMINI_API_KEY" not in st.secrets:
        return "AI Caption Error: 'GEMINI_API_KEY' not found in Streamlit secrets. Please check your .streamlit/secrets.toml file."
    
    try:
        # 2. INITIALIZE CLIENT
        # Pass the key explicitly for the most robust connection:
        client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])
        
        prompt = (
            f"Generate a single, short, funny, and relatable meme caption "
            f"based on the following topic: '{topic}'. "
            f"Only return the caption text, nothing else."
        )
        
        # 3. USE THE CORRECT GENERATION CALL
        response = client.models.generate_content(
            model=MODEL_NAME, 
            contents=prompt
        )
        
        # Clean the output 
        caption = response.text.strip().replace('"', '')
        
        # Extract only the first line/suggestion if the model gives multiple
        return caption.split('\n')[0].strip()
        
    except Exception as e:
        # If any other API or network error occurs, return the specific error
        return f"AI Caption Error: Could not connect to Gemini. ({e})"

# --- 3. IMAGE PROCESSING FUNCTION (Meme Creator) ---

def add_caption(image, caption, font_path=FONT_PATH):
    """Draws the caption onto the bottom of the image."""
    draw = ImageDraw.Draw(image)
    img_w, img_h = image.size
    
    # Define font size based on image height for proportionality (e.g., 8% of image height)
    # Let's make it a bit larger, maybe 10%
    font_size = int(img_h * 0.10) 

    # Font loading and fallback logic
    font = ImageFont.load_default() # Start with default as a guaranteed fallback
    try:
        # Attempt to load the custom font with the calculated size
        # Add a print statement to debug on Streamlit Cloud logs
        print(f"Attempting to load font from: {font_path}") 
        font = ImageFont.truetype(font_path, font_size)
        print("Custom font loaded successfully!")
    except IOError:
        st.warning(f"Custom font file not found at {font_path}. Using default font. "
                   f"Ensure '{os.path.basename(font_path)}' is in your repo's root.")
        # If custom font fails, 'font' remains ImageFont.load_default()
    
    # 2. Measure text
    # Pillow's textbbox is the modern way; textsize is deprecated
    try:
        bbox = draw.textbbox((0, 0), caption, font=font, spacing=0) # Added spacing=0
        text_w = bbox[2] - bbox[0]
        text_h = bbox[3] - bbox[1]
    except Exception as e:
        # Fallback for old PIL versions or load_default() incompatibility
        st.error(f"Error measuring text: {e}. Using estimated dimensions.")
        text_w, text_h = draw.textsize(caption, font=font, spacing=0) # Added spacing=0

    # Handle very long captions by potentially reducing font size or wrapping
    if text_w > img_w * 0.9: # If text is too wide, try to scale down or wrap
        st.warning("Caption is very long. Attempting to reduce font size for fit.")
        font_size = int(font_size * (img_w * 0.9 / text_w))
        try:
            font = ImageFont.truetype(font_path, font_size)
        except IOError:
            font = ImageFont.load_default()
        
        try: # Recalculate dimensions with new font size
            bbox = draw.textbbox((0, 0), caption, font=font, spacing=0)
            text_w = bbox[2] - bbox[0]
            text_h = bbox[3] - bbox[1]
        except Exception:
            text_w, text_h = draw.textsize(caption, font=font, spacing=0)


    # 3. Position text (centered horizontally, near the bottom)
    x = (img_w - text_w) / 2
    y = img_h - text_h - int(img_h * 0.05) # 5% padding from bottom
    
    # 4. Draw a black stroke (outline) for readability
    stroke_color = "black"
    fill_color = "white"
    # Proportional stroke width, adjusted slightly
    stroke_width = max(1, int(font_size / 20)) 
    
    # Draw stroke multiple times for a thicker effect
    for adj_x in range(-stroke_width, stroke_width + 1):
        for adj_y in range(-stroke_width, stroke_width + 1):
            if adj_x == 0 and adj_y == 0:
                continue # Skip the center
            draw.text((x + adj_x, y + adj_y), caption, font=font, fill=stroke_color)

    # 5. Draw the main text
    draw.text((x, y), caption, font=font, fill=fill_color)
    
    return image

       
    
# --- 4. STREAMLIT APPLICATION LAYOUT ---

st.title("🤖 AI Meme & Poster Creator")
st.markdown("Upload a base image, enter a topic, and let Gemini create the caption!")

# Sidebar for controls (or you can use main area)
with st.sidebar:
    st.header("1. Upload Image")
    uploaded_file = st.file_uploader("Choose an image file", type=['png', 'jpg', 'jpeg'])

    st.header("2. Define Topic")
    topic = st.text_input("Enter a topic (e.g., 'Exam Stress', 'Friday Feeling','college life',etc.,)")
    
    st.markdown("---")
    generate_button = st.button("Generate Meme 🎨", type="primary")

# --- MAIN EXECUTION ---

if uploaded_file:
    # Load the image from the uploader using in-memory file handling
    base_image = Image.open(io.BytesIO(uploaded_file.read())).convert("RGB")
    
    # Display the image preview
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Base Image")
        st.image(base_image, caption="Original Image", use_column_width=True)

    if generate_button:
        with st.spinner("Generating caption with Gemini..."):
            # A. Generate the caption
            caption_text = generate_caption(topic)
            
        st.info(f"Generated Caption: {caption_text}")

        # B. Process the image
        if not caption_text.startswith("AI Caption Error"):
            with st.spinner("Adding caption to image..."):
                # Use a fresh copy of the image for drawing
                meme_image = add_caption(base_image.copy(), caption_text)
            
            # C. Display the result
            with col2:
                st.subheader("Generated Meme")
                st.image(meme_image, caption="AI-Generated Meme", use_column_width=True)

            # D. Download button - Uses in-memory BytesIO
            buffer = io.BytesIO()
            meme_image.save(buffer, format="PNG")
            buffer.seek(0)
            
            st.download_button(
                label="Download Meme",
                data=buffer,
                file_name="ai_generated_meme.png",
                mime="image/png"
            )
        else:
            # Display the error if AI failed
            st.error(caption_text) 

else:
    st.info("Please upload an image and enter a topic in the sidebar to begin.")

