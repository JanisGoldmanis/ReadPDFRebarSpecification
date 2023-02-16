import PDF_read_files

source_directory = r"C:\Users\janis.goldmanis\Downloads\TestInsulation"
destination_directory = r"C:\Users\janis.goldmanis\Downloads"

PDF_read_files.generate_total_insulation_report(source_directory, destination_directory, debug=False)