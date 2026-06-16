import tkinter as tk
from tkinter import ttk, filedialog
import pyperclip
import random
import json
import os
import threading
import urllib.request
import urllib.error

# ── Data ──────────────────────────────────────────────────────────────────────

CHARACTER_SUFFIXES = [
    {"id": 101, "cat": "role",       "label": "Role & archetype",     "desc": "The kind of character in the scene",
     "examples": ["ancient warrior", "rogue AI android", "street merchant", "fallen angel", "cyberpunk hacker",
                  "wandering monk", "rebel soldier", "court jester", "sea captain", "bounty hunter",
                  "disgraced noble", "last of their kind", "hunted fugitive", "reluctant chosen one"]},
    {"id": 102, "cat": "backstory",  "label": "Backstory hint",       "desc": "Narrative depth for the character",
     "examples": ["exiled from their homeland", "carries a secret wound", "searching for someone lost",
                  "once powerful now broken", "betrayed by their own kind", "raised by wolves",
                  "sole survivor", "living under a false name", "haunted by their past"]},
    {"id": 103, "cat": "age",        "label": "Age & build",          "desc": "Physical presence and life stage",
     "examples": ["weathered elder", "lithe teenager", "stocky and scarred", "willowy and tall",
                  "imposing giant", "wiry middle-aged", "youthful early 20s", "aged beyond their years"]},
    {"id": 104, "cat": "ethnicity",  "label": "Ethnicity & skin tone", "desc": "Descriptive skin and heritage details",
     "examples": ["deep ebony skin", "warm olive complexion", "pale porcelain skin", "rich brown skin",
                  "sun-bronzed", "cool ivory tone", "golden-brown complexion", "freckled fair skin"]},
    {"id": 105, "cat": "hair",       "label": "Hair",                 "desc": "Style, color and length of hair",
     "examples": ["silver braided hair", "shaved head", "wild dreadlocks hair", "jet black undercut hair",
                  "fiery red curls hair", "platinum blonde bob hair", "long salt-and-pepper hair",
                  "tousled dark waves hair", "closely cropped natural hair"]},
    {"id": 106, "cat": "eyes",       "label": "Eyes",                 "desc": "Eye color, shape and quality",
     "examples": ["piercing green eyes", "dark almond-shaped eyes", "milky blind eye", "glowing cybernetic eyes",
                  "deep-set amber eyes", "wide silver eyes", "heterochromia", "heavy-lidded dark eyes",
                  "cold steel-blue eyes", "warm honey-brown eyes"]},
    {"id": 107, "cat": "face",       "label": "Facial features",      "desc": "Distinctive face details",
     "examples": ["sharp jawline", "high cheekbones", "broad flat nose", "full lips",
                  "prominent brow", "delicate features", "weathered wrinkles", "strong Roman nose"]},
    {"id": 108, "cat": "markings",   "label": "Body markings",        "desc": "Scars, tattoos, paint and marks",
     "examples": ["ritual facial scarring", "full sleeve tattoo", "war paint", "burn scars on neck",
                  "intricate henna patterns", "tribal markings", "dueling scar across cheek",
                  "faded prison tattoos", "glowing runic brands"]},
    {"id": 109, "cat": "expression", "label": "Expression & energy",  "desc": "The mood and presence they project",
     "examples": ["intense piercing gaze", "warm disarming smile", "cold and unreadable",
                  "mischievous smirk", "haunted distant look", "fierce determination",
                  "quiet dignity", "playful raised eyebrow"]},
    {"id": 110, "cat": "emotion",    "label": "Inner emotion",        "desc": "What the character is feeling in the moment",
     "examples": ["barely contained rage", "deep sorrow", "nervous excitement", "hollow emptiness",
                  "fierce pride", "desperate hope", "quiet resolve", "overwhelming guilt", "joy breaking through pain"]},
    {"id": 111, "cat": "clothing",   "label": "Clothing & costume",   "desc": "What the character is wearing",
     "examples": ["tattered battle cloak", "sleek black bodysuit", "ornate ceremonial armor",
                  "oversized trench coat", "futuristic streetwear", "flowing silk robes",
                  "worn leather jacket", "Victorian frock coat", "neon-lit hoodie"]},
    {"id": 112, "cat": "accessories","label": "Accessories & marks",  "desc": "Details that define the character",
     "examples": ["glowing cybernetic eye", "ancient runic scars", "gold septum ring",
                  "round wire-frame glasses", "missing left ear", "intricate neck tattoo",
                  "mechanical prosthetic arm", "ornate headdress", "worn dog tags"]},
]

