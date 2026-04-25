"""
Reusable Matrix Input/Display Widget
A QTableWidget-based component for entering and displaying matrices.
"""

import numpy as np
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QSpinBox, QTableWidget, QTableWidgetItem, QPushButton,
    QSizePolicy, QHeaderView
)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont


class MatrixWidget(QWidget):
    """A reusable widget for matrix input and display."""

    matrixChanged = pyqtSignal()

    def __init__(self, title="Matrix", rows=3, cols=3, editable=True, parent=None):
        super().__init__(parent)
        self._title = title
        self._editable = editable
        self._init_ui(rows, cols)

    def _init_ui(self, rows, cols):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(10)

        # ─── Header row ─────────────────────────────────────
        header_layout = QHBoxLayout()
        header_layout.setSpacing(8)

        title_label = QLabel(self._title)
        title_label.setObjectName("panelHeader")
        header_layout.addWidget(title_label)

        header_layout.addStretch()

        if self._editable:
            # Row controls
            row_label = QLabel("Rows")
            row_label.setObjectName("dimLabel")
            header_layout.addWidget(row_label)

            self.row_spin = QSpinBox()
            self.row_spin.setRange(1, 10)
            self.row_spin.setValue(rows)
            self.row_spin.setToolTip("Number of rows (1–10)")
            self.row_spin.valueChanged.connect(self._resize_matrix)
            header_layout.addWidget(self.row_spin)

            col_label = QLabel("Cols")
            col_label.setObjectName("dimLabel")
            header_layout.addWidget(col_label)

            self.col_spin = QSpinBox()
            self.col_spin.setRange(1, 10)
            self.col_spin.setValue(cols)
            self.col_spin.setToolTip("Number of columns (1–10)")
            self.col_spin.valueChanged.connect(self._resize_matrix)
            header_layout.addWidget(self.col_spin)

            # Clear button
            clear_btn = QPushButton("Clear")
            clear_btn.setObjectName("dangerButton")
            clear_btn.setFixedWidth(60)
            clear_btn.setCursor(Qt.PointingHandCursor)
            clear_btn.clicked.connect(self.clear)
            clear_btn.setToolTip("Clear all cells to 0")
            header_layout.addWidget(clear_btn)

            # Identity button
            identity_btn = QPushButton("I")
            identity_btn.setObjectName("secondaryButton")
            identity_btn.setFixedWidth(36)
            identity_btn.setCursor(Qt.PointingHandCursor)
            identity_btn.clicked.connect(self.set_identity)
            identity_btn.setToolTip("Fill with identity matrix")
            header_layout.addWidget(identity_btn)

        layout.addLayout(header_layout)

        # ─── Table ───────────────────────────────────────────
        self.table = QTableWidget(rows, cols)
        self.table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.table.setMinimumHeight(120)

        # Configure headers
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.horizontalHeader().setMinimumSectionSize(50)
        self.table.verticalHeader().setMinimumSectionSize(30)

        # Set monospace font for cells
        mono_font = QFont("Cascadia Mono", 12)
        mono_font.setStyleHint(QFont.Monospace)
        self.table.setFont(mono_font)

        # Initialize cells
        self._populate_cells(rows, cols)

        # Update header labels
        self._update_headers()

        if not self._editable:
            self.table.setEditTriggers(QTableWidget.NoEditTriggers)

        self.table.itemChanged.connect(lambda: self.matrixChanged.emit())

        layout.addWidget(self.table)

    def _populate_cells(self, rows, cols):
        """Fill all cells with default value 0."""
        self.table.blockSignals(True)
        for r in range(rows):
            for c in range(cols):
                item = QTableWidgetItem("0")
                item.setTextAlignment(Qt.AlignCenter)
                if not self._editable:
                    item.setFlags(item.flags() & ~Qt.ItemIsEditable)
                self.table.setItem(r, c, item)
        self.table.blockSignals(False)

    def _update_headers(self):
        """Set column and row headers to 1-indexed numbers."""
        for c in range(self.table.columnCount()):
            self.table.setHorizontalHeaderItem(c, QTableWidgetItem(str(c + 1)))
        for r in range(self.table.rowCount()):
            self.table.setVerticalHeaderItem(r, QTableWidgetItem(str(r + 1)))

    def _resize_matrix(self):
        """Handle dimension change from spin boxes."""
        rows = self.row_spin.value()
        cols = self.col_spin.value()

        old_rows = self.table.rowCount()
        old_cols = self.table.columnCount()

        # Save existing data
        old_data = {}
        for r in range(old_rows):
            for c in range(old_cols):
                item = self.table.item(r, c)
                if item:
                    old_data[(r, c)] = item.text()

        self.table.setRowCount(rows)
        self.table.setColumnCount(cols)

        # Restore data and fill new cells
        self.table.blockSignals(True)
        for r in range(rows):
            for c in range(cols):
                if (r, c) in old_data:
                    item = QTableWidgetItem(old_data[(r, c)])
                else:
                    item = QTableWidgetItem("0")
                item.setTextAlignment(Qt.AlignCenter)
                self.table.setItem(r, c, item)
        self.table.blockSignals(False)

        self._update_headers()
        self.matrixChanged.emit()

    def get_matrix(self):
        """Read the table contents and return a NumPy array."""
        rows = self.table.rowCount()
        cols = self.table.columnCount()
        data = np.zeros((rows, cols))

        for r in range(rows):
            for c in range(cols):
                item = self.table.item(r, c)
                text = item.text().strip() if item else "0"
                try:
                    data[r, c] = float(text) if text else 0.0
                except ValueError:
                    raise ValueError(
                        f"Invalid value '{text}' at row {r + 1}, col {c + 1}. "
                        f"Please enter a numeric value."
                    )
        return data

    def set_matrix(self, matrix):
        """Display a NumPy array in the table."""
        if isinstance(matrix, np.ndarray):
            rows, cols = matrix.shape
        else:
            rows, cols = 1, 1

        self.table.setRowCount(rows)
        self.table.setColumnCount(cols)

        if hasattr(self, 'row_spin'):
            self.row_spin.blockSignals(True)
            self.col_spin.blockSignals(True)
            self.row_spin.setValue(rows)
            self.col_spin.setValue(cols)
            self.row_spin.blockSignals(False)
            self.col_spin.blockSignals(False)

        self.table.blockSignals(True)
        for r in range(rows):
            for c in range(cols):
                val = matrix[r, c]
                # Format nicely: integers as integers, floats with precision
                if np.isclose(val, round(val)) and abs(val) < 1e10:
                    text = str(int(round(val)))
                else:
                    text = f"{val:.6g}"
                item = QTableWidgetItem(text)
                item.setTextAlignment(Qt.AlignCenter)
                if not self._editable:
                    item.setFlags(item.flags() & ~Qt.ItemIsEditable)
                self.table.setItem(r, c, item)
        self.table.blockSignals(False)

        self._update_headers()

    def clear(self):
        """Clear all cells to 0."""
        self.table.blockSignals(True)
        for r in range(self.table.rowCount()):
            for c in range(self.table.columnCount()):
                item = self.table.item(r, c)
                if item:
                    item.setText("0")
        self.table.blockSignals(False)
        self.matrixChanged.emit()

    def set_identity(self):
        """Fill with identity matrix (square part)."""
        rows = self.table.rowCount()
        cols = self.table.columnCount()
        n = min(rows, cols)

        self.table.blockSignals(True)
        for r in range(rows):
            for c in range(cols):
                val = "1" if (r == c and r < n) else "0"
                item = self.table.item(r, c)
                if item:
                    item.setText(val)
        self.table.blockSignals(False)
        self.matrixChanged.emit()

    def set_scalar_result(self, value):
        """Display a scalar result in a 1x1 table."""
        self.table.setRowCount(1)
        self.table.setColumnCount(1)

        if hasattr(self, 'row_spin'):
            self.row_spin.blockSignals(True)
            self.col_spin.blockSignals(True)
            self.row_spin.setValue(1)
            self.col_spin.setValue(1)
            self.row_spin.blockSignals(False)
            self.col_spin.blockSignals(False)

        self.table.blockSignals(True)
        if isinstance(value, (complex, np.complexfloating)):
            text = f"{value:.6g}"
        elif isinstance(value, (int, np.integer)):
            text = str(int(value))
        elif isinstance(value, (float, np.floating)):
            if np.isclose(value, round(value)) and abs(value) < 1e10:
                text = str(int(round(value)))
            else:
                text = f"{value:.6g}"
        else:
            text = str(value)

        item = QTableWidgetItem(text)
        item.setTextAlignment(Qt.AlignCenter)
        if not self._editable:
            item.setFlags(item.flags() & ~Qt.ItemIsEditable)
        self.table.setItem(0, 0, item)
        self.table.blockSignals(False)
        self._update_headers()

    def set_vector_result(self, values):
        """Display a vector of values (e.g., eigenvalues) as a column."""
        n = len(values)
        self.table.setRowCount(n)
        self.table.setColumnCount(1)

        if hasattr(self, 'row_spin'):
            self.row_spin.blockSignals(True)
            self.col_spin.blockSignals(True)
            self.row_spin.setValue(n)
            self.col_spin.setValue(1)
            self.row_spin.blockSignals(False)
            self.col_spin.blockSignals(False)

        self.table.blockSignals(True)
        for i, val in enumerate(values):
            if isinstance(val, (complex, np.complexfloating)):
                if np.isclose(val.imag, 0):
                    real = val.real
                    if np.isclose(real, round(real)):
                        text = str(int(round(real)))
                    else:
                        text = f"{real:.6g}"
                else:
                    text = f"{val:.6g}"
            elif isinstance(val, (float, np.floating)):
                if np.isclose(val, round(val)):
                    text = str(int(round(val)))
                else:
                    text = f"{val:.6g}"
            else:
                text = str(val)

            item = QTableWidgetItem(text)
            item.setTextAlignment(Qt.AlignCenter)
            if not self._editable:
                item.setFlags(item.flags() & ~Qt.ItemIsEditable)
            self.table.setItem(i, 0, item)
        self.table.blockSignals(False)

        # Header
        self.table.setHorizontalHeaderItem(0, QTableWidgetItem("λ"))
        for r in range(n):
            self.table.setVerticalHeaderItem(r, QTableWidgetItem(f"λ{r + 1}"))
