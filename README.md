# Multi-Modal Neural Machine Translation App

## Overview

This cutting-edge Neural Machine Translation (NMT) application leverages state-of-the-art transformer architecture to provide seamless translation across multiple input modalities and languages.

## Key Features

- **Multi-Modal Input Support**
  - Text translation
  - Speech-to-text translation
  - Image-based translation (OCR integration)

- **Language Coverage**
  - Input Language: English
  - Output Languages: 
    - Hindi
    - Bengali
    - Marathi
    - German

- **Translation Capabilities**
  - High accuracy: 94% translation precision
  - Text-to-speech output for translated results

## Model Architecture

### Transformer Model Specifications
- **Type**: Sequence-to-sequence Transformer
- **Encoder**: 6 layers with 8 multi-head attention mechanisms
- **Decoder**: 6 layers with 8 multi-head attention mechanisms
- **Key Technologies**:
  - Positional encoding
  - Multi-head attention
  - Feed-forward neural networks

### Training Details
- **Training Dataset**: 500,000 sentence pairs per language
- **Vocabulary Size**: 50,000 tokens
- **Maximum Sequence Length**: 40 tokens
- **Training Environment**:
  - Hardware: 4x NVIDIA V100 GPUs
  - Total Training Time: 72 hours

## Performance Metrics

| Metric | Score |
|--------|-------|
| BLEU Score | 38.2 |
| Word Error Rate | 5.8% |
| Character Error Rate | 3.2% |

### Runtime Performance
- Inference Time: ~100ms per translation
- Memory Usage: ~2GB RAM
- GPU Memory: ~4GB VRAM

## Installation

### Prerequisites
- Python 3.8+
- pip
- Tesseract OCR

### Setup Steps

1. Clone the repository:
   ```bash
   git clone https://github.com/AniruddhMukherjee/TranslationProject.git
   cd TranslationProject
   ```

2. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Install OCR tools:
   ```bash
   sudo apt-get update
   sudo apt-get install -y tesseract-ocr libtesseract-dev
   ```

## Running the Application

Launch the Streamlit application:
```bash
streamlit run app.py
```

## 🔍 Project Structure

```
project/
│
├── DATA/
│   ├── multi_language_translator.h5    # Trained model
│   ├── source_tokenizer.pkl            # English tokenizer
│   └── target_tokenizer.pkl            # Target languages tokenizer
│
├── app.py                              # Main Streamlit application
└── requirements.txt                    # Project dependencies
```

## Training Methodology

### Data Preprocessing
- Advanced tokenization techniques
- Sequence padding
- Language-specific token integration
- Noise injection for model robustness

### Training Strategies
- Teacher forcing for guided learning
- Label smoothing (smoothing factor: 0.1)
- Dropout regularization (rate: 0.1)
- Batch size: 64
- Training epochs: 50

## Future Roadmap
- Expand language support
- Improve translation accuracy
- Enhance multi-modal input capabilities
- Optimize inference speed

## Contributors
[Dev N]

## Website
[Project Link](https://translationproject.streamlit.app)
