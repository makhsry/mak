#!/bin/bash

input_dir = "assets/md_files/"
output_file = "README.md"

#

cat ${input_dir}Intro_Professional_Summary.md >> ${output_file}
cat "   " >> ${output_file}
cat ${input_dir}Intro_Organizational_Culture.md >> ${output_file}
cat "   " >> ${output_file}
cat ${input_dir}Intro_Technical_Summary.md >> ${output_file}
cat "   " >> ${output_file}
cat ${input_dir}Intro_Contact.md >> ${output_file}
cat "   " >> ${output_file}

# 