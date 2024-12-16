#from huggingface_hub import login
#login()

#Set-ExecutionPolicy RemoteSigned -Scope Process
#python -m venv .env

from transformers import pipeline

# Use GPT-2 model as a fallback
generator = pipeline('text-generation', model="gpt2")
output = generator("Please, before your answer write Output: , then answer this question. What is a dog?", max_length=150, num_return_sequences=1)

print(output)


'''
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

model_name = "AI-Sweden-Models/gpt-sw3-356m"
device = "cuda:0" if torch.cuda.is_available() else "cpu"

# Use AutoTokenizer with use_fast=False to avoid errors with non-fast tokenizers
tokenizer = AutoTokenizer.from_pretrained(model_name, use_fast=False)
model = AutoModelForCausalLM.from_pretrained(model_name)

model.eval()
model.to(device)

prompt = "Träd är fina för att"
input_ids = tokenizer(prompt, return_tensors="pt")["input_ids"].to(device)

# Generate text
generated_token_ids = model.generate(
    inputs=input_ids,
    max_new_tokens=100,
    do_sample=True,
    temperature=0.6,
    top_p=1,
)[0]

# Decode the generated text
generated_text = tokenizer.decode(generated_token_ids, skip_special_tokens=True)
print(generated_text)
'''