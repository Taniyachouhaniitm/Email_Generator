# chains.py
import os
import re
from dotenv import load_dotenv

from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.exceptions import OutputParserException

load_dotenv()


def extract_json_from_text(text: str) -> str:
    """
    Extract the first valid JSON object or array from text.
    This protects against <think> tags and any stray text.
    """
    match = re.search(r"(\{[\s\S]*\}|\[[\s\S]*\])", text)
    if not match:
        raise OutputParserException("No valid JSON found in model output")
    return match.group(1)


class Chain:
    def __init__(self):
        self.llm = ChatGroq(
            model="qwen/qwen3-32b",
            temperature=0,
            groq_api_key=os.getenv("GROQ_API_KEY")
        )

        self.parser = JsonOutputParser()

    def extract_jobs(self, cleaned_text: str):
        """
        Extract job postings from scraped career page text.
        Returns a list of job dicts.
        """

        prompt_extract = PromptTemplate.from_template(
            """
### SCRAPED TEXT FROM WEBSITE:
{page_data}

### INSTRUCTION:
Extract job postings and return ONLY valid JSON.

STRICT RULES:
- No explanations
- No markdown
- No text before or after JSON
- If no jobs exist, return []

Each job must contain:
- role (string)
- experience (string)
- skills (array of strings)
- description (string)

### JSON FORMAT:
{format_instructions}
"""
        )

        chain = prompt_extract | self.llm

        try:
            # 1Get raw LLM output
            raw_output = chain.invoke({
                "page_data": cleaned_text,
                "format_instructions": self.parser.get_format_instructions()
            }).content

            # Remove any <think> blocks (Qwen3 safety)
            raw_output = re.sub(
                r"<think>[\s\S]*?</think>",
                "",
                raw_output,
                flags=re.IGNORECASE
            ).strip()

            # Extract JSON only
            json_text = extract_json_from_text(raw_output)

            # Parse JSON safely
            result = self.parser.parse(json_text)

            # Normalize output
            if isinstance(result, dict):
                return [result]

            return result

        except Exception as e:
            raise OutputParserException(
                "JSON parsing failed after sanitization.\n\n"
                f"RAW OUTPUT:\n{raw_output}\n\n"
                f"ERROR:\n{e}"
            )

    def write_mail(self, job: dict, links: list[str]) -> str:
        """
        Generate professional cold referral email.
        Returns plain text email.
        """

        job_text = f"""
Role: {job.get('role', '')}
Experience: {job.get('experience', '')}
Skills: {', '.join(job.get('skills', []))}
Description: {job.get('description', '')}
"""

        prompt_email = PromptTemplate.from_template(
            """
You are Taniya, a Business Development Executive at XYZ Solutions.

Write a professional cold referral email.

FORMAT STRICTLY:

Subject: <concise subject related to role>

Dear Hiring Manager,

<Opening paragraph introducing XYZ Solutions and referencing the role>

<Technical capability paragraph aligned with the role>

<Portfolio paragraph with exactly 2 bullet points using links from: {link_list}>
* >
* >

<Paragraph about scalability, optimization, and efficiency>

<Closing paragraph requesting a discussion>

Best regards,
Taniya
Business Development Executive | XYZ Solutions

RULES:
- No markdown
- No thinking
- No explanations
- Output ONLY the email
- Start from Subject:
"""
        )

        res = (prompt_email | self.llm).invoke({
            "job_description": job_text,
            "link_list": links
        })

        # Final cleanup (extra safety)
        email_content = re.sub(r"<think>[\s\S]*?</think>", "", res.content)
        email_content = re.sub(r"\n\s*\n", "\n\n", email_content.strip())

        return email_content


if __name__ == "__main__":
    print("GROQ_API_KEY loaded:", bool(os.getenv("GROQ_API_KEY")))
    print("CHAIN VERSION: QWEN3 SAFE JSON v1")
