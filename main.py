from fastapi import FastAPI
from injection_detector import InjectionDetector
from presidio_scanner import PresidioScanner
from policy_engine import PolicyEngine
import time

app = FastAPI()

detector = InjectionDetector()
scanner = PresidioScanner()
policy = PolicyEngine()


@app.get("/")
def home():
    return {"message": "LLM Security Gateway Running"}


@app.post("/analyze")
def analyze_input(data: dict):

    text = data.get("text", "")

    # Start total timer
    total_start = time.perf_counter()

    # ---------------------------
    # Injection Detection
    # ---------------------------
    inj_start = time.perf_counter()
    injection_result = detector.detect(text)
    inj_end = time.perf_counter()

    injection_latency = inj_end - inj_start

    # ---------------------------
    # Presidio Analysis
    # ---------------------------
    pres_start = time.perf_counter()
    masked_text, pii_results = scanner.anonymize(text)
    pres_end = time.perf_counter()

    presidio_latency = pres_end - pres_start

    pii_entities = [str(entity.entity_type) for entity in pii_results]

    # ---------------------------
    # Policy Decision
    # ---------------------------
    pol_start = time.perf_counter()
    decision = policy.decide(
        injection_result=injection_result,
        pii_entities=pii_entities,
        masked_text=masked_text,
        original_text=text
    )
    pol_end = time.perf_counter()

    policy_latency = pol_end - pol_start

    # Total latency
    total_end = time.perf_counter()
    total_latency = total_end - total_start

    return {
        "input": text,
        "injection_analysis": injection_result,
        "pii_detected": pii_entities,
        "masked_output": masked_text,
        "policy_decision": decision,

        "latency_seconds": {
            "injection_detection": injection_latency,
            "presidio_analysis": presidio_latency,
            "policy_decision": policy_latency,
            "total_pipeline": total_latency
        }
    }