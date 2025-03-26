---
title: "Automating the Astronomy Workflow"
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

| Time (AEST)  | Focus                     | Details                                                                 |
|--------------|-----------------------------|-------------------------------------------------------------------------|
| 2:00 - 2:10 PM | Overview                    | Why automate? Benefits of workflow management.                           |
| 2:10 - 2:30 PM | Data Acquisition & Workflow Design | Downloading data from remote sources, workflow design.                   |
| 2:30 - 2:50 PM | Reproducible Environments   | Using venv, conda, containers; logging and checkpointing.                |
| 2:50 - 2:55 PM | Break                      |                                                                         |
| 2:55 - 3:15 PM | Workflow Tools in Action    | Introduction to Make, Nextflow; hands-on scripting.                      |
| 3:15 - 3:30 PM | Discussion & Problem Solving| Recap and address challenges in automation.                              |


## Overview
### Why automate?
Automation helps streamline repetitive tasks, reduce errors, and save time, allowing astronomers to focus on analysis and discovery.
### Common repetitive tasks in astronomy research:
  Researchers often face a variety of repetitive tasks that can benefit from automation, including:
  - **Data retrieval:** Regularly downloading large datasets from remote servers or online repositories.
  - **Data preprocessing:** Cleaning, filtering, and formatting raw data to prepare it for analysis.
  - **Data analysis:** Running the same analysis scripts on multiple datasets or subsets of data.
  - **Report generation:** Creating standardized reports or visualizations from analysis results.
  - **Environment setup:** Configuring computational environments with specific software dependencies for different projects.

### How automation can help:
  - **Efficiency:** Automating repetitive tasks can save significant time and effort, allowing researchers to focus on more complex and creative aspects of their work.
  - **Consistency:** Automated workflows ensure that tasks are performed the same way every time, reducing the risk of human error and increasing the reliability of results.
  - **Reproducibility:** By automating the setup of computational environments and the execution of analysis scripts, researchers can easily reproduce their work and share it with others.
  - **Scalability:** Automation makes it easier to scale up analyses to larger datasets or more complex workflows without a proportional increase in manual effort.
  - **Documentation:** Automated workflows often include built-in documentation and logging, making it easier to track what was done and troubleshoot any issues that arise.

### Tools and techniques for automation:
  - **Scripting languages:** Use languages like Python or Bash to write scripts that automate repetitive tasks.
  - **Workflow management tools:** Tools like Make, Nextflow, and Snakemake can help manage complex workflows with multiple dependencies and parallel tasks.
  - **Version control:** Use Git to track changes to scripts and workflows, ensuring that you can revert to previous versions if needed.
  - **Continuous integration:** Set up continuous integration (CI) pipelines to automatically run tests and analyses whenever changes are made to your code or data.

By incorporating these automation techniques into their research workflows, astronomers can improve the efficiency, consistency, and reproducibility of their work, ultimately leading to more reliable and impactful scientific discoveries.

### Benefits of workflow management:
  Effective workflow management ensures consistency, reproducibility, and efficiency in handling large datasets and complex processes.



## Data Acquisition & Workflow Design

### Downloading data from remote sources

Learn how to use tools like `wget`, `curl`, and APIs to fetch astronomical data from various online repositories.

#### Example 1: Downloading Data with `wget`
```bash
# Download a single file
wget http://example.com/data/file1.fits

# Download multiple files listed in a text file
wget -i file_list.txt
```

#### Example 2: Fetching Data with `curl`
```bash
# Download a single file
curl -O http://example.com/data/file1.fits

# Download multiple files using a loop
for url in $(cat file_list.txt); do
  curl -O $url
done
```

#### Example 3: Using APIs for Data Retrieval**
```python
import requests

# Define the API endpoint and parameters
url = "http://example.com/api/data"
params = {"query": "search_term"}

# Send a GET request to the API
response = requests.get(url, params=params)

# Save the response content to a file
with open("data.json", "w") as file:
    file.write(response.text)
```

#### Lesson: Automating Data Preprocessing with Python
```python
import pandas as pd

# Load raw data
raw_data = pd.read_csv("raw_data.csv")

# Clean and preprocess data
clean_data = raw_data.dropna().reset_index(drop=True)

# Save the cleaned data
clean_data.to_csv("clean_data.csv", index=False)
```

