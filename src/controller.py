from fastapi import FastAPI, BackgroundTasks, Query
from fastapi.responses import FileResponse
from diffusers import AutoPipelineForText2Image
import torch
import uuid
import os

app = FastAPI()

MODEL_NAME_DALLE = 'dataautogpt3/OpenDalleV1.1'
MODEL_NAME_STABLE_DIFF = 'runwayml/stable-diffusion-v1-5'


# Функция для генерации изображения
def create_image(description, task_id, is_dalle):
    if is_dalle is not True and torch.cuda.is_available() is not True:
        device = "mps"  # mps on Dalle has issue with dtype https://github.com/huggingface/diffusers/issues/1056
        dtype = torch.float32
        model_name = MODEL_NAME_STABLE_DIFF
    else:
        device = "cuda" if torch.cuda.is_available() else "cpu"
        dtype = torch.float16 if device == "cuda" else torch.float32
        model_name = MODEL_NAME_DALLE if is_dalle else MODEL_NAME_STABLE_DIFF

    pipeline = AutoPipelineForText2Image.from_pretrained(model_name, torch_dtype=dtype).to(device)

    pipeline.enable_attention_slicing()  # optimization of gen image Attention Slicing

    image = pipeline(description).images[0]
    # Сохранение изображения
    file_path = f"images/{task_id}.png"
    image.save(file_path)

    # Освобождение кэша
    if device == "cuda":
        torch.cuda.empty_cache()
    else:
        torch.mps.empty_cache()


# Эндпоинт для генерации изображения
@app.post("/generate-image")
async def generate_image(request: dict,
                         background_tasks: BackgroundTasks,
                         is_dalle: bool = Query(False, description="Flag to use DALL-E model or not"), ):
    """Generation images in async mode"""
    description = request.get("description", "")
    if not description:
        return {"error": "Description is required"}

    # ID для трекинга процесса генерации
    task_id = str(uuid.uuid4())

    # Запуск генерации изображения в фоновом режиме
    background_tasks.add_task(create_image, description, task_id, is_dalle)

    return {"task_id": task_id}


# Эндпоинт для получения статуса генерации и ссылки на скачивание
@app.get("/status/{task_id}")
async def get_status(task_id: str):
    """Checking the status and way to download completed file"""
    file_path = f"images/{task_id}.png"
    if os.path.exists(file_path):
        return {"status": "completed", "url": f"/download/{task_id}"}
    else:
        return {"status": "in_progress"}


# Эндпоинт для скачивания изображения
@app.get("/download/{task_id}")
async def download_image(task_id: str):
    """Downloading file"""
    file_path = f"images/{task_id}.png"
    if os.path.exists(file_path):
        return FileResponse(file_path)
    else:
        return {"error": "Image not found"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
