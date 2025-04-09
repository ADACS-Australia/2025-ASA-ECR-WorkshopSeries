---
title: "How to Build on Past Success"
teaching: 45
exercises: 45
questions:
- "How can automation improve my current workflow?"
- "What tools and software will we be using?"
- "How do I troubleshoot common issues in workflow automation?"
- "What are the best practices for maintaining reproducible environments?"
objectives:
- "Learn to streamline the routine tasks in your research - from downloading remote data to managing reproducible computational environments—so you can focus on discovery."
keypoints:
- "Automation can significantly streamline repetitive tasks and reduce errors."
- "Effective workflow management ensures consistency and reproducibility."
- "Tools like `wget`, `curl`, `venv`, `conda`, Docker, Make, and Nextflow are very helpful for automating and managing workflows."
- "Creating isolated and reproducible environments is crucial for reliable research."
- "Logging and checkpointing are important for tracking progress and recovering from failures."
---

## Workshop outline:

| Time (AEST) | Focus | Details |
| -- | -- | -- |
| 2:00 - 2:10 PM | Overview | The importance of repeatability and documentation. | 
| 2:10 - 2:25 PM | Documentation & Reproducibility | Best practices, configuration files. | 
| 2:25 - 2:45 PM | Automation & Workflow Repeatability | Using scripting and automation for consistency. | 
| 2:45 - 2:50 PM | Break | 
| 2:50 - 3:15 PM | Sharing & Building on Your Workflow | Publishing and designing workflows for reuse. | 
| 3:15 - 3:30 PM | Discussion & Problem Solving | Strategies for better documentation. | 

## Overview

The importance of repeatability and documentation.

Proper documentation is essential for making research repeatable. It ensures that all steps of the research process are clearly recorded, allowing others to understand and replicate the work. This transparency not only facilitates validation and verification of results but also enables other researchers to build upon the existing work. Comprehensive documentation includes detailed descriptions of methodologies, data sources, software used, and any specific configurations or parameters. By maintaining thorough documentation, researchers can avoid ambiguities and ensure that their work remains accessible and reproducible over time.

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

## Automation & Workflow Repeatability

Using scripting and automation for consistency.
### Parameterizing Workflows and Scripts

To make your workflows and scripts more flexible and reusable, you can design them to accept parameters or configuration files. This approach allows you to adjust the behavior of your scripts without modifying the source code directly. Here are some strategies to achieve this:

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

3. **Environment Variables**:
    - Use environment variables to pass configuration settings to your scripts. This is particularly useful for sensitive information like API keys.
    - Example in Python:
      ```python
      import os

      def main():
          data_source = os.getenv("DATA_SOURCE")
          output_dir = os.getenv("OUTPUT_DIR")
          # Your workflow logic here
          print(f"Processing data from {data_source} and saving results to {output_dir}")

      if __name__ == "__main__":
          main()
      ```

By parameterizing your workflows and scripts, you can easily adapt them to different scenarios and datasets without modifying the underlying code. This enhances the flexibility, maintainability, and reusability of your research workflows.

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

