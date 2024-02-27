Instantiate qdrant:

docker run -p 6333:6333 -p 6334:6334 \
    -v $(pwd)/qdrant_storage:/qdrant/storage:z \
    qdrant/qdrant

Kill all processes (including qdrant):
docker kill $(docker ps -q)

Run the service:

poetry run uvicorn api:app --reload   