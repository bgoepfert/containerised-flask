import os

import flask
from flask import request, jsonify

import numpy as np
from time import perf_counter

# Input: Size of the matrix to return and seed value for random number generator
# Output: A matrix filled with random numbers with columns and rows of the size input
def create_random_matrix(size, seed):
    np.random.seed(seed)
    return np.random.rand(size,size)

# Input: A NumPy array
# Output: The transpose of the given matrix
def transpose_matrix(matrix):
    return np.transpose(matrix)

# Input: A NumPy array
# Output: Result of (M∗M)∗(MT∗M)
def calculate_dot_product(matrix):
    # Check that the input is a NumPy matrix, otherwise return an error
    if not isinstance(matrix, np.ndarray):
        raise ValueError("matrix must be a numpy matrix")

    # Get transposed matrix (MT)
    transposed_matrix = np.transpose(matrix)

    # Get matrix multiplied by itself (M*M)
    matrix_product = np.dot(matrix, matrix)

    # Get matrix transpose multiplied by the original matrix (MT*M)
    transposed_matrix_product = np.dot(transposed_matrix, matrix)

    # Calculate (M∗M)∗(MT∗M)
    result = np.dot(matrix_product, transposed_matrix_product)

    return result

# Input: A NumPy array
# Output: The trace value (the sum along diagonals of the array)
def calculate_trace(matrix):
    return np.trace(matrix)

app = flask.Flask(__name__)

@app.route("/")
def hello_world():
    return """Hello, welcome to Bastien's Web Math Service.
            Please POST your data to /api/math_func for processing."""

# Input: request id, matrix size and seed value in JSON format
# Output: request id, calculation result, and processing time in seconds, in JSON format
@app.route('/api/math_func', methods=['POST'])
def math_func():
    # Start processing time counter
    processing_start = perf_counter() 

    # Extract data from request
    data = request.json
    id = data.get("id")
    file = data.get("file")
    matrixSize = file.get("matrixSize")
    seed = file.get("seed")

    # Create random matrix from request data
    matrix = create_random_matrix(matrixSize, seed)
    
    # Do calculations
    dot_product_result = calculate_dot_product(matrix)
    trace_result = calculate_trace(dot_product_result)

    # End processing time counter
    processing_stop = perf_counter()
    perf = processing_stop-processing_start

    # Send JSON results to client
    return jsonify({"id": id, "result": float(trace_result), "processing_time": perf })

app.run(host='0.0.0.0', port=8080, threaded=True)
