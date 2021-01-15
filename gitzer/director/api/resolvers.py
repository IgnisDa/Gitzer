import git
from ariadne import QueryType, convert_kwargs_to_snake_case

query = QueryType()


@query.field("status")
@convert_kwargs_to_snake_case
def status(*_, directory):
    repo = git.Repo(directory)
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
        return {"exists": False, "message": "The path is not a valid git repository"}
    except git.exc.NoSuchPathError:
        return {"exists": False, "message": "The path specified is not valid"}
