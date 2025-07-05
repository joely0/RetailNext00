# RetailNext00

A multimodal fashion recommendation system that analyzes clothing images and suggests matching outfit items using OpenAI's API and embedding-based similarity search.

Built for basic local demo. 

Original cookbook - https://cookbook.openai.com/examples/how_to_combine_gpt4o_with_rag_outfit_assistant

## Installation & Setup Guide

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

## ▶Usage

### Command Line Demo
```bash
python run_demo.py
```

### Web Interface (Recommended)
```bash
streamlit run app.py
```

The Streamlit app provides a user-friendly interface where you can:
- Upload clothing images
- View AI analysis results
- See matching item recommendations
- Validate matches with guardrails

## Features

- **GPT-4o mini** for multimodal image analysis
- **RAG (Retrieval-Augmented Generation)** for similarity search
- **Embeddings** using OpenAI's text-embedding-3-large
- **Guardrails** for quality control and validation
- **Streamlit UI** for easy interaction
- **Error handling** for robust operation

## Folder Structure

```
RetailNext00/
├── main.py
├── app.py                    # Streamlit web interface
├── run_demo.py              # Command line demo
├── config.py
├── requirements.txt
│
├── match/
│   ├── image_match.py
│   └── search_similar_items.py
│
├── embeddings/
│   ├── generate_embeddings.py
│   └── embed_samples_load.py
│
├── utils/
│   └── guardrails.py
│
├── data/
│   └── sample_clothes/
│       ├── sample_images/
│       ├── sample_styles.csv
│       └── sample_styles_with_embeddings.csv
│
└── README.md
```

## Technology Stack

- **OpenAI API**: GPT-4o mini, text-embedding-3-large
- **Python**: pandas, numpy, streamlit
- **Machine Learning**: cosine similarity, embeddings
- **Web Framework**: Streamlit for UI

## License

N/A - just testing this cookbook