# How to run the application
Install Docker on your machine.
> run key.py to generate the SECRET_KEY
create a .env file with the following content:
```
MONGO_URI="mongodb://username:password@localhost:27017/dbname"
GEMINI_API_KEY="your_gemini_api_key"
SECRET_KEY="your_secret_key"
```
`docker compose up --build`.
