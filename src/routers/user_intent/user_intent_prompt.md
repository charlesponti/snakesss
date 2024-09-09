<|begin_of_text|>

<|start_header_id|>system<|end_header_id|>

Tools: create_tasks, search_tasks, edit_task, chat
Cutting Knowledge Date: December 2023
Today Date: {today_date}

You are a helpful assistant with tool-calling capabilities.
<|eot_id|>

<|start_header_id|>user<|end_header_id|>

Given the following functions, please respond with a JSON for a function call with its proper arguments that best answers the given prompt.

## Available functions:
[
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
                  "description": "The name or description of the task"
                },
                "due_date": {
                  "type": "string",
                  "format": "date-time",
                  "description": "The optional due date for the task"
                },
                "related_tasks": {
                  "type": "array",
                  "items": {
                    "type": "string"
                  },
                  "description": "The name of the related tasks"
                }
              },
              "required": ["task_name"]
            },
            "description": "An array of tasks to be added to the list"
          }
        },
        "required": ["tasks"]
      }
    }
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
            "description": "Keyword to search for in task names or descriptions"
          },
          "due_before": {
            "type": "string",
            "format": "date-time",
            "description": "Filter tasks that are due before a specific date"
          },
          "status": {
            "type": "string",
            "enum": ["pending", "completed", "in-progress"],
            "description": "Filter tasks by their current status"
          }
        },
        "required": ["keyword"]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "chat",
      "description": "Chat with the user",
      "parameters": {
        "type": "object",
        "properties": {
          "message": {
            "type": "string",
            "description": "The message to be sent to the user"
          }
        },
        "required": ["message"]
      }
    }
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
            "description": "The unique identifier of the task to be edited"
          },
          "new_task_name": {
            "type": "string",
            "description": "The new name or description of the task"
          },
          "new_due_date": {
            "type": "string",
            "format": "date-time",
            "description": "The new due date for the task"
          },
          "new_status": {
            "type": "string",
            "enum": ["pending", "completed", "in-progress"],
            "description": "The updated status of the task"
          }
        },
        "required": ["task_id"]
      }
    }
  }
]

## Reminder:

- If the user wants to execute a search:
  - you MUST USE the `search_tasks` function
  - you MUST INCLUDE the `keyword` parameter.
- If the user wants to create a task:
  - you MUST USE the `create_tasks` function
  - you MUST INCLUDE the `tasks` parameter.
    - you MUST INCLUDE the `task_name` property.
- If the user mentions a relative date, such as "today", "tomorrow", or "next week":
  - you MUST USE provide a `due_date` parameter equal to the relative date relative to the current date in `YYYY-MM-DD` format.
