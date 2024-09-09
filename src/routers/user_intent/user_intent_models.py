import json
import uuid
from typing import Any, List, Optional

from langchain.pydantic_v1 import BaseModel, Field
from langchain_core.messages import AIMessage, BaseMessage, HumanMessage, ToolMessage
from typing_extensions import Dict


class Intent(BaseModel):
    function_name: str = Field(description="The name of the function to call")
    parameters: Dict[str, Any] = Field(description="The parameters to pass to the function")


class IntentExample(BaseModel):
    input: str = Field(description="The idea for the user story")
    tool_outputs: Optional[List[str]] = Field(description="The outputs of the tool calls", default=None)
    tool_calls: List[Intent] = Field(description="The tool calls to make")


intent_examples: List[IntentExample] = [
    IntentExample(
        input="I have to buy groceries, finish a report by tomorrow, and check my email for updates.",
        tool_calls=[
            Intent(
                function_name="create_tasks",
                parameters={
                    "tasks": [
                        {"task_name": "Buy groceries"},
                        {"task_name": "Finish report", "due_date": "2024-07-24"},
                    ]
                },
            ),
            Intent(function_name="search_tasks", parameters={"keyword": "email"}),
        ],
    ),
    IntentExample(
        input="What do I need to do today?",
        tool_calls=[Intent(function_name="search_tasks", parameters={"due_date": "2024-07-24"})],
    ),
    IntentExample(
        input="What's the status of my report?",
        tool_calls=[Intent(function_name="search_tasks", parameters={"keyword": "report"})],
    ),
    IntentExample(
        input="Remind me to call mom tomorrow.",
        tool_calls=[
            Intent(
                function_name="create_tasks",
                parameters={"tasks": [{"task_name": "Call mom", "due_date": "2024-07-24"}]},
            )
        ],
    ),
    IntentExample(
        input="Change the due date of my report to Friday.",
        tool_calls=[
            Intent(
                function_name="edit_task", parameters={"task_id": "report_id", "new_due_date": "2024-07-24"}
            )
        ],
    ),
    IntentExample(
        input="Mark the groceries as done.",
        tool_calls=[
            Intent(
                function_name="edit_task", parameters={"task_id": "groceries_id", "new_status": "completed"}
            )
        ],
    ),
    IntentExample(
        input="I have to go to the grocery store and buy milk.",
        tool_calls=[
            Intent(
                function_name="create_tasks",
                parameters={
                    "tasks": [
                        {"task_name": "Go to the grocery store"},
                        {"task_name": "Buy milk", "related_tasks": ["Go to the grocery store"]},
                    ]
                },
            )
        ],
    ),
]


def get_intent_examples_as_str() -> str:
    output = """
    ## User Intent Examples\n\n
    The following are examples of user intents and the tool calls generated from them.\n\n
    """

    for example in intent_examples:
        output += f"Input: {example.input}\n"
        output += "Tool calls:\n"
        calls = [call.json() for call in example.tool_calls]
        output += f"{json.dumps(calls, indent=4)}\n\n"
    print(output)

    return output


def get_user_intent_few_shot_examples() -> List[BaseMessage]:
    result = []

    for example in intent_examples:
        output = ""
        calls = [call.json() for call in example.tool_calls]
        output += f"{json.dumps(calls, indent=4)}\n\n"
        print(output)

        messages: List[BaseMessage] = [HumanMessage(content=example.input)]
        tool_calls = [
            {
                "id": str(uuid.uuid4()),
                "type": "function",
                "function": {"name": tool_call.__class__.__name__, "arguments": tool_call.json()},
            }
            for tool_call in example.tool_calls
        ]

        messages.append(AIMessage(content="", additional_kwargs={"tool_calls": tool_calls}))

        tool_outputs = example.tool_outputs or ["Tool called."] * len(tool_calls)
        messages.extend(
            [
                ToolMessage(content=output, tool_call_id=tool_call["id"])
                for output, tool_call in zip(tool_outputs, tool_calls)
            ]
        )

        result.append(messages)

    return result


user_intent_examples = [
    {
        "input": "I have to go to the grocery store and buy milk, email my boss, and check my email for updates.",
        "output": json.dumps(
            [
                {
                    "name": "create_tasks",
                    "parameters": {
                        "tasks": [
                            {"task_name": "Buy groceries"},
                            {"task_name": "Finish report", "due_date": "2024-07-24"},
                        ]
                    },
                },
                {"name": "search_tasks", "parameters": {"keyword": "email"}},
            ]
        ),
    },
    {
        "input": "Who I need to do today?",
        "output": json.dumps([{"name": "search_tasks", "parameters": {"due_before": "2024-07-24"}}]),
    },
    {
        "input": "Current Date: 2024-07-24 \n What tasks are due this week?",
        "output": json.dumps([{"name": "search_tasks", "parameters": {"due_before": "2024-07-31"}}]),
    },
    {
        "input": "What's the status of my report?",
        "output": json.dumps([{"name": "search_tasks", "parameters": {"keyword": "report"}}]),
    },
    {
        "input": "When is my dentist appointment?",
        "output": json.dumps([{"name": "search_tasks", "parameters": {"keyword": "dentist"}}]),
    },
    {
        "input": "Remind me to call mom tomorrow.",
        "output": json.dumps(
            [
                {
                    "name": "create_tasks",
                    "parameters": {"tasks": [{"task_name": "Call mom", "due_date": "2024-07-24"}]},
                }
            ]
        ),
    },
    {
        "input": "Change the due date of my report to Friday.",
        "output": json.dumps(
            [{"name": "edit_task", "parameters": {"task_id": "report_id", "new_due_date": "2024-07-24"}}]
        ),
    },
    {
        "input": "Mark the groceries as done.",
        "output": json.dumps(
            [{"name": "edit_task", "parameters": {"task_id": "groceries_id", "new_status": "completed"}}]
        ),
    },
    {
        "input": "I have to go to the grocery store and buy milk.",
        "output": json.dumps(
            [
                {
                    "name": "create_tasks",
                    "parameters": {
                        "tasks": [
                            {"task_name": "Go to the grocery store"},
                            {"task_name": "Buy milk", "related_tasks": ["Go to the grocery store"]},
                        ]
                    },
                }
            ]
        ),
    },
]
