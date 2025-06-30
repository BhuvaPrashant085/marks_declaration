import os

def print_tree(startpath):
    for root, dirs, files in os.walk(startpath):
        # Calculate the depth (level) of the current directory
        level = root.replace(startpath, '').count(os.sep)
        indent = ' ' * 4 * level
        # Print the folder name
        print(f"{indent}{os.path.basename(root)}/")
        # Print the file names inside the folder
        subindent = ' ' * 4 * (level + 1)
        for file in files:
            print(f"{subindent}{file}")

# Example usage
print_tree('.')
