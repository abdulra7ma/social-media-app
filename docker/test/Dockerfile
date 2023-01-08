FROM python:3.10.9-bullseye

RUN apt-get update && apt install -y netcat

# Set the working directory
WORKDIR /app

# Copy the required files
COPY . .

# Install the dependencies
RUN pip install -r requirements/test.txt

# copy entrypoint.prod.sh
RUN chmod +x  ./scripts/prestart.sh

# Run the application
ENTRYPOINT ["/app/scripts/prestart.sh"]