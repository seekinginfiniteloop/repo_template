#!/usr/bin/env /usr/bin/python3
import os
import shutil
import sys

from pathlib import Path

import git

from github import Auth, Github


def create_new_repo(
    project_name: str, source_path: Path, destination_path: Path
) -> None:
    if not destination_path.exists():
        destination_path.mkdir(parents=True, exist_ok=True)

    shutil.copytree(
        source_path,
        destination_path,
        dirs_exist_ok=True,
        ignore=shutil.ignore_patterns(
            "*.pyc",
            "__pycache__",
            ".git",
            ".idea",
            ".vscode",
            "venv",
            "env",
            "node_modules",
            "dist",
            "build",
            "target",
            "out",
            "output",
            "logs",
            "tmp",
            "temp",
            "cache",
            "data",
            "db",
            "database",
            "storage",
            "uploads",
            "files",
            "images",
            "assets",
            "static",
            "public",
            ".venv",
            "pyvenv.cfg",
            ".env",
            "*cache*",
            "*log*",
            "*tmp*",
            "*temp*",
            "*backup*",
            "*swp*",
        ),
    )

    template: Path = destination_path / "project_name_src"
    template.rename(destination_path / project_name)

    self_file = destination_path / "create_new_repo.py"
    self_file.unlink()


def initiate_git_repo(destination_path: Path) -> None:
    os.chdir(destination_path)
    repo = git.Repo.init()
    repo.git.add(A=True)
    repo.index.commit("Initial commit with project template")
    auth = Auth().Token(os.environ["GH"])
    g = Github(auth)
    g.get_user().create_repo(destination_path.name)
    repo.remote(name="origin", url=f"https://github.com/{g.get_user().login}/{destination_path.name}.git")



def main() -> None:
    project_name: str = (
        input("Project name: ").strip().replace(" ", "_").replace("-", "_")
    )
    if Path.cwd().name == "repo_template":
        source_path = Path.cwd()
    else:
        source_path = Path(sys.argv[0]).resolve().parent
    destination_directory: str = (
        input("Destination PARENT dir (default: ../)): ").strip() or source_path.parent
    )
    destination_directory = (
        Path(destination_directory[:-1])
        if destination_directory[-1] == "/"
        else Path(destination_directory)
    )

    dest_path: Path = Path(destination_directory) / project_name

    create_new_repo(project_name, source_path, dest_path)

    initiate_git_repo(dest_path)

    print(f"Created new repo: {dest_path}")


if __name__ == "__main__":
    main()
