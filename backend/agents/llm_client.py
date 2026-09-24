import os
import json
import subprocess
import time

from dotenv import load_dotenv
from azure.core.credentials import TokenCredential, AccessToken
from azure.ai.projects import AIProjectClient

load_dotenv()

PROJECT_ENDPOINT = os.getenv("FOUNDRY_PROJECT_ENDPOINT")
AGENT_NAME = os.getenv("FOUNDRY_AGENT_NAME")


class AzureCliTokenCredential(TokenCredential):
    """
    Gets an Azure token from the already logged-in Azure CLI.

    This is for local development only.
    """

    def get_token(self, *scopes, **kwargs):

        result = subprocess.run(
            [
                r"C:\Program Files\Microsoft SDKs\Azure\CLI2\wbin\az.cmd",
                "account",
                "get-access-token",
                "--output",
                "json",
                "--resource",
                "https://ai.azure.com",
            ],
            capture_output=True,
            text=True,
            timeout=30,
        )

        if result.returncode != 0:
            raise RuntimeError(
                "Azure CLI authentication failed:\n"
                + result.stderr
            )

        data = json.loads(result.stdout)

        return AccessToken(
            data["accessToken"],
            int(data["expires_on"])
        )


print("PROJECT_ENDPOINT:", PROJECT_ENDPOINT)
print("AGENT_NAME:", AGENT_NAME)

credential = AzureCliTokenCredential()

project = AIProjectClient(
    endpoint=PROJECT_ENDPOINT,
    credential=credential,
    allow_preview=True,
)

print("Project client created")

openai_client = project.get_openai_client(
    agent_name=AGENT_NAME
)

print("Agent OpenAI client created")


def generate_response(system_prompt: str, user_prompt: str):

    try:

        prompt = f"""
{system_prompt}

User:
{user_prompt}
"""

        print("Calling Foundry Agent...")

        response = openai_client.responses.create(
            input=prompt
        )

        print("FOUND RESPONSE:")
        print(response.output_text)

        return response.output_text

    except Exception as e:

        print("========== FOUNDRY ERROR ==========")
        print(type(e).__name__)
        print(str(e))
        print("===================================")

        return None


def is_azure_active():
    return bool(PROJECT_ENDPOINT) and bool(AGENT_NAME)