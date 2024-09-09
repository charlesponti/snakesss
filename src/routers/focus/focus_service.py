import json
from enum import Enum

from groq.types import CompletionUsage

from lib.ai_models import open_source_models
from lib.clients.groq_service import groq_client
from lib.file_service import FileRepository
from lib.generation_statistics import GenerationStatistics
from lib.logger import logger


def log_generation_statistics(usage: CompletionUsage, model: str):
    try:
        statistics_to_return = GenerationStatistics(
            input_time=int(usage.prompt_time) if usage.prompt_time else 0,
            output_time=(int(usage.completion_time) if usage.completion_time else 0),
            input_tokens=usage.prompt_tokens,
            output_tokens=usage.completion_tokens,
            total_time=int(usage.total_time) if usage.total_time else 0,
            model_name=model,
        )
        logger.info("focus_stats", statistics_to_return.get_stats())
    except Exception as e:
        logger.error(f" ********* STATISTICS GENERATION error ******* : {e} ")
        return None, {"error": str(e)}


def analyze_user_input(transcript: str, model: str = "llama3-70b-8192"):
    system_prompt = FileRepository.get_file_contents(f"src/routers/focus/user_input_formatter.md")

    if model in open_source_models:
        try:
            completion = groq_client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": transcript},
                ],
                temperature=0.3,
                max_tokens=8000,
                top_p=1,
                stream=False,
                response_format={"type": "json_object"},
                stop=None,
            )

            usage = completion.usage
        except Exception as e:
            logger.error(f" ********* API error ********: {e} ***** ")
            return None, {"error": str(e)}

        if usage:
            log_generation_statistics(usage, model)

        return (
            json.loads(completion.choices[0].message.content)
            if completion.choices[0].message.content
            else None
        )
