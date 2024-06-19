#!/bin/sh

alembic upgrade head
python presentation/cli/main.py

if [ "$APP_DEBUG" = "True" ]; then
    echo "DEBUG MODE"
    uvicorn presentation.api.main:app --host 0.0.0.0 --port 8000 --reload
else
    echo "RELEASE MODE"
    gunicorn presentation.api.main:app -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
fi