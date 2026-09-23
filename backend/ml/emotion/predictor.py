#This is the core module.
#Responsibilities:

#Load the Hugging Face model.
#Load the tokenizer.
#Accept text input.
#Predict emotions.
#Return structured output.

#Everything related to emotion prediction stays here.

from backend.ml.emotion.config import MODEL_NAME, MAX_LENGTH 

class EmotionPredictor:
    """Emotion prediction using a pretrained Hugging Face transformer model."""

    def __init__(self):
        """Load the model when available; otherwise use a local fallback."""
        self.model_available = False
        try:
            import torch
            from transformers import AutoModelForSequenceClassification, AutoTokenizer

            self.torch = torch
            self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
            self.tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
            self.model = AutoModelForSequenceClassification.from_pretrained(MODEL_NAME)
            self.model.to(self.device)
            self.model.eval()
            self.id2label = self.model.config.id2label
            self.model_available = True
        except Exception:
            # The application remains usable on a new machine without a
            # downloaded model. This is deliberately a simple screening fallback.
            self.model_available = False

    def _tokenize(self, text: str):
        """Convert input text into model-ready tensors."""

        return self.tokenizer(
        text,
        padding=True,
        truncation=True,
        max_length=MAX_LENGTH,
        return_tensors="pt"
    ).to(self.device)

    def _predict_logits(self, inputs):
        """Run the transformer model and return raw logits."""

        with self.torch.no_grad():
            outputs = self.model(**inputs)

        return outputs.logits

    
    def _postprocess(self, logits):
        """
        Convert logits into the top 3 emotions.
        """

        probabilities = self.torch.sigmoid(logits).squeeze()

        emotions = []

        for idx, score in enumerate(probabilities):
            emotions.append({
                "label": self.id2label[idx],
                "score": round(score.item(), 4)
            })

        emotions.sort(
            key=lambda x: x["score"],
            reverse=True
        )

        top3 = emotions[:3]

        return {
        "top_emotions": top3
        }


    def predict(self, text: str):
        """
        Predict emotions from input text.
        """

        if self.model_available:
            inputs = self._tokenize(text)
            logits = self._predict_logits(inputs)
            return self._postprocess(logits)

        lowered = text.lower()
        very_sad_terms = ("want to die", "kill myself", "hurt myself", "hopeless", "terrified", "depressed", "cannot go on", "can't go on")
        sad_terms = ("sad", "cry", "exhausted", "overwhelmed", "lonely", "cannot sleep", "depression")
        happy_terms = ("happy", "grateful", "joy", "love", "excited", "better")
        if any(term in lowered for term in very_sad_terms):
            label = "grief"
        elif any(term in lowered for term in sad_terms):
            label = "sadness"
        elif any(term in lowered for term in happy_terms):
            label = "joy"
        else:
            label = "neutral"
        return {"top_emotions": [{"label": label, "score": 0.6}]}
