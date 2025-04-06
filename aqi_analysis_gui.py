from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QTabWidget, QTreeWidget, QTreeWidgetItem, QFrame,
                             QGroupBox)
from PyQt5.QtCore import Qt
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from scipy.interpolate import lagrange, CubicSpline

class AQIAnalysisGUI(QWidget):
    """GUI application for Air Quality Index analysis visualization."""
    
    def __init__(self):
        """Initialize the GUI application."""
        super().__init__()
        
        # Data for AQI analysis
        self.days_subset = np.array([2, 3, 4])
        self.aqi_subset = np.array([80, 78, 82])
        
        self.days_full = np.array([1, 2, 3, 4, 5])
        self.aqi_full = np.array([75, 80, 78, 82, 77])
        
        # Interpolation target
        self.x_new = 2.5
        
        self.setup_gui()
        self.analyze_and_display()
        
    def setup_gui(self):
        """Set up the GUI components and styling."""
        # Main layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(10, 10, 10, 10)
        
        # Create a tabbed widget
        self.tabs = QTabWidget()
        main_layout.addWidget(self.tabs)
        
        # Create tab widgets
        self.results_widget = QWidget()
        self.plots_widget = QWidget()
        self.data_widget = QWidget()
        
        # Add tabs
        self.tabs.addTab(self.results_widget, "Results")
        self.tabs.addTab(self.plots_widget, "Visualizations")
        self.tabs.addTab(self.data_widget, "Data")
        
        # Set up layouts for each tab
        self.results_layout = QVBoxLayout(self.results_widget)
        self.plots_layout = QVBoxLayout(self.plots_widget)
        self.data_layout = QVBoxLayout(self.data_widget)

    def lagrange_interpolation(self, x, y, x_new):
        """Perform Lagrange interpolation."""
        poly = lagrange(x, y)
        return poly(x_new)

    def newton_divided_diff(self, x, y):
        """Calculate the divided difference coefficients."""
        n = len(x)
        coef = np.copy(y).astype(float)
        for j in range(1, n):
            coef[j:n] = (coef[j:n] - coef[j - 1:n - 1]) / (x[j:n] - x[0:n - j])
        return coef

    def newton_interpolation(self, x, coef, x_new):
        """Perform Newton interpolation."""
        n = len(coef)
        result = coef[0]
        product = 1.0
        for i in range(1, n):
            product *= (x_new - x[i - 1])
            result += coef[i] * product
        return result

    def neville_interpolation(self, x, y, x_new):
        """Perform Neville interpolation."""
        n = len(x)
        Q = np.zeros((n, n))
        Q[:, 0] = y
        for j in range(1, n):
            for i in range(n - j):
                Q[i][j] = ((x_new - x[i + j]) * Q[i][j - 1] -
                          (x_new - x[i]) * Q[i + 1][j - 1]) / (x[i] - x[i + j])
        return Q[0, n - 1]

    def least_squares_fit(self, x, y, degree=2):
        """Fit a polynomial using least squares."""
        coeffs = np.polyfit(x, y, degree)
        poly = np.poly1d(coeffs)
        return poly
        
    def analyze_and_display(self):
        """Perform AQI analysis and display results."""
        # Calculate results for subset data (3 points)
        lagrange_subset = self.lagrange_interpolation(self.days_subset, self.aqi_subset, self.x_new)
        
        coef_subset = self.newton_divided_diff(self.days_subset, self.aqi_subset)
        newton_subset = self.newton_interpolation(self.days_subset, coef_subset, self.x_new)
        
        neville_subset = self.neville_interpolation(self.days_subset, self.aqi_subset, self.x_new)
        
        # Calculate results for full dataset (5 points)
        lagrange_full = self.lagrange_interpolation(self.days_full, self.aqi_full, self.x_new)
        
        coef_full = self.newton_divided_diff(self.days_full, self.aqi_full)
        newton_full = self.newton_interpolation(self.days_full, coef_full, self.x_new)
        
        neville_full = self.neville_interpolation(self.days_full, self.aqi_full, self.x_new)
        
        # Display results in the results tab
        self.display_results(lagrange_subset, newton_subset, neville_subset, 
                             lagrange_full, newton_full, neville_full)
        
        # Create plots for visualization
        self.create_plots()
        
        # Display data used
        self.display_data()
        
    def display_results(self, lagrange_subset, newton_subset, neville_subset, 
                         lagrange_full, newton_full, neville_full):
        """Display interpolation results in table format."""
        # Add title
        title = QLabel("Interpolation Results")
        title.setStyleSheet("font-size: 18px; font-weight: bold;")
        title.setAlignment(Qt.AlignCenter)
        self.results_layout.addWidget(title)
        
        # Create tables container
        tables_widget = QWidget()
        tables_layout = QHBoxLayout(tables_widget)
        self.results_layout.addWidget(tables_widget)
        
        # Create the table for 3-point subset
        subset_group = QGroupBox("3-Point Dataset (Days 2, 3, 4)")
        subset_layout = QVBoxLayout(subset_group)
        tables_layout.addWidget(subset_group)
        
        subset_tree = QTreeWidget()
        subset_tree.setHeaderLabels(["Method", "AQI Value at Day 2.5"])
        subset_tree.setRootIsDecorated(False)
        subset_tree.setAlternatingRowColors(True)
        
        lagrange_item = QTreeWidgetItem(["Lagrange", f"{lagrange_subset:.2f}"])
        subset_tree.addTopLevelItem(lagrange_item)
        
        newton_item = QTreeWidgetItem(["Newton", f"{newton_subset:.2f}"])
        subset_tree.addTopLevelItem(newton_item)
        
        neville_item = QTreeWidgetItem(["Neville", f"{neville_subset:.2f}"])
        subset_tree.addTopLevelItem(neville_item)
        
        subset_layout.addWidget(subset_tree)
        
        # Create the table for full 5-point dataset
        full_group = QGroupBox("Full Dataset (Days 1-5)")
        full_layout = QVBoxLayout(full_group)
        tables_layout.addWidget(full_group)
        
        full_tree = QTreeWidget()
        full_tree.setHeaderLabels(["Method", "AQI Value at Day 2.5"])
        full_tree.setRootIsDecorated(False)
        full_tree.setAlternatingRowColors(True)
        
        lagrange_item = QTreeWidgetItem(["Lagrange", f"{lagrange_full:.2f}"])
        full_tree.addTopLevelItem(lagrange_item)
        
        newton_item = QTreeWidgetItem(["Newton", f"{newton_full:.2f}"])
        full_tree.addTopLevelItem(newton_item)
        
        neville_item = QTreeWidgetItem(["Neville", f"{neville_full:.2f}"])
        full_tree.addTopLevelItem(neville_item)
        
        full_layout.addWidget(full_tree)
        
        # Add explanation text
        explanation = (
            "Comparison of different interpolation methods to estimate the Air Quality Index at Day 2.5.\n"
            "All three methods should produce the same results when using the same dataset, as they are "
            "mathematically equivalent for polynomial interpolation."
        )
        
        explanation_label = QLabel(explanation)
        explanation_label.setWordWrap(True)
        explanation_label.setAlignment(Qt.AlignCenter)
        self.results_layout.addWidget(explanation_label)
    
    def create_plots(self):
        """Create and display visualization plots."""
        # Create a figure with 2 subplots
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 5))
        fig.set_tight_layout(True)
        
        # Cubic Spline for 3-point dataset
        cs_subset = CubicSpline(self.days_subset, self.aqi_subset)
        x_dense_subset = np.linspace(2, 4, 200)
        y_dense_subset = cs_subset(x_dense_subset)
        
        # Least Squares Fit for 3 points (Degree 2)
        ls_fit_subset_2 = self.least_squares_fit(self.days_subset, self.aqi_subset, degree=2)
        y_ls_subset_2 = ls_fit_subset_2(x_dense_subset)
        
        # Least Squares Fit for 3 points (Degree 3)
        ls_fit_subset_3 = self.least_squares_fit(self.days_subset, self.aqi_subset, degree=3)
        y_ls_subset_3 = ls_fit_subset_3(x_dense_subset)
        
        # Plot for 3-point dataset
        ax1.plot(self.days_subset, self.aqi_subset, 'o', label='Subset Data (3 pts)')
        ax1.plot(x_dense_subset, y_dense_subset, '-', label='Cubic Spline')
        ax1.plot(x_dense_subset, y_ls_subset_2, '--', label='Least Squares (Degree 2)', color='purple')
        ax1.plot(x_dense_subset, y_ls_subset_3, ':', label='Least Squares (Degree 3)', color='green')
        ax1.axvline(x=self.x_new, linestyle='--', color='gray', alpha=0.5)
        ax1.set_title('Cubic Spline and Least Squares Fits (3 Points)')
        ax1.set_xlabel('Day')
        ax1.set_ylabel('AQI')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # Cubic Spline for full dataset
        cs_full = CubicSpline(self.days_full, self.aqi_full)
        x_dense_full = np.linspace(1, 5, 200)
        y_dense_full = cs_full(x_dense_full)
        
        # Least Squares Fit for full dataset (Degree 2)
        ls_fit_full_2 = self.least_squares_fit(self.days_full, self.aqi_full, degree=2)
        y_ls_full_2 = ls_fit_full_2(x_dense_full)
        
        # Least Squares Fit for full dataset (Degree 3)
        ls_fit_full_3 = self.least_squares_fit(self.days_full, self.aqi_full, degree=3)
        y_ls_full_3 = ls_fit_full_3(x_dense_full)
        
        # Plot for full dataset
        ax2.plot(self.days_full, self.aqi_full, 'o', label='Full AQI Data')
        ax2.plot(x_dense_full, y_dense_full, '-', label='Cubic Spline')
        ax2.plot(x_dense_full, y_ls_full_2, '--', label='Least Squares (Degree 2)', color='purple')
        ax2.plot(x_dense_full, y_ls_full_3, ':', label='Least Squares (Degree 3)', color='green')
        ax2.axvline(x=self.x_new, linestyle='--', color='gray', alpha=0.5)
        ax2.set_title('Cubic Spline and Least Squares Fits (Full Data)')
        ax2.set_xlabel('Day')
        ax2.set_ylabel('AQI')
        ax2.legend()
        ax2.grid(True, alpha=0.3)
        
        # Create a canvas to display the figure in the GUI
        canvas = FigureCanvas(fig)
        self.plots_layout.addWidget(canvas)
        
        # Add explanation text below plots
        explanation = (
            "The plots show different methods for smoothing and analyzing the AQI data.\n"
            "The vertical dashed line at day 2.5 indicates the interpolation point used in the Results tab.\n"
            "The Cubic Spline provides a smooth curve through all data points, while the\n"
            "Least Squares Fit (Polynomial Regression) shows best-fit polynomials of degrees 2 and 3."
        )
        
        explanation_label = QLabel(explanation)
        explanation_label.setWordWrap(True)
        explanation_label.setAlignment(Qt.AlignCenter)
        self.plots_layout.addWidget(explanation_label)
    
    def display_data(self):
        """Display the raw data used in the analysis."""
        # Add title
        title = QLabel("Air Quality Index Data")
        title.setStyleSheet("font-size: 18px; font-weight: bold;")
        title.setAlignment(Qt.AlignCenter)
        self.data_layout.addWidget(title)
        
        # Data text
        data_text = (
            "This analysis uses the following Air Quality Index (AQI) values:\n\n"
            "Day 1: 75\n"
            "Day 2: 80\n"
            "Day 3: 78\n"
            "Day 4: 82\n"
            "Day 5: 77\n\n"
            "The 3-point dataset uses only days 2, 3, and 4.\n"
            "The full dataset uses all five days.\n\n"
            "We are estimating the AQI value at day 2.5 using various interpolation methods."
        )
        
        data_label = QLabel(data_text)
        data_label.setWordWrap(True)
        data_label.setAlignment(Qt.AlignCenter)
        self.data_layout.addWidget(data_label)
        
        # Add method explanations
        methods_group = QGroupBox("Interpolation and Smoothing Methods")
        self.data_layout.addWidget(methods_group)
        methods_layout = QVBoxLayout(methods_group)
        
        methods_text = (
            "1. Lagrange Interpolation: Creates a polynomial that passes through all given points.\n\n"
            "2. Newton Interpolation: Mathematically equivalent to Lagrange but uses a different formula "
            "that is computationally more efficient.\n\n"
            "3. Neville's Algorithm: Another form of polynomial interpolation with good numerical stability.\n\n"
            "4. Cubic Spline: Creates a piecewise cubic polynomial that is smooth at the knots (data points).\n\n"
            "5. Least Squares Fit: Finds a polynomial of specified degree that minimizes the sum of squared "
            "errors between the polynomial and the data points."
        )
        
        methods_label = QLabel(methods_text)
        methods_label.setWordWrap(True)
        methods_layout.addWidget(methods_label)

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    window = AQIAnalysisGUI()
    window.show()
    sys.exit(app.exec_()) 