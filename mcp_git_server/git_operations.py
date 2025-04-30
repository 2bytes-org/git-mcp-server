"""Git operations module for MCP Git Server."""

import os
import git
from typing import List, Optional, Dict, Any
import logging

logger = logging.getLogger(__name__)

class GitOperations:
    """Class to handle Git operations."""
    
    @staticmethod
    def validate_repo_path(repo_path: str) -> git.Repo:
        """Validate and return the Git repository."""
        if not os.path.exists(repo_path):
            raise ValueError(f"Repository path does not exist: {repo_path}")
        
        try:
            return git.Repo(repo_path)
        except git.InvalidGitRepositoryError:
            raise ValueError(f"Not a valid Git repository: {repo_path}")
    
    @staticmethod
    def git_status(repo_path: str) -> Dict[str, Any]:
        """Shows the working tree status."""
        repo = GitOperations.validate_repo_path(repo_path)
        
        # Get status information
        changed_files = [item.a_path for item in repo.index.diff(None)]
        staged_files = [item.a_path for item in repo.index.diff('HEAD')]
        untracked_files = repo.untracked_files
        
        # Get branch information
        try:
            current_branch = repo.active_branch.name
        except TypeError:
            # Handle detached HEAD state
            current_branch = f"HEAD detached at {repo.head.commit.hexsha[:7]}"
        
        return {
            "current_branch": current_branch,
            "changed_files": changed_files,
            "staged_files": staged_files,
            "untracked_files": untracked_files
        }
    
    @staticmethod
    def git_diff_unstaged(repo_path: str) -> str:
        """Shows changes in working directory not yet staged."""
        repo = GitOperations.validate_repo_path(repo_path)
        diff_output = repo.git.diff()
        return diff_output
    
    @staticmethod
    def git_diff_staged(repo_path: str) -> str:
        """Shows changes that are staged for commit."""
        repo = GitOperations.validate_repo_path(repo_path)
        diff_output = repo.git.diff('--staged')
        return diff_output
    
    @staticmethod
    def git_diff(repo_path: str, target: str) -> str:
        """Shows differences between branches or commits."""
        repo = GitOperations.validate_repo_path(repo_path)
        diff_output = repo.git.diff(target)
        return diff_output
    
    @staticmethod
    def git_commit(repo_path: str, message: str) -> Dict[str, str]:
        """Records changes to the repository."""
        repo = GitOperations.validate_repo_path(repo_path)
        
        if not message or message.strip() == "":
            raise ValueError("Commit message cannot be empty")
        
        # Check if there are staged changes
        if not repo.index.diff('HEAD'):
            raise ValueError("No changes staged for commit")
        
        # Commit changes
        commit = repo.index.commit(message)
        
        return {
            "commit_hash": commit.hexsha,
            "message": message,
            "author": f"{commit.author.name} <{commit.author.email}>"
        }
    
    @staticmethod
    def git_add(repo_path: str, files: List[str]) -> Dict[str, List[str]]:
        """Adds file contents to the staging area."""
        repo = GitOperations.validate_repo_path(repo_path)
        
        if not files:
            raise ValueError("No files specified for staging")
        
        # Verify all files exist before adding any
        non_existent_files = []
        for file_path in files:
            full_path = os.path.join(repo_path, file_path)
            if not os.path.exists(full_path):
                non_existent_files.append(file_path)
        
        if non_existent_files:
            raise ValueError(f"The following files do not exist: {', '.join(non_existent_files)}")
        
        # Add files to staging area
        repo.git.add(files)
        
        return {"staged_files": files}
    
    @staticmethod
    def git_reset(repo_path: str) -> Dict[str, bool]:
        """Unstages all staged changes."""
        repo = GitOperations.validate_repo_path(repo_path)
        repo.git.reset()
        return {"success": True}
    
    @staticmethod
    def git_log(repo_path: str, max_count: Optional[int] = 10) -> List[Dict[str, str]]:
        """Shows the commit logs."""
        repo = GitOperations.validate_repo_path(repo_path)
        
        logs = []
        for commit in repo.iter_commits(max_count=max_count):
            logs.append({
                "hash": commit.hexsha,
                "short_hash": commit.hexsha[:7],
                "author": f"{commit.author.name} <{commit.author.email}>",
                "date": commit.committed_datetime.isoformat(),
                "message": commit.message
            })
        
        return logs
    
    @staticmethod
    def git_create_branch(repo_path: str, branch_name: str, start_point: Optional[str] = None) -> Dict[str, str]:
        """Creates a new branch."""
        repo = GitOperations.validate_repo_path(repo_path)
        
        if not branch_name or branch_name.strip() == "":
            raise ValueError("Branch name cannot be empty")
        
        # Check if branch already exists
        if branch_name in repo.heads:
            raise ValueError(f"Branch '{branch_name}' already exists")
        
        # Create branch
        if start_point:
            repo.git.branch(branch_name, start_point)
        else:
            repo.git.branch(branch_name)
        
        return {"branch_name": branch_name}
    
    @staticmethod
    def git_checkout(repo_path: str, branch_name: str) -> Dict[str, str]:
        """Switches branches."""
        repo = GitOperations.validate_repo_path(repo_path)
        
        if not branch_name or branch_name.strip() == "":
            raise ValueError("Branch name cannot be empty")
        
        # Check if branch exists
        if branch_name not in repo.heads and branch_name not in [tag.name for tag in repo.tags]:
            raise ValueError(f"Branch or tag '{branch_name}' does not exist")
        
        repo.git.checkout(branch_name)
        
        return {"current_branch": branch_name}
    
    @staticmethod
    def git_show(repo_path: str, revision: str) -> str:
        """Shows the contents of a commit."""
        repo = GitOperations.validate_repo_path(repo_path)
        
        if not revision or revision.strip() == "":
            raise ValueError("Revision cannot be empty")
        
        try:
            show_output = repo.git.show(revision)
            return show_output
        except git.GitCommandError as e:
            raise ValueError(f"Invalid revision: {revision}. Error: {str(e)}")
    
    @staticmethod
    def git_init(repo_path: str) -> Dict[str, bool]:
        """Initializes a Git repository."""
        if not os.path.exists(repo_path):
            os.makedirs(repo_path)
        
        if os.path.exists(os.path.join(repo_path, ".git")):
            raise ValueError(f"Repository already exists at {repo_path}")
        
        git.Repo.init(repo_path)
        
        return {"success": True}