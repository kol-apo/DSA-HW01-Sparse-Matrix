import os
from sparse_matrix import SparseMatrix

def validate_user_input():
    """Get and validate operation choice"""
    print("\nSparse Matrix Operations Available:")
    print("1. Matrix Addition")
    print("2. Matrix Subtraction")
    print("3. Matrix Multiplication")
    print("4. View Matrix Content")
    
    operation = input("\nSelect operation (1/2/3/4): ").strip()
    
    if operation not in {'1', '2', '3', '4'}:
        print("Invalid operation selected. Program terminated.")
        return None
    
    return operation

def process_matrix_operations():
    # Get user choice
    operation_choice = validate_user_input()
    if not operation_choice:
        return

    # Get matrix file paths
    first_matrix_path = input(f"Enter path to{' first' if operation_choice != '4' else ''} matrix file: ").strip()
    second_matrix_path = ''
    
    if operation_choice != '4':
        second_matrix_path = input("Enter path to second matrix file: ").strip()

    try:
        # Load matrices
        primary_matrix = SparseMatrix(matrix_file_path=first_matrix_path)
        secondary_matrix = None
        
        if operation_choice != '4':
            secondary_matrix = SparseMatrix(matrix_file_path=second_matrix_path)

        # Handle display operation separately
        if operation_choice == '4':
            return primary_matrix.display()

        # Process matrix operations
        base_directory = first_matrix_path.split('sample_input_for_students')[0]
        output_directory = f'{base_directory}/outputs'
        os.makedirs(output_directory, exist_ok=True)

        # Perform selected operation and generate output path
        if operation_choice == '1':
            result_matrix = primary_matrix.add(secondary_matrix)
            output_name = f'Addition of {os.path.basename(first_matrix_path).split(".")[0]} and {os.path.basename(second_matrix_path).split(".")[0]}.txt'
            
        elif operation_choice == '2':
            result_matrix = primary_matrix.subtract(secondary_matrix)
            output_name = f'Subtraction of {os.path.basename(second_matrix_path).split(".")[0]} from {os.path.basename(first_matrix_path).split(".")[0]}.txt'
            
        else:  # Multiplication
            result_matrix = primary_matrix.multiply(secondary_matrix)
            output_name = f'Multiplication of {os.path.basename(first_matrix_path).split(".")[0]} and {os.path.basename(second_matrix_path).split(".")[0]}.txt'

        # Save result
        output_path = os.path.join(output_directory, output_name)
        result_matrix.write_to_file(output_path)
        print(f"\nOperation completed successfully. Results saved to: {output_path}")

    except SyntaxError as syntax_err:
        print(f"Matrix format error: {syntax_err}")
    except FileNotFoundError:
        print("Error: One or more input files could not be found.")
    except Exception as general_err:
        print(f"Operation failed: {general_err}")

if __name__ == "__main__":
    process_matrix_operations()