from faster_whisper import WhisperModel

from settings import *


WhisperModel(model_size, device=model_device, compute_type=compute_type)