SETTING_SUFFIXES = [
    # LIGHTING
    {"id": 1,  "cat": "lighting", "label": "Lighting type",       "desc": "Sets the quality and source of light",
     "examples": ["golden hour", "neon lights", "candlelight", "overcast", "rim lighting",
                  "studio lighting", "bioluminescent", "LED backlight", "firelight"]},
    {"id": 2,  "cat": "lighting", "label": "Lighting direction",  "desc": "Where the light comes from",
     "examples": ["front-lit", "side-lit", "backlit", "top-down lighting", "underlit"]},
    {"id": 3,  "cat": "lighting", "label": "Lighting mood",       "desc": "Emotional quality of the light",
     "examples": ["dramatic chiaroscuro", "soft diffused", "harsh shadows", "ethereal glow", "moody low-key"]},
    # LOCATION
    {"id": 4,  "cat": "location", "label": "Environment",         "desc": "The setting or world the subject inhabits",
     "examples": ["dense rainforest", "abandoned warehouse", "mountain summit", "underwater cave",
                  "Tokyo alleyway", "lavender field", "floating sky city", "arctic tundra"]},
    {"id": 5,  "cat": "location", "label": "Interior setting",    "desc": "Indoor scenes and spaces",
     "examples": ["cozy library", "brutalist office", "Victorian parlor", "space station corridor",
                  "cathedral interior", "neon-lit diner", "underground bunker"]},
    {"id": 6,  "cat": "location", "label": "Landscape scale",     "desc": "Conveys vastness or intimacy of space",
     "examples": ["wide open plains", "claustrophobic tunnels", "towering cliffs",
                  "intimate courtyard", "infinite expanse", "cramped rooftop"]},
    # WEATHER
    {"id": 7,  "cat": "weather",  "label": "Weather",             "desc": "Atmospheric weather conditions",
     "examples": ["heavy downpour", "thick fog", "blizzard", "scorching heat haze", "electrical storm",
                  "light drizzle", "tornado on the horizon", "ash falling like snow", "dead calm"]},
    # CAMERA
    {"id": 8,  "cat": "camera",   "label": "Shot type",           "desc": "Framing and distance from subject",
     "examples": ["extreme close-up", "full body shot", "aerial overhead", "Dutch angle",
                  "over-the-shoulder", "worm's eye view", "mid shot"]},
    {"id": 9,  "cat": "camera",   "label": "Lens & focal length", "desc": "Optical characteristics",
     "examples": ["35mm film", "fisheye lens", "telephoto compression", "tilt-shift", "macro lens"]},
    {"id": 10, "cat": "camera",   "label": "Camera settings",     "desc": "Technical photographic qualities",
     "examples": ["shallow depth of field", "long exposure", "bokeh", "motion blur", "f/1.4", "ISO 3200 grain"]},
    # STYLE
    {"id": 11, "cat": "style",    "label": "Art movement",        "desc": "Historical or contemporary visual styles",
     "examples": ["Art Nouveau", "Bauhaus", "Surrealist", "Ukiyo-e", "Brutalist", "Impressionist", "Memphis Design"]},
    {"id": 12, "cat": "style",    "label": "Medium & technique",  "desc": "Physical or digital artistic medium",
     "examples": ["oil painting", "watercolor wash", "pencil sketch", "woodblock print",
                  "digital matte painting", "charcoal"]},
    {"id": 13, "cat": "style",    "label": "Visual aesthetic",    "desc": "Overall look and feel shorthand",
     "examples": ["dark academia", "cottagecore", "Y2K", "vaporwave", "wabi-sabi", "solarpunk", "cyberpunk noir"]},
    {"id": 14, "cat": "style",    "label": "Render style",        "desc": "How the image is produced or looks produced",
     "examples": ["photorealistic", "cel-shaded", "pixel art", "low poly", "concept art", "storybook illustration"]},
    # MOOD
    {"id": 15, "cat": "mood",     "label": "Emotional tone",      "desc": "The feeling the image should evoke",
     "examples": ["melancholic", "triumphant", "eerie", "serene", "frantic", "nostalgic", "foreboding", "whimsical"]},
    {"id": 16, "cat": "mood",     "label": "Atmosphere",          "desc": "The pervasive sensory quality",
     "examples": ["hazy and dreamlike", "crisp and cold", "humid jungle air", "electric tension", "peaceful stillness"]},
    # SOUND / TEXTURE
    {"id": 17, "cat": "texture",  "label": "Sound & texture",     "desc": "Sensory details great for video/animation prompts",
     "examples": ["echoing silence", "distant thunder rumbling", "crackling fire", "howling wind",
                  "dripping water", "crowd murmur", "white noise static", "eerie hum"]},
    # SCALE
    {"id": 18, "cat": "scale",    "label": "Scale & framing",     "desc": "How the subject relates to their surroundings",
     "examples": ["human dwarfed by surroundings", "tight claustrophobic frame", "subject fills the frame",
                  "tiny figure in vast landscape", "looming presence", "eye-level intimate"]},
    # TIME
    {"id": 19, "cat": "time",     "label": "Time of day",         "desc": "When during the day the scene is set",
     "examples": ["blue hour", "high noon", "twilight", "midnight", "dawn mist", "late afternoon"]},
    {"id": 20, "cat": "time",     "label": "Era & period",        "desc": "Historical or futuristic time period",
     "examples": ["1970s", "far future", "medieval", "post-apocalyptic", "Victorian era", "retrofuturistic 1950s"]},
    # RENDER
    {"id": 21, "cat": "render",   "label": "Quality modifiers",   "desc": "General quality and detail boosters",
     "examples": ["highly detailed", "8K", "intricate", "sharp focus", "ultra-realistic", "professional"]},
    {"id": 22, "cat": "render",   "label": "Composition",         "desc": "How elements are arranged",
     "examples": ["rule of thirds", "symmetrical", "layered depth", "negative space", "dynamic diagonal", "golden ratio"]},
    {"id": 23, "cat": "render",   "label": "Texture & surface",   "desc": "Surface quality of materials",
     "examples": ["weathered stone", "wet glass", "iridescent scales", "brushed metal", "rough bark", "silk"]},
    # COLOR
    {"id": 24, "cat": "color",    "label": "Color palette",       "desc": "Overall color scheme",
     "examples": ["monochromatic blue", "earth tones", "neon on black", "muted pastels", "high contrast", "analogous warm"]},
    {"id": 25, "cat": "color",    "label": "Color temperature",   "desc": "Warm vs cool visual feel",
     "examples": ["warm amber tones", "cool blue cast", "neutral daylight", "warm shadows cool highlights"]},
]

CHAR_CAT_COLORS = {
    "role": "#fce7f3", "backstory": "#fdf2f8", "age": "#fef3c7", "ethnicity": "#fde8d8",
    "hair": "#ede9fe", "eyes": "#e0f2fe", "face": "#dbeafe", "markings": "#fef9c3",
    "expression": "#d1fae5", "emotion": "#ecfdf5", "clothing": "#fee2e2", "accessories": "#f0f9ff",
}
CHAR_CAT_TEXT = {
    "role": "#9d174d", "backstory": "#701a75", "age": "#92400e", "ethnicity": "#7c2d12",
    "hair": "#4c1d95", "eyes": "#0c4a6e", "face": "#1e40af", "markings": "#713f12",
    "expression": "#065f46", "emotion": "#064e3b", "clothing": "#991b1b", "accessories": "#0369a1",
}
SET_CAT_COLORS = {
    "lighting": "#dbeafe", "location": "#d1fae5", "weather": "#e0f2fe", "camera": "#ede9fe",
    "style": "#fee2e2", "mood": "#fef3c7", "texture": "#fdf4ff", "scale": "#f0fdf4",
    "time": "#dcfce7", "render": "#f3f4f6", "color": "#eef2ff",
}
SET_CAT_TEXT = {
    "lighting": "#1e40af", "location": "#065f46", "weather": "#0c4a6e", "camera": "#4c1d95",
    "style": "#991b1b", "mood": "#92400e", "texture": "#7e22ce", "scale": "#14532d",
    "time": "#14532d", "render": "#374151", "color": "#3730a3",
}

CHAR_CATS = ["all"] + sorted(set(d["cat"] for d in CHARACTER_SUFFIXES))
SET_CATS  = ["all"] + sorted(set(d["cat"] for d in SETTING_SUFFIXES))

