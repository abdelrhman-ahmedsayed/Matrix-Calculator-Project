# ⊞ Matrix Calculator

A premium native desktop matrix calculator built with **Python**, **PyQt5**, and **NumPy**.  
Features a modern dark theme with a custom frameless window, 12 matrix operations, and an intuitive grid-based interface.

---

## ✨ Features

### Matrix Operations

| Operation | Type | Description |
|-----------|------|-------------|
| **Addition** | Binary | A + B |
| **Subtraction** | Binary | A − B |
| **Multiplication** | Binary | A × B |
| **Scalar Multiply** | Unary | k × A |
| **Transpose** | Unary | Aᵀ |
| **Determinant** | Unary | det(A) |
| **Inverse** | Unary | A⁻¹ |
| **Rank** | Unary | rank(A) |
| **Trace** | Unary | tr(A) |
| **Eigenvalues** | Unary | λ₁, λ₂, … |
| **RREF** | Unary | Row Reduced Echelon Form |
| **Power** | Unary | Aⁿ |

### User Interface

- 🎨 **Dark Theme** — Premium charcoal/navy palette with cyan and purple accents
- 🪟 **Custom Title Bar** — Frameless window with draggable title bar and window controls
- 📐 **Dual Matrix Input** — Side-by-side Matrix A and Matrix B panels
- 🔢 **Configurable Dimensions** — Resize matrices from 1×1 up to 10×10
- ⚡ **Quick Actions** — One-click Clear and Identity matrix buttons
- 📋 **Copy Results** — Copy result back into Matrix A or B for chained calculations
- 📜 **History Sidebar** — Tracks all past operations
- ⚠️ **Smart Errors** — Descriptive messages for dimension mismatches, singular matrices, etc.

---

## 🚀 Getting Started

### Prerequisites

- **Python 3.8+** installed on your system
- **pip** (Python package manager)

### Installation

1. **Clone or download** this project:

   ```bash
   git clone <repository-url>
   cd Matrix_calculator
   ```

2. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

### Running the App

```bash
python main.py
```

The calculator window will open — start entering matrix values and performing operations!

---

## 📁 Project Structure

```
Matrix_calculator/
├── main.py              # Entry point — launches the application
├── calculator.py        # Matrix computation engine (NumPy)
├── ui_main_window.py    # Main window layout and all widgets
├── ui_matrix_widget.py  # Reusable matrix input/display component
├── ui_styles.py         # QSS dark theme stylesheet
├── requirements.txt     # Python dependencies
└── README.md            # This file
```

---

## 🛠️ Tech Stack

| Component | Technology |
|-----------|------------|
| **Language** | Python 3 |
| **GUI Framework** | PyQt5 |
| **Math Engine** | NumPy |
| **Styling** | QSS (Qt Style Sheets) |

---

## 📖 Usage Guide

### Entering Matrices

1. Set the matrix dimensions using the **Rows** and **Cols** spin boxes
2. Click on any cell in the grid and type a numeric value
3. Press **Tab** to move to the next cell
4. Use the **Clear** button to reset all cells to 0
5. Use the **I** button to fill with an identity matrix

### Performing Operations

- **Binary operations** (A + B, A − B, A × B) use both Matrix A and Matrix B
- **Unary operations** (transpose, inverse, etc.) are applied to **Matrix A** only
- For **Aⁿ** and **k × A**, a dialog will prompt you for the exponent or scalar value

### Working with Results

- Results appear in the **Result** panel at the bottom
- Click **Copy to A** or **Copy to B** to use the result as input for the next operation
- All operations are logged in the **History** sidebar on the right

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).
