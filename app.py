import streamlit as st
from PIL import Image, ImageDraw, ImageFont
from google import genai
import os
from pathlib import Path
import io # For in-memory file handling

# --- 1. CONFIGURATION ---
# ... (MODEL_NAME configuration lines) ...

# 1. Define the font filename (Now inside the static folder)
FONT_FILENAME = "static/Impact.ttf"  

# 2. Get the absolute path to the font file
# os.path.dirname(__file__) gets the directory of the current script (app.py)
script_dir = Path(os.path.dirname(os.path.abspath(__file__)))
# Path combines the script directory with the new font filename location
FONT_PATH = str(script_dir / FONT_FILENAME)


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
    """Draws the caption onto the bottom of the image, with wrapping and styling."""
    
    # Use a copy of the image for drawing
    draw = ImageDraw.Draw(image)
    img_w, img_h = image.size
    
    # 1. Define Font Size and Path
    # Define font size based on image height for proportionality (e.g., 8% of image height)
    font_size = int(img_h * 0.08) 
    
    # Font loading and fallback logic (Impact.ttf should be in the root)
    font = ImageFont.load_default() # Start with default as a guaranteed fallback
    try:
        # Attempt to load the custom font
        font = ImageFont.truetype(font_path, font_size)
    except IOError:
        st.warning(f"Custom font file not found. Using default font.")
        # If custom font fails, 'font' remains ImageFont.load_default()

    # 2. Text Wrapping and Formatting
    
    # Max width for text: 90% of the image width
    max_text_width = int(img_w * 0.9)
    
    # Function to check text width
    def get_text_dimensions(text, current_font):
        try:
            bbox = draw.textbbox((0, 0), text, font=current_font, spacing=0)
            return bbox[2] - bbox[0], bbox[3] - bbox[1]
        except Exception:
            # Fallback for old PIL versions
            return draw.textsize(text, font=current_font, spacing=0)

    # Simple word wrapping logic
    wrapped_lines = []
    current_line = ""
    for word in caption.split():
        test_line = f"{current_line} {word}".strip()
        test_w, _ = get_text_dimensions(test_line, font)

        if test_w <= max_text_width:
            current_line = test_line
        else:
            wrapped_lines.append(current_line)
            current_line = word
    wrapped_lines.append(current_line)
    
    final_caption = "\n".join(wrapped_lines)
    
    # Recalculate dimensions for the final wrapped text
    text_w, text_h = get_text_dimensions(final_caption, font)
    
    # 3. Position Text (Centered)
    
    # Vertical position: 5% padding from the bottom
    x = (img_w - text_w) / 2
    y = img_h - text_h - int(img_h * 0.05) 
    
    # 4. Draw a Black Stroke (Outline) for Readability
    stroke_color = "black"
    fill_color = "white"
    
    # Proportional stroke width based on font size
    stroke_width = max(1, int(font_size / 20)) 
    
    # Draw stroke multiple times for a clear outline
    for adj_x in range(-stroke_width, stroke_width + 1):
        for adj_y in range(-stroke_width, stroke_width + 1):
            if adj_x == 0 and adj_y == 0:
                continue # Skip the center
            draw.text((x + adj_x, y + adj_y), final_caption, font=font, fill=stroke_color, align="center")

    # 5. Draw the Main Text
    draw.text((x, y), final_caption, font=font, fill=fill_color, align="center")
    
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


