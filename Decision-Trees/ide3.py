import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.utils import resample
from sklearn.metrics import confusion_matrix, precision_recall_fscore_support

class Node:
    def __init__(self, feature=None, threshold=None, left=None, right=None, value=None):
        self.feature = feature
        self.threshold = threshold
        self.left = left
        self.right = right
        self.value = value  # This is the class label for leaf nodes

def entropy(y):
    classes, counts = np.unique(y, return_counts=True)
    entropy_val = 0
    total_samples = len(y)
    for count in counts:
        p = count / total_samples
        entropy_val -= p * np.log2(p)
    return entropy_val

def information_gain(X, y, feature, threshold):
    left_indices = X[:, feature] < threshold
    right_indices = ~left_indices
    num_left, num_right = np.sum(left_indices), np.sum(right_indices)
    total_samples = len(y)
    if num_left == 0 or num_right == 0:
        return 0
    left_entropy = entropy(y[left_indices])
    right_entropy = entropy(y[right_indices])
    ig = entropy(y) - (num_left / total_samples * left_entropy) - (num_right / total_samples * right_entropy)
    return ig

def find_best_split(X, y):
    best_feature, best_threshold, max_ig = None, None, -1
    for feature in range(X.shape[1]):
        thresholds = np.unique(X[:, feature])
        for threshold in thresholds:
            ig = information_gain(X, y, feature, threshold)
            if ig > max_ig:
                max_ig = ig
                best_feature = feature
                best_threshold = threshold
    return best_feature, best_threshold

def split(X, y, feature, threshold):
    left_indices = X[:, feature] < threshold
    right_indices = ~left_indices
    return X[left_indices], y[left_indices], X[right_indices], y[right_indices]

def majority_class(y):
    classes, counts = np.unique(y, return_counts=True)
    return classes[np.argmax(counts)]

def id3(X, y):
    if len(np.unique(y)) == 1:
        return Node(value=y[0])
    if X.shape[0] == 0:
        return Node(value=majority_class(y))
    best_feature, best_threshold = find_best_split(X, y)
    if best_feature is None:
        return Node(value=majority_class(y))
    X_left, y_left, X_right, y_right = split(X, y, best_feature, best_threshold)
    left_node = id3(X_left, y_left)
    right_node = id3(X_right, y_right)
    return Node(feature=best_feature, threshold=best_threshold, left=left_node, right=right_node)

def predict_one(node, sample):
    if node.value is not None:
        return node.value
    if sample[node.feature] < node.threshold:
        return predict_one(node.left, sample)
    else:
        return predict_one(node.right, sample)

def predict(root, X):
    return [predict_one(root, sample) for sample in X]

def accuracy(y_true, y_pred):
    return np.sum(y_true == y_pred) / len(y_true)

def bootstrap(data, target, n):
    data = data.to_numpy()
    target = target.to_numpy()
    accuracies = []
    for j in range(n):
        trainingData, y_train = resample(data, target, n_samples=200)
        testData, y_test = resample(data, target, n_samples=67)
        
        decisionTree = id3(trainingData, y_train)
        
        y_pred = predict(decisionTree, testData)
        
        acc = accuracy(y_test, y_pred)
        accuracies.append(acc)
        
        print("\nPredictive accuracy for Bootstrap = ", j + 1, " is ", acc)
        print(confusion_matrix(y_test, y_pred))
        a, b, c, d = precision_recall_fscore_support(y_test, y_pred, average='macro')
        print("Precision = ", a, "\nRecall = ", b, "\nF1-score = ", c)
    
    # Vẽ biểu đồ cho độ chính xác của n lần thử nghiệm
    plt.plot(range(1, n+1), accuracies, marker='o')
    plt.title('Accuracy for each Bootstrap')
    plt.xlabel('Bootstrap iteration')
    plt.ylabel('Accuracy')
    plt.xticks(range(1, n+1))
    plt.grid(True)
    plt.show()

if __name__ == '__main__':
    # Đọc dataset
    data = pd.read_csv("dt_data.csv")

    # Giả sử cột cuối cùng là nhãn và các cột còn lại là đặc trưng
    target = data.iloc[:, -1]
    features = data.iloc[:, :-1]

    # Thực hiện phương pháp bootstrap và vẽ biểu đồ
    bootstrap(features, target, n=10)
