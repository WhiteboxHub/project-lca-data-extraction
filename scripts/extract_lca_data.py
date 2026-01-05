
import csv
import sys
import datetime

import argparse
import os

# Define defaults
DEFAULT_IMMIGRATION_OUTPUT = 'immigration_emails.sql'
DEFAULT_OTHER_OUTPUT = 'other_emails.sql'

# Define current time string for CURRENT_TIMESTAMP replacement or usage
current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

def escape_sql(value):
    if value is None:
        return 'NULL'
    return "'" + str(value).replace("'", "''") + "'"

def format_location(row):
    parts = [
        row.get('EMPLOYER_POC_ADDRESS1', ''),
        row.get('EMPLOYER_POC_ADDRESS2', ''),
        row.get('EMPLOYER_POC_CITY', ''),
        row.get('EMPLOYER_POC_STATE', ''),
        row.get('EMPLOYER_POC_POSTAL_CODE', '')
    ]
    # Filter out empty strings and join with comma
    location = ", ".join([p for p in parts if p])
    return location

def main():
    parser = argparse.ArgumentParser(description='Extract vendor contact info from LCA CSV data.')
    parser.add_argument('--input', required=True, help='Path to the input CSV file')
    parser.add_argument('--output-dir', default='.', help='Directory to save output SQL files')
    
    args = parser.parse_args()
    
    input_file = args.input
    output_dir = args.output_dir
    
    immigration_output_file = os.path.join(output_dir, DEFAULT_IMMIGRATION_OUTPUT)
    other_output_file = os.path.join(output_dir, DEFAULT_OTHER_OUTPUT)

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    try:
        with open(input_file, mode='r', encoding='utf-8', errors='replace') as infile:
            reader = csv.DictReader(infile)
            
            with open(immigration_output_file, mode='w', encoding='utf-8') as imm_outfile, \
                 open(other_output_file, mode='w', encoding='utf-8') as other_outfile:
                
                seen_emails = set()

                for row in reader:
                    # Extract fields
                    first_name = row.get('EMPLOYER_POC_FIRST_NAME', '').strip()
                    last_name = row.get('EMPLOYER_POC_LAST_NAME', '').strip()
                    full_name = f"{first_name} {last_name}".strip()
                    
                    # Email to lowercase
                    email = row.get('EMPLOYER_POC_EMAIL', '').strip().lower()
                    
                    if not email or email in seen_emails:
                        continue
                    
                    seen_emails.add(email)

                    phone = row.get('EMPLOYER_POC_PHONE', '').strip() 
                    if not phone:
                         phone = row.get('EMPLOYER_PHONE', '').strip()

                    company_name = row.get('EMPLOYER_NAME', '').strip()
                    location = format_location(row)
                    job_title = row.get('EMPLOYER_POC_JOB_TITLE', '').strip()
                    
                    is_immigration = "immigration" in email
                    is_immigration_val = 'TRUE' if is_immigration else 'FALSE'

                    # Prepare values for SQL
                    values = [
                        escape_sql(full_name),
                        escape_sql(email),
                        escape_sql(phone),
                        escape_sql(company_name),
                        escape_sql(location),
                        escape_sql(job_title),
                        is_immigration_val,
                        'CURRENT_TIMESTAMP'
                    ]
                    
                    # Construct INSERT statement
                    sql = f"INSERT INTO whitebox_learning.company_hr_contacts ( full_name, email, phone, company_name, location, job_title, is_immigration_team, extraction_date) VALUES ({', '.join(values)});\n"
                    
                    if is_immigration:
                        imm_outfile.write(sql)
                    else:
                        other_outfile.write(sql)
                    
        print(f"Extraction complete.")
        print(f"Input file: {input_file}")
        print(f"Immigration related emails written to {immigration_output_file}")
        print(f"Other emails written to {other_output_file}")
        
    except FileNotFoundError:
        print(f"Error: File {input_file} not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
