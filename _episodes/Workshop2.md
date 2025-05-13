---
title: "How to Build on Past Success"
teaching: 45
exercises: 45
questions:
- "How can I make my workflows more flexible and reusable?"
- "What are the benefits of parameterizing scripts and workflows?"
- "How can I document my workflows to ensure reproducibility?"
objectives:
- "Understand the importance of documenting workflows for reproducibility."
- "Learn how to create self-documenting workflows that capture parameters, options, and software versions."
keypoints:
- "Parameterizing workflows increases flexibility and reusability."
- "Using configuration files helps separate code logic from settings."
- "Self-documenting workflows enhance reproducibility and transparency."
- "Automating documentation ensures it stays up-to-date with minimal effort."
- "Capturing software versions and parameters is essential for reproducibility."
- "Clear and consistent documentation improves collaboration and understanding."
---


# Overview
Your second research project benefits from the lessons you learned in the first, as does your second paper.
This retrospective attention to your work is highly beneficial, but what if we could turn this into a prospective activity?
Similar to the [FAIR principles for data](https://www.go-fair.org/fair-principles/) that we noted last lesson, there are equivalent [FAIR principles for research software](https://www.nature.com/articles/s41597-022-01710-x).
Today we are going to explore ways to set ourselves up for future success by focusing on the R component of FAIR, making our current work not only reproducible but also reusable.

## Why Reproducible and Reusable Workflows Matter

Reproducible and reusable workflows are essential for advancing research and fostering collaboration.
Some points to consider:

1. **Accelerates Scientific Discovery**:
    - By making workflows reproducible, other researchers can validate your findings and build upon them, accelerating the pace of discovery.

2. **Saves Time and Effort**:
    - Reusable workflows reduce the need to start from scratch, saving time for both you and others who may use your work.

3. **Enhances Collaboration**:
    - Clear, reproducible workflows make it easier for collaborators to understand and contribute to your research.

4. **Increases Research Impact**:
    - Sharing reusable workflows can lead to more citations and recognition, as others adopt and adapt your methods.

5. **Ensures Long-Term Accessibility**:
    - Properly documented workflows remain accessible and usable even years later, preserving the value of your research.

6. **Promotes Transparency and Trust**:
    - Reproducibility fosters trust in your results by allowing others to verify your methods and conclusions.

7. **Facilitates Teaching and Learning**:
    - Reusable workflows serve as excellent teaching tools, helping students and new researchers learn best practices.

By prioritizing reproducibility and reusability, you contribute to a more open, efficient, and impactful research ecosystem.


## Recap
We'll assume that you already have some level of automation in your workflow.
This automation was explored in our previous lesson, but if you are new to the workshop then here is a quick summary of what we did last time.
The example problem we worked on was to prepare some tables of data (radio source catalogues) for processing.
The first workshop focused only on processing one data source - the "AT20G" catalogue.

In the last workshop we:

- Worked through a data cleaning workflow that was initially written for a human.
- Looked at some different `bash` and `python` tools that could be used to automate different parts of the workflow.
- Combined all the tools together to make a `workflow.sh` script that we could run from the command line.
- Organised our project directory to make it clear what the intent of each file is.
- Creatd a virtual environment for our project to make it easy to run on different computers.
- Turned our `workflow.sh` into a `makefile` so that we could easily run the workflow without repeating unneccessary steps.
- Talkd about using Nextflow instead of make, but didn't actually do any Nextflow coding.

> ## Last weeks code
> If you didn't participate last week, no stress
> We ended up with a directory structure as follows:
> ```output
> my-project/
> ├── .env/
> ├── data
> │   ├── final/
> │   ├── processing/
> │   └── raw/
> ├── makefile
> ├── requirements.txt
> └── src
>     └── clean_AT20G.py
> ```
> > ## How to make these files
> > You can copy the following code to make the required files:
> > 
> > `makefile`
> > ```makefile
> > # List all the outputs that we want
> > all: data/final/AT20G_final.csv data/final/AT20G_header.txt
> > 
> > data/raw/AT20G.tsv:
> >         wget -O data/raw/AT20G.tsv https://raw.githubusercontent.com/ADACS-Australia/2025-ASA-ECR-WorkshopSeries/refs/heads/gh-pages/data/Workshop1/AT20G.tsv
> > 
> > data/final/AT20G_header.txt: data/raw/AT20G.tsv
> >         grep -e '^\#' data/raw/AT20G.tsv > data/final/AT20G_header.txt
> > 
> > data/processing/AT20G_table.tsv: data/raw/AT20G.tsv
> >         grep -v -e '^\#' -e '^-' -e '^deg' -e '^$$' data/raw/AT20G.tsv > data/processing/AT20G_table.tsv
> > 
> > # Note that I put the script as a dependency so that this step is redone if the script is updated :D
> > data/final/AT20G_final.csv: data/processing/AT20G_table.tsv src/clean_AT20G.py
> >         python src/clean_AT20G.py
> > 
> > # Delete all the data files
> > clean:
> >         rm data/*/AT20G*
> > ```
> > `clean_AT20G.py`
> > ```python
> > import pandas as pd
> > import numpy as np
> > 
> > # Read the table
> > df = pd.read_csv('data/processing/AT20G_table.tsv', delimiter='\t')
> > 
> > # replace all the spaces with nulls and change the column types
> > df_fix = df.replace(r'^\s*$', np.nan, regex=True)
> > for colname in ['S20', 'e_S20', 'S8', 'e_S8', 'S5', 'e_S5']:
> >   df_fix[colname] = df_fix[colname].astype(float)
> > 
> > # filter out all the rows with null S8/S5 and keep only those in a given RA range
> > mask = ~(df_fix['S5'].isnull() | df_fix['S8'].isnull())
> > mask = mask & ((df_fix['_RAJ2000'] > 12*15) & (df_fix['_RAJ2000']<18*15))
> > df_fix = df_fix[mask]
> > 
> > # drop the columns that we don't need
> > df_fix = df_fix[['_Glon', '_Glat', '_RAJ2000', '_DEJ2000', 'AT20G', 'RAJ2000', 'DEJ2000', 'S20', 'e_S20', 'S8', 'e_S8', 'S5', 'e_S5']]
> > 
> > # save to a file
> > df_fix.to_csv('data/final/AT20G_final.csv', index=False)
> > ```
> > `requirements.txt`
> > ```output
> > numpy==2.2.4
> > pandas==2.2.3
> > ```
> > 
> > Making the `.env` file we can run:
> > ```bash
> > python -m venv .env
> > source .env/bin/activate
> > pip install -r requirements.txt
> > ```
> {: .solution}
>
{: .callout}


# Today's focus

In this workshop we are going to revise the work that we did last time with the goal of making the scripts and workflow more flexible.
Our goal is to be able to process additional data without haveing to duplicate the entire workflow.
Secondary goals include documenting our work, and publishing workflows so that other's can build upon them.
Documenting our work means that it's easier to describe when it comes time for writing a report or paper.
Comprehensive documentation includes detailed descriptions of methodologies, data sources, software used, and any specific configurations or parameters.
Publishing our work makes it easier for others to build on your work (increasing your citations and impact), or for people to reach out with collaborative opportunities.

## Automation & Workflow Repeatability

We have already learned about using scripting and automation for consistency.
Now we are going to build on that past success and update our scripts to be more flexible.

### Parameterizing Workflows and Scripts

To make your workflows and scripts more flexible and reusable, you can design them to accept parameters or configuration files.
This approach allows you to adjust the behavior of your scripts without modifying the source code directly.

Here are some strategies to achieve this:

1. **Command-Line Arguments**:
    - Use command-line arguments to pass parameters to your scripts. Libraries like `argparse` in Python can help you handle these arguments.
    - Example in Python:
      ```python
      import argparse

      def main(data_source, output_dir):
          # Your workflow logic here
          print(f"Processing data from {data_source} and saving results to {output_dir}")

      if __name__ == "__main__":
          parser = argparse.ArgumentParser(description="Process some data.")
          parser.add_argument("--data_source", type=str, required=True, help="Path to the data source")
          parser.add_argument("--output_dir", type=str, required=True, help="Directory to save the output")
          args = parser.parse_args()
          main(args.data_source, args.output_dir)
      ```

2. **Configuration Files**:
    - Store parameters and settings in configuration files (e.g., YAML, JSON). This makes it easy to change configurations without altering the code.
    - Example of a YAML configuration file:
        ```yaml
        data_source: "https://example.com/data.csv"
        output_dir: "/path/to/output"
        preprocessing:
            - step: "normalize"
                method: "min-max"
        ```
    - Example of reading a YAML configuration file in Python:
      ```python
      import yaml

      def main(config):
          data_source = config['data_source']
          output_dir = config['output_dir']
          # Your workflow logic here
          print(f"Processing data from {data_source} and saving results to {output_dir}")

      if __name__ == "__main__":
          with open("config.yaml", 'r') as stream:
              config = yaml.safe_load(stream)
          main(config)
      ```

3. **Command-Line Arguments *and* Configuration Files**

    The `configargparse` library allows you to combine command-line arguments and configuration files seamlessly. This approach provides flexibility by allowing users to specify parameters either in a configuration file or directly via the command line.

    Here’s an example:

    ```python
    import configargparse

    def main(data_source, output_dir, preprocessing_steps):
        print(f"Processing data from {data_source}")
        print(f"Saving results to {output_dir}")
        print(f"Preprocessing steps: {preprocessing_steps}")

    if __name__ == "__main__":
        parser = configargparse.ArgParser(default_config_files=["config.yaml"])
        parser.add("--config", is_config_file=True, help="Path to configuration file")
        parser.add("--data_source", type=str, required=True, help="Path to the data source")
        parser.add("--output_dir", type=str, required=True, help="Directory to save the output")
        parser.add("--preprocessing_steps", nargs="+", help="List of preprocessing steps")

        args = parser.parse_args()
        main(args.data_source, args.output_dir, args.preprocessing_steps)
    ```

    Example `config.yaml` file:

    ```yaml
    data_source: "https://example.com/data.csv"
    output_dir: "/path/to/output"
    preprocessing_steps:
      - "normalize"
      - "filter"
    ```

    Usage:
    - Using a configuration file:
      ```bash
      python script.py --config config.yaml
      ```
    - Overriding parameters via the command line:
      ```bash
      python script.py --config config.yaml --output_dir /new/output/path
      ```

    This method provides the best of both worlds, enabling flexibility and ease of use for different scenarios. 

In our previous workshop we created a `python` script (`clean_AT20G.py`) that looked like this:

```python
import pandas as pd
import numpy as np

# Read the table
df = pd.read_csv('AT20G_table.tsv', delimiter='\t')

# replace all the spaces with nulls and change the column types
df_fix = df.replace(r'^\s*$', np.nan, regex=True)
for colname in ['S20', 'e_S20', 'S8', 'e_S8', 'S5', 'e_S5']:
  df_fix[colname] = df_fix[colname].astype(float)

# filter out all the rows with null S8/S5 and keep only those in a given RA range
mask = ~(df_fix['S5'].isnull() | df_fix['S8'].isnull())
mask = mask & ((df_fix['_RAJ2000'] > 12*15) & (df_fix['_RAJ2000']<18*15))
df_fix = df_fix[mask]

# drop the columns that we don't need
df_fix = df_fix[['_Glon', '_Glat', '_RAJ2000', '_DEJ2000', 'AT20G', 'RAJ2000', 'DEJ2000', 'S20', 'e_S20', 'S8', 'e_S8', 'S5', 'e_S5']]

# save to a file
df_fix.to_csv('AT20G_final.csv', index=False)

```

We can generalise the script by doing the following things:
1. Making the input and ouput tables configurable
2. Letting the user specify the delimiter, but having tabs as default.
3. Determining which columns should be kept/removed from user input
4. Keeping all the above options in a config file, so we can later determine how the script was run.

To do all of this we'll use the `configargparse` option noted above.
Note that in this example we have two blocks of code: the `if __name__`  block which parses all the command line options, and the `main()` function which does all the work.
We'll start by refactoring our code to reflect this idiom.

> ## Separate the configuring and "doing" parts of the code
> Refactor the `clean_AT20G.py` code so that it has an `if __name__` clause, and a `main()` function.
>
> > ## Solution
> > ```python
> > import pandas as pd
> > import numpy as np
> > 
> > def main():
> >   # Read the table
> >   df = pd.read_csv('AT20G_table.tsv', delimiter='\t')
> > 
> >   # replace all the spaces with nulls and change the column types
> >   df_fix = df.replace(r'^\s*$', np.nan, regex=True)
> >   for colname in ['S20', 'e_S20', 'S8', 'e_S8', 'S5', 'e_S5']:
> >     df_fix[colname] = df_fix[colname].astype(float)
> > 
> >   # filter out all the rows with null S8/S5 and keep only those in a given RA range
> >   mask = ~(df_fix['S5'].isnull() | df_fix['S8'].isnull())
> >   mask = mask & ((df_fix['_RAJ2000'] > 12*15) & (df_fix['_RAJ2000']<18*15))
> >   df_fix = df_fix[mask]
> > 
> >   # drop the columns that we don't need
> >   df_fix = df_fix[['_Glon', '_Glat', '_RAJ2000', '_DEJ2000', 'AT20G', 'RAJ2000', 'DEJ2000', 'S20', 'e_S20', 'S8', 'e_S8', 'S5', 'e_S5']]
> > 
> >   # save to a file
> >   df_fix.to_csv('AT20G_final.csv', index=False)
> > 
> > if __name__ == '__main__':
> >   main()
> > ```
> {: .solution}
{: .challenge}

Some of the work that was done in our script is specific to the AT20G catalogue (selection of columns) but other work is more generic (loading / saving data).
We have some options here:
1. Write separate functions for the different catalogues that we will use
2. Write a single, but very flexible, function that can handle any catalogue

The second option sounds good, but it will certainly be more work, and it may be over-engineering a solution.
Let us take the path of small resistance, and start with option 1, and then move toward option 2 in the future if we need to.
This minimises the initial outlay of work, without incurring a large technical debt.

> ## First small step
> Change the above code so that we have the following functions:
> 1. `load(filename, delimiter)` returns a pandas data frame
> 2. `save(table, filename)` returns nothing
> 3. `clean_AT20G(table)` returns a cleaned version of a data frame
> 
> Save this new file as `clean_tables.py`
>
> > ## `clean_tables.py`
> > ```python
> > import pandas as pd
> > import numpy as np
> > 
> > def load(filename, delimiter):
> >     return pd.read_csv(filename, delimiter=delimiter)
> > 
> > def save(table, filename):
> >     table.to_csv(filename, index=False)
> > 
> > def clean_AT20G(table):
> >     # replace all the spaces with nulls and change the column types
> >     table = table.replace(r'^\s*$', np.nan, regex=True)
> >     for colname in ['S20', 'e_S20', 'S8', 'e_S8', 'S5', 'e_S5']:
> >         table[colname] = table[colname].astype(float)
> > 
> >     # filter out all the rows with null S8/S5 and keep only those in a given RA range
> >     mask = ~(table['S5'].isnull() | table['S8'].isnull())
> >     mask = mask & ((table['_RAJ2000'] > 12 * 15) & (table['_RAJ2000'] < 18 * 15))
> >     table = table[mask]
> > 
> >     # drop the columns that we don't need
> >     table = table[['_Glon', '_Glat', '_RAJ2000', '_DEJ2000', 'AT20G', 'RAJ2000', 'DEJ2000', 'S20', 'e_S20', 'S8', 'e_S8', 'S5', 'e_S5']]
> >     return table
> > 
> > if __name__ == '__main__':
> >     table = load('AT20G_table.tsv')
> >     table = clean_AT20G(table)
> >     save(table, 'AT20G_final.csv')
> > ```
> {: .solution}
{: .challenge}

Now we are in a position to be able to use config argparse to modify the `if __name__` block of our code.

> ## Updated Script with `configargparse`
> Modify the `clean_tables.py` script to use `configargparse` for accepting input and output filenames as arguments.
> Keep the existing behaviour of our code by making the current hard-coded values the default.
>
> > ## `clean_tables.py`
> > ```python
> > import pandas as pd
> > import numpy as np
> > import configargparse
> > 
> > def load(filename, delimiter):
> >     return pd.read_csv(filename, delimiter=delimiter)
> > 
> > def save(table, filename):
> >     table.to_csv(filename, index=False)
> > 
> > def clean_AT20G(table):
> >     # replace all the spaces with nulls and change the column types
> >     table = table.replace(r'^\s*$', np.nan, regex=True)
> >     for colname in ['S20', 'e_S20', 'S8', 'e_S8', 'S5', 'e_S5']:
> >         table[colname] = table[colname].astype(float)
> > 
> >     # filter out all the rows with null S8/S5 and keep only those in a given RA range
> >     mask = ~(table['S5'].isnull() | table['S8'].isnull())
> >     mask = mask & ((table['_RAJ2000'] > 12 * 15) & (table['_RAJ2000'] < 18 * 15))
> >     table = table[mask]
> > 
> >     # drop the columns that we don't need
> >     table = table[['_Glon', '_Glat', '_RAJ2000', '_DEJ2000', 'AT20G', 'RAJ2000', 'DEJ2000', 'S20', 'e_S20', 'S8', 'e_S8', 'S5', 'e_S5']]
> >     return table
> > 
> > if __name__ == '__main__':
> >     parser = configargparse.ArgParser(default_config_files=["config.yaml"])
> >     parser.add("--config", is_config_file=True, help="Path to configuration file")
> >     parser.add("-i", "--input_file", type=str, default="AT20G_table.tsv", help="Path to the input file (default: AT20G_table.tsv)")
> >     parser.add("-o", "--output_file", type=str, default="AT20G_final.csv", help="Path to the output file (default: AT20G_final.csv)")
> >     parser.add("-d", "--delimiter", type=str, default="\t", help="Delimiter used in the input file (default: tab)")
> > 
> >     args = parser.parse_args()
> > 
> >     table = load(args.input_file, args.delimiter)
> >     table = clean_AT20G(table)
> >     save(table, args.output_file)
> > ```
> > Note that we provide both long and short versions of the commonly used options (`-i` being the shorthand for `--input_file`).
> >
> {: .solution}
{: .challenge}



Now we have a script that we can modify from the command line to read/write different filenames, and to accept different  file types (.csv and .tsv) using the `--delimiter` option.
Our next step is to change our script so that it can work on other catalogues.
Before we can do that we need to understand how the other catalogue formats are different, and that means doing some more work by hand.

> ## Download and inspect the NVSS data set
> The data set is [here](https://github.com/ADACS-Australia/2025-ASA-ECR-WorkshopSeries/raw/refs/heads/gh-pages/data/Workshop2/NVSS.tsv).
>
> Download using `wget` and then inspect using `less`.
>
> How would we change our workflow for pre-processing the AT20G catalogue for this new catalogue?
>
> What parts of the workflow would we keep the same?
>
> > ## Changes
> > Some of the processing is going to be common between the two catalogues:
> > - loading and saving
> > - filtering on the "_RA2000" column
> > 
> > Some of the processing is common but needs to be done slightly differnetly:
> > - The list of columns to keep
> > 
> > Some processing isn't needed for NVSS:
> > - dropping the rows with blanks
> > - converting column types
> > 
> {: .solution}
>
{: .challenge}

We can now start to break down the `clean_AT20G.py` script into more atomic pieces so that we can reuse some (but not all) of them for the NVSS catalogue.
This can be done without changing how the script is called from the command line, making the new script backwards compatible with our previous workflow.

> ## Update `clean_tables.py`
>
> Break the `clean_AT20G` function into smaller parts:
> - `drop_na(table, colnames)` - convert empty strings to `np.nan` and then remove rows with blanks
> - `convert_cols(table, colnames)` - convert the given columns into float format
> - `filter_rows(table, colname, min_value, max_value)` - remove rows where min_value < colname < max_value is not true.
> - `keep_columns(table, colnames)` - reduce the table to contain only the given columns
>
> Once complete, your `clean_AT20G` function should remain, but it should only be calling other functions.
>
> > ## New version!
> > ```python
> > import pandas as pd
> > import numpy as np
> > import configargparse
> > 
> > def load(filename, delimiter):
> >     return pd.read_csv(filename, delimiter=delimiter)
> > 
> > def save(table, filename):
> >     table.to_csv(filename, index=False)
> > 
> > def drop_na(table, colnames):
> >     """
> >     Drop rows with NaN values in specified columns.
> >     """
> >     # replace all the spaces with nulls and change the column types
> >     table = table.replace(r'^\s*$', np.nan, regex=True)
> > 
> >     for colname in colnames:
> >         table = table[~table[colname].isnull()]
> >     return table
> > 
> > def convert_cols(table, colnames):
> >     """
> >     Convert specified columns to float type.
> >     """
> >     for colname in colnames:
> >         table[colname] = table[colname].astype(float)
> >     return table
> > 
> > def filter_rows(table, colname, min_value, max_value):
> >     """
> >     Filter rows based on a range of values in a specified column.
> >     """
> >     mask = (table[colname] >= min_value) & (table[colname] <= max_value)
> >     return table[mask]
> > 
> > def keep_columns(table, colnames):
> >     """
> >     Keep only specified columns from the DataFrame.
> >     """
> >     return table[colnames]
> > 
> > def clean_AT20G(infile, outfile):
> >     # Use all our helper functions to clean the AT20G table
> >     table = load(infile, '\t')
> >     table = drop_na(table, colnames=['S20', 'e_S20', 'S8', 'e_S8', 'S5', 'e_S5'])
> >     table = convert_cols(table, colnames=['S20', 'e_S20', 'S8', 'e_S8', 'S5', 'e_S5'])
> >     table = filter_rows(table, colname='_RAJ2000', min_value=12 * 15, max_value=18 * 15)
> >     table = keep_columns(table, colnames=['_Glon', '_Glat', '_RAJ2000', '_DEJ2000', 'AT20G', 'RAJ2000', 'DEJ2000', 'S20', 'e_S20', 'S8', 'e_S8', 'S5', 'e_S5'])
> >     save(table, outfile)
> >     # return the table incase we want to do something else with it
> >     return table
> > 
> > if __name__ == '__main__':
> >     parser = configargparse.ArgParser(default_config_files=["config.yaml"])
> >     parser.add("--config", is_config_file=True, help="Path to configuration file")
> >     parser.add("-i", "--input_file", type=str, default="AT20G_table.tsv", help="Path to the input file (default: AT20G_table.tsv)")
> >     parser.add("-o", "--output_file", type=str, default="AT20G_final.csv", help="Path to the output file (default: AT20G_final.csv)")
> >     parser.add("-d", "--delimiter", type=str, default="\t", help="Delimiter used in the input file (default: tab)")
> >     parser.add("-s", "--survey", type=str, default="AT20G", help="Survey to clean (default: AT20G)")
> >     args = parser.parse_args()
> > 
> >     clean_AT20G(args.input_file, args.output_file)
> > ```
> > 
> {: .solution}
>
{: .challenge}

Now we can make a new function `clean_NVSS` to clean the NVSS dataset using the existing functions.

> ## Update `clean_tables.py`
> Use your newly created functions to create `clean_NVSS(infile, outfile)`
>
> > ## New code
> >```python
> > ...
> > 
> > def clean_NVSS(infile, outfile):
> >     # Use all our helper functions to clean the NVSS table
> >     table = load(infile, '\t')
> >     table = filter_rows(table, colname='_RAJ2000', min_value=12 * 15, max_value=18 * 15)
> >     table = keep_columns(table, colnames=['_Glon', '_Glat', '_RAJ2000', '_DEJ2000', 'NVSS', 'RAJ2000', 'DEJ2000', 'S1.4', 'e_S1.4'])
> >     save(table, outfile)
> >     # return the table incase we want to do something else with it
> >     return table
> > 
> > if __name__ == '__main__':
> >     parser = configargparse.ArgParser(default_config_files=["config.yaml"])
> >     parser.add("--config", is_config_file=True, help="Path to configuration file")
> >     parser.add("-i", "--input_file", type=str, default="AT20G_table.tsv", help="Path to the input file (default: AT20G_table.tsv)")
> >     parser.add("-o", "--output_file", type=str, default="AT20G_final.csv", help="Path to the output file (default: AT20G_final.csv)")
> >     parser.add("-d", "--delimiter", type=str, default="\t", help="Delimiter used in the input file (default: tab)")
> >     parser.add("-s", "--survey", type=str, default="AT20G", help="Survey to clean (default: AT20G)")
> >     args = parser.parse_args()
> > 
> >     if args.survey.upper() == "AT20G":
> >         clean_AT20G(args.input_file, args.output_file)
> >     elif args.survey.upper() == "NVSS":
> >         clean_NVSS(args.input_file, args.output_file)
> >     else:
> >         print(f"Unknown survey: {args.survey}. Please choose from AT20G or NVSS.")
> > ```
> {: .solution}
{: .challenge}

### Review
So far we have done the following:
- Manually download the NVSS data set
- Inspected the new data set to determine what processing is going to be needed
- Updated our python script to include the new filtering steps needed.

However, we haven't been able to test that our script works since we haven't done the pre-processing stages for the NVSS catalogue - it still has an attached header.
Let's now update our `makefile` to have a workflow for NVSS so that we can then test our new python file.
We can also update the `makefile` to use the new python script for the AT20G catalogue.
Unfortunately, we can't easily use the same tricks in make as we did in python - at least not without making it unreadable.
Fortunately, given the similarity between the workflows we can do a copy/paste/edit job to make the NVSS version!

> ## Create an NVSS workflow in our `makefile`
> Use your knowledge from inspecting the NVSS file, and the existing AT20G workflow, to make a workflow for NVSS in our `makefile`.
> - Allow users to choose wich workflow to run with new targets: `NVSS` and `AT20G`
> - Update the `all` target to include both `NVSS` and `AT20G`
> 
> > ## Result
> > ```makefile
> > .PHONY: AT20G NVSS all clean
> > 
> > AT20G: data/final/AT20G_final.csv data/final/AT20G_header.txt
> > 
> > NVSS: data/final/NVSS_final.csv data/final/NVSS_header.txt
> > 
> > all: AT20G NVSS
> > 
> > # AT20G survey
> > data/raw/AT20G.tsv:
> > 	wget -O data/raw/AT20G.tsv https://raw.githubusercontent.com/ADACS-Australia/2025-ASA-ECR-WorkshopSeries/refs/heads/gh-pages/data/Workshop1/AT20G.tsv
> > 
> > data/final/AT20G_header.txt: data/raw/AT20G.tsv
> > 	grep -e '^\#' data/raw/AT20G.tsv > data/final/AT20G_header.txt
> > 
> > data/processing/AT20G_table.tsv: data/raw/AT20G.tsv
> > 	grep -v -e '^\#' -e '^-' -e '^deg' -e '^$$' data/raw/AT20G.tsv > data/processing/AT20G_table.tsv
> > 
> > data/final/AT20G_final.csv: data/processing/AT20G_table.tsv src/clean_tables.py
> > 	python src/clean_tables.py -s AT20G -i data/processing/AT20G_table.tsv -o data/final/AT20G_final.csv
> > 
> > 
> > # NVSS survey
> > data/raw/NVSS.tsv:
> > 	wget -O data/raw/NVSS.tsv https://github.com/ADACS-Australia/2025-ASA-ECR-WorkshopSeries/raw/refs/heads/gh-pages/data/Workshop2/NVSS.tsv
> > 
> > data/final/NVSS_header.txt: data/raw/NVSS.tsv
> > 	grep -e '^\#' data/raw/NVSS.tsv > data/final/NVSS_header.txt
> > 
> > data/processing/NVSS_table.tsv: data/raw/NVSS.tsv
> > 	grep -v -e '^\#' -e '^-' -e '^deg' -e '^$$' data/raw/NVSS.tsv > data/processing/NVSS_table.tsv
> > 
> > data/final/NVSS_final.csv: data/processing/NVSS_table.tsv src/clean_tables.py
> > 	python src/clean_tables.py -s NVSS -i data/processing/NVSS_table.tsv -o data/final/NVSS_final.csv
> >
> > clean:
> >     rm data/*/AT20G*
> >     rm data/*/NVSS*
> > ```
> > 
> > In the above we have used `.PHONY` to tell `make` explicitly that the named targets are not files. 
> > It's not required but helps avoid confusion if you actually have a file in your directory with this name.
> > 
> {: .solution}
> 
{: .challenge}

Last week we created the workflow for AT20G from scratch and it took essentialy the whole lesson to do.
This week, however, we are building our knowledge and success from last week to make a workflow for NVSS in much less time.
If we now make a workflow that includes another survey (SUMSS), it should take even less time because:
- We can just think about what is different between SUMSS and NVSS or AT20G rather than working from scratch
- We have already set up our `clean_tables.py` script to be adaptable for different surveys
- Our `makefile` already has different sections for different surveys

We can of course test this hypothesis by completing all this workf ro the SUMSS survey.

> ## Incorporate the SUMSS survey into our workflow
> The data are here: [SUMSS.tsv](https://github.com/ADACS-Australia/2025-ASA-ECR-WorkshopSeries/raw/refs/heads/gh-pages/data/Workshop2/SUMSS.tsv)
>
> - Download the data
> - Decide what pre-processing needs to be done
> - Update the `makefile` to include a target called SUMSS, and to include SUMSS data in the clean target
> - Update `clean_tables.py` to accept SUMSS as a table option, and then perform the relevant cleaning operations
>
> > ## `the_workflow_final_v2_with_summs`
> > Using `...` to refer to unchanged previous content.
> > ```python
> > 
> > ...
> > 
> > def clean_SUMSS(infile, outfile):
> >     # Use all our helper functions to clean the SUMSS table
> >     table = load(infile, '\t')
> >     table = filter_rows(table, colname='_RAJ2000', min_value=12 * 15, max_value=18 * 15)
> >     table = keep_columns(table, colnames=['_Glon', '_Glat', '_DEJ2000', 'RAJ2000', 'DEJ2000', 'Sp', 'e_Sp'])
> >     save(table, outfile)
> >     # return the table incase we want to do something else with it
> >     return table
> > 
> > if __name__ == '__main__':
> >     
> >     ...
> > 
> >     if args.survey.upper() == "AT20G":
> >         clean_AT20G(args.input_file, args.output_file)
> >     elif args.survey.upper() == "NVSS":
> >         clean_NVSS(args.input_file, args.output_file)
> >     elif args.survey.upper() == "SUMSS":
> >         clean_SUMSS(args.input_file, args.output_file)
> >     else:
> >         print(f"Unknown survey: {args.survey}. Please choose from AT20G, NVSS, or SUMSS.")
> > 
> > ```
> > ```makefile
> > .PHONY: AT20G NVSS SUMSS all clean
> > 
> > SUMSS: data/final/SUMSS_final.csv data/final/SUMSS_header.txt
> > 
> > all: AT20G NVSS SUMSS
> > 
> > # ...
> > 
> > # SUMSS survey
> > data/raw/SUMSS.tsv:
> > 	wget -O data/raw/SUMSS.tsv https://github.com/ADACS-Australia/2025-ASA-ECR-WorkshopSeries/raw/refs/heads/gh-pages/data/Workshop2/SUMSS.tsv
> > 
> > data/final/SUMSS_header.txt: data/raw/SUMSS.tsv
> > 	grep -e '^\#' data/raw/SUMSS.tsv > data/final/SUMSS_header.txt
> > 
> > data/processing/SUMSS_table.tsv: data/raw/SUMSS.tsv
> > 	grep -v -e '^\#' -e '^-' -e '^deg' -e '^$$' data/raw/SUMSS.tsv > data/processing/SUMSS_table.tsv
> > 
> > data/final/SUMSS_final.csv: data/processing/SUMSS_table.tsv src/clean_tables.py
> > 	python src/clean_tables.py -s SUMSS -i data/processing/SUMSS_table.tsv -o data/final/SUMSS_final.csv
> > 
> > clean:
> > 	rm data/*/AT20G*
> > 	rm data/*/NVSS*
> > 	rm data/*/SUMSS*
> > ```
> {: .solution}
> 
{: .challenge}

Unless we fell into some crazy debuging holes, that should have taken a fraction of the time that the NVSS additions did.


## Documentation & Reproducibility
So far we have mainly focused on the automation and scripting side of making our work reproducible.
However, if you don't know what the wokflow is supposed to do or how it's supposed to work you wont know when it's appropriate to use or how you might go about adapting it for different uses in the future.
Thus it's important that you document not just what the workflow is doing but why.

Imagine a situation where you have run your workflow and it has produced some data that you are going to use for your thesis or a publication.
At some point you want to know what was done to your data.
In the case that you have flexibility and options in your workflow, you'll want to know what options were set for the particular data set that you are looking at (ideally without having to ramake it!).
Thus it would be nice if your workflow could be somehow self-documenting in describing how a given data set has been produced.

However you look at it, documentation is going to be a powerful tool in reproducibility and your ability to build on your previous work.

### ~~Best~~ Good Enough Practices for Documentation & Reproducibility

1. **Documentation**:
    - Document every step of your workflow, including data sources, preprocessing steps, analysis methods, and software used.
    - Use clear and consistent naming conventions for files and variables.
    - Keep the documentation updated as you change your workflow.

2. **Version Control**:
    - Use version control systems like Git to track changes in your code and documents.
    - Tag versions of your project that correspond to specific results or publications. (See [HOWTO: Leverage GitHub for Research]({{page.root}}{% link _episodes/Workshop4.md %}) for more on this).

3. **Configuration Files**:
    - Use configuration files (e.g., YAML, JSON) to store parameters and settings. This makes it easier to reproduce the environment and rerun analyses with different settings.
    - Example of a YAML configuration file:

      ```yaml
      data_source: "https://github.com/ADACS-Australia/2025-ASA-ECR-WorkshopSeries/raw/refs/heads/gh-pages/data/Workshop2/SUMSS.tsv"
      preprocessing:
         - step: "split_header"
         - step: "clean"
      analysis:
         - method: "crossmatch"
            parameters:
              distance: 0.05
      ```

4. **Metadata**:
    - Include metadata in your datasets and results to provide context. Metadata should describe the data, its source, the methods used to generate it, and any relevant parameters.
    - Example of metadata in a CSV file:
      ```csv
      # Dataset: Example Data
      # Source: https://example.com/data.csv
      # Description: This dataset contains example data for demonstration purposes.
      # Generated on: 2023-10-01
      # Generated by: my-workflow @<githash>
      ```

5. **Environment Management**:
    - Use tools like `venv`, `conda`, or Docker to create isolated environments that encapsulate all dependencies.
    - Provide environment specifications (e.g., `requirements.txt`, `environment.yml`, `Dockerfile`) to ensure others can recreate the same environment.

6. **Automated Workflows**:
    - Automate repetitive tasks using scripts or workflow management tools like Make or Nextflow.
    - Ensure that your scripts are well-documented and include comments explaining each step.
    - See the [previous workshop](../Workshop1.md) in this series for more about automating workflows.

7. **Regular Updates**:
    - Regularly update your documentation to reflect any changes in your workflow or methodologies.
    - Encourage team members to contribute to and review the documentation.


We have explore items 4,5,6 in our previous workshop, and item 3 has already been enabeled due to our use of `configargparse` earlier in this workshop.
Version control is an entire topic in and of itself (see [Git-Novice](https://swcarpentry.github.io/git-novice/) from [The Carpentries](https://carpentries.org/)), but will touch on in our [HOWTO: Leverage GitHub for Research]({{page.root}}{% link _episodes/Workshop4.md %}) workshop.
That leaves us with items 1 and 7 - writing and maintaining workflow documentation.


## Writing and Maintaining Workflow Documentation


### 1. **Self-Documenting Workflows**
- Workflows that automatically generate documentation about how they were executed.
- **How to implement?**
    - Use configuration files to store parameters and options.
    - Log the execution details (e.g., input/output files, parameters, timestamps) to a text or markdown file.
    - Example:

        ```python
        import logging
        from datetime import datetime

        __version__ = 'v1.2.3'

        def setup_logger(log_file="my_script.log"):
            logging.basicConfig(
            filename=log_file,
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
            )

        def log_workflow(config):
            logging.info("Program <my_script> started")
            logging.info(f"Parameters: {config}")
            logging.info(f"Software version: {__version__}")

        # Example usage
        if __name__ == "__main__":
            setup_logger()
            config = {"input_file": "data.csv", "output_file": "results.csv"}
            log_workflow(config)
            ... # do things
            logging.info("Program <my_script> completed")
        ```

### 2. **Capturing Software Versions**
- Use tools like `pip freeze` to capture the versions of all dependencies.
- This can be important eve if you have a `requirements.txt` file, as it shows what versions of code were **used** rather than which versions were **required**.
- Example:
    ```bash
    pip freeze > requirements_versions.txt
    ```

### 3. **Generating Metadata**
- Include metadata in your output files to describe how they were generated.
- Example of metadata in a CSV file:
    ```csv
    # Generated by: clean_tables.py
    # Parameters: input_file=AT20G_table.tsv, output_file=AT20G_final.csv
    # Software version: v1.2.3
    ```

### 4. **Automating Documentation Updates**
- Use scripts to append or update documentation files with new information after each workflow run.
- Example:
    ```bash
    echo "Workflow run on $(date)" >> documentation.md
    echo "Input file: $INPUT_FILE" >> documentation.md
    echo "Output file: $OUTPUT_FILE" >> documentation.md
    ```

### 5. **Using Markdown for Documentation**
- Markdown is lightweight and easy to read.
- Example structure for workflow documentation:
    ```markdown
    # Workflow Documentation

    ## Overview
    This workflow processes astronomical data to clean and filter it.

    ## Parameters
    - Input file: `AT20G_table.tsv`
    - Output file: `AT20G_final.csv`
    - RA range: 12h to 18h

    ## Software
    - Python: 3.10
    - Pandas: 2.2.3
    - NumPy: 2.2.4

    ## Execution Log
    - Run on: 2023-10-01
    - Command: `python clean_tables.py -i AT20G_table.tsv -o AT20G_final.csv`
    ```

### 6. **Version Control Integration**
- Use Git to track changes in your workflow and documentation.
- Include the Git commit hash in your logs for traceability.
- Example:
    ```bash
    git rev-parse HEAD >> workflow_log.txt
    ```

### Hands-On Exercise
1. **Create a Self-Documenting Workflow**:
    - Modify an existing script to log parameters, options, and software versions to a file.
2. **Generate Metadata**:
    - Add metadata to an output file describing how it was produced.
3. **Automate Documentation Updates**:
    - Write a script to append execution details to a markdown file.

> ## Modify `clean_tables.py` to add some metadata to the output table.
>
> Use the following updated save function to add some metadata to the output table.
> ```python
> def save(table, filename, metadata=None):
>     """
>     Save the DataFrame to a CSV file with metadata in the header.
>     """
>     with open(filename, 'w') as f:
>         if metadata:
>             # Write metadata as comments
>             for key, value in metadata.items():
>                 f.write(f"# {key}: {value}\n")
>         # Write the DataFrame to the file
>         table.to_csv(f, index=False)
> ```
>
> You'll need to collect the relevant meta data into a dictionary and hand it to this function when you save the file.
>
> > ## Example solution
> > ```python
> > ...
> > from datetime import datetime
> > ...
> > 
> > __version__ = 'v1.2.3'
> > 
> > ...
> > if __name__ == '__main__':
> >     ...
> > 
> >     # Metadata to include in the header
> >     metadata = {
> >         "Generated by": "clean_tables.py",
> >         "Parameters": vars(args),
> >         "Software version": __version__,
> >         "Dependencies": f"Pandas v{pd.__version__}, Numpy v{np.__version__}",
> >         "Filters": "12*15 < _RAJ2000 < 18*15, S8>0, S5>0",
> >         "Generated on": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
> >     }
> >     save(table, args.output_file, metadata)
> > ```
> {: .solution}
{: .challenge}



## Session 2 topics

### Strategies for Better Documentation

Effective documentation is crucial for ensuring that your research is understandable, reproducible, and extensible by others. One key strategy is to adopt a modular approach to documentation. Break down your documentation into distinct sections, such as an overview, installation instructions, usage examples, and API references. This structure helps users quickly find the information they need without wading through irrelevant details. Additionally, using tools like Jupyter Notebooks can combine code, results, and narrative text in a single document, making it easier to follow complex workflows.

Another important strategy is to maintain consistency in your documentation. Use a consistent style and format throughout your documents, and establish clear guidelines for naming conventions, code comments, and file organization. This consistency not only makes your documentation more professional but also reduces the cognitive load on users trying to understand your work. Regularly review and update your documentation to reflect any changes in your workflow or methodologies, and encourage contributions from team members to keep the documentation comprehensive and up-to-date. By prioritizing clarity and consistency, you can create documentation that is both user-friendly and robust.

