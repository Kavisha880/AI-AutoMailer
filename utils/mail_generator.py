import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


def generate_mail(role, company, jd):

    prompt = f"""
You are an expert cold outreach writer helping a fresher apply for AI/ML and Generative AI roles.

Candidate Information

Name: Kavisha Gupta

Phone:
+91 6388247619

Email:
kavishagupta8806@gmail.com

Portfolio:
https://porfolio-iota-red.vercel.app/

Skills:
- Python
- SQL
- Pandas
- Machine Learning
- LangChain
- LangGraph
- RAG
- OpenAI
- Hugging Face
- Streamlit

Projects:

1. AutoMailer AI
- AI-powered cold email automation platform
- Extracts hiring information from job descriptions
- Generates personalized outreach emails using LLMs
- Supports Excel and text-based workflows

2. ResuMatch AI
- ATS-friendly resume optimization system
- Uses ChromaDB and LLM-powered retrieval
- Generates tailored resumes and cold emails
- Reduced preparation time from 30–45 minutes to under 5 minutes

3. GenQuizAI
- AI-powered quiz generation platform
- Multi-model evaluation and comparison

4. Movie Recommendation System
- TF-IDF and cosine similarity recommendation engine

Target Company:
{company}

Target Role:
{role}

Job Description:
{jd}

SUBJECT RULES

- Write a professional subject line.
- Suitable for a fresher.
- Keep it concise.
- Prefer styles like:

  Enquiry Regarding <Role>
  Regarding Your <Role> Opening
  Interest in <Role>
  Enquiry for <Role> Opportunity

- Avoid:
  Application for...
  Job Application...
  Resume Attached...
  Urgent...
  Sales-style subjects

EMAIL RULES

Opening:
- Show that the JD was actually read.
- Reference company, role, technology stack or requirements.

Context:
- Explain why reaching out.

Value:
- Mention only the most relevant 1-2 projects.
- Do NOT simply list projects.
- Explain why those projects are relevant.
- Connect project experience to the JD requirements.
- Mention specific technologies found in the JD whenever relevant.

Portfolio:
- Include naturally.

Resume:
- Mention resume is attached.

CTA:
- Ask for a simple reply.
- Keep it low-pressure and professional.

Tone:
- Human
- Intelligent
- Confident
- Professional
- Conversational
- Not overly enthusiastic
- Not corporate sounding

Length:
- 220 to 300 words

Output Format:

Subject: ...

<email body>

Best Regards,

Kavisha Gupta
+91 6388247619
kavishagupta8806@gmail.com
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.8
    )

    return response.choices[0].message.content