import os

def load_project_nvm(project_name: str, invocation_dir: str):
    """
    Constructs the path to the project's nvm.yaml file and reads its contents.
    """
    # Construct the path to the nvm.yaml file
    nvm_path = os.path.join(invocation_dir, "_projects", project_name, "nvm.yaml")

    # Check if the file exists
    if not os.path.exists(nvm_path):
        raise FileNotFoundError(f"nvm.yaml file not found at: {nvm_path}")

    # Use the read_nvm function to parse the file
    return read_nvm(nvm_path)
