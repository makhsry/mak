import os

input_dir = "assets/md_files/"
output_file = "README.md"

# Opening the README.md file to update 
with open(output_file, "w", encoding="utf-8") as outfile:

    # Starting with Candidate Profile      
    file_order = [
        "Intro_Professional_Summary.md",
        "Intro_Organizational_Culture.md",
        "Intro_Technical_Summary.md",
        "Intro_Contact.md",
    ]

    # Combining the Introduction section    
    for md_file in file_order:
        file_path = os.path.join(input_dir, md_file)
        if os.path.exists(file_path):
            with open(file_path, "r", encoding="utf-8") as infile:
                outfile.write(infile.read())
                outfile.write("\n\n\n")  # 3 blank lines
