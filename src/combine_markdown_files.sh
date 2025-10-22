#!/bin/bash

input_dir="assets/md_files/"
output_file="README.md"

# Clear or create output file
> "${output_file}"

cat "${input_dir}headers-top.md" >> "${output_file}"
echo -e "\n\n" >> "${output_file}"

echo "## Introduction" >> "${output_file}"
echo -e "\n\n" >> "${output_file}"

cat "${input_dir}Intro_Professional_Summary.md" >> "${output_file}"
echo -e "\n\n" >> "${output_file}"

cat "${input_dir}Intro_Organizational_Culture.md" >> "${output_file}"
echo -e "\n\n" >> "${output_file}"

cat "${input_dir}Intro_Technical_Summary.md" >> "${output_file}"
echo -e "\n\n" >> "${output_file}"

cat "${input_dir}Intro_Contact.md" >> "${output_file}"
echo -e "\n\n" >> "${output_file}"

echo "## Education" >> "${output_file}"
echo -e "\n\n" >> "${output_file}"

cat "${input_dir}Edu_MASC_UBC_Mining.md" >> "${output_file}"
echo -e "\n\n" >> "${output_file}"

cat "${input_dir}Edu_MASC_UoT_ChemEng.md" >> "${output_file}"
echo -e "\n\n" >> "${output_file}"

cat "${input_dir}Edu_BASC_UoT_ChemEng.md" >> "${output_file}"
echo -e "\n\n" >> "${output_file}"

echo "## Experience" >> "${output_file}"
echo -e "\n\n" >> "${output_file}"



cat "${input_dir}Work_IE_UL.md" >> "${output_file}"
echo -e "\n\n" >> "${output_file}"




# EoF 
