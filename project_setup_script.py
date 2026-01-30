import os
import platform
import subprocess
import sys
import shutil
from cookiecutter.main import cookiecutter

# ANSI color codes
RED = "\033[91m"
YELLOW = "\033[93m"
GREEN = "\033[92m"
RESET = "\033[0m"

def run(cmd, check=True):
    """Helper function to run shell commands."""
    print(f"{YELLOW}>>{RESET} {cmd}")
    subprocess.run(cmd, shell=True, check=check)

def check_or_install(package, install_cmd):
    """Check if a tool is installed, otherwise install it."""
    if shutil.which(package):
        print(f"{GREEN}{package} is already installed.{RESET}")
        return True
    else:
        print(f"{YELLOW}Installing {package} ...{RESET}")
        try:
            run(install_cmd)
            return True
        except subprocess.CalledProcessError:
            print(f"{RED}Error: {package} could not be installed.{RESET}")
            return False

def detect_os():
    """Detect the operating system."""
    os_type = platform.system()
    print(f"Detected operating system: {GREEN}{os_type}{RESET}")
    return os_type

def install_requirements(os_type):
    """Install Git and Cookiecutter if missing."""
    print("\nChecking required tools...\n")

    # Install Git if not present
    check_or_install(
        "git",
        "sudo apt install git -y" if os_type == "Linux" else "choco install git -y"
    )

    # Install Cookiecutter using pipx for speed
    if not shutil.which("cookiecutter"):
        print(f"{YELLOW}Installing cookiecutter via pipx...{RESET}")
        # Ensure pipx is installed
        if not shutil.which("pipx"):
            print(f"{YELLOW}Installing pipx...{RESET}") 
            run(f"{sys.executable} -m pip install --user pipx") 
            run(f"{sys.executable} -m pipx ensurepath") 
        run(f"{sys.executable} -m pipx install cookiecutter")
    else:
        print(f"{GREEN}cookiecutter is already installed.{RESET}")

def generate_project(template_repo, target_path):
    """Create a new project from the Cookiecutter template."""

    project_name = input("Project name: ").strip()
    target_dir = os.path.join(os.path.abspath(target_path), project_name)

    if os.path.exists(target_dir):
        print(f"{RED}Error: The folder '{target_dir}' already exists. Aborting.{RESET}")
        sys.exit(1)

    print(f"{YELLOW} + '\nCreating project with Cookiecutter...' + {RESET}")

    # --------------------------------------------------------------------------------
    # NEW: Use Cookiecutter's Python API instead of subprocess to ensure compatibility
    # --------------------------------------------------------------------------------
    try:
        project_dir = cookiecutter(
            template_repo,
            no_input=False,  # Allow interactive prompts since template has multiple variables
            extra_context={"project_name": project_name},  # Pre-fill project_name
            output_dir=target_path  # Ensure it generates inside the chosen path
        )
    except Exception as e:
        print(f"{RED}Error while running Cookiecutter: {e}{RESET}")
        sys.exit(1)

    # NEW: Validate that Cookiecutter generated a project
    if not project_dir or not os.path.exists(project_dir):
        print(f"{RED}No project folder found. Cookiecutter may not have generated anything.{RESET}")
        sys.exit(1)

    # NEW: Print confirmation
    print(f"{GREEN}Project successfully created at: {project_dir}{RESET}")
    return project_dir

