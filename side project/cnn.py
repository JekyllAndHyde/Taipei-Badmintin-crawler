def forward(image, label):
    """
    Performs a forward pass of the CNN and calculates the accuracy and
    cross-entropy loss.
    -- image is a 2d numpy array
    -- label is a digit
    """
    # We transform the image from [0, 255] to [-0.5, 0.5] to make it easier
    # to work with. This is standard practice
    out = conv.forward((image / 255) - 0.5)
    out = pool.forward(out)
    out = softmax.forward(out)

    # Calculate cross-entropy loss and accuracy.
    # np.log() is the natural log.
    loss = -np.log(out[label])
    acc = 1 if np.argmax(out) == label else 0

    return out, loss, acc

def train(im, label, lr = 0.01):
    """
    Completes a full training step on the given image and label.
    return the Cross-Entropy ans accuracy
    -- lr is the learning rate
    """
    # Forward
    out, loss, acc = forward(im, label)

    # Calculate initial gradient
    gradient = np.zeros(10)
    gradient[label] = -1 / out[label]

    # Backprop
    gradient = softmax.backprop(gradient, lr)
    gradient = pool.backprop(gradient)
    gradient = conv.backprop(gradient, lr)

    return loss, acc


# print("MNIST CNN initialized!")

# Train the CNN for 3 epochs
def cnn(train_images, train_labels):
    for epoch in range(3):
        print('--- Epoch %d ---' % (epoch + 1))
        # Shuffle the training data
        permutation = np.random.permutation(len(train_images))
        train_images = train_images[permutation]
        train_labels = train_labels[permutation]
        # Train!
        loss = 0
        num_correct = 0
        for i, (im, label) in enumerate(zip(train_images, train_labels)):
            if i > 0 and i % 100 == 99:
                print(
                '[Step %d] Past 100 steps: Average Loss %.3f | Accuracy: %d%%' %
                (i + 1, loss / 100, num_correct)
                )
                loss = 0
                num_correct = 0

            l, acc = train(im, label)
            loss += l
            num_correct += acc

"""
# Test the CNN
print('\n--- Testing the CNN ---')
loss = 0
num_correct = 0
for i, (im, label) in enumerate(zip(test_images, test_labels)):
    # Print states every 100 steps.
    if i % 100 == 99:
        print(
        '[Step %d] Past 100 steps: Average Loss %.3f | Accuracy: %d%%' %
        (i + 1, loss / 100, num_correct)
        )
        loss = 0
        num_correct = 0

    # Train
    l, acc = train(im, label)
    loss += l
    num_correct += acc
print(cv2.imshow("img", train_images[0]))
cv2.waitKey(0)
"""
