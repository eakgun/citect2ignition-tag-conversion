import pandas as pd
import json

# Load the Excel file
df = pd.read_excel('tag_sheet.xlsx', engine='openpyxl')

# Mapping of Citect data types to Ignition data types
data_type_mapping = {
    'REAL': 'Float4',
    'DIGITAL': 'Boolean',
    'LONG': 'Int4',
    'INT': 'Int2',
    # Add other data type mappings here
}

# Define a function to create the OPC Item Path based on the address column
def create_opc_item_path(address, data_type, device_name):
    # Strip whitespace and check if the address contains a comma
    address = address.replace(" ", "")
    if ',' in address:
        # Split the address into parts
        parts = address.split(',')
        db_number = parts[0]  # Assuming 'DB' prefix is already included
        offset_bit = parts[1]
    else:
        print(f"Invalid address format for address: {address}")
        return None

    # Determine the address type based on the data type
    if data_type == 'REAL' or data_type == 'LONG':
        address_type = 'D'  # Double Word for 32-bit data types
    elif data_type == 'INT':
        address_type = 'W'  # Word for 16-bit data types
    elif data_type == 'DIGITAL':
        # For bit-level addressing, we expect the address to contain the bit location
        if '.' in offset_bit:
            offset, bit = offset_bit.split('.')
            return f"[{device_name}]{db_number},X{offset}.{bit}"
        else:
            print(f"Bit-level address expected for DIGITAL data type at address: {address}")
            return None
    else:
        print(f"Unrecognized data type: {data_type}")
        return None

    # Construct the OPC Item Path
    opc_item_path = f"[{device_name}]{db_number},{address_type}{offset_bit}"
    return opc_item_path

# Replace 'YourDeviceName' with the actual name of your Siemens device in Ignition
device_name = 'YourDeviceName'

# User input for tag source
tag_source = input("Enter tag source (opc or memory): ")
# Create a list to hold all the tags
tags = []

# Iterate over the rows of the DataFrame
for index, row in df.iterrows():
    # Convert the Citect data type to the Ignition data type
    ignition_data_type = data_type_mapping.get(row['Data Type'], 'UnknownType')

    # Skip the row if the data type is not recognized
    if ignition_data_type == 'UnknownType':
        continue

    # Construct the OPC Item Path if the tag source is OPC
    opc_item_path = None
    if tag_source == 'opc':
        opc_item_path = create_opc_item_path(row['Address'], row['Data Type'], device_name)

    # Create the tag dictionary
    tag = {
        "name": row['Tag Name'],
        "dataType": ignition_data_type,
        "valueSource": tag_source,
        "documentation": row['Comment'],
        # Add other properties as needed
        # Placeholder for engineering units, scales, etc.
        "Format String": row.get('Format',''),
        "engUnit": row.get('Eng Units', ''),
        "engLow": row.get('Eng Zero Scale', ''),
        "engHigh": row.get('Eng Full Scale', ''),
        "scaleMode": "linear",
        "rawLow": row.get('Raw Zero Scale', ''),
        "rawHigh": row.get('Raw Full Scale', ''),
        # Add additional properties as per your Excel file and requirements
    }

    # Set the initial value based on the data type
    if ignition_data_type == 'Boolean':
        tag["value"] = False
    elif ignition_data_type in ['Float4', 'Int4', 'Int2']:
        tag["value"] = 0
    # Add other data types and their default values here

    # Add the OPC Item Path to the tag dictionary if the tag source is OPC
    if tag_source == 'opc':
        tag["opcItemPath"] = opc_item_path
        tag["opcServer"] = "Ignition OPC UA Server"

    tags.append(tag)

# Convert the tags list to JSON
tags_json = json.dumps({"tags": tags}, indent=4)

# Write the JSON to a file
json_filename = tag_source + '_tags.json'
with open(json_filename, 'w') as json_file:
    json_file.write(tags_json)

print(f"JSON file '{json_filename}' created successfully.")