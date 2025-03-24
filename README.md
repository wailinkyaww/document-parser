### Document Parser

*Please forgive me if the repository naming sucks.*

**What's this about?**

Building a PDF parsing srvice that can extract useful insights from the document.
Currently focusing on table detection / extraction using a combination of followings:
- YOLOX
- Table Transformers
- algorithmic approach.

**Running FastAPI Application**

To run the application, run the following command:
```shell
doppler run -- poetry run uvicorn src:app --host 0.0.0.0 --port 4000 --workers 1
```

1. `doppler run -- <command>` - we use doppler to inject the env variables fetched from the shared service.
2. `poetry run <command>` - we use poetry to manage the python dependencies. This will look up relevant packages and run the `uvicorn`.
3. `--port 4000` - we need to use `4000` as other services also use 8000, 3000 respectively.
