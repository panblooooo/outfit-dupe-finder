from fastapi import FastAPI
app = FastAPI(title="Outfit Dupe Finder")

@app.get("/health")
def health():
  return {"status": "ok"}