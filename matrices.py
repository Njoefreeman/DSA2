import re  # For regular expressions
import os  # For handling file paths

class SparseMatrix:
    def __init__(self, matrixFilePath=None, numRows=0, numCols=0):
        self.numRows = numRows
        self.numCols = numCols
        self.elements = {}
        if matrixFilePath:
            self._load_matrix_from_file(matrixFilePath)
    
    def _load_matrix_from_file(self, matrixFilePath):
        try:
            abs_path = os.path.abspath(matrixFilePath)
            print(f"Loading matrix from: {abs_path}")
            with open(abs_path, 'r') as file:
                lines = file.readlines()
                
                # Extract matrix dimensions
                self.numRows = int(lines[0].strip().split('=')[1])
                self.numCols = int(lines[1].strip().split('=')[1])
                
                # Read matrix elements
                for line in lines[2:]:
                    line = line.strip()
                    if not line:  # Skip empty lines
                        continue
                    # Use regular expression to extract matrix elements
                    match = re.match(r'\((\d+),\s*(\d+),\s*(-?\d+)\)', line)
                    if not match:
                        raise ValueError("Invalid file format")
                    row, col, value = map(int, match.groups())
                    self.set_element(row, col, value)
        except Exception as e:
            raise ValueError(f"Failed to load matrix from file: {e}")

    def get_element(self, row, col):
        """Retrieve an element from the matrix, returns 0 if not present (sparse)."""
        return self.elements.get((row, col), 0)
    
    def set_element(self, row, col, value):
        """Set an element in the matrix, remove if value is zero to maintain sparsity."""
        if value != 0:
            self.elements[(row, col)] = value
        elif (row, col) in self.elements:
            del self.elements[(row, col)]  # Maintain sparsity

    def add(self, other):
        """Add two sparse matrices."""
        if self.numRows != other.numRows or self.numCols != other.numCols:
            raise ValueError("Matrix dimensions must match for addition")
        
        result = SparseMatrix(numRows=self.numRows, numCols=self.numCols)
        
        # Add elements from both matrices
        for (row, col), value in self.elements.items():
            result.set_element(row, col, value + other.get_element(row, col))
        
        for (row, col), value in other.elements.items():
            if (row, col) not in self.elements:
                result.set_element(row, col, value)
        
        return result
    
    def subtract(self, other):
        """Subtract two sparse matrices."""
        if self.numRows != other.numRows or self.numCols != other.numCols:
            raise ValueError("Matrix dimensions must match for subtraction")
        
        result = SparseMatrix(numRows=self.numRows, numCols=self.numCols)
        
        # Subtract elements from both matrices
        for (row, col), value in self.elements.items():
            result.set_element(row, col, value - other.get_element(row, col))
        
        for (row, col), value in other.elements.items():
            if (row, col) not in self.elements:
                result.set_element(row, col, -value)
        
        return result
    
    def multiply(self, other):
        """Multiply two sparse matrices."""
        if self.numCols != other.numRows:
            raise ValueError("Invalid dimensions for matrix multiplication")
        
        result = SparseMatrix(numRows=self.numRows, numCols=other.numCols)
        
        # Perform dot product for matrix multiplication
        for (row1, col1), value1 in self.elements.items():
            for col2 in range(other.numCols):
                value2 = other.get_element(col1, col2)
                if value2 != 0:
                    result.set_element(row1, col2, result.get_element(row1, col2) + value1 * value2)
        
        return result


def main():
    # Load two sparse matrices from file
    matrix1 = SparseMatrix(matrixFilePath='C:/Users/PC/Downloads/DSA2/DSA2/input_02.txt')
    matrix2 = SparseMatrix(matrixFilePath='C:/Users/PC/Downloads/DSA2/DSA2/input_03.txt')
    
    # Ask user for the operation
    operation = input("Choose operation: add, subtract, multiply: ").strip().lower()
    
    if operation == 'add':
        result = matrix1.add(matrix2)
    elif operation == 'subtract':
        result = matrix1.subtract(matrix2)
    elif operation == 'multiply':
        result = matrix1.multiply(matrix2)
    else:
        print("Invalid operation")
        return
    
    # Output result matrix (in sparse format)
    for (row, col), value in result.elements.items():
        print(f"({row}, {col}, {value})")


if __name__ == "__main__":
    main()
