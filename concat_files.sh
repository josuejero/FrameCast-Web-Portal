#!/bin/bash

# Clear the all_code.txt file if it exists
> all_code.txt

# Function to append file content to all_code.txt
append_file_content() {
    echo -e "\n=== $1 ===\n" >> all_code.txt
    cat "$1" >> all_code.txt
}

# Export the function for use in find -exec
export -f append_file_content

# Find all .py, .js, .html, and .css files excluding node_modules and venv directories
find . -type f \( -name "*.py" -o -name "*.js" -o -name "*.html" -o -name "*.css" \) ! -path "./node_modules/*" ! -path "./venv/*" -exec bash -c 'append_file_content "$0"' {} \;

echo "All code/text has been appended to all_code.txt."
