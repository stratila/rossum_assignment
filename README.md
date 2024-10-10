Copy and paste `.env` from submission files


Activate a virtual environment and install the dependencies:

```bash
python3.12 -m venv .venv
pip install -r requirements.txt
pip install -e ./src   
```

Build and run docker container
```bash
docker build -t rossum_api_assign .    
docker run --name rossum_api_assign_cont -p 8080:8000 --env-file .env -v "$(pwd)/src:/src" -d rossum_api_assign
```


Run test:

```bash
pytest tests
```

API:

`GET /exports`

Params: `queue_id` - int - required
Params: `annotation_id` - int- required



```
Annotation examples:
http://localhost:8080/test_result?queue_id=1355018&annotation_id=4379183  
http://localhost:8080/test_result?queue_id=1355018&annotation_id=4379164
http://localhost:8080/test_result?queue_id=1355018&annotation_id=4379179
http://localhost:8080/test_result?queue_id=1355018&annotation_id=4379186
```
