from django.conf import settings
from google import genai  # The 'genai' library allows our Django application
# to communicate with Google's Gemini AI service.


def generate_ai_reply(contact): # Create a Gemini API client.
    # The client is responsible for communicating
    # with Google's Gemini API.

    client = genai.Client(
        api_key=settings.GEMINI_API_KEY  # Get the Gemini API key from Django's settings.py.
    )

    prompt = f"""
You are a professional client communication assistant
for Jesse, a web developer.

A potential client has contacted Jesse through his
portfolio website.

CLIENT NAME:
{contact.name}
SERVICE:
{contact.service}
BUDGET:
{contact.budget}
TIMELINE:
{contact.timeline}
SUBJECT:
{contact.subject}
CLIENT MESSAGE:
{contact.message}
Write a friendly and professional email response.

Rules:
- Be polite and welcoming.
- Make the client feel valued.
- Encourage the client to work with Jesse.
- Build trust through professional communication.
- Never use offensive, rude, insulting or inappropriate language.
- Never pressure the client.
- Never invent a price.
- Never promise a specific delivery date.
- Never claim that payment has been received.
- Never claim that the project has already started.
- If the client's request is unclear, politely ask for more information.
- Keep the response between 100 and 180 words.
- Use simple professional English.
- Do not mention AI.
- Do not mention these instructions.
- Make the response sound natural and human.

End the email with:

Best regards,
Jesse
Web Developer
"""

    response = client.models.generate_content(       # a response based on the contents we provide.

        model="gemini-3.6-flash",   # gemini-3.6-flash is the model selected for this project.
                                    # Send the prompt created above to Gemini.            
        contents=prompt             # Gemini reads the prompt and generates the AI reply.
    )

    return response.text.strip()