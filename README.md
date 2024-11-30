# Multi-Modal Translation App

**A neural machine translation (NMT) application powered by a sequence-to-sequence transformer model, supporting text, speech, and image inputs for seamless multi-language translation.**

---

## Model Architecture

- **Type:** Sequence-to-sequence Transformer
- **Key Components:**
  - **Encoder:** 6 layers, 8 attention heads
  - **Decoder:** 6 layers, 8 attention heads
  - **Positional Encoding** to capture word order
  - **Multi-head Attention** for capturing complex patterns
  - **Feed-forward Networks** for efficient learning

---

## Project Structure

```plaintext
project/
├── DATA/
│   ├── multi_language_translator.h5   # Trained model
│   ├── source_tokenizer.pkl           # English tokenizer
│   └── target_tokenizer.pkl           # Target languages tokenizer
├── app.py                             # Main Streamlit application
└── requirements.txt                   # Dependencies
