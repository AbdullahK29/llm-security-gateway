# LLM Security Gateway

This project implements a security gateway for systems that use Large Language Models (LLMs). The goal of the gateway is to analyze user input before it is processed by an LLM in order to reduce security risks such as prompt injection attacks and sensitive data leakage.

The system processes incoming requests through a structured pipeline that performs threat detection, sensitive data analysis, and policy enforcement. Microsoft Presidio is used for identifying personally identifiable information (PII), while additional custom rules allow the system to detect domain-specific data such as student IDs, API keys, and secret tokens.

By introducing these checks before the request reaches the language model, the gateway helps ensure that AI-powered systems operate in a safer and more controlled environment.

---

# System Pipeline

The input passes through several stages before a final decision is made.

User Input → Injection Detection → Presidio Analyzer → Policy Decision → Secure Output

### Injection Detection

The first stage analyzes the input for patterns that may indicate prompt injection or malicious instructions. If such patterns are detected, the request can be flagged or blocked.

### Presidio Analyzer

If the input passes the injection check, it is analyzed using Microsoft Presidio. This stage identifies sensitive entities such as emails, phone numbers, and other confidential data.

### Policy Decision

After analysis is completed, a decision module determines how the system should respond. Sensitive entities may be masked, while suspicious inputs may be restricted or modified before producing the final output.

---

# Features

Prompt Injection Detection

PII Detection using Microsoft Presidio

Custom Entity Recognizers

* Student ID detection
* API key detection
* Secret token detection

Context-Aware Scoring
Detection confidence is adjusted based on surrounding context to improve accuracy.

Composite Entity Detection
Multiple sensitive entities appearing together can increase risk levels.

Confidence Calibration
Detection results are filtered using a configurable confidence threshold.

Latency Measurement
Processing time for each stage of the pipeline is measured for evaluation.

---

# Requirements

Python 3.10 or higher

---

# Installation

## 1. Clone the Repository

```
git clone https://github.com/AbdullahK29/llm-security-gateway.git
cd llm-security-gateway
```

---

## 2. Create Virtual Environment

```
python -m venv venv
```

Activate the environment:

Windows

```
venv\Scripts\activate
```

Mac / Linux

```
source venv/bin/activate
```

---

## 3. Install Dependencies

```
pip install -r requirements.txt
```

---

## 4. Download the spaCy Language Model

```
python -m spacy download en_core_web_lg
```

This model is required by Presidio for natural language processing and entity recognition.

---

# Running the System

Start the FastAPI server using:

```
uvicorn main:app --reload
```

Once the server starts, open the interactive API interface in your browser:

```
http://127.0.0.1:8000/docs
```

This interface allows you to test the system by sending requests directly to the API.

---

# Project Structure

```
llm-security-gateway
│
├── main.py                # FastAPI application entry point
├── injection_detector.py # Prompt injection detection logic
├── presidio_config.py    # Presidio configuration and custom recognizers
├── policy_engine.py      # Decision logic for masking or blocking
├── tests/
│   └── test_prompts.txt  # Example prompts used for evaluation
├── requirements.txt      # Python dependencies
└── README.md
```

---

# Configuration

The system uses a confidence threshold to filter unreliable entity detections.

Default threshold: **0.6**

This value can be adjusted inside the policy or detection configuration files depending on the desired balance between sensitivity and accuracy.

Lower thresholds increase detection sensitivity but may introduce false positives, while higher thresholds reduce false detections but may miss some entities.

---

# Reproducing Evaluation Results

The results presented in the report can be reproduced using the following steps.

1. Start the server using the instructions above.
2. Open the API documentation interface at `/docs`.
3. Use the **/analyze** endpoint.
4. Submit the test prompts located in:

```
tests/test_prompts.txt
```

These prompts represent different scenarios including:

* Normal user input
* Prompt injection attempts
* Email and phone number detection
* Student ID detection
* API key and token detection
* Combined sensitive information scenarios

The API response will include:

* Injection detection result
* Identified PII entities
* Masked output text
* Policy decision
* Latency measurements for each processing stage

---

# Example Request

Input:

```
My email is abdullah@gmail.com
```

Example Output:

```
{
 "input": "My email is abdullah@gmail.com",
 "pii_detected": ["EMAIL_ADDRESS"],
 "masked_output": "My email is <EMAIL_ADDRESS>",
 "latency_seconds": {
   "injection_detection": 0.0001,
   "presidio_analysis": 0.03,
   "policy_decision": 0.00002
 }
}
```

---

# Technologies Used

Python 3

FastAPI

Microsoft Presidio

spaCy NLP

---

# Purpose of the Project

The purpose of this project is to demonstrate how a structured security layer can be integrated into LLM-based systems. By combining injection detection, sensitive data analysis, and policy enforcement, the gateway helps reduce common risks associated with large language models.

The project also illustrates how open-source tools such as Microsoft Presidio and FastAPI can be combined to build practical security solutions for modern AI applications.


