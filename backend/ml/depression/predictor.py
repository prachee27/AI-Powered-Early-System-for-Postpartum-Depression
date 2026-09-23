import logging

from backend.ml.depression.config import MODEL_PATH, MAX_LENGTH
from backend.ml.depression.schemas import DepressionPrediction
from backend.ml.depression.utils import sigmoid


class DepressionPredictor:
    """
    Depression prediction using a fine-tuned transformer model.
    """

    def __init__(self):
        self.model_available = False
        self.model_source = "keyword screening fallback"
        if not MODEL_PATH.is_dir():
            logging.getLogger(__name__).info(
                "No local depression model found at %s; using screening fallback.", MODEL_PATH
            )
            return
        try:
            import torch
            from transformers import AutoModelForSequenceClassification, AutoTokenizer

            self.torch = torch
            self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
            self.tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)
            self.model = AutoModelForSequenceClassification.from_pretrained(MODEL_PATH)
            self.model.to(self.device)
            self.model.eval()
            self.model_available = True
            self.model_source = f"local transformer model at {MODEL_PATH}"
        except Exception as exc:
            logging.getLogger(__name__).warning(
                "Local depression model is unavailable; using screening fallback: %s", exc
            )
            self.model_available = False

    def _tokenize(self, text: str):
        """
        Convert input text into model-ready tensors.
        """

        return self.tokenizer(
            text,
            padding=True,
            truncation=True,
            max_length=MAX_LENGTH,
            return_tensors="pt"
        ).to(self.device)

    def _predict_logits(self, inputs):
        """
        Run the transformer model and return raw logits.
        """

        with self.torch.no_grad():

            outputs = self.model(**inputs)

        return outputs.logits

    def _postprocess(self, logits):
        """
        Convert logits into a depression prediction.
        """

        probabilities = sigmoid(logits)

        score, prediction = self.torch.max(probabilities, dim=1)

        label = (
            "Depressed"
            if prediction.item() == 1
            else "Not Depressed"
        )

        return DepressionPrediction(
            label=label,
            score=round(score.item(), 4)
        )

    def predict(self, text: str):
        """
        Predict depression from input text.
        """

        if self.model_available:
            inputs = self._tokenize(text)
            logits = self._predict_logits(inputs)
            return self._postprocess(logits)

        lowered = text.lower()
        warning_terms = (
            "hopeless", "worthless", "want to die", "kill myself", "hurt myself",
            "nothing will get better", "empty", "cannot cope", "depressed",
            "depression", "can't go on", "cannot go on", "self harm",
        )
        is_depressed = any(term in lowered for term in warning_terms)
        return DepressionPrediction(
            label="Depressed" if is_depressed else "Not Depressed",
            score=0.6 if is_depressed else 0.6,
        )
