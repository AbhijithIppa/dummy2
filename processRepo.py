from typing import List, Optional
from pydantic import BaseModel, Field
from api.models.commonModels import ProcessRequest, ProcessResponse
from fastapi import APIRouter, BackgroundTasks, HTTPException
import os
from db.repo_manager import full_repository_process, process_changed_files
from utils.git_utils import get_current_commit_hash
processRouter= APIRouter()

@processRouter.post("/process", response_model=ProcessResponse)
async def process_repository(
    background_tasks: BackgroundTasks,
    request: ProcessRequest
):
    """Process a repository to extract and update code chunks"""
    if not os.path.exists(request.repo_path):
        raise HTTPException(status_code=404, detail="Repository path not found")
    
    if not os.path.exists(os.path.join(request.repo_path, ".git")):
        raise HTTPException(status_code=400, detail="Not a valid git repository")
    
    # Start processing in background
    background_tasks.add_task(
        full_repository_process if request.full_process else process_changed_files,
        request.repo_path,
        request.database_name
    )
    
    commit_hash = get_current_commit_hash(request.repo_path)
    
    return {
        "status": "processing_started",
        "new_chunks": 0,
        "updated_chunks": 0,
        "deleted_chunks": 0,
        "unchanged_chunks": 0,
        "commit_hash": commit_hash
    }

@processRouter.post("/process/sync", response_model=ProcessResponse)
def process_repository_sync(request: ProcessRequest):
    """Process a repository synchronously and wait for results"""
    if not os.path.exists(request.repo_path):
        raise HTTPException(status_code=404, detail="Repository path not found")
    
    if not os.path.exists(os.path.join(request.repo_path, ".git")):
        raise HTTPException(status_code=400, detail="Not a valid git repository")
    
    # Process and wait for results
    if request.full_process:
        stats = full_repository_process(request.repo_path, request.database_name)
    else:
        stats = process_changed_files(request.repo_path, request.database_name)
    
    commit_hash = get_current_commit_hash(request.repo_path)
    stats["commit_hash"] = commit_hash
    
    return stats
