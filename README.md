# de Frosty - AI Voice Assistant  


Frosty is a **voice-activated AI assistant** inspired by **JARVIS** from Iron Man. It is designed to run on a **circular touchscreen interface** and supports **voice commands for AI responses, weather updates, music playback (Spotify), system monitoring, and more**.  

## **🚀 Features**
👉 **Hotword Detection:** Say `"Frosty"` to wake up the assistant.  
👉 **Voice Recognition:** Understands and processes voice commands.  
👉 **Text-to-Speech (TTS):** Speaks responses using Microsoft David (US Male Voice).  
👉 **Chatbot Integration:** Uses **GPT-4 API** to answer queries.  
👉 **Real-time Weather Updates:** Fetches live weather data using OpenWeather API.  
👉 **Spotify Integration (Coming Soon):** Control music playback via voice.  
👉 **System Monitoring (Upcoming):** Check CPU usage, battery, RAM, and temperature.  
👉 **Circular UI Interface:** A visually appealing circular touchscreen UI.  
👉 **Multi-Command Mode:** Frosty stays active for multiple commands.  

---

## **📂 Project Structure**
```
ai_assistant/
 assets/              # Images, icons, and backgrounds
 ui/                  # UI components (PyQt6)
   ├─ main_window.py   # Main UI window (circular display)
   ├─ widgets.py       # Custom UI widgets
   └─ styles.qss       # CSS-like styles for UI
 core/                # Core functionalities
   ├─ voice.py         # Voice recognition & AI processing
   ├─ openai_api.py    # Chatbot logic (OpenAI API)
   ├─ spotify_api.py   # Spotify integration (Upcoming)
   ├─ weather_api.py   # Weather data fetching
   └─ system_monitor.py # CPU, RAM, battery stats (Upcoming)
 config/              # Configuration files
   └─ settings.py      # Stores API keys & settings
 resources/           # UI resources (icons, themes)
 main.py              # Main entry point to launch assistant
 requirements.txt     # Dependencies (PyQt6, OpenAI, etc.)
 .env                 # API keys (not included in repo)
 README.md            # Project documentation
```

---

## **🛠️ Installation & Setup**
### **1️⃣ Prerequisites**
Make sure you have the following installed:
- **Python 3.8+**  
- **pip (Python package manager)**  
- **A microphone** (for voice recognition)

---

### **2️⃣ Clone the Repository**
```bash
git clone https://github.com/siddhesh1008/HomePod.git
cd HomePod
```

---

### **3️⃣ Create a Virtual Environment**
```bash
# On Windows
python -m venv venv
venv\Scripts\activate

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

---

### **4️⃣ Install Dependencies**
```bash
pip install -r requirements.txt
```

---

### **5️⃣ Set Up API Keys**
#### **👉 OpenAI API Key (GPT-4)**
You need an OpenAI API key to enable AI responses.

1. Get your API key from **[OpenAI's website](https://platform.openai.com/)**.  
2. Create a `.env` file in the project root and add:
   ```
   OPENAI_API_KEY=your_openai_api_key_here
   ```

#### **👉 OpenWeather API Key**
For real-time weather updates:

1. Get your API key from **[OpenWeatherMap](https://home.openweathermap.org/api_keys)**.  
2. Add it to the `.env` file:
   ```
   WEATHER_API_KEY=your_weather_api_key_here
   ```

---

### **6️⃣ Run the Assistant**
```bash
python main.py
```
Once running, say **"Frosty"** to activate the assistant.

---

## **🗣️ Voice Commands (Examples)**
| Command | Description |
|---------|------------|
| **"Frosty"** | Wakes up the assistant |
| **"What’s the weather in Berlin?"** | Fetches real-time weather |
| **"Tell me a joke"** | AI tells a joke |
| **"Play some music"** | (Upcoming) Plays music via Spotify |
| **"What's my CPU usage?"** | (Upcoming) Checks system stats |
| **"Exit"** | Stops the assistant |

---

## **📝 Future Enhancements**
💡 **Spotify Music Playback** 🎵  
💡 **System Monitoring (CPU, RAM, Battery, Temp)** 💪  
💡 **To-Do List & Reminders** 🗓️  
💡 **Smart Home Integration (IoT)** 🏡  

---

## **💡 Troubleshooting**
### **1️⃣ Voice Recognition Not Working?**
- Ensure your microphone is **enabled and working**.
- Try increasing the timeout value in `voice.py`:
  ```python
  audio = recognizer.listen(source, timeout=6)
  ```

### **2️⃣ Weather Not Responding?**
- Check if **your OpenWeather API key is correct**.
- Run this test:
  ```bash
  python core/weather_api.py
  ```

### **3️⃣ OpenAI API Not Responding?**
- Ensure **you have API credits** on OpenAI.
- Run:
  ```bash
  python core/openai_api.py "Tell me a joke"
  ```

---

## **👨‍💻 Contributing**
Want to improve Frosty? Contributions are welcome!  

1. **Fork the repository**  
2. **Create a new branch** (`feature-new-feature`)  
3. **Commit your changes**  
4. **Push to GitHub** and submit a PR  

---

## **📚 License**
This project is licensed under the **MIT License**.

---

## **⭐ Support**
If you like this project, **give it a star ⭐ on GitHub!**  

