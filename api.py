from fastapi import FastAPI
app=FastAPI()
@app.get("/process")
def process():
    return ({"response": "Processed successfully"})
@app.get("/ask")
def requests():
    return ({"answer": "Object showing different behaviour"})

