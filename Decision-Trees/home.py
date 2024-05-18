import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import make_classification
from sklearn.tree import DecisionTreeClassifier
from sklearn.decomposition import PCA

# Generate synthetic binary classification data with 9 features
X, y = make_classification(n_samples=100, n_features=9, n_classes=2, n_clusters_per_class=1, random_state=42)

# Reduce the dimensionality of the data to 2 using PCA
pca = PCA(n_components=2)
X_pca = pca.fit_transform(X)

# Train DecisionTreeClassifier on the PCA-reduced data
clf = DecisionTreeClassifier(criterion="gini", max_depth=3, min_samples_leaf=5)

clf.fit(X_pca, y)

# Plot scatter plot of the PCA-reduced data
plt.figure(figsize=(10, 6))
plt.scatter(X_pca[:, 0], X_pca[:, 1], c=y, cmap=plt.cm.RdBu, edgecolors='k', label='Data')

# Create a mesh grid to plot the decision boundary
x_min, x_max = X_pca[:, 0].min() - 1, X_pca[:, 0].max() + 1
y_min, y_max = X_pca[:, 1].min() - 1, X_pca[:, 1].max() + 1
xx, yy = np.meshgrid(np.arange(x_min, x_max, 0.02), np.arange(y_min, y_max, 0.02))

# Predict class labels for each point in the mesh grid
Z = clf.predict(np.c_[xx.ravel(), yy.ravel()])
Z = Z.reshape(xx.shape)

# Plot decision boundary
plt.contourf(xx, yy, Z, alpha=0.3, cmap=plt.cm.RdBu)

plt.xlabel('Principal Component 1')
plt.ylabel('Principal Component 2')
plt.title('Decision Boundary Visualization (PCA)')
plt.legend()
plt.show()
