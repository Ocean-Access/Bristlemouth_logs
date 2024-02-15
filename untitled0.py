import glob
import os

# Define functions to check for error or warning lines
def is_error_line(line):
    error_keywords = ['ERR', 'error', 'Error', 'ERROR']
    return any(keyword in line for keyword in error_keywords)

# Additional function to check for warnings if needed
# This can be used for more nuanced filtering or left out if warnings are not needed in any specific output

# Output files
output_file_all_err = 'ALL_ERR.log'
output_file_no_info = 'ALL_ERR_NO_INFO.log'
output_file_warnings_errors = 'ALL_WARNINGS_AND_ERRORS.log'
output_file_errors_only = 'ALL_ERRORS.log'

# Initialize writing to all output files
with open(output_file_all_err, 'w', encoding='utf-8', errors='replace') as outfile_all_err, \
     open(output_file_no_info, 'w', encoding='utf-8', errors='replace') as outfile_no_info, \
     open(output_file_warnings_errors, 'w', encoding='utf-8', errors='replace') as outfile_warnings_errors, \
     open(output_file_errors_only, 'w', encoding='utf-8', errors='replace') as outfile_errors_only:

    for root, dirs, files in os.walk('.'):
        for filename in files:
            filepath = os.path.join(root, filename)
            header = f"----- {os.path.basename(filename)} -----\n"

            if 'ERR.log' in filename:
                # Process ERR.log files
                with open(filepath, 'r', encoding='utf-8', errors='replace') as infile:
                    outfile_all_err.write(header)
                    outfile_no_info.write(header)
                    for line in infile:
                        outfile_all_err.write(line)
                        if '[INFO]' not in line:
                            outfile_no_info.write(line)
                    outfile_all_err.write('\n\n')
                    outfile_no_info.write('\n\n')
            else:
                # Process other files for errors and warnings, and errors only
                with open(filepath, 'r', encoding='utf-8', errors='replace') as infile:
                    lines_written_warnings_errors = False
                    lines_written_errors_only = False
                    for line in infile:
                        if is_error_line(line):
                            if not lines_written_warnings_errors:
                                outfile_warnings_errors.write(header)
                                lines_written_warnings_errors = True
                            outfile_warnings_errors.write(line)
                            if not lines_written_errors_only:
                                outfile_errors_only.write(header)
                                lines_written_errors_only = True
                            outfile_errors_only.write(line)
                    if lines_written_warnings_errors:
                        outfile_warnings_errors.write('\n\n')
                    if lines_written_errors_only:
                        outfile_errors_only.write('\n\n')

print("Processing complete.")
print(f"Full logs are saved in {output_file_all_err}.")
print(f"Filtered logs (excluding '[INFO]') are saved in {output_file_no_info}.")
print(f"Warnings and errors from other files are saved in {output_file_warnings_errors}.")
print(f"Only errors from other files are saved in {output_file_errors_only}.")
