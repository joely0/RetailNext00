# RetailNext00

A multimodal fashion recommendation system that analyzes clothing images and suggests matching outfit items using OpenAI's API and embedding-based similarity search.

Original cookbook - https://cookbook.openai.com/examples/how_to_combine_gpt4o_with_rag_outfit_assistant

## 📋 Table of Contents

- [Demo](#demo)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Folder Structure](#folder-structure)
- [API Keys](#api-keys)
- [License](#license)

## 🚀 Features

- Image-to-outfit matching using GPT-4 and vision API
- Embedding-based item similarity search
- Outfit compatibility check (guardrails)
- Base64 image processing
- Modular architecture (`analysis.py`, `search_similar_items.py`, etc.)

## 🛠 Installation & Setup Guide

```bash
# Clone the repository
git clone https://github.com/joely0/RetailNext00.git
cd RetailNext00

# Set up virtual environment
python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows

# Install dependencies
pip install -r requirements.txt
```

## ▶️ Usage

```bash
python test_prompt.py
```

This script will:
- Load a clothing image
- Extract textual features
- Find matching items in the dataset
- Display visually compatible outfits with reasoning

## 🗂 Folder Structure

```
RetailNext00/
├── data/
│   └── sample_clothes/
│       ├── sample_images/
│       └── sample_styles_with_embeddings.csv
├── analysis.py
├── search_similar_items.py
├── guardrails.py
├── generate_embeddings.py
├── test_prompt.py
└── README.md
```

## 🔐 API Keys

Create a `.env` or `config.py` to store your OpenAI API key securely. Do **not** commit your key.

## 📝 License

N/A