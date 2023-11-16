FROM python:3.11-slim

# Install FastAPI, Uvicorn, and other dependencies
RUN pip3 install fastapi uvicorn[standard]
RUN pip3 install python-multipart
RUN pip3 install loguru
RUN pip3 install alembic
RUN pip3 install pydantic-settings

# Install MongoDB driver for Python
RUN pip3 install motor

WORKDIR /bot_configuration
# COPY .. /server

