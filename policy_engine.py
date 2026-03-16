class PolicyEngine:

    def __init__(self):
        # Thresholds
        self.injection_threshold = 0.7

    def decide(self, injection_result, pii_entities, masked_text, original_text):

        # Rule 1: If injection detected → BLOCK
        if injection_result["is_injection"]:
            return {
                "status": "blocked",
                "reason": "prompt injection detected",
                "output": None
            }

        # Rule 2: If PII detected → MASK
        if pii_entities:
            return {
                "status": "masked",
                "reason": f"PII detected: {', '.join(pii_entities)}",
                "output": masked_text
            }

        # Rule 3: Safe text → ALLOW
        return {
            "status": "allowed",
            "reason": "no issues detected",
            "output": original_text
        }