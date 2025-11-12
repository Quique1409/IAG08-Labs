import numpy as np
def activation(w, x, threshold):
    z = w * x
    if z.sum() + threshold > 0:
        return 1
    else:
        return 0


person = [[0.30, 0.40], [0.40, 0.30], [0.30, 0.20], [0.40, 0.10], [0.50, 0.20],
          [0.40, 0.80], [0.60, 0.80], [0.50, 0.60], [0.70, 0.60], [0.80, 0.50]]
clas = [0, 0, 0, 0, 0, 1, 1, 1, 1, 1]
w = np.random.uniform(-1,1, size=2)
b = np.random.uniform(-1,1)

learning_rate = 0.01
epochs = 1000

for epoca in range(epochs):
    error_in_epoch = 0
    for i in range(len(person)):
        prediction = activation(w, person[i], b)
        error = clas[i] - prediction
        error_in_epoch += error**2
        w[0] += learning_rate * person[i][0] * error
        w[1] += learning_rate * person[i][1] * error
        b += learning_rate * error
    print(error_in_epoch)

print (w, b, activation(w, [50,50], b))