import numpy as np
from sklearn import datasets
from sklearn.model_selection import train_test_split
from sklearn.linear_model import Perceptron
from sklearn.metrics import accuracy_score, classification_report


# The Iris dataset is included in sklearn
iris = datasets.load_iris()
X = iris.data
y = iris.target # Labels (0: Setosa, 1: Versicolor, 2: Virginica)

print(f"Total samples: {len(X)}")
print(f"Classes to predict: {iris.target_names}")

# 'test_size=0.2' reserves 20% for testing
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

print(f"Training samples: {len(X_train)}")
print(f"Test samples: {len(X_test)}")


# Scikit-learn automatically handles multiclass classification
ppn = Perceptron(max_iter=1000, eta0=0.1, random_state=42)

# Train the model with 80% of the data
ppn.fit(X_train, y_train)

# Make predictions on the remaining 20%
y_pred = ppn.predict(X_test)

# Calculate accuracy
accuracy = accuracy_score(y_test, y_pred)

print("-" * 30)
print(f"Model Accuracy: {accuracy * 100:.2f}%")
print("-" * 30)

# Detailed classification report
print("Classification Report:\n")
print(classification_report(y_test, y_pred, target_names=iris.target_names))