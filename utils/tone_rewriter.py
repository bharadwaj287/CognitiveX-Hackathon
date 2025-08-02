from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
import streamlit as st

@st.cache_resource
def load_model():
    tokenizer = AutoTokenizer.from_pretrained("gpt2-medium")
    model = AutoModelForCausalLM.from_pretrained("gpt2-medium")
    return pipeline("text-generation", model=model, tokenizer=tokenizer)

tone_model = load_model()

def rewrite_text(original_text: str, tone: str = "suspenseful") -> str:
    """
    Rewrites the given text in the specified tone using a text-generation model.
    Returns only the rewritten portion, cleaned of prompt echoes.
    """
    prompt = (
        f"Rewrite the following scene in a {tone} tone. "
        "Keep the original meaning, but enhance the atmosphere with vivid, expressive language. "
        "Do not add unrelated details or fictional elements."
        f"Original Scene:\n{original_text}\n\n"
        f"{tone.capitalize()} Rewrite:"
    )
    # Generate response
    response = tone_model(prompt)[0]["generated_text"]
    print("🔍 Raw model output:", response)  # Debugging

    # Extract rewritten portion
    rewritten = response.split("Rewrite: ")[-1].strip()

    return rewritten
