# 😂 AI Meme & Poster Creator

AI Meme & Poster Creator Using Streamlit and Gemini

An AI-powered web app that automatically generates  funny memes or posters from any image and topic using Google Gemini AI and Streamlit.  
This project helps students and creators easily design memes without needing design or coding skills!

---

## 🚀 Features
- 🧠 AI Caption Generation:Generates short, funny captions using Gemini AI.  
- 🖼️ Automatic Meme Creation: Adds AI-generated text directly on your uploaded image.  
- 🎨 Clean Streamlit Interface: Simple UI for instant results.  
- 💾 Download Option: Save your generated meme as an image file.  
- 🔒 Secure API Key: Managed using `.streamlit/secrets.toml`.

---

## 🧩 Tech Stack

Frontend - Streamlit 

Backend AI Model - Google Gemini 2.5 Flash

Image Editing - Python PIL (Pillow)

Language - Python 3

Hosting - Streamlit Cloud 

---

## 🚀 Installation & Setup

1️⃣  Clone the Repository
   
   Bash
   
   git clone <your-repo-url>
   cd ai-meme-and-poster

2️⃣ Set up the Environment

Bash

pip install -r requirements.txt

3️⃣ Configure the API Key

GEMINI_API_KEY="AIzaSyChgILNWbwq2G1UzRUMkggGJmO5sQ_apmo"

Streamlit Cloud Deployment: Create a directory named .streamlit and a file inside it named secrets.toml.

▶️ How to Run the App

streamlit run app.py
The app will open in your default web browser

---

## 👨‍💻 How to Use

**Upload Image:** Use the file uploader in the sidebar to select a base image.

**Enter Topic:** Type a topic (e.g., "Mondays," "When the code finally runs") into the text box.

**Generate Meme:** Click the **"Generate Meme 🎨"** button.

The application will call the Gemini API, display the generated caption, and render the final meme image.

Click the **"Download Meme"** button to save the result.

---

## 🧠 Example Output

**Topic:** Exam Stress

**Image:** Student holding books

**AI Generated Meme:**
"When you study all night and still forget your name on the exam!"

---

## 🔑 Built for Streamlit Community Cloud and Gemini

![image alt](https://github.com/VishnupriyaS19/AI-MEME-AND-POSTER/blob/2ad61f37b06acfa41195b5d0753705d07289744b/AIMEME%20AND%20POSTER.jpg)

---

## 🎥 Demo

🔗https://ai-meme-and-poster-bb7tr4yydkbyerstain5bv.streamlit.app/ -[LIVE DEPLOYMENT LINK]


---

## 🔮 Future Scope

This project can be expanded and improved in several exciting ways:

1. **AI Caption Style Selection:**  
   Allow users to choose between funny, motivational, sarcastic, or inspirational meme styles.

2. **Auto Image Suggestions:** 
   Integrate an AI image generator (like Imagen or DALL·E) to automatically create meme backgrounds.

3. **Multi-Language Support:**  
   Enable meme generation in regional languages such as Hindi, Tamil, or Telugu.

4. **Meme Templates Library:**  
   Add a collection of popular meme templates for quick selection and automatic caption placement.

5. **Cloud Storage Integration:**  
   Store generated memes in AWS



