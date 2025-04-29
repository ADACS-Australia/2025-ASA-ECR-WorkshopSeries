---
title: "How to Build on Past Success"
teaching: 45
exercises: 45
questions:
- "Why should I spend time making my work reusable?"
objectives:
- 
keypoints:
- 
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


TODO: Link / show final versions of our workflows that we might build upon them.

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
2. Letting the user specify the delimiter, but having commas as default.
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

## Documentation & Reproducibility

Best practices, configuration files.
### Best Practices for Documentation & Reproducibility

1. **Comprehensive Documentation**:
    - Document every step of your workflow, including data sources, preprocessing steps, analysis methods, and software used.
    - Use clear and consistent naming conventions for files and variables.

2. **Version Control**:
    - Use version control systems like Git to track changes in your code and documents.
    - Tag versions of your project that correspond to specific results or publications.

3. **Configuration Files**:
    - Use configuration files (e.g., YAML, JSON) to store parameters and settings. This makes it easier to reproduce the environment and rerun analyses with different settings.
    - Example of a YAML configuration file:
      ```yaml
      data_source: "https://example.com/data.csv"
      preprocessing:
         - step: "normalize"
            method: "min-max"
      analysis:
         - method: "regression"
            parameters:
              alpha: 0.05
      ```

4. **Metadata**:
    - Include metadata in your datasets and results to provide context. Metadata should describe the data, its source, the methods used to generate it, and any relevant parameters.
    - Example of metadata in a CSV file:
      ```csv
      # Dataset: Example Data
      # Source: https://example.com/data.csv
      # Description: This dataset contains example data for demonstration purposes.
      # Generated on: 2023-10-01
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

By following these best practices, you can enhance the reproducibility and transparency of your research, making it easier for others to understand, replicate, and build upon your work.

#

## Sharing & Building on Your Workflow

Publishing and designing workflows for reuse.

### Publishing to PyPI and Uploading to Zenodo

#### Publishing to PyPI

To share your Python project with the community, you can publish it to the Python Package Index (PyPI). Here are the steps to do so:

1. **Prepare Your Project**:
    - Ensure your project has the necessary files, including `pyproject.toml`, `README.md`, and a license file.
     - Example `pyproject.toml`:
        ```toml
        [build-system]
        requires = ["setuptools>=42", "wheel"]
        build-backend = "setuptools.build_meta"

        [project]
        name = "your_project_name"
        version = "0.1.0"
        description = "A brief description of your project"
        readme = "README.md"
        requires-python = ">=3.10"
        license = {text = "MIT"}
        authors = [
          {name = "Your Name", email = "your.email@example.com"}
        ]
        classifiers = [
          "Programming Language :: Python :: 3",
          "License :: OSI Approved :: MIT License",
          "Operating System :: OS Independent"
        ]
        dependencies = []

        [project.urls]
        "Homepage" = "https://github.com/yourusername/your_project"
        ```

2. **Build Your Package**:
    - Use `build` to create your package:
      ```sh
      pip install build
      python -m build
      ```

3. **Upload to PyPI**:
    - Use `uv` to upload your package to PyPI:
      ```sh
      pip install uv
      uv pypi publish dist/*
      ```

#### Uploading to Zenodo

Zenodo is a research data repository that allows you to share datasets, software, and other research outputs. Here's how to upload your project to Zenodo:

1. **Create a Zenodo Account**:
    - Sign up for an account at [Zenodo](https://zenodo.org/).

2. **Upload Your Project**:
    - Go to the "Upload" page and fill in the required metadata fields, such as title, author(s), description, and keywords.
    - Upload your project files (e.g., source code, documentation, datasets).

3. **Assign a DOI**:
    - Zenodo will automatically assign a Digital Object Identifier (DOI) to your upload, making it citable.

#### Required Metadata

When publishing to PyPI and Zenodo, it's important to include comprehensive metadata to ensure your project is discoverable and properly attributed. Key metadata fields include:

- **Title**: A clear and descriptive title of your project.
- **Author(s)**: Names and contact information of the contributors.
- **Description**: A detailed description of your project, including its purpose and key features.
- **Keywords**: Relevant keywords to help others find your project.
- **License**: The license under which your project is released.
- **Version**: The version number of your project.

#### Associating a DOI with a Version

To associate a DOI with a specific version of your work, follow these steps:

1. **Versioning**:
    - Use semantic versioning (e.g., 1.0.0) to clearly identify different versions of your project.

2. **Zenodo Integration**:
    - If your project is hosted on GitHub, you can enable Zenodo integration to automatically generate a DOI for each release. Go to the Zenodo GitHub page and enable the repository you want to link.

3. **Release on GitHub**:
    - Create a new release on GitHub, which will trigger Zenodo to archive the release and assign a DOI.

By following these steps, you can effectively share your project with the community, ensuring it is properly documented, discoverable, and citable.

## Discussion & Problem Solving

### Strategies for Better Documentation

Effective documentation is crucial for ensuring that your research is understandable, reproducible, and extensible by others. One key strategy is to adopt a modular approach to documentation. Break down your documentation into distinct sections, such as an overview, installation instructions, usage examples, and API references. This structure helps users quickly find the information they need without wading through irrelevant details. Additionally, using tools like Jupyter Notebooks can combine code, results, and narrative text in a single document, making it easier to follow complex workflows.

Another important strategy is to maintain consistency in your documentation. Use a consistent style and format throughout your documents, and establish clear guidelines for naming conventions, code comments, and file organization. This consistency not only makes your documentation more professional but also reduces the cognitive load on users trying to understand your work. Regularly review and update your documentation to reflect any changes in your workflow or methodologies, and encourage contributions from team members to keep the documentation comprehensive and up-to-date. By prioritizing clarity and consistency, you can create documentation that is both user-friendly and robust.

