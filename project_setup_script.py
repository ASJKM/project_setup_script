import os
import platform
import subprocess
import sys
import shutil

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

    print("\nCreating project with Cookiecutter...\n")
    # Run Cookiecutter via pipx to ensure cross-platform compatibility
    run(f"{sys.executable} -m pipx run cookiecutter {template_repo} --no-input project_name='{project_name}'")


    # Find generated folder
    dirs = [d for d in os.listdir('.') if os.path.isdir(d) and d.startswith(project_name)]
    if not dirs:
        print(f"{RED}No project folder found. Cookiecutter may not have generated anything.{RESET}")
        sys.exit(1)

    # Move the project to the target path
    generated_dir = dirs[0]
    final_path = os.path.join(target_path, generated_dir)
    shutil.move(generated_dir, final_path)
    print(f"{GREEN}Project successfully created at: {final_path}{RESET}")
    return final_path

def init_and_push_to_github(project_dir):
    """Initialize Git and push the project to GitHub."""
    os.chdir(project_dir)

    print("\nInitializing local Git repository ...")
    run("git init")
    run("git add .")
    run('git commit -m "Initial commit from setup script"')

    repo_name = os.path.basename(os.getcwd())
    create_choice = input("Do you want to create a GitHub repository? [y/n]: ").strip().lower()
    if create_choice != "y":
        print(f"{YELLOW}No remote repository will be created.{RESET}")
        return

    if not shutil.which("gh"):
        print(f"{YELLOW}Warning: GitHub CLI (gh) not found. Please create a repository manually or use a PAT.{RESET}")
        return

    print("\nCreating GitHub repository ...")
    run(f"gh repo create {repo_name} --public --source=. --remote=origin --push")

    print(f"{GREEN}Project successfully created and pushed to GitHub.{RESET}")

def main():
    print("=== Automatic GitHub Project Setup with Cookiecutter ===\n")

    os_type = detect_os()
    confirm = input(f"Proceed with setup on {os_type}? [y/n]: ").strip().lower()
    if confirm != "y":
        print(f"{YELLOW}Aborted by user.{RESET}")
        sys.exit(0)

    install_requirements(os_type)

    # Ask for target path
    target_path = input("\nEnter the path where the project should be created: ").strip()
    if not os.path.isdir(target_path):
        print(f"{YELLOW}Path does not exist. Creating directory...{RESET}")
        os.makedirs(target_path, exist_ok=True)
        print(f"{GREEN}Directory created: {target_path}{RESET}")

    template_repo = input(
        "\nEnter the URL of your Cookiecutter template (e.g., https://github.com/ASJKM/project_setup_script.git ):\n> "
    ).strip()

    project_dir = generate_project(template_repo, target_path)
    init_and_push_to_github(project_dir)

    print(f"\n{GREEN}Done! Your project has been successfully set up.{RESET}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{RED}Aborted by user.{RESET}")
