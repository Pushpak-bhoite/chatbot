from pathlib import Path

WORKSPACE = Path("workspace").resolve()

print("workspace path->", WORKSPACE)
def list_files():
    files = []

    for path in WORKSPACE.rglob("*"):
        if path.is_file():
            files.append(str(path.relative_to(WORKSPACE)))

    return files


def read_file(path: str):
    file_path = (WORKSPACE / path).resolve()

    if not file_path.is_relative_to(WORKSPACE):
        return "Error: Access denied."

    if not file_path.exists():
        return f"Error: File '{path}' does not exist."

    return file_path.read_text()


def write_file(path: str, content: str):
    file_path = (WORKSPACE / path).resolve()

    if not file_path.is_relative_to(WORKSPACE):
        return "Error: Access denied."

    file_path.parent.mkdir(parents=True, exist_ok=True)

    file_path.write_text(content)

    return f"Successfully wrote {path}"