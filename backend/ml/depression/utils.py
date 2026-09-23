def sigmoid(logits):
    """Convert classifier logits to probabilities when PyTorch is installed."""
    import torch
    return torch.softmax(logits, dim=1)
