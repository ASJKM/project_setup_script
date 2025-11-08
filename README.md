# setup_cookiecutter_project.py

## Overview

`setup_cookiecutter_project.py` is a **cross-platform Python automation script** that helps you set up new GitHub projects quickly and consistently using a **Cookiecutter template**.  
It automatically detects your operating system, installs required tools, generates a new project from a specified Cookiecutter repository, and optionally pushes the result to a new GitHub repository.

---

## Features

- Detects whether the script is running on **Windows** or **Linux**
- Checks for required tools (`git`, `cookiecutter`) and installs them if missing
- Prompts the user for:
  - The **target directory** where the project should be created  
  - The **Cookiecutter template repository URL**  
  - The **project name**
- Automatically generates a new project from the provided template
- Initializes a **Git repository**, commits the initial files
- Optionally creates and pushes to a **GitHub repository** using the `gh` CLI
- Uses **colored console output** for better readability  
  - ✅ Green → successful actions  
  - ⚠️ Yellow → warnings or non-critical information  
  - ❌ Red → errors or failures

---

## Requirements

- **Python 3.9+**
- **Git**
- **Pip** (comes with Python)
- **Cookiecutter** (will be installed automatically if missing)
- *(Optional)* **GitHub CLI (`gh`)** – required for automatic repository creation on GitHub

---

## Installation

1. Clone this repository or download the script:
   ```bash
   git clone https://github.com/<your-username>/setup-cookiecutter-project.git
   cd setup-cookiecutter-project
2. Ensure you have Python installed:
    ```bash
    python --version
3. (Optional) Install the GitHub CLI if you want automatic repo creation:
    * Linux:
    ```bash
    sudo apt install gh
    ```
    * Windows:
    ```bash
    choco install gh
4. Make sure you have pip available and up to date:
    ```bash
    python -m ensurepip --upgrade
    python -m pip install --upgrade pip
5. (Optional) Create and activate a virtual environment:
    ```bash
    python -m venv .venv
    source .venv/bin/activate        # Linux/macOS
    .venv\Scripts\activate           # Windows

## Usage

Run the script with:
    ```bash
    python setup_cookiecutter_project.py

You’ll be guided through several interactive steps:

1. Confirm the detected operating system.
2. Verify and install dependencies (Git and Cookiecutter).
3. Enter the target path where the project should be created.
4. Provide the Cookiecutter template repository URL (e.g. https://github.com/ASJKM/project_setup_script.git )
5. Specify the project name.
6. Optionally push the generated project to GitHub.

## Example Worlflow


    === Automatic GitHub Project Setup with Cookiecutter ===

    Detected OS: Linux
    Proceed with setup on Linux? [y/n]: y

    Checking required tools...
    git is already installed.
    cookiecutter is already installed.

    Enter target directory: /home/user/projects
    Enter the Cookiecutter template URL:
    > https://github.com/your-org/cookiecutter-template

    Project name: demo_app

    Creating project with Cookiecutter...
    Project successfully created at: /home/user/projects/demo_app

    Initialize Git repository? [y/n]: y
    Create GitHub repository? [y/n]: y
    Repository created and pushed successfully!

## Example Project Structure

    /home/user/projects/demo_app/
    ├── development/
    ├── deployment/
    ├── tests/
    │   ├── unit/
    │   ├── system/
    │   └── static_analysis/
    ├── docs/
    │   ├── source/
    │   └── build/
    └── README.md

## Contributing

Contributions are welcome!
If you find a bug or have a feature request, please open an issue or submit a pull request.

Steps to contribute:

1. Fork this repository
2. Create a new branch (git checkout -b feature-name)
3. Commit your changes (git commit -m "Add feature XYZ")
4. Push your branch (git push origin feature-name)
5. Open a Pull Request