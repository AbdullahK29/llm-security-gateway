# LLM Security Gateway

This project implements a secure processing pipeline for Large Language Model (LLM) inputs.
The system detects prompt injection attacks and sensitive information using Microsoft Presidio before allowing the request to proceed.

## Pipeline

User Input → Injection Detection → Presidio Analyzer → Policy Decision → Output

## Features

* Prompt Injection Detection
* PII Detection using Microsoft Presidio
* Custom Recognizers:

  * Student ID
  * API Keys
  * Secret Tokens
* Context-Aware Scoring
* Composite Entity Detection
* Confidence Calibration
* Latency Measurement

---

# Installation

## 1. Clone the Repository

```
git clone https://github.com/AbdullahK29/llm-security-gateway.git
cd llm-security-gateway
```

## 2. Create Virtual Environment

```
python -m venv venv
```

Activate it:

Windows

```
venv\Scripts\activate
```

Mac/Linux

```
source venv/bin/activate
```

## 3. Install Dependencies

```
pip install -r requirements.txt
```

## 4. Download spaCy Model

```
python -m spacy download en_core_web_lg
```

---

# Running the System

Start the FastAPI server:

```
uvicorn main:app --reload
```

Open in browser:

```
http://127.0.0.1:8000/docs
```

---

# Reproducing Evaluation Results

To reproduce the results used in the report:

1. Run the server using the steps above
2. Open `/docs`
3. Use the `/analyze` endpoint
4. Test the prompts from:

```
tests/test_prompts.txt
```

The API response will show:

* Injection detection results
* PII entities detected
* Masked output
* Policy decision
* Latency measurements

---

# Example Response

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

* FastAPI
* Microsoft Presidio
* spaCy NLP
* Python 3
