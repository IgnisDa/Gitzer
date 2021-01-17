import os

import git
from ariadne import MutationType, QueryType, convert_kwargs_to_snake_case

from .. import models

query = QueryType()
mutation = MutationType()


@query.field("status")
@convert_kwargs_to_snake_case
def status(*_, directory):
    repo = git.Repo(directory)
    models.Repository.objects.get_or_create(path=repo.working_dir)
    untracked_files = [{"name": file} for file in repo.untracked_files]
    modified_files = [{"name": file.a_path} for file in repo.index.diff(None)]
    try:
        staged_files = [{"name": file.a_path} for file in repo.index.diff("HEAD")]
    except git.exc.BadName:
        staged_files = []
    return {
        "untracked_files": untracked_files,
        "modified_files": modified_files,
        "staged_files": staged_files,
    }


@query.field("existence")
@convert_kwargs_to_snake_case
def existence(*_, directory):
    try:
        git.Repo(directory)
        return {
            "exists": True,
            "message": "The specified repository was found successfully",
        }
    except git.exc.InvalidGitRepositoryError:
        message = "The path is not a valid git repository"
    except git.exc.NoSuchPathError:
        message = "The path specified is not valid"
    return {"exists": False, "message": message}


@mutation.field("stageFile")
@convert_kwargs_to_snake_case
def stage_file(*_, data):
    filename = data.get("filename")
    directory = data.get("directory")
    repo = git.Repo(directory)
    path = os.path.join(directory, filename)
    print(path)
    repo.index.add(path)
    return {"filename": filename, "status": True}


@mutation.field("unstageFile")
@convert_kwargs_to_snake_case
def unstage_file(*_, data):
    filename = data.get("filename")
    directory = data.get("directory")
    error = None
    repo = git.Repo(directory)
    restore = repo.git
    try:
        restore.restore(filename, "--staged")
        status = True
    except git.exc.GitCommandError:
        status = False
        error = "This file was not found in the staging area"
    return {"filename": filename, "status": status, "error": error}


@mutation.field("discardFileChange")
@convert_kwargs_to_snake_case
def discard_file_change(*_, data):
    filename = data.get("filename")
    directory = data.get("directory")
    error = None
    repo = git.Repo(directory)
    restore = repo.git
    try:
        restore.restore(filename)
        status = True
    except git.exc.GitCommandError:
        status = False
        error = "This file does not exist in the git logs"
    return {"filename": filename, "status": status, "error": error}


@mutation.field("performCommit")
@convert_kwargs_to_snake_case
def perform_commit(*_, data):
    name = data.get("name")
    commit_type = data.get("commit_type")
    print(name, commit_type)
    return {"name": data["name"], "status": False}
