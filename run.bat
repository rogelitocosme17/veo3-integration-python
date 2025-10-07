@echo off

call venv\Scripts\activate

uvicorn server:app --host 127.0.0.1 --port 9000

pause