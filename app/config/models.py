DEFAULT_MODEL = "openai/gpt-oss-120b:free"

# Здесь позже можно заменить бесплатные модели на платные без изменения Worker.
WORKER_MODELS = {
    "devops": DEFAULT_MODEL,
    "marketing": DEFAULT_MODEL,
    "qa": DEFAULT_MODEL,
}
