import requests


OLLAMA_URL = "http://localhost:11434"


def check_ollama():

    try:
        response = requests.get(f"{OLLAMA_URL}/api/tags", timeout=5)

        response.raise_for_status()

        print("Ollama is running.")

        data = response.json()

        print("Available models:")

        for model in data.get("models", []):
            print("-", model["name"])

    except Exception as error:
        print("Ollama check failed:")

        print(error)


if __name__ == "__main__":
    check_ollama()
