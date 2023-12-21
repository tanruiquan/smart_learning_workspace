import torch
import torch.nn as nn
from sklearn import metrics

torch.manual_seed(42)


def train_model(model, X_train, y_train, criterion, optimizer, num_epochs=10, device="cpu"):
    """
    Generic training loop for PyTorch models.

    Args:
        model (torch.nn.Module): The neural network model to train.
        criterion (torch.nn.Module): The loss function (e.g., nn.CrossEntropyLoss() for classification).
        optimizer (torch.optim.Optimizer): The optimizer (e.g., Adam, SGD, etc.).
        num_epochs (int): Number of training epochs (default is 10).
        device (str): Device for training, "cuda" for GPU or "cpu" for CPU (default is "cuda").

    Returns:
        model: Trained model.
    """

    # Set the model and data to the specified device
    model.to(device)
    X_train, y_train = X_train.to(device), y_train.to(device)

    model.train()

    # Training loop
    for epoch in range(num_epochs):

        # Zero the parameter gradients
        optimizer.zero_grad()

        # Forward pass
        outputs = model(X_train)
        loss = criterion(outputs, y_train)

        # Backward pass and optimization
        loss.backward()
        optimizer.step()

        # Print the average loss for this epoch
        print(
            f"Epoch {epoch + 1}/{num_epochs}, Loss: {loss.item():.4f}")

    return model


def evaluate_model(model, X_test, y_test, criterion, device="cpu"):
    """
    Generic evaluation function for PyTorch models.

    Args:
        model (torch.nn.Module): The neural network model to evaluate.
        criterion (torch.nn.Module): The loss function (e.g., nn.CrossEntropyLoss() for classification).
        device (str): Device for evaluation, "cuda" for GPU or "cpu" for CPU (default is "cuda").

    Returns:
        accuracy (float): Accuracy of the model on the evaluation dataset.
        average_loss (float): Average loss on the evaluation dataset.
    """

    # Set the model and data to the specified device
    model.to(device)
    X_test, y_test = X_test.to(device), y_test.to(device)

    model.eval()

    with torch.no_grad():
        # Forward pass
        outputs = model(X_test)
        y_pred = outputs.argmax(dim=1)

    score = metrics.f1_score(y_test.cpu(), y_pred.cpu(), average='micro')
    print(f"F1 score: {score}")

    return score
