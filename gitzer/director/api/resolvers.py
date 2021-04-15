import os
import sys

import git
from ariadne import MutationType, QueryType, convert_kwargs_to_snake_case
from django.conf import settings
from loguru import logger

logger.remove()

if settings.DEBUG:
    logger.add(sys.stdout, format=settings.GITZER_LOGGING_FORMAT)
logger.add(settings.GITZER_LOGGING_FILE, format=settings.GITZER_LOGGING_FORMAT)

query = QueryType()
mutation = MutationType()


@query.field("status")
@convert_kwargs_to_snake_case
def status(*_, directory):
    repo = git.Repo(directory)
    untracked_files = [
        {"name": file, "change_type": "U"} for file in repo.untracked_files
    ]
    modified_files = [
        {"name": file.a_path, "change_type": file.change_type}
        for file in repo.index.diff(None)
    ]
    logger.success("Requested status, directory: '{}'", directory)
    try:
        staged_files = [{"name": file.a_path} for file in repo.index.diff("HEAD")]
    except git.exc.BadName:
        staged_files = []
    return {
        "untracked_files": untracked_files,
        "modified_files": modified_files,
        "staged_files": staged_files,
        "branch": repo.active_branch,
    }


@query.field("presentWorkingDirectory")
@convert_kwargs_to_snake_case
def present_working_directory(*_):
    logger.info("Requested present working directory")
    path = os.getcwd()
    return str(path)


@query.field("existence")
@convert_kwargs_to_snake_case
def existence(*_, directory):
    try:
        git.Repo(directory)
        logger.success("Valid repository: '{}'", directory)
        return {
            "exists": True,
            "message": "The specified repository was found successfully",
        }
    except git.exc.InvalidGitRepositoryError:
        logger.debug("Invalid repository: '{}'", directory)
        message = "The path is not a valid git repository"
    except git.exc.NoSuchPathError:
        logger.error("Invalid path: '{}'", directory)
        message = "The path specified is not valid"
    return {"exists": False, "message": message}


@mutation.field("stageFile")
@convert_kwargs_to_snake_case
def stage_file(*_, data):
    filename = data.get("filename")
    directory = data.get("directory")
    repo = git.Repo(directory)
    path = os.path.join(directory, filename)
    file_changed = False
    for diff_added in repo.index.diff(None).iter_change_type("D"):
        """This has to be done because git doesn't track renaming of files
        inherently, so we check if the `filename` in question is a deleted one,
        and if it is, we remove it from the git index. The renamed file will show
        up as an untracked file, but we don't worry about it because as soon as it
        is added to the index, git will automatically detect it as a renamed file
        and adjust accordingly."""
        if str(diff_added.a_path) == str(filename):
            file_changed = True
            repo.index.remove(path)
    if not file_changed:
        repo.index.add(path)
    logger.success("Staged file: '{}'", path)
    return {"filename": filename, "status": True}


@mutation.field("unstageFile")
@convert_kwargs_to_snake_case
def unstage_file(*_, data):
    filename = data.get("filename")
    directory = data.get("directory")
    error = None
    repo = git.Repo(directory)
    path = os.path.join(directory, filename)
    restore = repo.git
    try:
        restore.restore(filename, "--staged")
        status = True
        logger.success("Unstaged file: '{}'", path)
    except git.exc.GitCommandError:
        status = False
        error = "This file was not found in the staging area"
        logger.error("Error while un-staging file: '{}'", path)
    return {"filename": filename, "status": status, "error": error}


@mutation.field("discardFileChange")
@convert_kwargs_to_snake_case
def discard_file_change(*_, data):
    filename = data.get("filename")
    directory = data.get("directory")
    path = os.path.join(directory, filename)
    error = None
    repo = git.Repo(directory)
    restore = repo.git
    try:
        restore.restore(filename)
        status = True
        logger.success("Discarded changes in file: '{}'", path)
    except git.exc.GitCommandError:
        status = False
        error = "This file does not exist in the git logs"
        logger.error("Error while discarding changes in file: '{}'", path)
    return {"filename": filename, "status": status, "error": error}


@mutation.field("performCommit")
@convert_kwargs_to_snake_case
def perform_commit(*_, message, directory):
    repo = git.Repo(directory)
    repo.index.commit(message)
    logger.success("Created a commit in directory: '{}'", directory)
    return {"status": False, "error": None}


@mutation.field("stageAllUntrackedFiles")
@convert_kwargs_to_snake_case
def stage_all_untracked_files(*_, directory):
    repo = git.Repo(directory)
    for filename in repo.untracked_files:
        path = os.path.join(directory, filename)
        repo.index.add(path)
    logger.info("Staged all untracked files in: '{}'", directory)
    return {"status": True, "error": None}


@mutation.field("stageAllModifiedFiles")
@convert_kwargs_to_snake_case
def stage_all_modified_files(*_, directory):
    repo = git.Repo(directory)
    for filename in repo.index.diff(None):
        path = os.path.join(directory, filename.a_path)
        repo.index.add(path)
    logger.info("Staged all modified files in: '{}'", directory)
    return {"status": True, "error": None}


@mutation.field("discardAllModifiedFiles")
@convert_kwargs_to_snake_case
def discard_all_modified_files(*_, directory):
    repo = git.Repo(directory)
    restore = repo.git
    status = True
    error = None
    for filename in repo.index.diff(None):
        try:
            path = os.path.join(directory, filename.a_path)
            restore.restore(path)
            logger.success("Discarded file: '{}'", path)
        except git.exc.GitCommandError:
            status = False
            error = "There was a problem resolving your request"
            logger.error("Error in discarding file: '{}'", path)
    return {"status": status, "error": error}


@mutation.field("unstageAllStagedFiles")
@convert_kwargs_to_snake_case
def unstage_all_staged_files(*_, directory):
    repo = git.Repo(directory)
    restore = repo.git
    status = True
    error = None
    for filename in repo.index.diff("HEAD"):
        try:
            path = os.path.join(directory, filename.a_path)
            restore.restore(path, "--staged")
            logger.success("Unstaged file: '{}'", path)
        except git.exc.GitCommandError:
            status = False
            error = "There was a problem resolving your request"
            logger.error("Error in un-staging file: '{}'", path)
    return {"status": status, "error": error}


@mutation.field("pushToOrigin")
def push_to_origin(*_, directory):
    """ This will push to an upsteam called `origin` """
    repo = git.Repo(directory)
    try:
        origin = repo.remote("origin")
        origin.push()
        logger.success("Pushed to origin: '{}'", directory)
        return True
    except ValueError:
        logger.error("Error in pushing to origin: '{}'", directory)
        return False
