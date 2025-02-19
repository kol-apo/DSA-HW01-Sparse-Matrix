class SparseMatrix:
    def __init__(self, matrix_file_path='', num_rows=0, num_cols=0):
        # Store non-zero elements using tuple keys instead of string
        self.elements = {}  # Using (row,col) as key instead of 'row.col'
        self.row_count = num_rows
        self.col_count = num_cols
        
        if matrix_file_path:
            self.load_matrix_file(matrix_file_path)
            return
            
        if num_rows > 0 and num_cols > 0:
            self.row_count = num_rows
            self.col_count = num_cols
            return
            
        raise SyntaxError("Invalid matrix initialization parameters")

    def load_matrix_file(self, file_path: str):
        with open(file_path, 'r') as matrix_file:
            # Parse dimensions
            self.row_count = int(matrix_file.readline().split('=')[1].strip())
            self.col_count = int(matrix_file.readline().split('=')[1].strip())
            
            # Process matrix entries
            for entry in matrix_file:
                entry = entry.strip()
                if not entry:
                    continue
                    
                if not (entry[0] == '(' and entry[-1] == ')'):
                    continue
                    
                try:
                    # Parse the entry content
                    values = entry[1:-1].split(',')
                    if len(values) != 3:
                        continue
                        
                    i, j, val = map(int, values)
                    self.update_element(i, j, val)
                        
                except ValueError:
                    continue

    def update_element(self, i, j, val):
        if val != 0:
            self.elements[(i, j)] = val
        elif (i, j) in self.elements:
            del self.elements[(i, j)]

    def fetch_element(self, i, j):
        return self.elements.get((i, j), 0)

    def add(self, other: 'SparseMatrix') -> 'SparseMatrix':
        if (self.row_count, self.col_count) != (other.row_count, other.col_count):
            raise SyntaxError("Matrix dimensions must match for addition")
            
        result = SparseMatrix(num_rows=self.row_count, num_cols=self.col_count)
        
        # Process all positions with non-zero elements
        positions = set(self.elements.keys()) | set(other.elements.keys())
        for i, j in positions:
            total = self.fetch_element(i, j) + other.fetch_element(i, j)
            result.update_element(i, j, total)
            
        return result

    def subtract(self, other: 'SparseMatrix') -> 'SparseMatrix':
        if (self.row_count, self.col_count) != (other.row_count, other.col_count):
            raise SyntaxError("Matrix dimensions must match for subtraction")
            
        result = SparseMatrix(num_rows=self.row_count, num_cols=self.col_count)
        
        # Process all positions with non-zero elements
        positions = set(self.elements.keys()) | set(other.elements.keys())
        for i, j in positions:
            diff = self.fetch_element(i, j) - other.fetch_element(i, j)
            result.update_element(i, j, diff)
            
        return result

    def multiply(self, other: 'SparseMatrix') -> 'SparseMatrix':
        if self.col_count != other.row_count:
            raise SyntaxError("Invalid dimensions for matrix multiplication")

        result = SparseMatrix(num_rows=self.row_count, num_cols=other.col_count)
        
        # Group elements by column for efficient multiplication
        col_elements = {}
        for (i, j), val in other.elements.items():
            if j not in col_elements:
                col_elements[j] = []
            col_elements[j].append((i, val))
        
        # Perform multiplication
        for (i, k), val1 in self.elements.items():
            if k in col_elements:
                for j, val2 in col_elements[k]:
                    product = result.fetch_element(i, j) + (val1 * val2)
                    result.update_element(i, j, product)
                    
        return result

    def display(self):
        print(f'rows={self.row_count}')
        print(f'cols={self.col_count}')
        
        for (i, j), val in sorted(self.elements.items()):
            print(f"({i}, {j}, {val})")

    def write_to_file(self, output_path):
        with open(output_path, 'w') as out_file:
            out_file.write(f'rows={self.row_count}\n')
            out_file.write(f'cols={self.col_count}\n')
            
            for (i, j), val in sorted(self.elements.items()):
                out_file.write(f'({i}, {j}, {val})\n')