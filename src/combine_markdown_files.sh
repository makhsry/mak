#!/bin/bash

input_dir="assets/md_files/"
output_file="README.md"

# Clear or create output file
> "${output_file}"

cat "${input_dir}headers-top.md" >> "${output_file}"
echo -e "\n\n" >> "${output_file}"


cat "${input_dir}introduction.md" >> "${output_file}"
echo -e "\n\n" >> "${output_file}"

cat "${input_dir}education.md" >> "${output_file}"
echo -e "\n\n" >> "${output_file}"

echo "## Experience" >> "${output_file}"
echo -e "\n\n" >> "${output_file}"

cat "${input_dir}Work_IE_UL_1.md" >> "${output_file}"
echo -e "\n\n" >> "${output_file}"

cat "${input_dir}Work_IE_UL_2.md" >> "${output_file}"
echo -e "\n\n" >> "${output_file}"

cat "${input_dir}Work_RU_SkolTech.md" >> "${output_file}"
echo -e "\n\n" >> "${output_file}"

cat "${input_dir}Work_HK_CityU.md" >> "${output_file}"
echo -e "\n\n" >> "${output_file}"

cat "${input_dir}Work_CN_IoPCAS.md" >> "${output_file}"
echo -e "\n\n" >> "${output_file}"


# EoF 