# chains.py
import os
import re
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.exceptions import OutputParserException

load_dotenv()


class Chain:
    def __init__(self):
        self.llm = ChatGroq(
            temperature=0,
            groq_api_key=os.getenv("GROQ_API_KEY"),
            model="qwen/qwen3-32b"
        )
        # JSON parser enforces structure
        self.parser = JsonOutputParser()

    def extract_jobs(self, cleaned_text):
        """
        Extract job postings from a cleaned text string.
        Returns a list of jobs (each as dict).
        """
        prompt_extract = PromptTemplate.from_template(
            """
### SCRAPED TEXT FROM WEBSITE:
{page_data}

### INSTRUCTION:

Only provide the final answer.
The scraped text is from the career's page of a website.
Your job is to extract the job post and return it in JSON format containing the following keys:
'role', 'experience', 'skills', and 'description'.

Extract all job postings from the text above.

Each job MUST contain:
- role (string)
- experience (string)
- skills (array of strings)
- description (string)

STRICT RULES:
- Answer the question directly and concisely.
- Do NOT show your reasoning.
- Do NOT include thoughts, explanations, or analysis.
- Do NOT Provide <think> </think>
- If multiple jobs exist, return a JSON array
- If no jobs exist, return []

Only return the valid JSON.
### VALID JSON (NO PREAMBLE):

{format_instructions}
"""
        )

        chain = prompt_extract | self.llm | self.parser

        try:
            result = chain.invoke({
                "page_data": cleaned_text,
                "format_instructions": self.parser.get_format_instructions()
            })

            # Clean any HTML tags
            if isinstance(result, str):
                cleaned_result = re.sub(r"<.*?>", "", result).strip()
                result = self.parser.parse(cleaned_result)

            # Wrap dict in list if only one job
            if isinstance(result, dict):
                return [result]

            return result

        except OutputParserException as e:
            raise OutputParserException(
                "Unable to parse job postings into valid JSON.\n"
                f"LLM Output:\n{e}"
            )

    def write_mail(self, job, links):
        """
        Generate a professional cold email for a given job posting.
        Returns only plain text email.
        """
        # Convert job dict into readable text
        job_text = f"""
Role: {job.get('role', '')}
Experience: {job.get('experience', '')}
Skills: {', '.join(job.get('skills', []))}
Description: {job.get('description', '')}
"""

        prompt_email = PromptTemplate.from_template(
            """
### JOB DESCRIPTION:
{job_description}

### INSTRUCTION:
You are Taniya, a Business Development Executive at XYZ Solutions, an AI & Software Consulting company.

Write a professional cold email strictly in the format below. Follow the structure, tone, and flow.

FORMAT TO FOLLOW:

Subject: <One concise professional subject related to the role>

Dear Hiring Manager,

<Opening paragraph: mention the role from job description and introduce XYZ Solutions>

<Second paragraph: describe technical capabilities aligned with the job>

<Portfolio paragraph: introduce 2 relevant examples using links from: {link_list}, in bullet points starting with * >

<Paragraph about company impact: scalability, optimization, cost reduction, efficiency>

<Closing paragraph: express interest in a discussion>

Best regards,
Taniya
Business Development Executive | XYZ Solutions

STRICT RULES:
- Use the name Taniya only.
- Use company name XYZ Solutions only.
- Do NOT use markdown, bold, or special formatting.
- Do NOT add greetings like Hi.
- Do NOT include any contact details.
- Output ONLY the email.
- Start from Subject: 
- Do NOT include any instructions or explanations in the output.

### EMAIL:
"""
        )

        chain_email = prompt_email | self.llm
        res = chain_email.invoke({
            "job_description": job_text,
            "link_list": links
        })

        # Clean HTML tags and extra newlines
        email_content = re.sub(r"<.*?>", "", res.content)
        
        # Ensure it starts from Subject
        match = re.search(r"(Subject:.*)", email_content, re.DOTALL)
        if match:
            email_content = match.group(1)
        else:
            email_content = email_content.strip()

        # Remove extra blank lines
        email_content = re.sub(r"\n\s*\n", "\n\n", email_content.strip())

        return email_content


if __name__ == "__main__":
    print("GROQ_API_KEY loaded:", bool(os.getenv("GROQ_API_KEY")))
    print("CHAIN VERSION: JSON-LOCKED v2")
