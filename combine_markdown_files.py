import os

input_dir = "./assets/md_files"
output_file = "combined.md"

file_order = [
    # TBD
]

def combine_markdown_files():

    with open(output_file, "w", encoding="utf-8") as outfile:
        for md_file in file_order:
            file_path = os.path.join(input_dir, md_file)
            if os.path.exists(file_path):
                with open(file_path, "r", encoding="utf-8") as infile:
                    #outfile.write(f"\n# {md_file}\n\n")  
                    outfile.write(infile.read())
                    outfile.write("\n\n\n")  # 3 blank lines 
            #else:
            #    print(f"Warning: '{md_file}' not found in directory.")

if __name__ == "__main__":
    combine_markdown_files()