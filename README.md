# AlphaSense

A demonstration project showcasing how to leverage financial news and stock price data for fine-tuning Language Models (LLMs) and implementing a Retrieval-Augmented Generation (RAG) system for financial insights and investment recommendations.

## Project Overview

AlphaSense combines the power of Large Language Models with financial domain data to create an intelligent system capable of:

1. Collecting and processing financial news and stock price data
2. Fine-tuning LLMs on financial domain data
3. Building a RAG system to provide context-aware financial insights
4. Generating investment recommendations based on user queries

## Project Structure

```
AlphaSense/
├── data/                  # Raw and processed data
├── src/                   # Source code
│   ├── data_scraper.py    # Functions for fetching stock data and news
│   ├── data_processing.py # Data cleaning and preparation
│   ├── fine_tune.py       # LLM fine-tuning code
│   └── rag_integration.py # RAG system implementation
├── alpha.ipynb            # Demo notebook showing the complete workflow
├── requirements.txt       # Project dependencies
├── .env                   # Environment variables
└── README.md              # Project documentation
```

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/AlphaSense.git
cd AlphaSense
```

2. Create a virtual environment and install dependencies:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Usage

The project workflow is demonstrated in the `alpha.ipynb` notebook, which covers:

1. Data collection from financial sources
2. Data processing and preparation
3. Fine-tuning an LLM on financial data
4. Building and querying the RAG system
5. Generating investment recommendations

To run the notebook:
```bash
jupyter notebook alpha.ipynb
```

## Components

### Data Collection
- Stock price data using yfinance
- Financial news from Yahoo Finance

### LLM Fine-tuning
- Uses Hugging Face Transformers
- Implements parameter-efficient fine-tuning techniques
- Focuses on financial domain adaptation

### RAG System
- Vectorizes financial documents using SentenceTransformers
- Creates vector indices using FAISS/Chroma
- Retrieves relevant context for user queries
- Generates responses using the fine-tuned LLM

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- This project is for educational purposes
- Inspired by advancements in LLMs and their applications in finance 