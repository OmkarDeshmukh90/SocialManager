from transformers import pipeline

# Initialize text generation pipeline (using distilgpt2 as an example)
generator = pipeline("text-generation", model="distilgpt2")

def generate_text(prompt):
    """
    Generate text based on the provided prompt.
    This function is used for generating toots with diverse topics.
    """
    response = generator(prompt, max_length=100, do_sample=True)
    return response[0]['generated_text']

def generate_personality_reply(prompt, personality="witty"):
    """
    Generate a witty reply based on the provided prompt.
    """
    full_prompt = f"As a {personality} AI bot, reply to this: {prompt}"
    response = generator(full_prompt, max_length=50, do_sample=True)
    return response[0]['generated_text']
