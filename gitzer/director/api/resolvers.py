import git
from ariadne import QueryType, convert_kwargs_to_snake_case

query = QueryType()


@query.field("status")
@convert_kwargs_to_snake_case
def status(*_, directory="."):
    repo = git.Repo(directory)
    untracked_files = [{"name": file} for file in repo.untracked_files]
    modified_files = [{"name": file.a_path} for file in repo.index.diff(None)]
    staged_files = [{"name": file.a_path} for file in repo.index.diff("HEAD")]
    return {
        "untracked_files": untracked_files,
        "modified_files": modified_files,
        "staged_files": staged_files,
    }
