"""
Main Window for the Matrix Calculator
Assembles all UI components into the main application window.
"""

import numpy as np
from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QSizePolicy, QFrame, QListWidget, QListWidgetItem,
    QInputDialog, QMessageBox, QStatusBar, QSplitter, QApplication,
    QGraphicsDropShadowEffect
)
from PyQt5.QtCore import Qt, QPoint, QSize, QPropertyAnimation, QEasingCurve
from PyQt5.QtGui import QFont, QColor, QIcon

from ui_matrix_widget import MatrixWidget
from ui_styles import MAIN_STYLESHEET, ACCENT, ERROR, SUCCESS, TEXT_SECONDARY
import calculator as calc


class TitleBar(QWidget):
    """Custom frameless title bar with window controls."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("titleBar")
        self.setFixedHeight(38)
        self._parent = parent
        self._drag_pos = None

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # App icon/title
        icon_label = QLabel("  ⊞")
        icon_label.setObjectName("titleIcon")
        icon_label.setFixedWidth(36)
        icon_label.setAlignment(Qt.AlignCenter)
        font = QFont("Segoe UI", 14)
        icon_label.setFont(font)
        icon_label.setStyleSheet(f"color: {ACCENT};")
        layout.addWidget(icon_label)

        title = QLabel("Matrix Calculator")
        title.setObjectName("titleLabel")
        layout.addWidget(title)

        layout.addStretch()

        # Window controls
        btn_min = QPushButton("─")
        btn_min.setObjectName("btnMinimize")
        btn_min.setCursor(Qt.PointingHandCursor)
        btn_min.clicked.connect(self._minimize)
        layout.addWidget(btn_min)

        self._btn_max = QPushButton("□")
        self._btn_max.setObjectName("btnMaximize")
        self._btn_max.setCursor(Qt.PointingHandCursor)
        self._btn_max.clicked.connect(self._toggle_maximize)
        layout.addWidget(self._btn_max)

        btn_close = QPushButton("✕")
        btn_close.setObjectName("btnClose")
        btn_close.setCursor(Qt.PointingHandCursor)
        btn_close.clicked.connect(self._close)
        layout.addWidget(btn_close)

    def _minimize(self):
        self._parent.showMinimized()

    def _toggle_maximize(self):
        if self._parent.isMaximized():
            self._parent.showNormal()
            self._btn_max.setText("□")
        else:
            self._parent.showMaximized()
            self._btn_max.setText("❐")

    def _close(self):
        self._parent.close()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self._drag_pos = event.globalPos() - self._parent.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if self._drag_pos and event.buttons() == Qt.LeftButton:
            # If maximized, restore before dragging
            if self._parent.isMaximized():
                self._parent.showNormal()
                self._btn_max.setText("□")
                # Re-center the drag position
                self._drag_pos = QPoint(self._parent.width() // 2, 19)
            self._parent.move(event.globalPos() - self._drag_pos)
            event.accept()

    def mouseReleaseEvent(self, event):
        self._drag_pos = None

    def mouseDoubleClickEvent(self, event):
        self._toggle_maximize()


class MainWindow(QMainWindow):
    """Main application window for the Matrix Calculator."""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Matrix Calculator")
        self.setMinimumSize(1100, 750)
        self.resize(1300, 850)

        # Frameless window for custom title bar
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground, False)

        self._history = []
        self._init_ui()

    def _init_ui(self):
        """Build the complete UI layout."""
        central = QWidget()
        self.setCentralWidget(central)

        root_layout = QVBoxLayout(central)
        root_layout.setContentsMargins(0, 0, 0, 0)
        root_layout.setSpacing(0)

        # ─── Title Bar ──────────────────────────────────────
        self.title_bar = TitleBar(self)
        root_layout.addWidget(self.title_bar)

        # ─── Main Content ───────────────────────────────────
        content = QWidget()
        content_layout = QHBoxLayout(content)
        content_layout.setContentsMargins(16, 16, 16, 16)
        content_layout.setSpacing(16)

        # Left side: matrices + operations + result
        left_widget = QWidget()
        left_layout = QVBoxLayout(left_widget)
        left_layout.setContentsMargins(0, 0, 0, 0)
        left_layout.setSpacing(14)

        # ── Matrix inputs row ────────────────────────────────
        matrix_row = QHBoxLayout()
        matrix_row.setSpacing(16)

        # Matrix A
        matrix_a_frame = QFrame()
        matrix_a_frame.setObjectName("matrixPanel")
        matrix_a_layout = QVBoxLayout(matrix_a_frame)
        matrix_a_layout.setContentsMargins(16, 16, 16, 16)
        self.matrix_a = MatrixWidget("Matrix A", 3, 3, editable=True)
        matrix_a_layout.addWidget(self.matrix_a)
        matrix_row.addWidget(matrix_a_frame, stretch=1)

        # Matrix B
        matrix_b_frame = QFrame()
        matrix_b_frame.setObjectName("matrixPanel")
        matrix_b_layout = QVBoxLayout(matrix_b_frame)
        matrix_b_layout.setContentsMargins(16, 16, 16, 16)
        self.matrix_b = MatrixWidget("Matrix B", 3, 3, editable=True)
        matrix_b_layout.addWidget(self.matrix_b)
        matrix_row.addWidget(matrix_b_frame, stretch=1)

        left_layout.addLayout(matrix_row, stretch=3)

        # ── Operations panel ─────────────────────────────────
        ops_frame = QFrame()
        ops_frame.setObjectName("operationPanel")
        ops_layout = QVBoxLayout(ops_frame)
        ops_layout.setContentsMargins(16, 12, 16, 12)
        ops_layout.setSpacing(10)

        # Binary operations row
        binary_label = QLabel("BINARY OPERATIONS")
        binary_label.setObjectName("groupLabel")
        ops_layout.addWidget(binary_label)

        binary_row = QHBoxLayout()
        binary_row.setSpacing(8)
        self._add_op_button(binary_row, "A + B", "Add matrices A and B", self._op_add, "accentButton")
        self._add_op_button(binary_row, "A − B", "Subtract B from A", self._op_subtract, "accentButton")
        self._add_op_button(binary_row, "A × B", "Multiply A by B", self._op_multiply, "accentButton")
        ops_layout.addLayout(binary_row)

        # Unary operations row
        unary_label = QLabel("UNARY OPERATIONS  (applied to Matrix A)")
        unary_label.setObjectName("groupLabel")
        ops_layout.addWidget(unary_label)

        unary_row1 = QHBoxLayout()
        unary_row1.setSpacing(8)
        self._add_op_button(unary_row1, "Aᵀ", "Transpose of A", self._op_transpose, "secondaryButton")
        self._add_op_button(unary_row1, "A⁻¹", "Inverse of A", self._op_inverse, "secondaryButton")
        self._add_op_button(unary_row1, "det(A)", "Determinant of A", self._op_determinant, "secondaryButton")
        self._add_op_button(unary_row1, "rank(A)", "Rank of A", self._op_rank, "secondaryButton")
        self._add_op_button(unary_row1, "tr(A)", "Trace of A", self._op_trace, "secondaryButton")
        ops_layout.addLayout(unary_row1)

        unary_row2 = QHBoxLayout()
        unary_row2.setSpacing(8)
        self._add_op_button(unary_row2, "Eigenvals", "Eigenvalues of A", self._op_eigenvalues, "secondaryButton")
        self._add_op_button(unary_row2, "RREF", "Row Reduced Echelon Form of A", self._op_rref, "secondaryButton")
        self._add_op_button(unary_row2, "Aⁿ", "Raise A to power n", self._op_power, "secondaryButton")
        self._add_op_button(unary_row2, "k × A", "Scalar multiply A", self._op_scalar_multiply, "secondaryButton")
        unary_row2.addStretch()
        ops_layout.addLayout(unary_row2)

        left_layout.addWidget(ops_frame)

        # ── Result panel ─────────────────────────────────────
        result_frame = QFrame()
        result_frame.setObjectName("resultPanel")
        result_layout = QVBoxLayout(result_frame)
        result_layout.setContentsMargins(16, 16, 16, 16)

        result_header = QHBoxLayout()
        result_title = QLabel("Result")
        result_title.setObjectName("panelHeader")
        result_header.addWidget(result_title)

        self.result_info = QLabel("")
        self.result_info.setObjectName("dimLabel")
        result_header.addWidget(self.result_info)

        result_header.addStretch()

        copy_btn = QPushButton("Copy to A")
        copy_btn.setToolTip("Copy the result into Matrix A")
        copy_btn.setCursor(Qt.PointingHandCursor)
        copy_btn.clicked.connect(self._copy_result_to_a)
        result_header.addWidget(copy_btn)

        copy_b_btn = QPushButton("Copy to B")
        copy_b_btn.setToolTip("Copy the result into Matrix B")
        copy_b_btn.setCursor(Qt.PointingHandCursor)
        copy_b_btn.clicked.connect(self._copy_result_to_b)
        result_header.addWidget(copy_b_btn)

        result_layout.addLayout(result_header)

        self.result_widget = MatrixWidget("", 3, 3, editable=False)
        result_layout.addWidget(self.result_widget)

        # Status label for errors/success
        self.status_label = QLabel("")
        self.status_label.setWordWrap(True)
        self.status_label.setMaximumHeight(40)
        result_layout.addWidget(self.status_label)

        left_layout.addWidget(result_frame, stretch=2)

        content_layout.addWidget(left_widget, stretch=4)

        # ─── Right side: History ─────────────────────────────
        history_frame = QFrame()
        history_frame.setObjectName("historyPanel")
        history_frame.setFixedWidth(240)
        history_layout = QVBoxLayout(history_frame)
        history_layout.setContentsMargins(12, 12, 12, 12)
        history_layout.setSpacing(8)

        hist_title = QLabel("History")
        hist_title.setObjectName("panelHeader")
        history_layout.addWidget(hist_title)

        self.history_list = QListWidget()
        self.history_list.setToolTip("Click to recall a past operation")
        history_layout.addWidget(self.history_list)

        clear_hist_btn = QPushButton("Clear History")
        clear_hist_btn.setObjectName("dangerButton")
        clear_hist_btn.setCursor(Qt.PointingHandCursor)
        clear_hist_btn.clicked.connect(self._clear_history)
        history_layout.addWidget(clear_hist_btn)

        content_layout.addWidget(history_frame)

        root_layout.addWidget(content, stretch=1)

        # ─── Status Bar ─────────────────────────────────────
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Ready — Enter matrix values and choose an operation")

    def _add_op_button(self, layout, text, tooltip, callback, style_id=None):
        """Helper to create an operation button."""
        btn = QPushButton(text)
        btn.setToolTip(tooltip)
        btn.setCursor(Qt.PointingHandCursor)
        if style_id:
            btn.setObjectName(style_id)
        btn.clicked.connect(callback)
        btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        layout.addWidget(btn)
        return btn

    def _show_result_matrix(self, result, operation_name):
        """Display a matrix result."""
        self.result_widget.set_matrix(result)
        self.result_info.setText(f"{result.shape[0]}×{result.shape[1]}")
        self._set_status(f"✓ {operation_name} — Result: {result.shape[0]}×{result.shape[1]} matrix", "success")
        self._add_history(operation_name)
        self._last_result = result
        self._last_result_type = "matrix"

    def _show_result_scalar(self, value, operation_name):
        """Display a scalar result."""
        self.result_widget.set_scalar_result(value)
        self.result_info.setText("scalar")

        if isinstance(value, (complex, np.complexfloating)):
            disp = f"{value:.6g}"
        elif isinstance(value, (float, np.floating)):
            if np.isclose(value, round(value)):
                disp = str(int(round(value)))
            else:
                disp = f"{value:.6g}"
        else:
            disp = str(value)

        self._set_status(f"✓ {operation_name} = {disp}", "success")
        self._add_history(f"{operation_name} = {disp}")
        self._last_result = None
        self._last_result_type = "scalar"

    def _show_result_vector(self, values, operation_name):
        """Display eigenvalues or similar vector result."""
        self.result_widget.set_vector_result(values)
        self.result_info.setText(f"{len(values)} values")
        self._set_status(f"✓ {operation_name} — {len(values)} eigenvalue(s)", "success")
        self._add_history(operation_name)
        self._last_result = None
        self._last_result_type = "vector"

    def _show_error(self, message):
        """Display an error message."""
        self._set_status(f"✗ {message}", "error")
        self.status_bar.showMessage(f"Error: {message}", 5000)

    def _set_status(self, text, kind="info"):
        """Set the status label with styling."""
        if kind == "success":
            self.status_label.setObjectName("successLabel")
        elif kind == "error":
            self.status_label.setObjectName("errorLabel")
        else:
            self.status_label.setObjectName("dimLabel")
        self.status_label.setText(text)
        # Force style refresh
        self.status_label.setStyleSheet(self.status_label.styleSheet())
        self.status_label.style().unpolish(self.status_label)
        self.status_label.style().polish(self.status_label)

    def _add_history(self, text):
        """Add an entry to the history list."""
        self._history.insert(0, text)
        if len(self._history) > 50:
            self._history.pop()
        self._refresh_history()
        self.status_bar.showMessage(f"Computed: {text}", 3000)

    def _refresh_history(self):
        """Rebuild the history list widget."""
        self.history_list.clear()
        for entry in self._history:
            item = QListWidgetItem(entry)
            self.history_list.addItem(item)

    def _clear_history(self):
        """Clear the history."""
        self._history.clear()
        self.history_list.clear()
        self.status_bar.showMessage("History cleared", 2000)

    def _copy_result_to_a(self):
        """Copy the result matrix into Matrix A."""
        if hasattr(self, '_last_result') and self._last_result is not None:
            self.matrix_a.set_matrix(self._last_result)
            self.status_bar.showMessage("Result copied to Matrix A", 2000)
        else:
            self.status_bar.showMessage("No matrix result to copy", 2000)

    def _copy_result_to_b(self):
        """Copy the result matrix into Matrix B."""
        if hasattr(self, '_last_result') and self._last_result is not None:
            self.matrix_b.set_matrix(self._last_result)
            self.status_bar.showMessage("Result copied to Matrix B", 2000)
        else:
            self.status_bar.showMessage("No matrix result to copy", 2000)

    # ─── Operation Callbacks ─────────────────────────────────

    def _op_add(self):
        try:
            a = self.matrix_a.get_matrix()
            b = self.matrix_b.get_matrix()
            result = calc.add(a, b)
            self._show_result_matrix(result, "A + B")
        except Exception as e:
            self._show_error(str(e))

    def _op_subtract(self):
        try:
            a = self.matrix_a.get_matrix()
            b = self.matrix_b.get_matrix()
            result = calc.subtract(a, b)
            self._show_result_matrix(result, "A − B")
        except Exception as e:
            self._show_error(str(e))

    def _op_multiply(self):
        try:
            a = self.matrix_a.get_matrix()
            b = self.matrix_b.get_matrix()
            result = calc.multiply(a, b)
            self._show_result_matrix(result, "A × B")
        except Exception as e:
            self._show_error(str(e))

    def _op_transpose(self):
        try:
            a = self.matrix_a.get_matrix()
            result = calc.transpose(a)
            self._show_result_matrix(result, "Aᵀ")
        except Exception as e:
            self._show_error(str(e))

    def _op_inverse(self):
        try:
            a = self.matrix_a.get_matrix()
            result = calc.inverse(a)
            self._show_result_matrix(result, "A⁻¹")
        except Exception as e:
            self._show_error(str(e))

    def _op_determinant(self):
        try:
            a = self.matrix_a.get_matrix()
            result = calc.determinant(a)
            self._show_result_scalar(result, "det(A)")
        except Exception as e:
            self._show_error(str(e))

    def _op_rank(self):
        try:
            a = self.matrix_a.get_matrix()
            result = calc.rank(a)
            self._show_result_scalar(result, "rank(A)")
        except Exception as e:
            self._show_error(str(e))

    def _op_trace(self):
        try:
            a = self.matrix_a.get_matrix()
            result = calc.trace(a)
            self._show_result_scalar(result, "tr(A)")
        except Exception as e:
            self._show_error(str(e))

    def _op_eigenvalues(self):
        try:
            a = self.matrix_a.get_matrix()
            result = calc.eigenvalues(a)
            self._show_result_vector(result, "Eigenvalues(A)")
        except Exception as e:
            self._show_error(str(e))

    def _op_rref(self):
        try:
            a = self.matrix_a.get_matrix()
            result = calc.rref(a)
            self._show_result_matrix(result, "RREF(A)")
        except Exception as e:
            self._show_error(str(e))

    def _op_power(self):
        try:
            n, ok = QInputDialog.getInt(
                self, "Matrix Power", "Enter the exponent (n):",
                value=2, min=0, max=100
            )
            if not ok:
                return
            a = self.matrix_a.get_matrix()
            result = calc.power(a, n)
            self._show_result_matrix(result, f"A^{n}")
        except Exception as e:
            self._show_error(str(e))

    def _op_scalar_multiply(self):
        try:
            k, ok = QInputDialog.getDouble(
                self, "Scalar Multiply", "Enter the scalar (k):",
                value=2.0, decimals=6
            )
            if not ok:
                return
            a = self.matrix_a.get_matrix()
            result = calc.scalar_multiply(a, k)
            self._show_result_matrix(result, f"{k} × A")
        except Exception as e:
            self._show_error(str(e))
