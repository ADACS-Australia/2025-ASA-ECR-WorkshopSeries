import pandas as pd
import numpy as np
import configargparse

def load(filename, delimiter):
    return pd.read_csv(filename, delimiter=delimiter)

def save(table, filename):
    table.to_csv(filename, index=False)

# def clean_AT20G(table):
#     # replace all the spaces with nulls and change the column types
#     table = table.replace(r'^\s*$', np.nan, regex=True)
#     for colname in ['S20', 'e_S20', 'S8', 'e_S8', 'S5', 'e_S5']:
#         table[colname] = table[colname].astype(float)

#     # filter out all the rows with null S8/S5 and keep only those in a given RA range
#     mask = ~(table['S5'].isnull() | table['S8'].isnull())
#     mask = mask & ((table['_RAJ2000'] > 12 * 15) & (table['_RAJ2000'] < 18 * 15))
#     table = table[mask]

#     # drop the columns that we don't need
#     table = table[['_Glon', '_Glat', '_RAJ2000', '_DEJ2000', 'AT20G', 'RAJ2000', 'DEJ2000', 'S20', 'e_S20', 'S8', 'e_S8', 'S5', 'e_S5']]
#     return table

def drop_na(table, colnames):
    """
    Drop rows with NaN values in specified columns.
    """
    # replace all the spaces with nulls and change the column types
    table = table.replace(r'^\s*$', np.nan, regex=True)

    for colname in colnames:
        table = table[~table[colname].isnull()]
    return table

def convert_cols(table, colnames):
    """
    Convert specified columns to float type.
    """
    for colname in colnames:
        table[colname] = table[colname].astype(float)
    return table

def filter_rows(table, colname, min_value, max_value):
    """
    Filter rows based on a range of values in a specified column.
    """
    mask = (table[colname] >= min_value) & (table[colname] <= max_value)
    return table[mask]

def keep_columns(table, colnames):
    """
    Keep only specified columns from the DataFrame.
    """
    return table[colnames]

def clean_AT20G(infile, outfile):
    # Use all our helper functions to clean the AT20G table
    table = load(infile, '\t')
    table = drop_na(table, colnames=['S20', 'e_S20', 'S8', 'e_S8', 'S5', 'e_S5'])
    table = convert_cols(table, colnames=['S20', 'e_S20', 'S8', 'e_S8', 'S5', 'e_S5'])
    table = filter_rows(table, colname='_RAJ2000', min_value=12 * 15, max_value=18 * 15)
    table = keep_columns(table, colnames=['_Glon', '_Glat', '_RAJ2000', '_DEJ2000', 'AT20G', 'RAJ2000', 'DEJ2000', 'S20', 'e_S20', 'S8', 'e_S8', 'S5', 'e_S5'])
    save(table, outfile)
    # return the table incase we want to do something else with it
    return table

def clean_NVSS(infile, outfile):
    # Use all our helper functions to clean the NVSS table
    table = load(infile, '\t')
    table = filter_rows(table, colname='_RAJ2000', min_value=12 * 15, max_value=18 * 15)
    table = keep_columns(table, colnames=['_Glon', '_Glat', '_RAJ2000', '_DEJ2000', 'NVSS', 'RAJ2000', 'DEJ2000', 'S1.4', 'e_S1.4'])
    save(table, outfile)
    # return the table incase we want to do something else with it
    return table

def clean_SUMSS(infile, outfile):
    # Use all our helper functions to clean the SUMSS table
    table = load(infile, '\t')
    table = filter_rows(table, colname='_RAJ2000', min_value=12 * 15, max_value=18 * 15)
    table = keep_columns(table, colnames=['_Glon', '_Glat', '_DEJ2000', 'RAJ2000', 'DEJ2000', 'Sp', 'e_Sp'])
    save(table, outfile)
    # return the table incase we want to do something else with it
    return table

if __name__ == '__main__':
    parser = configargparse.ArgParser(default_config_files=["config.yaml"])
    parser.add("--config", is_config_file=True, help="Path to configuration file")
    parser.add("-i", "--input_file", type=str, default="AT20G_table.tsv", help="Path to the input file (default: AT20G_table.tsv)")
    parser.add("-o", "--output_file", type=str, default="AT20G_final.csv", help="Path to the output file (default: AT20G_final.csv)")
    parser.add("-d", "--delimiter", type=str, default="\t", help="Delimiter used in the input file (default: tab)")
    parser.add("-s", "--survey", type=str, default="AT20G", help="Survey to clean (default: AT20G)")
    args = parser.parse_args()

    # table = load(args.input_file, args.delimiter)
    # table = clean_AT20G(table)
    # save(table, args.output_file)
    if args.survey.upper() == "AT20G":
        clean_AT20G(args.input_file, args.output_file)
    elif args.survey.upper() == "NVSS":
        clean_NVSS(args.input_file, args.output_file)
    elif args.survey.upper() == "SUMSS":
        clean_SUMSS(args.input_file, args.output_file)
    else:
        print(f"Unknown survey: {args.survey}. Please choose from AT20G, NVSS, or SUMSS.")
