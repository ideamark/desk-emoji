from openai import OpenAI


# OpenAI API
client = OpenAI(
    base_url = "",
    api_key = ""
)

# Whisper
model_size = "large-v3"
model_device = "cpu"
compute_type = "int8"   # int8 for CPU, float16, float32 for GPU.
model_language = "zh"
