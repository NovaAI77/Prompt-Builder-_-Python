# Prompt Suffix Reference

A lightweight desktop app for browsing, searching, and building image generation prompt suffixes — with a built-in AI prompt finalizer powered by your choice of local or cloud LLM.

![Python](https://img.shields.io/badge/python-3.8%2B-blue) ![License](https://img.shields.io/badge/license-MIT-green) ![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey)

---

## Features

- 👤 **Character builder** — role, backstory, age, ethnicity, hair, eyes, face, markings, expression, emotion, clothing, accessories
- 🌍 **Setting builder** — lighting, location, weather, camera, style, mood, sound/texture, scale, time, render, color
- 🎲 **Random generators** — separate random character and random setting buttons
- 🔒 **Lock tokens** — right-click any tag to lock it; locked tokens survive Clear and are skipped by Random
- ⭐ **Favourites** — double-click any tag to favourite it; Random picks favourites first; saved between sessions
- ✏️ **Subject prefix** — type your subject ("a woman", "a samurai") and it prepends to the combined prompt
- ⚡ **Combined output** — character + setting merged into one copyable prompt string
- 💾 **Export to .txt** — save your prompt to a text file
- ✨ **AI Finalize** — send your prompt to a local or cloud LLM to polish it into a final image gen prompt

---

## Requirements

- Python 3.8 or higher
- `tkinter` (bundled with Python on Windows and macOS — see Linux note below)
- `pyperclip`

---

## Installation

**1. Clone the repo**

```bash
git clone https://github.com/YOUR_USERNAME/prompt-suffix-ref.git
cd prompt-suffix-ref
```

**2. Install dependencies**

Use the **same Python you'll run the script with**:

```bash
python -m pip install -r requirements.txt
```

> ⚠️ **Windows tip:** If you have multiple Python installs (e.g. Anaconda + Python 3.12), always use the full path to the Python executable for both pip install and running the script:
> ```bash
> C:\Python312\python.exe -m pip install -r requirements.txt
> C:\Python312\python.exe prompt_suffixes.py
> ```

---

## Usage

```bash
python prompt_suffixes.py
```

---

## Linux — tkinter note

`tkinter` is not always bundled on Linux. Install it with:

```bash
# Debian / Ubuntu
sudo apt install python3-tk

# Fedora
sudo dnf install python3-tkinter

# Arch
sudo pacman -S tk
```

---

## How to use

### Building a prompt

1. Browse the **Character** and **Setting** columns — click any tag to add it to your builder
2. **Right-click** a tag to add it locked (🔒), so Random won't replace it
3. **Double-click** a tag to ⭐ favourite it — favourites are highlighted yellow and Random picks them first
4. Type a subject in the **prefix box** (e.g. "a lone warrior") — it prepends to the combined output
5. Hit **🎲 Random Character** or **🎲 Random Setting** to auto-fill from the tag library
6. Click **📋 Copy Combined Prompt** or **💾 Export to .txt** to use your prompt

### AI Finalize

Click **✨ AI Finalize Prompt** to open the finalize window. It takes your combined prompt and rewrites it into a polished, vivid image generation prompt using your choice of LLM.

See the [AI Finalize setup section](#ai-finalize-setup) below for how to connect each LLM.

---

## AI Finalize Setup

The AI Finalize window lets you pick from four LLM options. The system instruction is fully editable — customize it to change how the AI rewrites your prompt.

---

### 🖥 LM Studio (default — local, no API key)

LM Studio runs models locally on your machine. No internet required, no API key needed.

**Setup:**

1. Download and install LM Studio from [lmstudio.ai](https://lmstudio.ai)
2. Open LM Studio and download a model (recommended: `Mistral 7B Instruct`, `Llama 3 8B Instruct`, or any instruct model)
3. Click the **Local Server** tab (the `<->` icon on the left sidebar)
4. Click **Start Server** — it will start on port `1234` by default

**In the app:**

- Select **LM Studio (local)** from the dropdown (it's the default)
- Leave the **Model** field blank to use whichever model is loaded in LM Studio, or type a specific model name
- Leave **Port** as `1234` unless you've changed it in LM Studio settings
- Click **✨ Finalize**

> **Tip:** LM Studio must have a model loaded and the server running before you click Finalize. If you get a connection error, check that the server tab shows "Server is running".

---

### 🦙 Ollama (local, no API key)

Ollama runs open-source models locally via a simple command-line tool.

**Setup:**

1. Download and install Ollama from [ollama.com](https://ollama.com)
2. Open a terminal and pull a model:
   ```bash
   ollama pull llama3
   ```
   Other good options: `mistral`, `phi3`, `gemma2`
3. Start the Ollama server:
   ```bash
   ollama serve
   ```
   It runs on port `11434` by default.

**In the app:**

- Select **Ollama (local)** from the dropdown
- Type your model name in the **Model** field (e.g. `llama3`, `mistral`)
- Click **✨ Finalize**

> **Tip:** `ollama serve` must be running in a terminal before you click Finalize. On macOS, Ollama may start automatically in the menu bar after installation.

---

### ⚡ Groq (free cloud API — very fast)

Groq offers a free API tier with extremely fast inference on Llama and Mixtral models.

**Setup:**

1. Go to [console.groq.com](https://console.groq.com) and sign up for a free account
2. Navigate to **API Keys** and click **Create API Key**
3. Copy the key — you'll only see it once

**In the app:**

- Select **Groq (free API)** from the dropdown
- The **Model** field defaults to `llama3-8b-8192` — other good free options:
  - `llama3-70b-8192` (smarter, slightly slower)
  - `mixtral-8x7b-32768` (great for longer prompts)
  - `gemma2-9b-it`
- Paste your API key into the **API Key** field
- Click **✨ Finalize**

> **Free tier limits:** Groq's free tier is generous for personal use — check [console.groq.com/settings/limits](https://console.groq.com/settings/limits) for current rate limits.

---

### 🌐 OpenRouter (free cloud API — many models)

OpenRouter gives you access to dozens of models including free-tier options from Meta, Mistral, Google and others.

**Setup:**

1. Go to [openrouter.ai](https://openrouter.ai) and sign up for a free account
2. Navigate to **Keys** and click **Create Key**
3. Copy the key

**In the app:**

- Select **OpenRouter (free API)** from the dropdown
- The **Model** field defaults to `mistralai/mistral-7b-instruct:free` — other free models to try:
  - `meta-llama/llama-3-8b-instruct:free`
  - `google/gemma-2-9b-it:free`
  - `mistralai/mistral-nemo:free`
  - Browse all free models at [openrouter.ai/models?q=free](https://openrouter.ai/models?q=free)
- Paste your API key into the **API Key** field
- Click **✨ Finalize**

> **Note:** Free models on OpenRouter may have rate limits or occasional availability issues. If one model fails, try another from the free list.

---

## Customizing the system instruction

The **System instruction** box in the AI Finalize window tells the LLM how to rewrite your prompt. The default is optimized for image generation, but you can change it for different use cases:

**Default (image gen):**
```
You are an expert image generation prompt writer. The user will give you a list of descriptive tags and suffixes. Rewrite them into a single, polished, vivid image generation prompt. Keep it concise but detailed. Optimize for visual clarity and impact. Output ONLY the final prompt text, no explanation, no preamble.
```

**For video/animation:**
```
You are an expert at writing prompts for AI video generation tools like Sora and Kling. Rewrite the user's tags into a flowing, cinematic scene description with camera movement and atmosphere. Output ONLY the prompt, no preamble.
```

**For more artistic/painterly output:**
```
You are an art director. Rewrite the user's tags as a detailed artist's brief — rich with texture, light quality, and compositional direction. Output ONLY the brief, no preamble.
```

---

## Adding your own suffixes

Open `prompt_suffixes.py` and find the `CHARACTER_SUFFIXES` or `SETTING_SUFFIXES` list. Each entry follows this pattern:

```python
{
    "id": 200,
    "cat": "my_category",
    "label": "My Category Label",
    "desc": "Short description of what this controls",
    "examples": ["example one", "example two", "example three"],
},
```

To add a new category, also add entries to the matching `CAT_COLORS` and `CAT_TEXT` dicts:

```python
CHAR_CAT_COLORS["my_category"] = "#fde8d8"
CHAR_CAT_TEXT["my_category"]   = "#7c2d12"
```

Restart the app and the new tab and cards appear automatically.

---

## Project structure

```
prompt-suffix-ref/
├── prompt_suffixes.py   # main app
├── requirements.txt     # pyperclip
├── favourites.json      # auto-created when you star your first tag
└── README.md
```

---

## License

MIT — free to use, modify, and share.
