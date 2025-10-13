# AI-MEME-AND-POSTER
AI Meme & Poster Creator Using Streamlit and Gemini

# 😂 AI Meme & Poster Creator

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

## 📂 Project Structure

ai-meme-generator/
├── app.py # Main Streamlit app
├── requirements.txt # Dependencies list
└── .streamlit/
└── secrets.toml # Stores API key securely

🚀 Installation & Setup
1️⃣  Clone the Repository
   
   Bash
   git clone <your-repo-url>
   cd ai-meme-and-poster

2️⃣ Set up the Environment

Bash
pip install -r requirements.txt

3️⃣ Configure the API Key

GEMINI_API_KEY="YOUR_API_KEY_HERE"

Streamlit Cloud Deployment: Create a directory named .streamlit and a file inside it named secrets.toml. Add your key as follows:
# .streamlit/secrets.toml
GEMINI_API_KEY="YOUR_API_KEY_HERE"

▶️ How to Run the App

streamlit run app.py
The app will open in your default web browser

👨‍💻 How to Use
Upload Image: Use the file uploader in the sidebar to select a base image.

Enter Topic: Type a topic (e.g., "Mondays," "When the code finally runs") into the text box.

Generate Meme: Click the "Generate Meme 🎨" button.

The application will call the Gemini API, display the generated caption, and render the final meme image.

Click the "Download Meme" button to save the result.

🧠 Example Output
Topic: Exam Stress

Image: Student holding books

AI Generated Meme:
"When you study all night and still forget your name on the exam!"





