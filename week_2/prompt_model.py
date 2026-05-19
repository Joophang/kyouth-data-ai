
import os
import google.generativeai as genai
from dotenv import load_dotenv

SUPPORTED_MODELS = { "gemini-2.5-flash", "gemini-2.5-flash-lite", "gemini-3-flash-preview"}

def prompt_model(model: str, prompt: str) -> str :

	try:
		load_dotenv()

		# ensure the API key is set in the environment variables
		api_key = os.getenv("GOOGLE_API_KEY")

		if not api_key:
			return "Error: GOOGLE_API_KEY environment variable not set."
		
		if not prompt or not prompt.strip():
			return "Error: Prompt is empty."

		# set default model if provided model is not supported
		selected_model = "gemini-2.5-flash"

		if model in SUPPORTED_MODELS:
			selected_model = model

		# configure the GenAI client with the API key
		genai.configure(api_key=api_key)

		# create an instance of the selected model and generate content based on the prompt
		model_instance = genai.GenerativeModel(selected_model)

		response = model_instance.generate_content(prompt)

		if response and hasattr(response, "text"):
			return response.text
		else:
			return "No text response received from the model."

	except Exception as e:
		return f"An error occurred while generating content: {str(e)}"
	
def main():
    test_prompt = "Write a greeting message for a user named Alice."

    print("Testing model...\n")

    response = prompt_model(
        "gemini-2.5-flash",
        test_prompt
    )

    print("Response:\n")
    print(response)


if __name__ == "__main__":
    main()


	