import numpy as np
from data.city_graph import VALID_SEVERITY

# ── Training Data ──────────────────────────────────────────────
TRAINING_DATA = [
    ([1, 2, 1, 0.90, 1, 1.0], 3),
    ([1, 2, 1, 0.85, 1, 1.0], 3),
    ([1, 2, 0, 0.70, 1, 1.0], 2),
    ([1, 1, 1, 0.60, 1, 1.0], 2),
    ([1, 1, 0, 0.50, 0, 1.0], 2),
    ([1, 0, 1, 0.40, 1, 1.0], 2),
    ([1, 0, 0, 0.30, 0, 1.0], 1),
    ([0, 0, 0, 0.20, 0, 1.0], 0),
    ([0, 0, 0, 0.10, 0, 1.0], 0),
    ([0, 1, 0, 0.40, 0, 1.0], 1),
    ([0, 1, 1, 0.50, 0, 1.0], 1),
    ([0, 2, 1, 0.80, 1, 1.0], 1),
    ([1, 2, 1, 0.95, 1, 1.0], 3),
    ([1, 1, 1, 0.75, 1, 1.0], 2),
    ([0, 0, 0, 0.15, 0, 1.0], 0),
]

PRIORITY_LABELS = {0: "Low", 1: "Normal", 2: "High", 3: "Critical"}

# ── Activation Functions ───────────────────────────────────────

def relu(x):
    """
    ReLU activation function.
    Returns x if positive, 0 otherwise.
    """
    return np.maximum(0, x)

def relu_derivative(x):
    """
    Derivative of ReLU for backpropagation.
    Returns 1 if x > 0, else 0.
    """
    return (x > 0).astype(float)

def softmax(x):
    """
    Softmax activation for output layer.
    Converts raw scores to probabilities that sum to 1.
    """
    e_x = np.exp(x - np.max(x))  # subtract max for numerical stability
    return e_x / e_x.sum()

# ── ANN Class ─────────────────────────────────────────────────

class ANN:
    """
    Simple Multi Layer Perceptron with:
    - Input layer  : 6 neurons
    - Hidden layer1: 8 neurons (ReLU)
    - Hidden layer2: 6 neurons (ReLU)
    - Output layer : 4 neurons (Softmax)
    Trained using backpropagation and gradient descent.
    """

    def __init__(self):
        """
        Initializes weights and biases randomly using
        small values for stable training.
        """
        np.random.seed(42)  # for reproducibility

        # weights — random small values
        self.W1 = np.random.randn(6, 8) * 0.1   # input → hidden1
        self.W2 = np.random.randn(8, 6) * 0.1   # hidden1 → hidden2
        self.W3 = np.random.randn(6, 4) * 0.1   # hidden2 → output

        # biases — start at zero
        self.b1 = np.zeros(8)
        self.b2 = np.zeros(6)
        self.b3 = np.zeros(4)

    def forward(self, x):
        """
        Forward pass through the network.
        Returns output probabilities for each class.
        """
        # hidden layer 1
        self.z1 = np.dot(x, self.W1) + self.b1
        self.a1 = relu(self.z1)

        # hidden layer 2
        self.z2 = np.dot(self.a1, self.W2) + self.b2
        self.a2 = relu(self.z2)

        # output layer
        self.z3 = np.dot(self.a2, self.W3) + self.b3
        self.a3 = softmax(self.z3)

        return self.a3

    def one_hot(self, label, num_classes=4):
        """
        Converts integer label to one hot encoded vector.
        Example: 2 → [0, 0, 1, 0]
        """
        vec = np.zeros(num_classes)
        vec[label] = 1.0
        return vec

    def train(self, training_data, epochs=1000, lr=0.01):
        """
        Trains the ANN using backpropagation and gradient descent.
        Runs for specified number of epochs over training data.
        """
        print("[ANN] Training started...")

        for epoch in range(epochs):
            total_loss = 0

            for features, label in training_data:
                x = np.array(features, dtype=float)
                y = self.one_hot(label)

                # ── Forward Pass ──
                output = self.forward(x)

                # ── Loss (Cross Entropy) ──
                loss = -np.sum(y * np.log(output + 1e-8))
                total_loss += loss

                # ── Backward Pass ──

                # output layer gradient
                d_out = output - y                              # (4,)

                # hidden2 → output
                d_W3 = np.outer(self.a2, d_out)                # (6,4)
                d_b3 = d_out                                    # (4,)

                # hidden2 gradient
                d_a2 = np.dot(d_out, self.W3.T)                # (6,)
                d_z2 = d_a2 * relu_derivative(self.z2)         # (6,)

                # hidden1 → hidden2
                d_W2 = np.outer(self.a1, d_z2)                 # (8,6)
                d_b2 = d_z2                                     # (6,)

                # hidden1 gradient
                d_a1 = np.dot(d_z2, self.W2.T)                 # (8,)
                d_z1 = d_a1 * relu_derivative(self.z1)         # (8,)

                # input → hidden1
                d_W1 = np.outer(x, d_z1)                       # (6,8)
                d_b1 = d_z1                                     # (8,)

                # ── Update Weights ──
                self.W3 -= lr * d_W3
                self.b3 -= lr * d_b3
                self.W2 -= lr * d_W2
                self.b2 -= lr * d_b2
                self.W1 -= lr * d_W1
                self.b1 -= lr * d_b1

            # print loss every 200 epochs
            if (epoch + 1) % 200 == 0:
                print(f"[ANN] Epoch {epoch+1}/{epochs} — Loss: {total_loss:.4f}")

        print("[ANN] Training complete.")

    def predict(self, features):
        """
        Predicts priority label for a given feature vector.
        Returns predicted priority as a string.
        """
        x = np.array(features, dtype=float)
        output = self.forward(x)
        predicted_index = np.argmax(output)
        return PRIORITY_LABELS[predicted_index]


# ── Module level ANN instance ──────────────────────────────────

_ann_model = None

def run_ann(request):
    """
    Master ANN function. Trains model if not already trained.
    Uses feature vector from request to predict priority level.
    Returns predicted priority string.
    """
    global _ann_model

    # train only once
    if _ann_model is None:
        _ann_model = ANN()
        _ann_model.train(TRAINING_DATA, epochs=1000, lr=0.01)

    feature_vector = request["feature_vector"]
    predicted      = _ann_model.predict(feature_vector)

    print(f"[ANN] Feature Vector : {feature_vector}")
    print(f"[ANN] Predicted Priority: {predicted}")

    return predicted

# Index 0 → vehicle_class    (1=Emergency, 0=Civilian)
# Index 1 → severity         (0=low, 1=medium, 2=high)
# Index 2 → time_sensitivity (1=True, 0=False)
# Index 3 → traffic_density  (0.0 to 1.0)
# Index 4 → priority_claim   (1=True, 0=False)
# Index 5 → distance         (1.0 hardcoded for now)