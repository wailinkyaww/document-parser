from fastapi import FastAPI

app = FastAPI()


@app.get('/')
def health_check():
    return {"message": 'Document Parser - AI Agent is running fine!'}


@app.get('/detect-table-bounding')
def detect_table_bounding_box():
    return {"table": []}
