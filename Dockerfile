#Step 1: Use python image as base image
FROM python:3.11-slim
#Step 2: Set the working directory inside the container
WORKDIR /app
#Step 3: Copy only the requiremints file first
#this helps with caching builds so builds are faster
COPY requirements.txt .

#Step 4: Install the dependencies
RUN pip install -r requirements.txt

#Step 5: Copy the rest of the application code
COPY . .
#Step 6: Set the command to run the application

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]