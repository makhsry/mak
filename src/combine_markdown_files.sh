#!/bin/bash

input_dir="assets/md_files/"
output_file="README.md"

# Clear or create output file
> "${output_file}"

#cat "${input_dir}headers-top.md" >> "${output_file}"
#echo -e "\n\n" >> "${output_file}"

cat "${input_dir}introduction.md" >> "${output_file}"
echo -e "\n\n" >> "${output_file}"

cat "${input_dir}education.md" >> "${output_file}"
echo -e "\n\n" >> "${output_file}"

cat "${input_dir}exprience.md" >> "${output_file}"
echo -e "\n\n" >> "${output_file}"

# EoF 