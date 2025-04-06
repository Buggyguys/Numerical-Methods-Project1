# Numerical Methods Project

This project implements solutions for two numerical analysis problems:

1. **Problem A5 - Transportation Network Flow**: Analyzing flows in a transportation network using conservation laws.
2. **Problem B7 - Air Quality Index Trends**: Smoothing and analyzing AQI values over time from monitoring stations.

## How to Run the Application

### Quick Setup

1. Make sure you have Python 3.8+ installed
2. Install the required packages:
   ```bash
   pip install numpy matplotlib scipy PyQt5
   ```
3. Run the application:
   ```bash
   python main.py
   ```

### Using Virtual Environment (Recommended)

#### macOS/Linux:
```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the application
python main.py
```

#### Windows:
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the application
python main.py
```

## How to Use the Application

After running the application, you will see a main menu with two problem options:

1. **Problem A5: Transportation Network Flow** - Analyzes flows in a transportation network using conservation laws
2. **Problem B7: Air Quality Index Trends** - Analyzes AQI values over time with various interpolation methods

### Using the Transportation Network Flow Analysis

1. Click on the "Solve Network Flow" button
2. The analysis will automatically run and display three tabs:
   - **Solutions**: Shows the calculated flow values using different numerical methods
   - **Visualizations**: Displays comparison graphs of the solutions and convergence rates
   - **Matrix Info**: Shows the system matrix, its properties, and explanation

### Using the Air Quality Index Analysis

1. Click on the "Analyze AQI Data" button
2. The analysis will automatically run and display three tabs:
   - **Results**: Shows interpolated AQI values at day 2.5 using different methods
   - **Visualizations**: Displays graphs with different smoothing techniques
   - **Data**: Shows the raw data and explanations of the methods used

Click "Back to Main Menu" to return to the problem selection screen.

## Project Structure

- `main.py` - Main entry point with GUI for selecting problems
- `network_flow_gui.py` - Implementation of the Transportation Network Flow problem
- `aqi_analysis_gui.py` - Implementation of the Air Quality Index trends analysis
- `requirements.txt` - Required dependencies
- `run.sh` - Shell script for Unix/Mac setup
- `run.bat` - Batch script for Windows setup
- `charts/` - Directory containing output charts and visualizations

## Mathematical Approaches and Solutions

### Problem A5: Transportation Network Flow

#### Problem Statement

We need to analyze flows in a transportation network using conservation laws. The system is represented by the linear system Ax = b:

```
A = [
    [ 1, -1,  0,  0],
    [-1,  2, -1,  0],
    [ 0, -1,  2, -1],
    [ 0,  0, -1,  1]
]

b = [10, 5, -3, -12]
```

Where:
- A is the coefficient matrix representing the network connections
- b is the right-hand side vector representing flow requirements at each node
- x is the solution vector representing flow values between nodes

#### Mathematical Approach

1. **Singular Value Decomposition (SVD)**:
   - Decompose A = UΣV^T
   - Calculate the pseudo-inverse of A: A^+ = VΣ^+U^T
   - Compute the solution: x = A^+b
   - This approach is particularly useful for ill-conditioned matrices

2. **Gaussian Elimination with Partial Pivoting**:
   - Transform the augmented matrix [A|b] to an upper triangular form
   - Use partial pivoting to enhance numerical stability
   - Perform back-substitution to obtain the solution

3. **Jacobi Iterative Method**:
   - Start with an initial guess x^(0)
   - For each iteration k, compute:
     x_i^(k+1) = (b_i - Σ_{j≠i} a_{ij}x_j^(k)) / a_{ii}
   - Continue until convergence or maximum iterations reached

4. **Gauss-Seidel Iterative Method**:
   - Similar to Jacobi but uses updated values within each iteration
   - For each iteration k, compute:
     x_i^(k+1) = (b_i - Σ_{j<i} a_{ij}x_j^(k+1) - Σ_{j>i} a_{ij}x_j^(k)) / a_{ii}
   - Usually converges faster than Jacobi method

#### Results and Analysis

The results from the application show:

1. **SVD Solution**: [18, 8, -7, -19]
   - Very small residual (8.70e-15)
   - Fast computation time

2. **Gaussian Elimination Solution**: [37, 27, 12, 0]
   - Zero residual (machine precision)
   - Fastest computation time

3. **Jacobi Method**:
   - Did not converge within 1000 iterations
   - High residual (7.38e+00)

4. **Gauss-Seidel Method**: [24, 14, -1, -13]
   - Converged in 19 iterations
   - Very small residual (3.48e-10)

This demonstrates that for this particular network problem:
- Direct methods (SVD, Gaussian Elimination) provide accurate solutions quickly
- The Gauss-Seidel method converges efficiently
- The Jacobi method struggles to converge

Each solution represents valid flow patterns that satisfy the conservation laws at each node.

![Flow Solutions Chart](charts/flow_solutions.png)
![Convergence History Chart](charts/convergence_history.png)

### Problem B7: Air Quality Index Trends

#### Problem Statement

We need to smooth and analyze AQI values over time from monitoring stations. The sample data is:

```
Day 1: 75, Day 2: 80, Day 3: 78, Day 4: 82, Day 5: 77
```

We want to estimate the AQI value at day 2.5 using various interpolation methods.

#### Mathematical Approach

1. **Lagrange Interpolation**:
   - For a set of n+1 data points, construct the Lagrange polynomial:
     L(x) = Σ_{j=0}^n y_j * Π_{k=0,k≠j}^n (x - x_k)/(x_j - x_k)
   - Each term is weighted by the y value and a product of terms that equal 1 at x_j and 0 at other data points

2. **Newton Interpolation**:
   - Compute divided differences: f[x_0,...,x_k]
   - Construct the Newton form of the interpolation polynomial:
     N(x) = f[x_0] + f[x_0,x_1](x-x_0) + f[x_0,x_1,x_2](x-x_0)(x-x_1) + ...

3. **Neville's Algorithm**:
   - Initialize a table Q with the data points
   - Recursively compute:
     Q_{i,j}(x) = ((x - x_{i+j})*Q_{i,j-1}(x) - (x - x_i)*Q_{i+1,j-1}(x)) / (x_i - x_{i+j})
   - The final value Q_{0,n}(x) gives the interpolated value

4. **Cubic Spline**:
   - Construct a piecewise cubic polynomial that passes through all data points
   - Ensure continuity of the function and its first and second derivatives at the knots

5. **Least Squares Fit**:
   - Find polynomial coefficients that minimize the sum of squared errors
   - For degree m: min Σ_{i=0}^n (y_i - Σ_{j=0}^m a_j x_i^j)^2

#### Results and Analysis

For estimating the AQI value at day 2.5, we get:

1. **Using 3-Point Dataset** (Days 2, 3, 4):
   - Lagrange Interpolation: 78.25
   - Newton Interpolation: 78.25
   - Neville's Algorithm: 78.25

2. **Using Full Dataset** (Days 1-5):
   - Lagrange Interpolation: 78.41
   - Newton Interpolation: 78.41
   - Neville's Algorithm: 78.41

The results show that:
- All three polynomial interpolation methods produce identical results when using the same dataset
- The full dataset produces a slightly different estimate than the 3-point dataset
- Different smoothing methods (Cubic Spline vs. Least Squares) provide different curves through the data points

![AQI Interpolation Results](charts/aqi_interpolation.png)
![AQI Smoothing Methods](charts/aqi_smoothing.png)

## Technical Information

The application uses:
- PyQt5 for the graphical user interface
- Matplotlib for data visualization
- NumPy and SciPy for numerical calculations

## License

This project is provided for educational purposes. 