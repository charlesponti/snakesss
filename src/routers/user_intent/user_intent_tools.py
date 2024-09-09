from datetime import datetime
from typing import List, Optional

from langchain.pydantic_v1 import BaseModel, Field


class Task(BaseModel):
    task_name: str = Field(..., description="The name or description of the task")
    due_date: Optional[datetime] = Field(None, description="The optional due date for the task")
    related_tasks: Optional[List[str]] = Field(None, description="The name of the related tasks")


class CreateTasksParameters(BaseModel):
    tasks: List[Task] = Field(..., description="An array of tasks to be added to the list")


class CreateTasksFunction(BaseModel):
    name: str = Field("create_tasks", description="Create a new list of tasks")
    description: str = Field("Create a new list of tasks")
    parameters: CreateTasksParameters


# Schema for the "search_tasks" function
class SearchTasksParameters(BaseModel):
    keyword: str = Field(..., description="Keyword to search for in task names or descriptions")
    due_before: Optional[datetime] = Field(
        None, description="Filter tasks that are due before a specific date"
    )
    status: Optional[str] = Field(
        None, description="Filter tasks by their current status", enum=["pending", "completed", "in-progress"]
    )


class SearchTasksFunction(BaseModel):
    name: str = Field(
        "search_tasks", description="Search for tasks based on a keyword or specific attributes"
    )
    description: str = Field("Search for tasks based on a keyword or specific attributes")
    parameters: SearchTasksParameters


# Schema for the "edit_task" function
class EditTaskParameters(BaseModel):
    task_id: str = Field(..., description="The unique identifier of the task to be edited")
    new_task_name: Optional[str] = Field(None, description="The new name or description of the task")
    new_due_date: Optional[datetime] = Field(None, description="The new due date for the task")
    new_status: Optional[str] = Field(
        None, description="The updated status of the task", enum=["pending", "completed", "in-progress"]
    )


class EditTaskFunction(BaseModel):
    name: str = Field("edit_task", description="Edit an existing task in a task list")
    description: str = Field("Edit an existing task in a task list")
    parameters: EditTaskParameters


tool_definitions = [
    {
        "type": "function",
        "function": {
            "name": "create_tasks",
            "description": "Create a new list of tasks",
            "parameters": {
                "type": "object",
                "properties": {
                    "tasks": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "task_name": {
                                    "type": "string",
                                    "description": "The name or description of the task",
                                },
                                "due_date": {
                                    "type": "string",
                                    "format": "date-time",
                                    "description": "The optional due date for the task",
                                },
                                "related_tasks": {
                                    "type": "array",
                                    "items": {"type": "string"},
                                    "description": "The name of the related tasks",
                                },
                            },
                            "required": ["task_name"],
                        },
                        "description": "An array of tasks to be added to the list",
                    }
                },
                "required": ["tasks"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "search_tasks",
            "description": "Search for tasks based on a keyword or specific attributes",
            "parameters": {
                "type": "object",
                "properties": {
                    "keyword": {
                        "type": "string",
                        "description": "Keyword to search for in task names or descriptions",
                    },
                    "due_before": {
                        "type": "string",
                        "format": "date-time",
                        "description": "Filter tasks that are due before a specific date",
                    },
                    "status": {
                        "type": "string",
                        "enum": ["pending", "completed", "in-progress"],
                        "description": "Filter tasks by their current status",
                    },
                },
                "required": ["keyword"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "edit_task",
            "description": "Edit an existing task in a task list",
            "parameters": {
                "type": "object",
                "properties": {
                    "task_id": {
                        "type": "string",
                        "description": "The unique identifier of the task to be edited",
                    },
                    "new_task_name": {
                        "type": "string",
                        "description": "The new name or description of the task",
                    },
                    "new_due_date": {
                        "type": "string",
                        "format": "date-time",
                        "description": "The new due date for the task",
                    },
                    "new_status": {
                        "type": "string",
                        "enum": ["pending", "completed", "in-progress"],
                        "description": "The updated status of the task",
                    },
                },
                "required": ["task_id"],
            },
        },
    },
]