### Workflow design principles
Understand the basics of designing a robust workflow, including task dependencies, parallel processing, and error handling.

#### Task dependencies
When designing a workflow, it's important to identify and define the dependencies between tasks. This ensures that tasks are executed in the correct order and that each task has the necessary inputs available before it starts. For example, data preprocessing should occur before data analysis, as the analysis depends on the cleaned data.

Exercise: Draw a dependency graph for a workflow.

#### Parallel processing
To improve efficiency, consider which tasks can be executed in parallel. Parallel processing allows multiple tasks to run simultaneously, reducing the overall time required to complete the workflow. Tools like Nextflow and Snakemake can help manage parallel execution and resource allocation.

Exercise: Identify tasks that can be run simultaneously without interfering with each other.

#### Logging
Logging is a crucial aspect of any workflow for several reasons:

1. Debugging: Logs provide detailed information about the application's execution, which helps developers identify and fix bugs more efficiently.
2. Monitoring: Logs allow you to monitor the application's behavior in real-time, ensuring that it is running as expected and helping to detect any anomalies or issues early.
3. Auditing: Logs can serve as an audit trail, recording important events and actions taken by users or the system. This is particularly useful if you want to know how your program ran, and what inputs were used, without having to run it again.
4. Performance Analysis: By analyzing logs, you can identify performance bottlenecks and optimize the application's performance.

#### Example: Logging with Python's `logging` Module
```python
import logging

# Configure logging
logging.basicConfig(filename='workflow.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def log_example():
  logging.info("This is an info message")
  logging.warning("This is a warning message")
  logging.error("This is an error message")

# Example usage
log_example()
```
This example demonstrates how to configure and use Python's built-in `logging` module to log messages to a file.

#### Example: Checkpointing with Python
```python
import os
import pickle

# Function to save a checkpoint
def save_checkpoint(data, filename='checkpoint.pkl'):
  with open(filename, 'wb') as f:
    pickle.dump(data, f)

# Function to load a checkpoint
def load_checkpoint(filename='checkpoint.pkl'):
  if os.path.exists(filename):
    with open(filename, 'rb') as f:
      return pickle.load(f)
  return None

# Example usage
data = {'step': 1, 'result': 'intermediate data'}
save_checkpoint(data)

# Later in the workflow
checkpoint_data = load_checkpoint()
if checkpoint_data:
  print(f"Resuming from step {checkpoint_data['step']} with data: {checkpoint_data['result']}")
```
This example shows how to use Python's `pickle` module to save and load checkpoints, allowing workflows to resume from intermediate states.


#### Error handling
Incorporate error handling mechanisms to manage and recover from failures. This can include retrying failed tasks, logging errors for later analysis, and implementing checkpointing to save intermediate results. Effective error handling ensures that the workflow can continue or be easily restarted in case of issues.

#### Example: Running a Program with `os.popen` in Python
```python
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def run_command(command):
  process = os.popen(command)
  output = process.read()
  return_code = process.close()

  if return_code is None:
    return_code = 0

  if return_code == 0:
    logger.info(f"Command succeeded: {command}")
    logger.info(f"Output: {output}")
  else:
    logger.error(f"Command failed with return code {return_code}: {command}")
    logger.error(f"Output: {output}")

  return output, return_code

# Example usage
command = "ls -l"
output, return_code = run_command(command)
```
This example demonstrates how to use `os.popen` to run a command, capture its output, and log the results.

Also show example from MGlowacki project.

Reiterate the importance of workflows failing gracefully - in a way where you know where they failed and why.

#### Example: Workflow Design with Make
```makefile
# Makefile example for a simple workflow

# Define the final target
all: results/clean_data.csv

# Rule to preprocess raw data
results/clean_data.csv: data/raw_data.csv
  python scripts/preprocess.py data/raw_data.csv results/clean_data.csv

# Clean up generated files
clean:
  rm -f results/clean_data.csv
```

By following these principles, you can create robust and efficient workflows that are easier to maintain and scale.

