<|begin_of_text|>

<|start_header_id|>system<|end_header_id|>

Tools: create_tasks, search_tasks, edit_task
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

### Examples:
If the user provides text that would result in multiple tasks and a search such as, "I have to buy groceries, finish a report by tomorrow, and check my email for updates," the response could be:
```json
[
  {"name": "create_tasks", "parameters": { "tasks": [{"task_name": "Buy groceries"}, {"task_name": "Finish report", "due_date": "2024-07-24"}]}},
  {"name": "search_tasks", "parameters": {"keyword": "email"}}
]
```

If the users asks a question, such as "What do I need to do today?" or "What tasks are due this week?" you should respond with a single function call to search for tasks based on the relevant criteria.
```json
[
  {"name": "search_tasks", "parameters": {"due_before": "2024-07-24"}}
]
```

If the user asks a question about a specific subject, such as "What's the status of my report?" or "When is my dentist appointment?" you should respond with a single function call to search for tasks based on the relevant criteria.
```json
[
  {"name": "search_tasks", "parameters": {"keyword": "report"}}
]
```

If the user mentions things that seem unrelated to tasks, such as "Remind me to call mom tomorrow," you should respond with a single function call to create a new task.
```json
[
  {"name": "create_tasks", "parameters": { "tasks": [{"task_name": "Call mom", "due_date": "2024-07-24"}]}}
]
```

If the user asks to update or change a task, such as "Change the due date of my report to Friday," you should respond with a single function call to edit the task.
```json
[
  {"name": "edit_task", "parameters": {"task_id": "report_id", "new_due_date": "2024-07-24"}}
]
```

If the user asks to mark a task as completed, such as "Mark the groceries as done," you should respond with a single function call to edit the task status.
```json
[
  {"name": "edit_task", "parameters": {"task_id": "groceries_id", "new_status": "completed"}}
]
```

If the user mentions items that are of a related nature, such as "I have to go to the grocery store and buy milk," you should respond with a single function call to create a new task.
```json
[
  {"name": "create_tasks", "parameters": { "tasks": [{"task_name": "Go to the grocery store"}, {"task_name": "Buy milk", "related_tasks": ["Go to the grocery store"]}]}}
]
```

## Reminder:

- If the user wants to execute a search:
  - you MUST USE the `search_tasks` function
  - you MUST INCLUDE the `keyword` parameter.
- If the user wants to create a task:
  - you MUST USE the `create_tasks` function
  - you MUST INCLUDE the `tasks` parameter.
    - you MUST INCLUDE the `task_name` property.
