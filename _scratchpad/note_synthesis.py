import anthropic
import os
from collections import defaultdict
from typing import List, Dict

# Initialize the Anthropic client
# Note: You'll need to set your API key as an environment variable
client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

def read_life_tips(file_path: str) -> List[str]:
    """
    Read life tips from a file.
    Each tip should be on a new line.
    """
    with open(file_path, 'r') as file:
        return [line.strip() for line in file if line.strip()]

def create_initial_categories(tips: List[str]) -> List[str]:
    """
    Use Claude to suggest initial broad categories based on the tips.
    """
    # Prepare a sample of tips for Claude to analyze
    sample_tips = "\n".join(tips[:50])  # Use first 50 tips as a sample

    prompt = f"""Based on the following sample of life tips, suggest 5-10 broad categories that could be used to organize all ~500 tips. Just list the categories, don't explain them.

Sample tips:
{sample_tips}

Categories:"""

    response = client.messages.create(
        model="claude-3-sonnet-20240229",
        max_tokens=300,
        temperature=0,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    # Extract categories from Claude's response
    categories = response.content[0].text.strip().split("\n")
    return [cat.strip() for cat in categories if cat.strip()]

def categorize_tips(tips: List[str], categories: List[str]) -> Dict[str, List[str]]:
    """
    Use Claude to categorize each tip into one of the broad categories.
    """
    categorized_tips = defaultdict(list)

    for tip in tips:
        prompt = f"""Categorize the following life tip into one of these categories: {', '.join(categories)}.
        Just respond with the category name, nothing else.

        Tip: {tip}

        Category:"""

        response = client.messages.create(
            model="claude-3-sonnet-20240229",
            max_tokens=50,
            temperature=0,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        category = response.content[0].text.strip()
        categorized_tips[category].append(tip)

    return dict(categorized_tips)

def create_subcategories(category: str, tips: List[str]) -> List[str]:
    """
    Use Claude to suggest subcategories for a given category and its tips.
    """
    tips_sample = "\n".join(tips[:20])  # Use first 20 tips as a sample

    prompt = f"""For the category "{category}", suggest 3-5 subcategories based on these sample tips. Just list the subcategories, don't explain them.

Sample tips:
{tips_sample}

Subcategories:"""

    response = client.messages.create(
        model="claude-3-sonnet-20240229",
        max_tokens=200,
        temperature=0,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    subcategories = response.content[0].text.strip().split("\n")
    return [subcat.strip() for subcat in subcategories if subcat.strip()]

def synthesize_tips(subcategory: str, tips: List[str]) -> str:
    """
    Use Claude to synthesize tips within a subcategory.
    """
    tips_text = "\n".join(tips)

    prompt = f"""Synthesize the following tips for the subcategory "{subcategory}".
    Combine similar ideas, create overarching principles, and list specific examples.
    Maintain all unique insights and context. Provide the synthesis in markdown format.

    Tips:
    {tips_text}

    Synthesized content:"""

    response = client.messages.create(
        model="claude-3-sonnet-20240229",
        max_tokens=1000,
        temperature=0,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    return response.content[0].text.strip()

def main(file_path: str):
    # Step 1: Read life tips
    tips = read_life_tips(file_path)

    # Step 2: Create broad categories
    categories = create_initial_categories(tips)

    # Step 3: First-pass categorization
    categorized_tips = categorize_tips(tips, categories)

    # Steps 4-7: Subcategorization, synthesis, and summary
    final_structure = {}
    for category, tips in categorized_tips.items():
        subcategories = create_subcategories(category, tips)
        subcategorized_tips = categorize_tips(tips, subcategories)

        synthesized_subcategories = {}
        for subcategory, subtips in subcategorized_tips.items():
            synthesized_content = synthesize_tips(subcategory, subtips)
            synthesized_subcategories[subcategory] = synthesized_content

        final_structure[category] = synthesized_subcategories

    # Step 8: Create hierarchical structure (already done in the dictionary structure)

    # Step 9: Review and refine (This would typically be a manual step)

    # Output the result (you might want to save this to a file instead)
    for category, subcategories in final_structure.items():
        print(f"# {category}")
        for subcategory, content in subcategories.items():
            print(f"## {subcategory}")
            print(content)
            print()

if __name__ == "__main__":
    file_path = "life_tips.txt"  # Replace with your file path
    main(file_path)
