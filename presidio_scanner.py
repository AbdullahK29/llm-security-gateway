from presidio_analyzer import AnalyzerEngine, PatternRecognizer, Pattern
from presidio_anonymizer import AnonymizerEngine


class PresidioScanner:

    def __init__(self):

        # Initialize Presidio
        self.analyzer = AnalyzerEngine()
        self.anonymizer = AnonymizerEngine()

        # Add custom recognizers
        self.add_custom_recognizers()

    def add_custom_recognizers(self):

        #STUDENT ID recognizer
        student_pattern = Pattern(
            name="STUDENT_ID_PATTERN",
            regex=r"STU-\d{4,6}",
            score=0.9
        )

        student_recognizer = PatternRecognizer(
            supported_entity="STUDENT_ID",
            patterns=[student_pattern]
        )

        self.analyzer.registry.add_recognizer(student_recognizer)

        #API KEY recognizer
        api_pattern = Pattern(
            name="API_KEY_PATTERN",
            regex=r"API-[A-Za-z0-9]{10,}",
            score=0.95
        )

        api_recognizer = PatternRecognizer(
            supported_entity="API_KEY",
            patterns=[api_pattern]
        )

        self.analyzer.registry.add_recognizer(api_recognizer)

        #SECRET TOKEN recognizer
        secret_pattern = Pattern(
            name="SECRET_TOKEN_PATTERN",
            regex=r"SECRET-[A-Za-z0-9]{12,}",
            score=0.95
        )

        secret_recognizer = PatternRecognizer(
            supported_entity="SECRET_TOKEN",
            patterns=[secret_pattern]
        )

        self.analyzer.registry.add_recognizer(secret_recognizer)

    def scan(self, text):

        results = self.analyzer.analyze(
            text=text,
            entities=[],
            language="en"
        )

        # ---------------------------
        # Context-Aware Scoring
        # ---------------------------
        lower_text = text.lower()

        for entity in results:

            # If API_KEY appears with suspicious context
            if entity.entity_type == "API_KEY" and "send secret" in lower_text:
                entity.score = min(1.0, entity.score + 0.2)

            # If SECRET_TOKEN appears with leak context
            if entity.entity_type == "SECRET_TOKEN" and "expose" in lower_text:
                entity.score = min(1.0, entity.score + 0.2)

        # ---------------------------
        # Confidence Calibration
        # ---------------------------
        calibrated_results = []

        for entity in results:
            if entity.score >= 0.6:   # filter low confidence entities
                calibrated_results.append(entity)

        # ---------------------------
        # Composite Entity Detection
        # Example: EMAIL + PHONE together
        # ---------------------------
        entity_types = [e.entity_type for e in calibrated_results]

        if "EMAIL_ADDRESS" in entity_types and "PHONE_NUMBER" in entity_types:
            print("Composite entity detected: CONTACT_INFORMATION")

        return calibrated_results

    def anonymize(self, text):

        results = self.scan(text)

        anonymized_text = self.anonymizer.anonymize(
            text=text,
            analyzer_results=results
        )

        return anonymized_text.text, results