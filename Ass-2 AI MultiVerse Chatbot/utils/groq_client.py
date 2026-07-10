import os
from groq import Groq, GroqError

def get_groq_client():
    """Initializes and returns the Groq client."""
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError("GROQ_API_KEY environment variable is not set.")
    return Groq(api_key=api_key)

def generate_chat_response(messages, model, temperature, max_tokens):
    """
    Sends a request to the Groq API and yields the response stream.
    
    Args:
        messages (list): List of message dictionaries.
        model (str): The Groq model to use.
        temperature (float): The temperature for generation.
        max_tokens (int): Maximum tokens to generate.
        
    Yields:
        str: Chunks of the generated response.
    """
    try:
        client = get_groq_client()
        stream = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
            stream=True
        )
        
        for chunk in stream:
            if chunk.choices[0].delta.content is not None:
                yield chunk.choices[0].delta.content
                
    except GroqError as e:
        yield f"\n\n**Groq API Error:** {str(e)}"
    except ValueError as e:
        yield f"\n\n**Configuration Error:** {str(e)}"
    except Exception as e:
        yield f"\n\n**Unexpected Error:** {str(e)}"
