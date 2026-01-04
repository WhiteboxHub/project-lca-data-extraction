# LCA Data Extraction

This project provides tools to extract vendor contact information from LCA (Labor Condition Application) Disclosure Data CSV files and convert them into SQL `INSERT` statements.

## Data Source

This project depends on data provided by the **IT Contractors Union**.
You can find the data repository here: [ITContractorsUnion/ITContractorsUnion](https://github.com/ITContractorsUnion/ITContractorsUnion)

The scripts in this repository are designed to process the CSV files found in the `LCA_Disclosure_Data` folders of that repository (e.g., `LCA_Disclosure_Data_FY2025_Q4.csv`).

## Usage

The main script is `extract_lca_data.py`. It takes a CSV file as input and generates two SQL files:
1.  `immigration_emails.sql`: Contains records where the email address relates to immigration departments.
2.  `other_emails.sql`: Contains all other records.

### Running the Script

```bash
python3 scripts/extract_lca_data.py --input <path_to_input_csv> --output-dir <path_to_output_dir>
```

**Example:**

```bash
python3 scripts/extract_lca_data.py --input input/LCA_Disclosure_Data_FY2025_Q4.csv --output-dir output
```

This will generate `immigration_emails.sql` and `other_emails.sql` in the `output` directory.

### Features
- **Deduplication**: Ensures that each email address generates only one SQL INSERT statement.
- **Categorization**: Splits output based on whether the email contains "immigration".
- **Formatting**: Handles special characters in SQL values and formats location data.