FAVS_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "favourites.json")

# ── App ───────────────────────────────────────────────────────────────────────

class PromptSuffixApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Prompt Suffix Reference")
        self.geometry("1400x820")
        self.minsize(1000, 640)
        self.configure(bg="#f9fafb")

        # tokens: dict of token -> locked bool
        self.char_tokens    = {}   # {token: locked}
        self.setting_tokens = {}

        self.char_cat_var    = tk.StringVar(value="all")
        self.setting_cat_var = tk.StringVar(value="all")
        self.char_search     = tk.StringVar()
        self.setting_search  = tk.StringVar()
        self.prefix_var      = tk.StringVar()
        self.prefix_var.trace_add("write", lambda *_: self._refresh_outputs())

        self.favourites = self._load_favs()   # set of token strings
        self.show_favs  = tk.BooleanVar(value=False)

        self.char_search.trace_add("write",    lambda *_: self._render_char())
        self.setting_search.trace_add("write", lambda *_: self._render_set())

        self._active_canvas = None
        self._build_ui()
        self._render_char()
        self._render_set()

    # ── Favourites persistence ────────────────────────────────────────────────

    def _load_favs(self):
        try:
            with open(FAVS_FILE) as f:
                return set(json.load(f))
        except Exception:
            return set()

    def _save_favs(self):
        try:
            with open(FAVS_FILE, "w") as f:
                json.dump(list(self.favourites), f)
        except Exception:
            pass

    # ── UI ────────────────────────────────────────────────────────────────────

    def _build_ui(self):
        hdr = tk.Frame(self, bg="#111827", padx=20, pady=13)
        hdr.pack(fill="x")
        tk.Label(hdr, text="✦  Prompt Suffix Reference",
                 font=("Helvetica", 15, "bold"), fg="white", bg="#111827").pack(side="left")
        tk.Label(hdr, text="click tags to add · right-click to lock · ⭐ to favourite",
                 font=("Helvetica", 10), fg="#9ca3af", bg="#111827").pack(side="right")

        body = tk.Frame(self, bg="#f9fafb")
        body.pack(fill="both", expand=True, padx=10, pady=10)
        body.columnconfigure(0, weight=1)
        body.columnconfigure(1, weight=1)
        body.columnconfigure(2, minsize=280, weight=0)
        body.rowconfigure(0, weight=1)

        # Character column
        char_col = tk.Frame(body, bg="#f9fafb")
        char_col.grid(row=0, column=0, sticky="nsew", padx=(0, 6))
        self._build_column(char_col, "👤  Character", "#9d174d",
                           CHARACTER_SUFFIXES, CHAR_CAT_COLORS, CHAR_CAT_TEXT,
                           CHAR_CATS, self.char_cat_var, self.char_search, "char",
                           "#be185d", "🎲  Random Character",
                           "char_cards_frame", "char_canvas", "char_tab_frame")

        # Setting column
        set_col = tk.Frame(body, bg="#f9fafb")
        set_col.grid(row=0, column=1, sticky="nsew", padx=(0, 6))
        self._build_column(set_col, "🌍  Setting", "#1e40af",
                           SETTING_SUFFIXES, SET_CAT_COLORS, SET_CAT_TEXT,
                           SET_CATS, self.setting_cat_var, self.setting_search, "set",
                           "#1d4ed8", "🎲  Random Setting",
                           "set_cards_frame", "set_canvas", "set_tab_frame")

        # Output column
        out_col = tk.Frame(body, bg="#f9fafb", width=280)
        out_col.grid(row=0, column=2, sticky="nsew")
        out_col.pack_propagate(False)
        self._build_output_panel(out_col)

    def _build_column(self, parent, title, title_color, suffixes, cat_colors, cat_text,
                      all_cats, cat_var, search_var, side, rand_color, rand_label,
                      cards_attr, canvas_attr, tabs_attr):
        tk.Label(parent, text=title, font=("Helvetica", 12, "bold"),
                 fg=title_color, bg="#f9fafb").pack(anchor="w", pady=(0, 5))

        sf = tk.Frame(parent, bg="#ffffff", bd=1, relief="solid",
                      highlightbackground="#d1d5db", highlightthickness=1)
        sf.pack(fill="x", pady=(0, 5))
        tk.Label(sf, text="🔍", bg="#ffffff", font=("Helvetica", 11)).pack(side="left", padx=(6, 2))
        tk.Entry(sf, textvariable=search_var, font=("Helvetica", 11),
                 relief="flat", bg="#ffffff", fg="#111827",
                 insertbackground="#111827").pack(side="left", fill="x", expand=True, pady=5, padx=4)

        tab_frame = tk.Frame(parent, bg="#f9fafb")
        tab_frame.pack(fill="x", pady=(0, 5))
        setattr(self, tabs_attr, tab_frame)
        self._build_tabs(tab_frame, all_cats, cat_var, suffixes, cat_colors, cat_text, side)

        wrapper = tk.Frame(parent, bg="#f9fafb")
        wrapper.pack(fill="both", expand=True)
        canvas = tk.Canvas(wrapper, bg="#f9fafb", highlightthickness=0)
        vsb = ttk.Scrollbar(wrapper, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=vsb.set)
        canvas.pack(side="left", fill="both", expand=True)
        vsb.pack(side="left", fill="y")
        setattr(self, canvas_attr, canvas)

        cf = tk.Frame(canvas, bg="#f9fafb")
        setattr(self, cards_attr, cf)
        win = canvas.create_window((0, 0), window=cf, anchor="nw")
        cf.bind("<Configure>", lambda e, c=canvas: c.configure(scrollregion=c.bbox("all")))
        canvas.bind("<Configure>", lambda e, c=canvas, w=win: c.itemconfig(w, width=e.width))
        canvas.bind("<Enter>", lambda e, c=canvas: self._bind_scroll(c))
        canvas.bind("<Leave>", lambda e: self._unbind_scroll())

        tk.Button(parent, text=rand_label, font=("Helvetica", 10, "bold"),
                  bg=rand_color, fg="white", relief="flat",
                  padx=10, pady=6, cursor="hand2",
                  command=lambda s=side: self._random_prompt(s)).pack(fill="x", pady=(6, 0))

    def _build_output_panel(self, parent):
        # Prefix
        tk.Label(parent, text="✦  Combined Prompt", font=("Helvetica", 12, "bold"),
                 fg="#111827", bg="#f9fafb").pack(anchor="w", pady=(0, 6))
        tk.Label(parent, text="Subject / prefix (optional)", font=("Helvetica", 9),
                 fg="#6b7280", bg="#f9fafb").pack(anchor="w")
        pf = tk.Frame(parent, bg="#ffffff", bd=1, relief="solid")
        pf.pack(fill="x", pady=(2, 8))
        tk.Entry(pf, textvariable=self.prefix_var, font=("Helvetica", 11),
                 relief="flat", bg="#ffffff", fg="#111827",
                 insertbackground="#111827").pack(fill="x", pady=5, padx=6)

        # Character out
        tk.Label(parent, text="👤 Character", font=("Helvetica", 10, "bold"),
                 fg="#9d174d", bg="#f9fafb").pack(anchor="w")
        self.char_out = tk.Text(parent, wrap="word", font=("Helvetica", 10),
                                bg="#fce7f3", fg="#111827", relief="solid", bd=1,
                                padx=6, pady=5, height=5)
        self.char_out.pack(fill="x", pady=(2, 3))
        self.char_out.config(state="disabled")

        row1 = tk.Frame(parent, bg="#f9fafb")
        row1.pack(fill="x", pady=(0, 6))
        tk.Button(row1, text="🗑 Clear", font=("Helvetica", 9), bg="#e5e7eb", fg="#374151",
                  relief="flat", pady=3, cursor="hand2",
                  command=lambda: self._clear("char")).pack(side="left", fill="x", expand=True, padx=(0, 3))
        tk.Button(row1, text="🔓 Unlock all", font=("Helvetica", 9), bg="#e5e7eb", fg="#374151",
                  relief="flat", pady=3, cursor="hand2",
                  command=lambda: self._unlock_all("char")).pack(side="left", fill="x", expand=True)

        # Setting out
        tk.Label(parent, text="🌍 Setting", font=("Helvetica", 10, "bold"),
                 fg="#1e40af", bg="#f9fafb").pack(anchor="w")
        self.set_out = tk.Text(parent, wrap="word", font=("Helvetica", 10),
                               bg="#dbeafe", fg="#111827", relief="solid", bd=1,
                               padx=6, pady=5, height=5)
        self.set_out.pack(fill="x", pady=(2, 3))
        self.set_out.config(state="disabled")

        row2 = tk.Frame(parent, bg="#f9fafb")
        row2.pack(fill="x", pady=(0, 6))
        tk.Button(row2, text="🗑 Clear", font=("Helvetica", 9), bg="#e5e7eb", fg="#374151",
                  relief="flat", pady=3, cursor="hand2",
                  command=lambda: self._clear("set")).pack(side="left", fill="x", expand=True, padx=(0, 3))
        tk.Button(row2, text="🔓 Unlock all", font=("Helvetica", 9), bg="#e5e7eb", fg="#374151",
                  relief="flat", pady=3, cursor="hand2",
                  command=lambda: self._unlock_all("set")).pack(side="left", fill="x", expand=True)

        tk.Frame(parent, bg="#e5e7eb", height=1).pack(fill="x", pady=(0, 6))

        # Combined out
        tk.Label(parent, text="⚡ Combined", font=("Helvetica", 10, "bold"),
                 fg="#111827", bg="#f9fafb").pack(anchor="w")
        self.combined_out = tk.Text(parent, wrap="word", font=("Helvetica", 10),
                                    bg="#f0fdf4", fg="#111827", relief="solid", bd=1,
                                    padx=6, pady=5, height=6)
        self.combined_out.pack(fill="x", pady=(2, 6))
        self.combined_out.config(state="disabled")

        tk.Button(parent, text="📋  Copy Combined Prompt", font=("Helvetica", 10, "bold"),
                  bg="#111827", fg="white", relief="flat",
                  padx=10, pady=7, cursor="hand2",
                  command=self._copy_combined).pack(fill="x", pady=(0, 4))
        tk.Button(parent, text="💾  Export to .txt", font=("Helvetica", 10),
                  bg="#374151", fg="white", relief="flat",
                  padx=10, pady=5, cursor="hand2",
                  command=self._export_txt).pack(fill="x", pady=(0, 4))

        tk.Button(parent, text="✨  AI Finalize Prompt", font=("Helvetica", 10, "bold"),
                  bg="#7c3aed", fg="white", relief="flat",
                  padx=10, pady=6, cursor="hand2",
                  command=self._open_ai_window).pack(fill="x", pady=(0, 6))

        tk.Frame(parent, bg="#e5e7eb", height=1).pack(fill="x", pady=(0, 6))

        # Favourites
        fav_hdr = tk.Frame(parent, bg="#f9fafb")
        fav_hdr.pack(fill="x")
        tk.Label(fav_hdr, text="⭐ Favourites", font=("Helvetica", 10, "bold"),
                 fg="#92400e", bg="#f9fafb").pack(side="left")
        tk.Button(fav_hdr, text="▼ show/hide", font=("Helvetica", 8),
                  bg="#f9fafb", fg="#6b7280", relief="flat", cursor="hand2",
                  command=self._toggle_favs).pack(side="right")

        self.fav_frame = tk.Frame(parent, bg="#fefce8", bd=1, relief="solid")
        # don't pack yet — toggled
        self.fav_inner = tk.Frame(self.fav_frame, bg="#fefce8")
        self.fav_inner.pack(fill="both", padx=4, pady=4)
        self._refresh_fav_panel()

    # ── Tabs ──────────────────────────────────────────────────────────────────

    def _build_tabs(self, frame, all_cats, cat_var, suffixes, cat_colors, cat_text, side):
        for w in frame.winfo_children():
            w.destroy()
        for cat in all_cats:
            active = cat == cat_var.get()
            tk.Button(frame, text=cat,
                      font=("Helvetica", 9, "bold" if active else "normal"),
                      bg="#111827" if active else "#ffffff",
                      fg="#ffffff" if active else "#374151",
                      relief="solid", bd=1, padx=7, pady=3, cursor="hand2",
                      command=lambda c=cat: self._set_tab(c, frame, all_cats, cat_var, suffixes, cat_colors, cat_text, side)
                      ).pack(side="left", padx=(0, 3), pady=2)

    def _set_tab(self, cat, frame, all_cats, cat_var, suffixes, cat_colors, cat_text, side):
        cat_var.set(cat)
        self._build_tabs(frame, all_cats, cat_var, suffixes, cat_colors, cat_text, side)
        if side == "char":
            self._render_char()
        else:
            self._render_set()

    # ── Render cards ──────────────────────────────────────────────────────────

    def _render_char(self):
        self._render_cards(self.char_cards_frame, CHARACTER_SUFFIXES,
                           CHAR_CAT_COLORS, CHAR_CAT_TEXT,
                           self.char_cat_var, self.char_search, "char")

    def _render_set(self):
        self._render_cards(self.set_cards_frame, SETTING_SUFFIXES,
                           SET_CAT_COLORS, SET_CAT_TEXT,
                           self.setting_cat_var, self.setting_search, "set")

    def _render_cards(self, cards_frame, suffixes, cat_colors, cat_text, cat_var, search_var, side):
        for w in cards_frame.winfo_children():
            w.destroy()
        q   = search_var.get().lower().strip()
        cat = cat_var.get()
        filtered = [
            d for d in suffixes
            if (cat == "all" or d["cat"] == cat)
            and (not q or q in d["label"].lower() or q in d["desc"].lower()
                 or any(q in e.lower() for e in d["examples"]))
        ]
        if not filtered:
            tk.Label(cards_frame, text="No results.", font=("Helvetica", 11),
                     fg="#9ca3af", bg="#f9fafb").pack(pady=30)
            return
        for i, item in enumerate(filtered):
            row, col = divmod(i, 2)
            card = self._make_card(cards_frame, item, cat_colors, cat_text, side)
            card.grid(row=row, column=col, padx=4, pady=4, sticky="nsew")
        cards_frame.columnconfigure(0, weight=1, minsize=180)
        cards_frame.columnconfigure(1, weight=1, minsize=180)

    def _make_card(self, parent, item, cat_colors, cat_text, side):
        cat    = item["cat"]
        bg_col = cat_colors.get(cat, "#f3f4f6")
        tc     = cat_text.get(cat, "#374151")

        card = tk.Frame(parent, bg="#ffffff", bd=1, relief="solid",
                        highlightbackground="#e5e7eb", highlightthickness=1)

        top = tk.Frame(card, bg="#ffffff")
        top.pack(fill="x", padx=8, pady=(7, 2))
        tk.Label(top, text=cat, font=("Helvetica", 8, "bold"),
                 bg=bg_col, fg=tc, padx=5, pady=1).pack(side="left")

        def copy_all(examples=item["examples"]):
            try:    pyperclip.copy(", ".join(examples))
            except: self.clipboard_clear(); self.clipboard_append(", ".join(examples))
            self._flash("Copied!")

        tk.Button(top, text="copy all", font=("Helvetica", 8),
                  bg="#f3f4f6", fg="#374151", relief="flat",
                  padx=4, pady=1, cursor="hand2", command=copy_all).pack(side="right")

        tk.Label(card, text=item["label"], font=("Helvetica", 10, "bold"),
                 bg="#ffffff", fg="#111827", anchor="w").pack(fill="x", padx=8, pady=(1, 0))
        tk.Label(card, text=item["desc"], font=("Helvetica", 9),
                 bg="#ffffff", fg="#6b7280", anchor="w",
                 wraplength=240, justify="left").pack(fill="x", padx=8)

        tag_frame = tk.Frame(card, bg="#ffffff")
        tag_frame.pack(fill="x", padx=6, pady=(4, 7))

        for ex in item["examples"]:
            is_fav = ex in self.favourites
            fav_marker = " ⭐" if is_fav else ""
            t = tk.Label(tag_frame, text=ex + fav_marker, font=("Helvetica", 9),
                         bg="#fef9c3" if is_fav else "#f3f4f6",
                         fg="#374151", padx=5, pady=2,
                         cursor="hand2", relief="flat")
            t.pack(side="left", padx=2, pady=2, anchor="w")
            t.bind("<Button-1>",   lambda e, s=ex, sd=side: self._add_token(sd, s))
            t.bind("<Button-3>",   lambda e, s=ex, sd=side: self._toggle_lock_from_card(sd, s))
            t.bind("<Double-Button-1>", lambda e, s=ex, w=t, bg=bg_col, tc_=tc: self._toggle_fav(s, w, bg, tc_))
            t.bind("<Enter>", lambda e, w=t, s=ex: w.configure(
                bg="#fef08a" if s in self.favourites else bg_col, fg=tc))
            t.bind("<Leave>", lambda e, w=t, s=ex: w.configure(
                bg="#fef9c3" if s in self.favourites else "#f3f4f6", fg="#374151"))
        return card

    # ── Token management ──────────────────────────────────────────────────────

    def _add_token(self, side, token):
        tokens = self.char_tokens if side == "char" else self.setting_tokens
        if token not in tokens:
            tokens[token] = False  # not locked
            self._refresh_outputs()

    def _toggle_lock_from_card(self, side, token):
        tokens = self.char_tokens if side == "char" else self.setting_tokens
        if token in tokens:
            tokens[token] = not tokens[token]
            self._refresh_outputs()
        else:
            # add it and lock immediately
            tokens[token] = True
            self._refresh_outputs()

    def _unlock_all(self, side):
        tokens = self.char_tokens if side == "char" else self.setting_tokens
        for k in tokens:
            tokens[k] = False
        self._refresh_outputs()

    def _clear(self, side):
        tokens = self.char_tokens if side == "char" else self.setting_tokens
        # only remove unlocked
        locked = {k: v for k, v in tokens.items() if v}
        if side == "char":
            self.char_tokens = locked
        else:
            self.setting_tokens = locked
        self._refresh_outputs()

    def _refresh_outputs(self):
        def set_text(widget, text):
            widget.config(state="normal")
            widget.delete("1.0", "end")
            widget.insert("1.0", text)
            widget.config(state="disabled")

        def fmt(tokens):
            parts = []
            for t, locked in tokens.items():
                parts.append(f"🔒{t}" if locked else t)
            return ", ".join(parts)

        def clean(tokens):
            return ", ".join(tokens.keys())

        char_text    = fmt(self.char_tokens)
        setting_text = fmt(self.setting_tokens)
        prefix       = self.prefix_var.get().strip()
        combined     = ", ".join(filter(None, [prefix, clean(self.char_tokens), clean(self.setting_tokens)]))

        set_text(self.char_out,     char_text)
        set_text(self.set_out,      setting_text)
        set_text(self.combined_out, combined)

    # ── Favourites ────────────────────────────────────────────────────────────

    def _toggle_fav(self, token, widget, bg_col, tc):
        if token in self.favourites:
            self.favourites.discard(token)
            widget.configure(text=token, bg="#f3f4f6")
        else:
            self.favourites.add(token)
            widget.configure(text=token + " ⭐", bg="#fef9c3")
        self._save_favs()
        self._refresh_fav_panel()

    def _refresh_fav_panel(self):
        for w in self.fav_inner.winfo_children():
            w.destroy()
        if not self.favourites:
            tk.Label(self.fav_inner, text="Double-click any tag to favourite it",
                     font=("Helvetica", 9), fg="#9ca3af", bg="#fefce8").pack(pady=4)
            return
        for fav in sorted(self.favourites):
            row = tk.Frame(self.fav_inner, bg="#fefce8")
            row.pack(fill="x", pady=1)
            tk.Label(row, text=fav, font=("Helvetica", 9),
                     bg="#fefce8", fg="#374151").pack(side="left")
            tk.Button(row, text="✕", font=("Helvetica", 8),
                      bg="#fefce8", fg="#9ca3af", relief="flat", cursor="hand2",
                      command=lambda f=fav: self._remove_fav(f)).pack(side="right")

    def _remove_fav(self, token):
        self.favourites.discard(token)
        self._save_favs()
        self._refresh_fav_panel()
        self._render_char()
        self._render_set()

    def _toggle_favs(self):
        if self.fav_frame.winfo_ismapped():
            self.fav_frame.pack_forget()
        else:
            self.fav_frame.pack(fill="x", pady=(4, 0))

    # ── Random ────────────────────────────────────────────────────────────────

    def _random_prompt(self, side):
        suffixes = CHARACTER_SUFFIXES if side == "char" else SETTING_SUFFIXES
        tokens   = self.char_tokens   if side == "char" else self.setting_tokens

        # Keep locked tokens, replace unlocked
        locked = {k: True for k, v in tokens.items() if v}

        by_cat = {}
        for item in suffixes:
            by_cat.setdefault(item["cat"], {"favs": [], "all": []})
            for ex in item["examples"]:
                by_cat[item["cat"]]["all"].append(ex)
                if ex in self.favourites:
                    by_cat[item["cat"]]["favs"].append(ex)

        new_tokens = dict(locked)
        locked_vals = set(locked.keys())

        cats = list(by_cat.keys())
        random.shuffle(cats)
        for cat in cats:
            pool = by_cat[cat]["favs"] or by_cat[cat]["all"]
            # filter out already locked picks
            pool = [p for p in pool if p not in locked_vals]
            if pool:
                pick = random.choice(pool)
                if pick not in new_tokens:
                    new_tokens[pick] = False

        if side == "char":
            self.char_tokens = new_tokens
            self._flash("🎲 Random character!")
        else:
            self.setting_tokens = new_tokens
            self._flash("🎲 Random setting!")
        self._refresh_outputs()

    # ── Copy & export ─────────────────────────────────────────────────────────

    def _copy_combined(self):
        prefix = self.prefix_var.get().strip()
        text   = ", ".join(filter(None, [prefix,
                                         ", ".join(self.char_tokens.keys()),
                                         ", ".join(self.setting_tokens.keys())]))
        if not text:
            return
        try:    pyperclip.copy(text)
        except: self.clipboard_clear(); self.clipboard_append(text)
        self._flash("📋 Prompt copied!")

    def _export_txt(self):
        prefix = self.prefix_var.get().strip()
        text   = ", ".join(filter(None, [prefix,
                                         ", ".join(self.char_tokens.keys()),
                                         ", ".join(self.setting_tokens.keys())]))
        if not text:
            self._flash("Nothing to export yet!")
            return
        path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt")],
            initialfile="my_prompt.txt",
            title="Export prompt")
        if path:
            with open(path, "w", encoding="utf-8") as f:
                f.write(text)
            self._flash("💾 Exported!")

    # ── Scroll ────────────────────────────────────────────────────────────────

    def _bind_scroll(self, canvas):
        self._active_canvas = canvas
        self.bind_all("<MouseWheel>", self._on_scroll)

    def _unbind_scroll(self):
        self.unbind_all("<MouseWheel>")

    def _on_scroll(self, event):
        if self._active_canvas:
            self._active_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    # ── AI Finalize ───────────────────────────────────────────────────────────────

    def _open_ai_window(self):
        """Open the AI Finalize popup window."""
        win = tk.Toplevel(self)
        win.title("✨ AI Finalize Prompt")
        win.geometry("680x700")
        win.minsize(500, 550)
        win.configure(bg="#f9fafb")
        win.attributes("-topmost", False)

        # Header
        hdr = tk.Frame(win, bg="#7c3aed", padx=16, pady=12)
        hdr.pack(fill="x")
        tk.Label(hdr, text="✨  AI Finalize Prompt", font=("Helvetica", 14, "bold"),
                 fg="white", bg="#7c3aed").pack(side="left")

        body = tk.Frame(win, bg="#f9fafb", padx=16, pady=12)
        body.pack(fill="both", expand=True)

        # LLM selector
        llm_row = tk.Frame(body, bg="#f9fafb")
        llm_row.pack(fill="x", pady=(0, 10))
        tk.Label(llm_row, text="LLM:", font=("Helvetica", 10, "bold"),
                 bg="#f9fafb", fg="#374151", width=8, anchor="w").pack(side="left")
        llm_var = tk.StringVar(value="LM Studio (local)")
        llm_options = ["LM Studio (local)", "Ollama (local)", "Groq (free API)", "OpenRouter (free API)"]
        llm_menu = ttk.Combobox(llm_row, textvariable=llm_var, values=llm_options,
                                state="readonly", font=("Helvetica", 10), width=24)
        llm_menu.pack(side="left", padx=(0, 8))

        # Ollama model
        ollama_row = tk.Frame(body, bg="#f9fafb")
        ollama_row.pack(fill="x", pady=(0, 6))
        tk.Label(ollama_row, text="Model:", font=("Helvetica", 10, "bold"),
                 bg="#f9fafb", fg="#374151", width=8, anchor="w").pack(side="left")
        ollama_model_var = tk.StringVar(value="llama3")
        ollama_entry = tk.Entry(ollama_row, textvariable=ollama_model_var,
                                font=("Helvetica", 10), relief="solid", bd=1, width=20)
        ollama_entry.pack(side="left")
        tk.Label(ollama_row, text="  (Ollama model name)",
                 font=("Helvetica", 9), fg="#9ca3af", bg="#f9fafb").pack(side="left")

        # LM Studio model + port
        lms_row = tk.Frame(body, bg="#f9fafb")
        lms_model_var = tk.StringVar(value="")
        lms_model_entry = tk.Entry(lms_row, textvariable=lms_model_var,
                                   font=("Helvetica", 10), relief="solid", bd=1, width=26)
        lms_port_var = tk.StringVar(value="1234")
        lms_port_entry = tk.Entry(lms_row, textvariable=lms_port_var,
                                  font=("Helvetica", 10), relief="solid", bd=1, width=6)

        # OpenRouter model
        or_model_row = tk.Frame(body, bg="#f9fafb")
        or_model_var = tk.StringVar(value="mistralai/mistral-7b-instruct:free")
        or_model_entry = tk.Entry(or_model_row, textvariable=or_model_var,
                                  font=("Helvetica", 10), relief="solid", bd=1, width=38)

        # Groq model
        groq_model_row = tk.Frame(body, bg="#f9fafb")
        groq_model_var = tk.StringVar(value="llama3-8b-8192")
        groq_model_entry = tk.Entry(groq_model_row, textvariable=groq_model_var,
                                    font=("Helvetica", 10), relief="solid", bd=1, width=38)

        # API key row (hidden for Ollama)
        key_row = tk.Frame(body, bg="#f9fafb")
        tk.Label(key_row, text="API Key:", font=("Helvetica", 10, "bold"),
                 bg="#f9fafb", fg="#374151", width=8, anchor="w").pack(side="left")
        api_key_var = tk.StringVar()
        key_entry = tk.Entry(key_row, textvariable=api_key_var, show="*",
                             font=("Helvetica", 10), relief="solid", bd=1, width=34)
        key_entry.pack(side="left")

        def on_llm_change(*_):
            llm = llm_var.get()
            # hide all optional rows first
            key_row.pack_forget()
            or_model_row.pack_forget()
            groq_model_row.pack_forget()
            ollama_row.pack_forget()
            lms_row.pack_forget()
            if llm == "LM Studio (local)":
                lms_row.pack(fill="x", pady=(0, 6), after=llm_row)
                if not lms_row.winfo_children():
                    tk.Label(lms_row, text="Model:", font=("Helvetica", 10, "bold"),
                             bg="#f9fafb", fg="#374151", width=8, anchor="w").pack(side="left")
                    lms_model_entry.pack(side="left", padx=(0, 6))
                    tk.Label(lms_row, text="Port:", font=("Helvetica", 10, "bold"),
                             bg="#f9fafb", fg="#374151").pack(side="left", padx=(0, 4))
                    lms_port_entry.pack(side="left")
                    tk.Label(lms_row, text="  (leave model blank for active model)",
                             font=("Helvetica", 9), fg="#9ca3af", bg="#f9fafb").pack(side="left")
            elif llm == "Ollama (local)":
                ollama_row.pack(fill="x", pady=(0, 6), after=llm_row)
            elif llm == "Groq (free API)":
                groq_model_row.pack(fill="x", pady=(0, 6), after=llm_row)
                tk.Label(groq_model_row, text="Model:", font=("Helvetica", 10, "bold"),
                         bg="#f9fafb", fg="#374151", width=8, anchor="w").pack(side="left") if not groq_model_row.winfo_children() else None
                groq_model_entry.pack(side="left")
                key_row.pack(fill="x", pady=(0, 6))
            elif llm == "OpenRouter (free API)":
                or_model_row.pack(fill="x", pady=(0, 6), after=llm_row)
                tk.Label(or_model_row, text="Model:", font=("Helvetica", 10, "bold"),
                         bg="#f9fafb", fg="#374151", width=8, anchor="w").pack(side="left") if not or_model_row.winfo_children() else None
                or_model_entry.pack(side="left")
                key_row.pack(fill="x", pady=(0, 6))

        llm_var.trace_add("write", on_llm_change)
        on_llm_change()  # init state

        # Divider
        tk.Frame(body, bg="#e5e7eb", height=1).pack(fill="x", pady=(4, 10))

        # System instruction
        tk.Label(body, text="System instruction", font=("Helvetica", 10, "bold"),
                 fg="#374151", bg="#f9fafb").pack(anchor="w")
        tk.Label(body, text="Customize how the AI rewrites your prompt",
                 font=("Helvetica", 9), fg="#9ca3af", bg="#f9fafb").pack(anchor="w", pady=(0, 4))
        sys_text = tk.Text(body, wrap="word", font=("Helvetica", 10),
                           bg="#ffffff", fg="#111827", relief="solid", bd=1,
                           padx=6, pady=6, height=4, insertbackground="#111827")
        sys_text.pack(fill="x", pady=(0, 8))
        default_sys = (
            "You are an expert image generation prompt writer. "
            "The user will give you a list of descriptive tags and suffixes. "
            "Rewrite them into a single, polished, vivid image generation prompt. "
            "Keep it concise but detailed. Optimize for visual clarity and impact. "
            "Output ONLY the final prompt text, no explanation, no preamble."
        )
        sys_text.insert("1.0", default_sys)

        # Input prompt preview
        tk.Label(body, text="Input prompt (editable)", font=("Helvetica", 10, "bold"),
                 fg="#374151", bg="#f9fafb").pack(anchor="w")
        input_text = tk.Text(body, wrap="word", font=("Helvetica", 10),
                             bg="#f0fdf4", fg="#111827", relief="solid", bd=1,
                             padx=6, pady=6, height=4, insertbackground="#111827")
        input_text.pack(fill="x", pady=(4, 8))

        # Pull current combined prompt in
        prefix = self.prefix_var.get().strip()
        combined = ", ".join(filter(None, [prefix,
                                           ", ".join(self.char_tokens.keys()),
                                           ", ".join(self.setting_tokens.keys())]))
        input_text.insert("1.0", combined)

        # Status label
        status_var = tk.StringVar(value="")
        status_lbl = tk.Label(body, textvariable=status_var, font=("Helvetica", 9),
                              fg="#7c3aed", bg="#f9fafb")
        status_lbl.pack(anchor="w")

        # Finalize button
        fin_btn = tk.Button(body, text="✨  Finalize", font=("Helvetica", 11, "bold"),
                            bg="#7c3aed", fg="white", relief="flat",
                            padx=12, pady=7, cursor="hand2")
        fin_btn.pack(fill="x", pady=(4, 8))

        # Output
        tk.Label(body, text="✨ Finalized prompt", font=("Helvetica", 10, "bold"),
                 fg="#374151", bg="#f9fafb").pack(anchor="w")
        out_text = tk.Text(body, wrap="word", font=("Helvetica", 10),
                           bg="#faf5ff", fg="#111827", relief="solid", bd=1,
                           padx=6, pady=6, height=5, insertbackground="#111827")
        out_text.pack(fill="x", pady=(4, 6))
        out_text.config(state="disabled")

        copy_btn = tk.Button(body, text="📋  Copy Finalized Prompt",
                             font=("Helvetica", 10, "bold"),
                             bg="#111827", fg="white", relief="flat",
                             padx=10, pady=6, cursor="hand2",
                             command=lambda: self._copy_from_text(out_text))
        copy_btn.pack(fill="x")

        def do_finalize():
            prompt_in = input_text.get("1.0", "end").strip()
            sys_instr = sys_text.get("1.0", "end").strip()
            llm       = llm_var.get()
            api_key   = api_key_var.get().strip()

            if not prompt_in:
                status_var.set("⚠️  No prompt to finalize.")
                return

            fin_btn.config(state="disabled", text="⏳  Working...")
            status_var.set("Sending to LLM...")
            out_text.config(state="normal")
            out_text.delete("1.0", "end")
            out_text.config(state="disabled")

            def run():
                try:
                    result = self._call_llm(llm, api_key, sys_instr, prompt_in,
                                            ollama_model_var.get().strip(),
                                            groq_model_var.get().strip(),
                                            or_model_var.get().strip(),
                                            lms_model_var.get().strip(),
                                            lms_port_var.get().strip())
                    win.after(0, lambda: _show_result(result, None))
                except Exception as e:
                    win.after(0, lambda: _show_result(None, str(e)))

            def _show_result(result, error):
                fin_btn.config(state="normal", text="✨  Finalize")
                if error:
                    status_var.set(f"❌  {error}")
                else:
                    out_text.config(state="normal")
                    out_text.delete("1.0", "end")
                    out_text.insert("1.0", result)
                    out_text.config(state="disabled")
                    status_var.set("✅  Done!")

            threading.Thread(target=run, daemon=True).start()

        fin_btn.config(command=do_finalize)

    def _call_llm(self, llm, api_key, system, user_prompt, ollama_model, groq_model, or_model, lms_model="", lms_port="1234"):
        """Call the selected LLM and return the response text."""
        import json as _json

        if llm == "LM Studio (local)":
            port    = lms_port or "1234"
            url     = f"http://localhost:{port}/v1/chat/completions"
            payload = _json.dumps({
                "model": lms_model or "local-model",
                "messages": [
                    {"role": "system", "content": system},
                    {"role": "user",   "content": user_prompt},
                ],
                "max_tokens": 512,
            }).encode()
            req = urllib.request.Request(url, data=payload,
                                         headers={"Content-Type": "application/json"})
            try:
                with urllib.request.urlopen(req, timeout=60) as r:
                    data = _json.loads(r.read())
                    return data["choices"][0]["message"]["content"].strip()
            except urllib.error.URLError:
                raise Exception("Can\'t reach LM Studio — is the local server running? (port " + port + ")")

        elif llm == "Ollama (local)":
            url     = "http://localhost:11434/api/chat"
            payload = _json.dumps({
                "model": ollama_model,
                "stream": False,
                "messages": [
                    {"role": "system", "content": system},
                    {"role": "user",   "content": user_prompt},
                ]
            }).encode()
            req = urllib.request.Request(url, data=payload,
                                         headers={"Content-Type": "application/json"})
            try:
                with urllib.request.urlopen(req, timeout=60) as r:
                    data = _json.loads(r.read())
                    return data["message"]["content"].strip()
            except urllib.error.URLError:
                raise Exception("Can't reach Ollama — is it running? (ollama serve)")

        elif llm == "Groq (free API)":
            if not api_key:
                raise Exception("Groq API key required. Get one free at console.groq.com")
            url     = "https://api.groq.com/openai/v1/chat/completions"
            payload = _json.dumps({
                "model": groq_model,
                "messages": [
                    {"role": "system", "content": system},
                    {"role": "user",   "content": user_prompt},
                ],
                "max_tokens": 512,
            }).encode()
            req = urllib.request.Request(url, data=payload, headers={
                "Content-Type":  "application/json",
                "Authorization": f"Bearer {api_key}",
            })
            with urllib.request.urlopen(req, timeout=30) as r:
                data = _json.loads(r.read())
                return data["choices"][0]["message"]["content"].strip()

        elif llm == "OpenRouter (free API)":
            if not api_key:
                raise Exception("OpenRouter API key required. Get one free at openrouter.ai")
            url     = "https://openrouter.ai/api/v1/chat/completions"
            payload = _json.dumps({
                "model": or_model,
                "messages": [
                    {"role": "system", "content": system},
                    {"role": "user",   "content": user_prompt},
                ],
                "max_tokens": 512,
            }).encode()
            req = urllib.request.Request(url, data=payload, headers={
                "Content-Type":  "application/json",
                "Authorization": f"Bearer {api_key}",
                "HTTP-Referer":  "https://github.com/prompt-suffix-ref",
                "X-Title":       "Prompt Suffix Reference",
            })
            with urllib.request.urlopen(req, timeout=30) as r:
                data = _json.loads(r.read())
                return data["choices"][0]["message"]["content"].strip()

        raise Exception("Unknown LLM selected")

    def _copy_from_text(self, widget):
        text = widget.get("1.0", "end").strip()
        if not text:
            return
        try:    pyperclip.copy(text)
        except: self.clipboard_clear(); self.clipboard_append(text)
        self._flash("📋 Finalized prompt copied!")

    # ── Toast ─────────────────────────────────────────────────────────────────

    def _flash(self, msg):
        w = tk.Toplevel(self)
        w.overrideredirect(True)
        w.attributes("-topmost", True)
        x = self.winfo_x() + self.winfo_width() // 2 - 140
        y = self.winfo_y() + self.winfo_height() - 60
        w.geometry(f"280x36+{x}+{y}")
        tk.Label(w, text=msg, font=("Helvetica", 11, "bold"),
                 bg="#111827", fg="white", padx=16, pady=8).pack(fill="both", expand=True)
        w.after(1500, w.destroy)


# ── Entry point ───────────────────────────────────────────────────────────────

if __name__ == "__main__":
    try:
        import pyperclip
    except ImportError:
        import subprocess, sys
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyperclip", "-q"])
    app = PromptSuffixApp()
    app.mainloop()
