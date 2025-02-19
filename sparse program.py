class SparseMatrix:
    def __init__(self, matrix_file_path=None, num_rows=0, num_cols=0):
        self.rows = num_rows
        self.cols = num_cols
        # Dictionary to store non-zero elements with (row, col) as key
        self.elements = {}
        
        if matrix_file_path:
            self._load_from_file(matrix_file_path)
    
    def _load_from_file(self, matrix_file_path):
        try:
            with open(matrix_file_path, 'r') as file:
                # Read rows and columns
                rows_line = file.readline().strip()
                cols_line = file.readline().strip()
                
                # Validate format and extract dimensions
                if not rows_line.startswith('rows=') or not cols_line.startswith('cols='):
                    raise ValueError("Input file has wrong format")
                
                self.rows = int(rows_line[5:])
                self.cols = int(cols_line[5:])
                
                # Read matrix elements
                for line in file:
                    line = line.strip()
                    if not line:
                        continue
                    
                    # Validate format and parse element
                    if not (line.startswith('(') and line.endswith(')')):
                        raise ValueError("Input file has wrong format")
                    
                    # Extract values between parentheses
                    values = line[1:-1].split(',')
                    if len(values) != 3:
                        raise ValueError("Input file has wrong format")
                    
                    # Convert and validate values
                    try:
                        row = int(values[0].strip())
                        col = int(values[1].strip())
                        value = int(values[2].strip())
                    except ValueError:
                        raise ValueError("Input file has wrong format")
                    
                    # Validate indices
                    if row >= self.rows or col >= self.cols:
                        raise ValueError("Matrix indices out of bounds")
                    
                    # Store non-zero element
                    if value != 0:
                        self.elements[(row, col)] = value
                        
        except FileNotFoundError:
            raise FileNotFoundError("Unable to open file")
    
    def get_element(self, curr_row, curr_col):
        """Get element at specified position"""
        return self.elements.get((curr_row, curr_col), 0)
    
    def set_element(self, curr_row, curr_col, value):
        """Set element at specified position"""
        if curr_row >= self.rows or curr_col >= self.cols:
            raise ValueError("Matrix indices out of bounds")
        
        if value != 0:
            self.elements[(curr_row, curr_col)] = value
        elif (curr_row, curr_col) in self.elements:
            del self.elements[(curr_row, curr_col)]
    
    def add(self, other):
        """Add two sparse matrices"""
        if self.rows != other.rows or self.cols != other.cols:
            raise ValueError("Matrix dimensions don't match for addition")
        
        result = SparseMatrix(num_rows=self.rows, num_cols=self.cols)
        
        # Add elements from both matrices
        all_positions = set(self.elements.keys()) | set(other.elements.keys())
        for row, col in all_positions:
            value = self.get_element(row, col) + other.get_element(row, col)
            if value != 0:
                result.elements[(row, col)] = value
        
        return result
    
    def subtract(self, other):
        """Subtract two sparse matrices"""
        if self.rows != other.rows or self.cols != other.cols:
            raise ValueError("Matrix dimensions don't match for subtraction")
        
        result = SparseMatrix(num_rows=self.rows, num_cols=self.cols)
        
        # Process all positions that have non-zero elements in either matrix
        all_positions = set(self.elements.keys()) | set(other.elements.keys())
        for row, col in all_positions:
            value = self.get_element(row, col) - other.get_element(row, col)
            if value != 0:
                result.elements[(row, col)] = value
        
        return result
    
    def multiply(self, other):
        """Multiply two sparse matrices"""
        if self.cols != other.rows:
            raise ValueError("Matrix dimensions don't match for multiplication")
        
        result = SparseMatrix(num_rows=self.rows, num_cols=other.cols)
        
        # For each non-zero element in first matrix
        for (row1, col1), value1 in self.elements.items():
            # For each non-zero element in second matrix with matching row
            for (row2, col2), value2 in other.elements.items():
                if col1 == row2:
                    # Update result
                    pos = (row1, col2)
                    current = result.elements.get(pos, 0)
                    new_value = current + value1 * value2
                    if new_value != 0:
                        result.elements[pos] = new_value
                    elif pos in result.elements:
                        del result.elements[pos]
        
        return result
    
    def save_to_file(self, filename):
        """Save matrix to file in specified format"""
        with open(filename, 'w') as file:
            file.write(f"rows={self.rows}\n")
            file.write(f"cols={self.cols}\n")
            
            # Write non-zero elements in sorted order
            for (row, col), value in sorted(self.elements.items()):
                file.write(f"({row}, {col}, {value})\n")