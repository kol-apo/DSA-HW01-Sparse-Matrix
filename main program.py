def main():
    try:
        print("Sparse Matrix Operations")
        print("1. Addition")
        print("2. Subtraction")
        print("3. Multiplication")
        choice = int(input("Enter your choice (1-3): "))
        
        # Get file paths
        file1 = input("Enter first matrix file path: ")
        file2 = input("Enter second matrix file path: ")
        output_file = input("Enter output file path: ")
        
        # Load matrices
        matrix1 = SparseMatrix(file1)
        matrix2 = SparseMatrix(file2)
        
        # Perform operation
        if choice == 1:
            result = matrix1.add(matrix2)
        elif choice == 2:
            result = matrix1.subtract(matrix2)
        elif choice == 3:
            result = matrix1.multiply(matrix2)
        else:
            raise ValueError("Invalid choice")
        
        # Save result
        result.save_to_file(output_file)
        print(f"Operation completed successfully. Result saved to {output_file}")
        
    except Exception as e:
        print(f"Error: {str(e)}")
        return 1
    
    return 0

if __name__ == "__main__":
    main()