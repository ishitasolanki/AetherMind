import logging
import random
import torch
import torch.nn as nn
from config import (
    INPUT_SIZE, HIDDEN_SIZE, OUTPUT_SIZE,
    TRAINING_DATA_SIZE, TRAINING_EPOCHS, LEARNING_RATE, LOG_EVERY_N_EPOCHS,
    MAX_USAGE, MAX_AGE,
    EMOTION_WEIGHT, USAGE_WEIGHT, RECENCY_WEIGHT
)

logger = logging.getLogger(__name__)


class ImportanceNet(nn.Module):
    def __init__(self):
        super().__init__()

        self.model = nn.Sequential(
            nn.Linear(INPUT_SIZE, HIDDEN_SIZE),   # input: usage, age, emotion
            nn.ReLU(),
            nn.Linear(HIDDEN_SIZE, OUTPUT_SIZE),
            nn.Sigmoid()                          # output between 0 and 1
        )

    def forward(self, x):
        return self.model(x)


def generate_data(n=TRAINING_DATA_SIZE):
    X = []
    y = []

    for _ in range(n):

        usage = random.randint(0, MAX_USAGE)
        age = random.randint(0, MAX_AGE)
        emotion = random.random()

        recency = 1 / (1 + age)

        importance = (
            EMOTION_WEIGHT * emotion +
            USAGE_WEIGHT * (usage / MAX_USAGE) +
            RECENCY_WEIGHT * recency
        )

        X.append([usage, age, emotion])
        y.append([importance])

    return torch.tensor(X, dtype=torch.float32), torch.tensor(y, dtype=torch.float32)


def train_model():

    logger.info("Generating synthetic training data...")
    X, y = generate_data()

    model = ImportanceNet()

    optimizer = torch.optim.Adam(model.parameters(), lr=LEARNING_RATE)
    loss_fn = nn.MSELoss()

    logger.info(f"Training ImportanceNet for {TRAINING_EPOCHS} epochs...")
    for epoch in range(TRAINING_EPOCHS):

        pred = model(X)
        loss = loss_fn(pred, y)

        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        if epoch % LOG_EVERY_N_EPOCHS == 0:
            print(f"  Epoch {epoch:>4d} | Loss: {loss.item():.6f}")

    final_loss = loss.item()
    logger.info(f"Training complete. Final loss: {final_loss:.6f}")
    print(f"  Training complete. Final loss: {final_loss:.6f}")

    return model


def predict_importance(model, usage, age, emotion):

    x = torch.tensor([[usage, age, emotion]], dtype=torch.float32)

    with torch.no_grad():
        importance = model(x).item()

    return importance