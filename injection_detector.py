class InjectionDetector:

    def __init__(self):

        # phrases commonly used in prompt injection attacks
        self.attack_patterns = {
            "ignore previous instructions": 0.9,
            "reveal system prompt": 0.95,
            "jailbreak": 0.8,
            "act as developer": 0.7,
            "bypass safety": 0.85
        }

        # threshold above which the prompt is considered malicious
        self.threshold = 0.7

    def detect(self, text):

        text = text.lower()

        score = 0
        triggers = []

        for pattern in self.attack_patterns:

            if pattern in text:
                score += self.attack_patterns[pattern]
                triggers.append(pattern)

        return {
            "score": score,
            "triggers": triggers,
            "is_injection": score >= self.threshold
        }