# Multi-Modal Neural Machine Translation App

## Overview

This Neural Machine Translation (NMT) application leverages an advanced sequence-to-sequence LSTM model with an attention mechanism to provide translation across multiple languages, focusing on English to Hindi, Bengali, Marathi, and German translations.

## Key Features

### Multi-Modal Translation
- Text translation
- Advanced attention-based sequence modeling
- Support for multiple Indian and European languages

### Technical Specifications
- **Input Language**: English
- **Output Languages**: 
  - Hindi
  - Bengali 
  - Marathi
  - German

## Model Architecture

### Model Details
- **Type**: Sequence-to-Sequence LSTM with Attention Layer
- **Encoder**: 
  - LSTM Layer with 300 units
  - Embedding dimension: 100
  - Dropout: 0.3
- **Decoder**:
  - LSTM Layer with 300 units
  - Custom Attention Mechanism
  - Dropout: 0.3

### Training Specifications
- **Dataset**: Multilingual translation dataset
- **Training Pairs**: 500,000 sentence pairs
- **Vocabulary Size**: 50,000 tokens
- **Maximum Sequence Length**: 40 tokens

## Performance Metrics

| Metric | Score |
|--------|-------|
| Training Loss | Decreased from 1.0394 to 0.1881 |
| Validation Loss | Stabilized at 0.9086 |
| Training Epochs | 5 |

## Technical Components

### Key Technologies
- TensorFlow/Keras
- Custom Attention Layer
- LSTM Neural Networks
- Sequence Padding
- Text Preprocessing

### Preprocessing Techniques
- Text cleaning
- Lowercase conversion
- Punctuation removal
- Tokenization
- Sequence padding

## Installation

### Prerequisites
- Python 3.8+
- TensorFlow
- Keras
- NumPy
- Pandas

### Setup Steps
```bash
# Clone the repository
git clone https://github.com/AniruddhMukherjee/TranslationProject.git
cd TranslationProject

# Install dependencies
pip install -r requirements.txt

# Install additional tools
sudo apt-get update
sudo apt-get install -y tesseract-ocr
```

## Project Structure
```
translation-project/
│
├── DATA/
│   ├── multi_language_translator.h5    # Trained model
│   ├── source_tokenizer.pkl            # Source language tokenizer
│   └── target_tokenizer.pkl            # Target language tokenizer
│
├── notebooks/
│   └── Single_Translation.ipynb        # Model training notebook
│
├── main.py                              # Main application
└── requirements.txt                    # Project dependencies
```

## Contributors
- [Dev Nandurbarkar](https://github.com/dev13n)

## Website
[Project Link](https://translationproject.streamlit.app)
