import csv
import os

# Set the directory to where the script is located
script_dir = os.path.dirname(os.path.abspath(__file__))

def convert_csv_to_sql(csv_filename, sql_filename, table_name):
    csv_path = os.path.join(script_dir, csv_filename)
    sql_path = os.path.join(script_dir, sql_filename)
    
    if not os.path.exists(csv_path):
        print(f"ERROR: {csv_filename} NOT FOUND!")
        return

    with open(csv_path, 'r', encoding='utf-8') as csv_file:
        reader = csv.DictReader(csv_file)
        rows = list(reader)
        columns = reader.fieldnames

    if not rows:
        print(f"ERROR: {csv_filename} IS EMPTY!")
        return

    with open(sql_path, 'w', encoding='utf-8') as sql_file:
        sql_file.write(f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES\n")
        for i, row in enumerate(rows):
            values = []
            for col in columns:
                val = row[col]
                # Format: add quotes for strings/dates, keep numbers as is
                if not val:
                    values.append("NULL")
                else:
                    try:
                        # Try to see if it's a number
                        float(val)
                        values.append(val)
                    except ValueError:
                        values.append(f"'{val}'")
            
            line = f"({', '.join(values)})"
            line += ";" if i == len(rows) - 1 else ",\n"
            sql_file.write(line)
            
    print(f"SUCCESSFULLY CONVERTED {csv_filename} TO {sql_filename}")

# --- EXECUTION ---
# This converts the CSV data files into SQL configuration files for the merge script
convert_csv_to_sql('DEPARTMENTS.csv', 'DEPARTMENTS.sql', 'DEPARTMENTS')
convert_csv_to_sql('INPATIENT_ADMISSIONS.csv', 'INPATIENT_ADMISSIONS.sql', 'INPATIENT_ADMISSIONS')