def handle_skip_license(project_dir):
    """Remove LICENSE file and license references if user selected 'Skip'."""
    import json
    import re

    context_file = os.path.join(project_dir, ".cookiecutter.json")

    if not os.path.exists(context_file):
        print(f"{YELLOW}Warning: No .cookiecutter.json found. Skipping license cleanup.{RESET}")
        return

    try:
        with open(context_file, "r", encoding="utf-8") as f:
            context = json.load(f)

        if context.get("license") not in ["Skip", "None"]:
            return  # ✅ Nothing to clean

        print(f"{YELLOW}License skipped/none. Cleaning all license references...{RESET}")

        # -------------------------------------------------------
        # ✅ 1. DELETE LICENSE FILE
        # -------------------------------------------------------
        license_path = os.path.join(project_dir, "LICENSE")
        if os.path.exists(license_path):
            os.remove(license_path)
            print(f"{GREEN}Removed LICENSE file.{RESET}")

        # -------------------------------------------------------
        # ✅ 2. CLEAN pyproject.toml
        # -------------------------------------------------------
        pyproject_path = os.path.join(project_dir, "pyproject.toml")
        if os.path.exists(pyproject_path):
            with open(pyproject_path, "r", encoding="utf-8") as f:
                content = f.read()

            # Remove license field safely
            content = re.sub(r'license\s*=\s*".*?"\n', '', content)

            # Remove classifiers that reference licenses
            content = re.sub(
                r'classifiers\s*=\s*\[(?:.|\n)*?\]',
                lambda m: '\n'.join(
                    [line for line in m.group(0).splitlines() if "License ::" not in line]
                ),
                content
            )

            with open(pyproject_path, "w", encoding="utf-8") as f:
                f.write(content)

            print(f"{GREEN}Cleaned license from pyproject.toml.{RESET}")

        # -------------------------------------------------------
        # ✅ 3. CLEAN setup.cfg
        # -------------------------------------------------------
        setup_cfg_path = os.path.join(project_dir, "setup.cfg")
        if os.path.exists(setup_cfg_path):
            with open(setup_cfg_path, "r", encoding="utf-8") as f:
                content = f.read()

            # Remove license field
            content = re.sub(r'^license\s*=.*\n', '', content, flags=re.MULTILINE)

            # Remove license classifiers
            content = re.sub(r'.*License ::.*\n', '', content)

            with open(setup_cfg_path, "w", encoding="utf-8") as f:
                f.write(content)

            print(f"{GREEN}Cleaned license from setup.cfg.{RESET}")

        # -------------------------------------------------------
        # ✅ 4. CLEAN README.md
        # -------------------------------------------------------
        readme_path = os.path.join(project_dir, "README.md")
        if os.path.exists(readme_path):
            with open(readme_path, "r", encoding="utf-8") as f:
                content = f.read()

            # Remove common license sections
            content = re.sub(
                r'## License(?:.|\n)*?$',
                '',
                content,
                flags=re.IGNORECASE
            )

            # Remove badge-style license lines
            content = re.sub(r'.*license.*badge.*\n', '', content, flags=re.IGNORECASE)
            content = re.sub(r'.*license.*\n', '', content, flags=re.IGNORECASE)

            with open(readme_path, "w", encoding="utf-8") as f:
                f.write(content.strip() + "\n")

            print(f"{GREEN}Cleaned license from README.md.{RESET}")

    except Exception as e:
        print(f"{RED}Failed to fully process license cleanup: {e}{RESET}")

def main():
    print("=== Automatic Project Setup with Cookiecutter ===\n")

    os_type = detect_os()
    confirm = input(f"Proceed with setup on {os_type}? [y/n]: ").strip().lower()
    if confirm != "y":
        print(f"{YELLOW}Aborted by user.{RESET}")
        sys.exit(0)

    install_requirements(os_type)

    # Ask for target path
    target_path = input("\nEnter the complete path (~/../path/project or C:\\path\\project) where the project should be created: ").strip()
    if not os.path.isdir(target_path):
        print(f"{YELLOW}Path does not exist. Creating directory...{RESET}")
        os.makedirs(target_path, exist_ok=True)
        print(f"{GREEN}Directory created: {target_path}{RESET}")

    template_repo = input(
        "\nEnter the URL of your Cookiecutter template (e.g., https://github.com/ASJKM/project_setup.git ):\n> "
    ).strip()

    project_dir = generate_project(template_repo, target_path)
    handle_skip_license(project_dir)

    print(f"\n{GREEN}Done! Your project has been successfully set up.{RESET}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{RED}Aborted by user.{RESET}")
