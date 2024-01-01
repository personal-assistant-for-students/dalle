from fastapi import FastAPI, BackgroundTasks, Query
from fastapi.responses import FileResponse
from diffusers import AutoPipelineForText2Image
import uuid
import os

app = FastAPI()

MODEL_NAME_STABLE_DIFF = 'runwayml/stable-diffusion-v1-5'


# Функция для генерации изображения
def create_image(description, task_id):
    pipeline = AutoPipelineForText2Image.from_pretrained(MODEL_NAME_STABLE_DIFF).to('cpu')

    pipeline.enable_attention_slicing()  # optimization of gen image Attention Slicing

    image = pipeline(description).images[0]
    # Сохранение изображения
    file_path = f"images/{task_id}.png"
    image.save(file_path)


# Health checker
@app.get("/")
def root():
    return {"message": "Service is working"}


# Эндпоинт для генерации изображения
@app.post("/generate-image")
async def generate_image(request: dict,
                         background_tasks: BackgroundTasks):
    """Generation images in async mode"""
    description = request.get("description", "")
    if not description:
        return {"error": "Description is required"}

    # ID для трекинга процесса генерации
    task_id = str(uuid.uuid4())

    # Запуск генерации изображения в фоновом режиме
    background_tasks.add_task(create_image, description, task_id)

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
