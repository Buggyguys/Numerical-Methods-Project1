from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QTabWidget, QTreeWidget, QTreeWidgetItem, 
                             QGroupBox, QScrollArea)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
import numpy as np
from scipy import linalg
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import time

class NetworkFlowGUI(QWidget):
    """Main GUI application for network flow analysis visualization."""
    
    def __init__(self):
        """Initialize the GUI application."""
        super().__init__()
        
        self.setup_gui()
        self.solve_and_display()
        
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
        self.matrix_widget = QWidget()
        
        # Add tabs
        self.tabs.addTab(self.results_widget, "Solutions")
        self.tabs.addTab(self.plots_widget, "Visualizations")
        self.tabs.addTab(self.matrix_widget, "Matrix Info")
        
        # Set up layouts for each tab
        self.results_layout = QVBoxLayout(self.results_widget)
        self.plots_layout = QVBoxLayout(self.plots_widget)
        self.matrix_layout = QVBoxLayout(self.matrix_widget)
        
    def solve_and_display(self):
        """Solve the network flow problem and display results."""
        A = np.array([
            [1, -1, 0, 0],
            [-1, 2, -1, 0],
            [0, -1, 2, -1],
            [0, 0, -1, 1]
        ], dtype=np.float64)
        
        b = np.array([10, 5, -3, -12], dtype=np.float64)
        
        solutions = self.compute_solutions(A, b)
        self.display_matrix_info(A, b)
        self.display_solutions(solutions)
        self.create_plots(solutions)
        
    def compute_solutions(self, A, b):
        """Compute solutions using multiple numerical methods."""
        solutions = {}
        
        # SVD solution
        t0 = time.time()
        U, s, Vh = linalg.svd(A)
        tol = 1e-10
        s_inv = np.array([1/x if x > tol else 0 for x in s])
        solutions['SVD'] = {
            'solution': Vh.T @ (s_inv * (U.T @ b)),
            'time': time.time() - t0
        }
        
        # Gauss Elimination solution
        t0 = time.time()
        solutions['Gauss'] = {
            'solution': self.gauss_elimination(A, b),
            'time': time.time() - t0
        }
        
        # Jacobi solution
        t0 = time.time()
        jacobi_solution, jacobi_history = self.jacobi_method(A, b)
        solutions['Jacobi'] = {
            'solution': jacobi_solution,
            'history': jacobi_history,
            'time': time.time() - t0
        }
        
        # Gauss-Seidel solution
        t0 = time.time()
        gs_solution, gs_history = self.gauss_seidel_method(A, b)
        solutions['Gauss-Seidel'] = {
            'solution': gs_solution,
            'history': gs_history,
            'time': time.time() - t0
        }
        
        # Calculate residuals
        for method in solutions:
            solutions[method]['residual'] = np.linalg.norm(A @ solutions[method]['solution'] - b)
        
        return solutions
    
    def gauss_elimination(self, A, b):
        """Solve system using Gauss elimination with partial pivoting."""
        n = len(A)
        Ab = np.column_stack((A.copy(), b.copy()))
        
        for i in range(n):
            pivot = abs(Ab[i:, i]).argmax() + i
            if pivot != i:
                Ab[i], Ab[pivot] = Ab[pivot].copy(), Ab[i].copy()
            
            for j in range(i+1, n):
                if Ab[i,i] != 0:
                    factor = Ab[j,i] / Ab[i,i]
                    Ab[j, i:] -= factor * Ab[i, i:]
        
        x = np.zeros(n)
        for i in range(n-1, -1, -1):
            if abs(Ab[i,i]) < 1e-10:
                continue
            x[i] = (Ab[i,-1] - np.dot(Ab[i,i+1:n], x[i+1:])) / Ab[i,i]
        
        return x
    
    def jacobi_method(self, A, b, max_iter=1000, tol=1e-10):
        """Solve system using Jacobi iterative method."""
        n = len(A)
        x = np.zeros(n)
        D = np.diag(A)
        R = A - np.diagflat(D)
        history = []
        
        for i in range(max_iter):
            x_old = x.copy()
            x = (b - np.dot(R, x)) / D
            error = np.linalg.norm(x - x_old) / np.linalg.norm(x)
            history.append(error)
            
            if error < tol:
                print(f"Jacobi method converged in {i+1} iterations")
                return x, history
        
        print("Jacobi method did not converge within maximum iterations")
        return x, history
    
    def gauss_seidel_method(self, A, b, max_iter=1000, tol=1e-10):
        """Solve system using Gauss-Seidel iterative method."""
        n = len(A)
        x = np.zeros(n)
        history = []
        
        for i in range(max_iter):
            x_old = x.copy()
            for j in range(n):
                x[j] = (b[j] - np.sum(A[j,:j] * x[:j]) - 
                       np.sum(A[j,j+1:] * x_old[j+1:])) / A[j,j]
            
            error = np.linalg.norm(x - x_old) / np.linalg.norm(x)
            history.append(error)
            
            if error < tol:
                print(f"Gauss-Seidel method converged in {i+1} iterations")
                return x, history
        
        print("Gauss-Seidel method did not converge within maximum iterations")
        return x, history
    
    def display_matrix_info(self, A, b):
        """Display matrix properties in the GUI."""
        # Add title
        title = QLabel("Matrix Properties")
        title.setStyleSheet("font-size: 18px; font-weight: bold;")
        title.setAlignment(Qt.AlignCenter)
        self.matrix_layout.addWidget(title)
        
        # Matrix visualization
        matrix_group = QGroupBox("System Matrix (A)")
        self.matrix_layout.addWidget(matrix_group)
        matrix_layout = QVBoxLayout(matrix_group)
        
        matrix_text = "A = \n"
        for row in A:
            matrix_text += "    [ "
            for val in row:
                matrix_text += f"{val:5.1f} "
            matrix_text += "]\n"
        
        matrix_label = QLabel(matrix_text)
        matrix_label.setFont(QFont("Courier", 12))
        matrix_layout.addWidget(matrix_label)
        
        # Right-hand side visualization
        b_text = "b = [ "
        for val in b:
            b_text += f"{val:5.1f} "
        b_text += "]"
        
        b_label = QLabel(b_text)
        b_label.setFont(QFont("Courier", 12))
        matrix_layout.addWidget(b_label)
        
        # Add matrix properties
        props_group = QGroupBox("Properties")
        self.matrix_layout.addWidget(props_group)
        props_layout = QVBoxLayout(props_group)
        
        cond_num = np.linalg.cond(A)
        det = np.linalg.det(A)
        rank = np.linalg.matrix_rank(A)
        
        props_text = (
            f"Condition Number: {cond_num:.2e}\n"
            f"Determinant: {det:.2e}\n"
            f"Rank: {rank}\n"
            f"Size: {A.shape[0]}x{A.shape[1]}"
        )
        
        props_label = QLabel(props_text)
        props_label.setFont(QFont("Courier", 10))
        props_layout.addWidget(props_label)
        
        # Add explanation
        explanation = (
            "The matrix represents the conservation laws in the transportation network.\n"
            "Each row corresponds to a node in the network, and the entries represent the connections.\n"
            "The right-hand side vector (b) represents the flow requirements at each node."
        )
        
        explanation_label = QLabel(explanation)
        explanation_label.setWordWrap(True)
        explanation_label.setAlignment(Qt.AlignCenter)
        self.matrix_layout.addWidget(explanation_label)
    
    def display_solutions(self, solutions):
        """Display solution results in a table format."""
        # Add title
        title = QLabel("Flow Solution Results")
        title.setStyleSheet("font-size: 18px; font-weight: bold;")
        title.setAlignment(Qt.AlignCenter)
        self.results_layout.addWidget(title)
        
        # Create a scrollable area for the table
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        self.results_layout.addWidget(scroll_area)
        
        # Container widget for scroll area
        scroll_content = QWidget()
        scroll_area.setWidget(scroll_content)
        scroll_layout = QVBoxLayout(scroll_content)
        
        # Create a tree widget for the table
        tree = QTreeWidget()
        tree.setHeaderLabels(["Method", "Flow Values", "Residual", "Time (s)", "Iterations"])
        tree.setAlternatingRowColors(True)
        tree.setRootIsDecorated(False)
        scroll_layout.addWidget(tree)
        
        # Add data
        for method, data in solutions.items():
            solution_str = np.array2string(data['solution'], precision=4, suppress_small=True)
            iterations = "N/A"
            if 'history' in data:
                iterations = str(len(data['history']))
            
            item = QTreeWidgetItem([
                method, 
                solution_str, 
                f"{data['residual']:.2e}", 
                f"{data['time']:.5f}",
                iterations
            ])
            tree.addTopLevelItem(item)
        
        # Auto-adjust column widths
        for i in range(tree.columnCount()):
            tree.resizeColumnToContents(i)
        
        # Add explanation
        explanation = (
            "The solution represents the flow values between nodes in the transportation network.\n"
            "A lower residual value indicates a more accurate solution.\n"
            "The iterative methods (Jacobi and Gauss-Seidel) may take more time but can be more stable for certain problems."
        )
        
        explanation_label = QLabel(explanation)
        explanation_label.setWordWrap(True)
        explanation_label.setAlignment(Qt.AlignCenter)
        self.results_layout.addWidget(explanation_label)
        
        # Add interpretation
        interp_group = QGroupBox("Interpretation")
        self.results_layout.addWidget(interp_group)
        interp_layout = QVBoxLayout(interp_group)
        
        interp_text = (
            "The system represents a network with 4 nodes:\n"
            "• Node 1 requires a net flow of +10 units (source)\n"
            "• Node 2 requires a net flow of +5 units (source)\n"
            "• Node 3 requires a net flow of -3 units (sink)\n"
            "• Node 4 requires a net flow of -12 units (sink)\n\n"
            "The solution values represent the amount of flow between connected nodes."
        )
        
        interp_label = QLabel(interp_text)
        interp_label.setWordWrap(True)
        interp_layout.addWidget(interp_label)
    
    def create_plots(self, solutions):
        """Create and display solution comparison and convergence plots."""
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))
        fig.set_tight_layout(True)
        
        x = np.arange(len(next(iter(solutions.values()))['solution']))
        width = 0.2
        
        # Solution comparison plot
        for i, (method, data) in enumerate(solutions.items()):
            ax1.bar(x + i*width - width*len(solutions)/2, 
                   data['solution'], width, label=method)
        
        ax1.set_xlabel('Flow Component')
        ax1.set_ylabel('Flow Value')
        ax1.set_title('Solution Comparison')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        ax1.set_xticks(x)
        ax1.set_xticklabels([f'Flow {i+1}' for i in x])
        
        # Convergence history plot
        for method in ['Jacobi', 'Gauss-Seidel']:
            if 'history' in solutions[method]:
                ax2.semilogy(solutions[method]['history'], label=f"{method}")
        
        ax2.set_xlabel('Iteration')
        ax2.set_ylabel('Relative Error')
        ax2.set_title('Convergence History')
        ax2.legend()
        ax2.grid(True)
        
        # Display the plot in the GUI
        canvas = FigureCanvas(fig)
        self.plots_layout.addWidget(canvas)
        
        # Add explanation
        explanation = (
            "The top graph compares the flow values computed by each method.\n"
            "The bottom graph shows the convergence history for the iterative methods (Jacobi and Gauss-Seidel).\n"
            "The convergence rate indicates how quickly each method approaches the solution."
        )
        
        explanation_label = QLabel(explanation)
        explanation_label.setWordWrap(True)
        explanation_label.setAlignment(Qt.AlignCenter)
        self.plots_layout.addWidget(explanation_label)

if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    window = NetworkFlowGUI()
    window.show()
    sys.exit(app.exec_()) 