"""3-stage Straight Dope council orchestration."""

import asyncio
from typing import List, Dict, Any, Tuple

from .openrouter import query_model, query_roles_parallel
from .config import ADVISOR_MODEL, CHAIRMAN_MODEL
from .agents.prompts import (
    FORECASTER_SYSTEM_PROMPT,
    CRITIC_SYSTEM_PROMPT,
    REALITY_CHECKER_SYSTEM_PROMPT,
    CHAIRMAN_SYSTEM_PROMPT,
    CROSS_EXAM_SYSTEM_PROMPT_TEMPLATE,
)

ADVISORS = [
    {"name": "Forecaster", "model": ADVISOR_MODEL, "system_prompt": FORECASTER_SYSTEM_PROMPT},
    {"name": "Critic", "model": ADVISOR_MODEL, "system_prompt": CRITIC_SYSTEM_PROMPT},
    {"name": "Reality-Checker", "model": ADVISOR_MODEL, "system_prompt": REALITY_CHECKER_SYSTEM_PROMPT},
]


async def stage1_advisor_perspectives(user_query: str) -> List[Dict[str, Any]]:
    """
    Stage 1: Run all 3 advisors in parallel on the user's question.
    Returns list of dicts with 'role' and 'response'.
    """
    messages = [{"role": "user", "content": user_query}]
    responses = await query_roles_parallel(ADVISORS, messages)

    results = []
    for advisor, response in zip(ADVISORS, responses):
        results.append({
            "role": advisor["name"],
            "response": response.get("content", "Error: advisor did not respond.") if response else "Error: advisor did not respond.",
        })
    return results


async def stage2_cross_examination(
    user_query: str,
    stage1_results: List[Dict[str, Any]],
) -> List[Dict[str, Any]]:
    """
    Stage 2: Each advisor challenges the weakest argument from the other two.
    Runs in parallel.
    """
    # Build a summary of all other advisors' views for each role
    def build_cross_exam_context(current_role: str) -> str:
        others = [r for r in stage1_results if r["role"] != current_role]
        context = f"Original question: {user_query}\n\n"
        for o in others:
            context += f"--- {o['role']}'s analysis ---\n{o['response']}\n\n"
        return context

    roles_with_context = []
    for advisor in ADVISORS:
        context = build_cross_exam_context(advisor["name"])
        system_prompt = CROSS_EXAM_SYSTEM_PROMPT_TEMPLATE.format(role_name=advisor["name"])
        roles_with_context.append({
            "name": advisor["name"],
            "model": advisor["model"],
            "system_prompt": system_prompt,
            "context": context,
        })

    async def run_cross_exam(role_info: Dict) -> Dict[str, Any]:
        messages = [{"role": "user", "content": role_info["context"]}]
        response = await query_model(
            role_info["model"],
            role_info["system_prompt"],
            messages,
        )
        return {
            "role": role_info["name"],
            "challenge": response.get("content", "Error: no challenge generated.") if response else "Error: no challenge generated.",
        }

    tasks = [run_cross_exam(r) for r in roles_with_context]
    return await asyncio.gather(*tasks)


async def stage3_chairman_verdict(
    user_query: str,
    stage1_results: List[Dict[str, Any]],
    stage2_results: List[Dict[str, Any]],
) -> Dict[str, Any]:
    """
    Stage 3: Chairman synthesizes all views into the two-part verdict.
    """
    advisor_views = "\n\n".join([
        f"=== {r['role'].upper()} ===\n{r['response']}"
        for r in stage1_results
    ])

    challenges = "\n\n".join([
        f"=== {r['role'].upper()}'s CHALLENGE ===\n{r['challenge']}"
        for r in stage2_results
    ])

    chairman_input = f"""ORIGINAL QUESTION:
{user_query}

ADVISOR ANALYSES:
{advisor_views}

CROSS-EXAMINATION (advisors challenging each other):
{challenges}"""

    messages = [{"role": "user", "content": chairman_input}]
    response = await query_model(CHAIRMAN_MODEL, CHAIRMAN_SYSTEM_PROMPT, messages)

    return {
        "role": "Chairman",
        "verdict": response.get("content", "Error: Chairman did not respond.") if response else "Error: Chairman did not respond.",
    }


async def generate_conversation_title(user_query: str) -> str:
    """Generate a short title for the conversation."""
    title_prompt = """Generate a very short title (3-5 words maximum) that summarizes the following question.
No quotes, no punctuation, no explanation — just the title.

Question: """ + user_query + "\n\nTitle:"

    messages = [{"role": "user", "content": title_prompt}]
    response = await query_model(ADVISOR_MODEL, "You generate concise titles.", messages, timeout=30.0)

    if response is None:
        return "New Session"

    title = response.get("content", "New Session").strip().strip('"\'')
    return title[:50] if len(title) > 50 else title


async def run_full_council(user_query: str) -> Tuple[List, List, Dict]:
    """Run the complete 3-stage Straight Dope council."""
    stage1_results = await stage1_advisor_perspectives(user_query)

    if not stage1_results:
        empty_verdict = {"role": "Chairman", "verdict": "All advisors failed to respond. Please try again."}
        return [], [], empty_verdict

    stage2_results = await stage2_cross_examination(user_query, stage1_results)
    stage3_result = await stage3_chairman_verdict(user_query, stage1_results, stage2_results)

    return stage1_results, stage2_results, stage3_result
