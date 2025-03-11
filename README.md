
---

## 📊 Datasets Used

- **MNIST**: 70,000 grayscale images of handwritten digits (0-9), each of size **28×28 pixels**.
- **CIFAR-10**: 60,000 color images in 10 classes, with each image of size **32×32×3 pixels**.

---

## 🛠 Technologies & Libraries

- **Programming Language**: Python
- **Libraries**: TensorFlow, Keras, Scikit-learn, NumPy, Pandas, Matplotlib, Seaborn
- **Machine Learning Models**: SVM (Linear, RBF, Polynomial Kernels), KNN, NCC
- **Dimensionality Reduction**: PCA, Kernel PCA (Linear, Polynomial, RBF Kernels), LDA

---

## 🔥 Implementation Overview

### **1️⃣ SVM Classification (MNIST & CIFAR-10)**
- **Data Preprocessing**
  - Normalization to scale pixel values to **[0,1]**
  - Conversion of images to **1D feature vectors** for SVM compatibility
- **Feature Extraction**
  - **PCA**: Reduces dimensionality while preserving 95% variance
  - **Kernel PCA**: Non-linear transformation for improved feature separation
  - **LDA**: Maximizes class separability
- **Model Training**
  - Explored different SVM Kernels: **Linear, RBF, Polynomial**
  - **Best Kernel:** RBF (highest accuracy)
  - **Hyperparameter Tuning:** Used **Grid Search & Cross Validation**

### **2️⃣ KNN Classification**
- Used PCA/KPCA for dimensionality reduction
- **Best number of neighbors**: 4 (MNIST) / 31 (CIFAR-10)
- Performed **Grid Search CV** to optimize `n_neighbors`, `weights`, and `metric`

### **3️⃣ NCC (Nearest Centroid Classifier)**
- Implemented with **Euclidean & Manhattan distances**
- Performed **5-fold and 10-fold Cross Validation**
- Accuracy was lower than SVM & KNN, but served as a baseline

---

## 📈 Results & Performance

| Dataset  | Model     | Best Accuracy (Test Set) |
|----------|----------|------------------------|
| MNIST    | SVM (RBF Kernel) | **0.951** |
| MNIST    | KNN (PCA + LDA) | **0.946** |
| MNIST    | NCC (PCA + LDA) | **0.949** |
| CIFAR-10 | SVM (RBF Kernel) | **0.4615** |
| CIFAR-10 | KNN (RBF KPCA + LDA) | **0.4445** |
| CIFAR-10 | NCC (RBF KPCA + LDA) | **0.4325** |

📌 *Observations*:
- SVM outperformed KNN and NCC in both datasets.
- Kernel PCA + LDA improved class separability in CIFAR-10.
- Higher-dimensional datasets (CIFAR-10) required **stronger feature extraction techniques**.

---

## 🔧 How to Run

1. **Clone the repository**  
   ```bash
   git clone https://github.com/yourusername/Computational-Intelligence.git
   cd Computational-Intelligence
