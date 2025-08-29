# Clean Meet AI 🚀

🌐 What is Clean Meet AI?

Clean Meet AI is a real-time content safety system for video conferencing. It continuously monitors video, audio, and text streams during online meetings to detect and prevent NSFW visuals, offensive speech, and toxic chat messages.

Works both as a standalone platform and as a plug-and-play integration with major conferencing tools like Zoom, Google Meet, and Microsoft Teams.

Uses deep learning models (computer vision, speech-to-text + toxicity detection, NLP) to analyze multimodal inputs.

Ensures privacy-first processing by handling everything in real-time without storing raw data.

---
<div style="display: flex; flex-wrap: wrap; gap: 10px; justify-content: center;">

  <img src="assets/arch1.jpeg" alt="Architecture" width="200"/>
  <img src="assets/videosc1.png" alt="Video Scan 1" width="200"/>
  <img src="assets/videosc2.png" alt="Video Scan 2" width="200"/>
  <img src="assets/textsc1.png" alt="Text Scan 1" width="200"/>
  <img src="assets/text2.png" alt="Text Scan 2" width="200"/>
  <img src="assets/audio1.png" alt="Audio Scan 1" width="200"/>
  <img src="assets/audio2.png" alt="Audio Scan 2" width="200"/>

</div>
## ✨ Features

- 🔍 **Standalone Product**  
  - Runs as a dedicated platform.  
  - Monitors all streams (video, audio, text) in real-time.  
  - Flags or blocks inappropriate content.  

- 🔗 **Integration Layer**  
  - Plug & play integration with any video conferencing system (Zoom, Google Meet, MS Teams, etc.).  
  ![Integration Platforms](assets/googleMeet_ing.jpeg)

- ⚡ **Multi-Modal Detection**  
  - **Video:** NSFW or inappropriate visual content.  
  - **Audio:** Offensive language or vulgar speech.  
  - **Text:** Toxic messages in chat.  

- 🔒 **Privacy First**  
  - All processing happens securely.  
  - No unnecessary data storage.  

---

## 🛠️ Tech Stack

- **Backend:** FastAPI (real-time APIs)  
- **Models:** Deep learning (NSFW detection, speech-to-text, toxicity classifiers)  
- **Video Integration:** OBS Virtual Camera / Conferencing APIs  
- **Frontend (Optional):** React-based dashboard for monitoring  

---
