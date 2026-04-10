import os
import anthropic
from dotenv import load_dotenv

load_dotenv()

client = anthropic.Anthropic(api_key=os.getenv("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"))

reponse = client.messages.create(
    model      = "claude-opus-4-5",
    max_tokens = 200,
    messages   = [
        {
            "role":    "user",
            "content": "Dis bonjour en français en une phrase."
        }
    ]
)

print(reponse.content[0].text)