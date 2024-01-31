# Ignition Tag Importer

This Python script is designed to import tags from an Excel file into Ignition using the Ignition data types. The script reads an Excel file, converts the data types from Citect to Ignition, and generates a JSON file that can be imported into Ignition.
Features

- Reads tag data from an Excel file.
- Maps Citect data types to Ignition data types.
- Generates an OPC Item Path based on the address column.
- Creates a JSON file with all the tags that can be imported into Ignition.
## Usage

1. Load your Excel file named 'tag_sheet.xlsx' in the same directory as the script.
2. Replace 'YourDeviceName' with the actual name of your Siemens device in Ignition.
3. Run the script. It will create a JSON file named 'tags.json'.
## Requirements

- Python 3
- pandas
- openpyxl
- json
- 
## Note

This script assumes that the Excel file has a specific format. The columns should be named 'Tag Name', 'Data Type', 'Address', 'Comment', 'Format', 'Eng Units', 'Eng Zero Scale', 'Eng Full Scale', 'Raw Zero Scale', and 'Raw Full Scale'. If your Excel file has a different format, you may need to modify the script.