Make is good for simple workflows, but doesn't have any way of telling you when things break, and can also be a write-only language.
Something like a python script that checks the before/after state between each workflow step can be easier to manage (though doesn't "save state").

A nextflow workflow gives a nice balance between the simplicity of Make and the adaptability of Python.

## Reproducible Environments

### Project structure
Structuring your files and directories properly is crucial for maintaining a clean, organized, and manageable Python project. A well-structured project makes it easier to navigate, understand, and collaborate with others. Here are some key points to consider:

1. **Root Directory**: The root directory should contain essential files like `README.md`, `setup.py`, and a license file. These files provide important information about the project, installation instructions, and licensing details.

2. **Source Code Directory**: Create a dedicated directory (e.g., `src` or the project name) for your source code. This directory should contain all the Python modules and packages related to your project.

3. **Tests Directory**: Include a separate directory (e.g., `tests`) for your test cases. Organizing tests in a dedicated directory helps ensure that they are easily accessible and maintainable.

4. **Configuration Files**: Store configuration files (e.g., `config.yaml`, `.env`) in a dedicated directory (e.g., `config`). This keeps configuration settings separate from the source code and makes it easier to manage different environments.

5. **Data Directory**: If your project involves data processing, create a directory (e.g., `data`) to store raw and processed data files. This helps keep data organized and prevents cluttering the source code directory.

6. **Documentation Directory**: Maintain a directory (e.g., `docs`) for project documentation. This can include user guides, API references, and other relevant documentation.

7. **Virtual Environment**: Use a virtual environment to manage dependencies. Create a directory (e.g., `venv`) for the virtual environment to ensure that dependencies are isolated and do not interfere with other projects.

Example project structure:
```
my_project/
├── config/
│   └── config.yaml
├── data/
│   ├── raw/
│   └── processed/
├── docs/
│   └── index.md
├── src/
│   ├── __init__.py
│   └── main.py
├── tests/
│   ├── __init__.py
│   └── test_main.py
├── venv/
├── .gitignore
├── README.md
├── requirements.txt
└── setup.py
```

By following these guidelines, you can create a well-organized project structure that enhances readability, maintainability, and collaboration.


### Python environments
Python environments are useful because they allow you to create isolated spaces for your projects, ensuring that dependencies and packages do not conflict with each other. This is particularly important when working on multiple projects that require different versions of the same package or library. By using environments, you can maintain consistency and reproducibility in your workflows.

#### Setting up a Conda environment
Conda is a popular package and environment management system that allows you to create and manage isolated environments.

1. **Install Conda**: If you don't have Conda installed, you can download and install it from the [Anaconda](https://www.anaconda.com/products/distribution) website or use [Miniconda](https://docs.conda.io/en/latest/miniconda.html) for a minimal installation.

2. **Create a new environment**:
  ```bash
  conda create --name myenv python=3.10
  ```

3. **Activate the environment**:
  ```bash
  conda activate myenv
  ```

4. **Install packages**:
  ```bash
  conda install numpy pandas
  ```

5. **Deactivate the environment**:
  ```bash
  conda deactivate
  ```

#### Setting up a virtual environment with `venv`
The `venv` module is included in Python's standard library and allows you to create lightweight virtual environments.

1. **Create a new environment**:
  ```bash
  python -m venv myenv
  ```

2. **Activate the environment**:
  - On Windows:
    ```bash
    myenv\Scripts\activate
    ```
  - On macOS and Linux:
    ```bash
    source myenv/bin/activate
    ```

3. **Install packages**:
  ```bash
  pip install numpy pandas
  ```

4. **Deactivate the environment**:
  ```bash
  deactivate
  ```

By using Conda or `venv`, you can ensure that your projects have the necessary dependencies without interfering with each other, leading to more reliable and reproducible research workflows.

### Containers

Docker containers are useful for preserving a software environment because they encapsulate all the dependencies, libraries, and configurations needed to run an application. This ensures that the application runs consistently across different environments, from development to production. Containers are lightweight, portable, and can be easily shared, making them ideal for reproducible research and collaborative projects.

#### Example: Dockerfile for a Python Program

```dockerfile
# Use the official Python image from the Docker Hub
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install the required Python packages
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Specify the command to run the application
CMD ["python", "main.py"]
```

In this example:
- `FROM python:3.10-slim` specifies the base image with Python 3.10.
- `WORKDIR /app` sets the working directory inside the container.
- `COPY requirements.txt .` copies the `requirements.txt` file into the container.
- `RUN pip install --no-cache-dir -r requirements.txt` installs the required Python packages.
- `COPY . .` copies the rest of the application code into the container.
- `CMD ["python", "main.py"]` specifies the command to run the Python program.

By using Docker, you can ensure that your Python program runs in a consistent environment, regardless of where it is deployed.


## Workflow Tools in Action
### Introduction to Make and Nextflow

### Make
Make is a build automation tool that helps manage and execute workflows by defining a series of tasks and their dependencies. It is particularly useful for scientific research because:

- **Simplicity:** Makefiles are straightforward to write and understand, making it easy to define workflows.
- **Dependency Management:** Make ensures that tasks are executed in the correct order based on their dependencies, which is crucial for reproducible research.
- **Efficiency:** Make only re-executes tasks that have changed, saving time and computational resources.
- **Portability:** Makefiles can be shared and executed on different systems, ensuring consistency across environments.

### Creating a Simple Workflow with Make**
```makefile
# Define targets and dependencies
all: clean_data.csv

clean_data.csv: raw_data.csv
    python preprocess.py raw_data.csv clean_data.csv

# Define a clean target to remove generated files
clean:
    rm -f clean_data.csv
```

### Nextflow
Nextflow is a workflow management system designed for scalable and reproducible scientific workflows. It offers several advantages for researchers:

- **Scalability:** Nextflow can handle complex workflows with many tasks and dependencies, and it supports parallel execution to speed up processing.
- **Reproducibility:** Nextflow workflows are defined in a domain-specific language that captures the entire workflow, making it easy to reproduce results.
- **Portability:** Nextflow can run on various computing environments, including local machines, clusters, and cloud platforms, ensuring that workflows are portable and adaptable.
- **Error Handling:** Nextflow provides robust error handling and checkpointing, allowing workflows to resume from intermediate states in case of failures.
- **Community Support:** Nextflow has a large and active user community, providing a wealth of resources, tutorials, and support for researchers.

By using tools like Make and Nextflow, scientists can create efficient, reproducible, and scalable workflows, ultimately enhancing the reliability and impact of their research.


### EXample: Using Nextflow for Workflow Management**
```groovy
# Define a simple Nextflow workflow
process preprocess {
    input:
    path raw_data

    output:
    path "clean_data.csv"

    script:
    """
    python preprocess.py $raw_data clean_data.csv
    """
}

workflow {
    raw_data = file("raw_data.csv")
    preprocess(raw_data)
}
```


### Pros and Cons of Using Make vs Nextflow for Workflow Management

#### Make
**Pros:**
- **Simplicity:** Easy to write and understand Makefiles for simple workflows.
- **Dependency Management:** Automatically handles task dependencies, ensuring correct execution order.
- **Efficiency:** Only re-executes tasks that have changed, saving time and resources.
- **Portability:** Makefiles can be shared and executed on different systems.

**Cons:**
- **Limited Scalability:** Not well-suited for complex workflows with many tasks and dependencies.
- **Error Handling:** Lacks robust error handling and checkpointing features.
- **Parallel Execution:** Limited support for parallel task execution.
- **Verbose Syntax:** Can become cumbersome and difficult to manage for larger workflows.

#### Nextflow
**Pros:**
- **Scalability:** Handles complex workflows with many tasks and dependencies, supporting parallel execution.
- **Reproducibility:** Captures the entire workflow in a domain-specific language, ensuring reproducibility.
- **Portability:** Runs on various computing environments, including local machines, clusters, and cloud platforms.
- **Error Handling:** Provides robust error handling and checkpointing, allowing workflows to resume from intermediate states.
- **Community Support:** Large and active user community with extensive resources and support.

**Cons:**
- **Learning Curve:** Steeper learning curve compared to Make, especially for users unfamiliar with the domain-specific language.
- **Overhead:** May introduce additional overhead for simple workflows that do not require advanced features.
- **Complexity:** Can be more complex to set up and manage compared to Make for straightforward tasks.


## Discussion & Problem Solving
- **Recap of key points:**  
  Summarize the main takeaways from the workshop.
- **Address challenges in automation:**  
  Discuss common challenges and potential solutions in automating astronomy workflows.
- **Open floor for questions and problem-solving:**  
  Provide an opportunity for participants to ask questions and seek advice on specific issues they are facing.

