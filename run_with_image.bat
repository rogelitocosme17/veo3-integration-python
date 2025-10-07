@echo off

call venv\Scripts\activate

uvicorn server_image:app --host 127.0.0.1 --port 9000

pause