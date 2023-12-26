from diffusers import AutoPipelineForText2Image
import torch

pipeline = AutoPipelineForText2Image.from_pretrained('dataautogpt3/OpenDalleV1.1', torch_dtype=torch.float16).to('cuda')
image = pipeline(
    'black fluffy gorgeous dangerous cat animal creature, large orange eyes, big fluffy ears, piercing gaze, full moon, dark ambiance, best quality, extremely detailed').images[
    0]