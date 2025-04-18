# Taming LLMs with Groq API
📌 **Overview**

This project implements a content classification and analysis tool using the Groq API. It applies structured prompts, analyzes confidence in classifications, and compares different prompt strategies.

✅ **Features**

Basic LLM completion using the Groq API.

Structured completions with key section extraction.

Text classification with confidence filtering.

Comparison of different prompt strategies (Basic, Structured, Few-Shot).

⚙️ **Setup Instructions**

1️⃣ Clone the Repository

git clone https://github.com/ShahdTarek4/taming_llms.git
cd taming_llms

2️⃣ Create a Virtual Environment 

python -m venv venv

venv\Scripts\activate 

3️⃣ Install Required Libraries

pip install groq python-dotenv

4️⃣ Set Up Your API Key

Create a .env file inside the project directory:

touch .env

Open .env and add your Groq API key:

GROQ_API_KEY=your_api_key_here

🚀 **Usage Instructions**

🔹 Running Part 1: Basic Completion

python taming_llm.py

Expected Output: Model generates a response to a simple question.

🔹 Running Part 2: Structured Completion & Extraction

python taming_llm.py

Expected Output: Structured AI response with extracted key sections.

🔹 Running Part 3: Classification with Confidence Analysis

python taming_llm.py

Expected Output: Classified text with confidence levels and reasoning.

🔹 Running Part 4: Prompt Strategy Comparison

python taming_llm.py

Expected Output: Comparison of classification results across different prompt strategies.


📂 **Project Structure**

│-- taming_llm.py         # Main Python script

│-- .env.example          # Sample .env file (without actual API key)

│-- README.md             # Project documentation


🛠 **Troubleshooting**

1. ModuleNotFoundError?

Run: pip install groq python-dotenv


