from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional, List

app = FastAPI()

class Bookmark(BaseModel):
    id: Optional[int] = None
    title: str
    url: str
    description: Optional[str] = None

bookmarks: List[Bookmark] = []

@app.post("/bookmarks/")
def create_bookmark(bookmark: Bookmark):
    bookmark.id = len(bookmarks) + 1
    bookmarks.append(bookmark)
    return bookmark

@app.get("/bookmarks/")
def read_bookmarks():
    return bookmarks

@app.put("/bookmarks/{bookmark_id}")
def update_bookmark(bookmark_id: int, bookmark: Bookmark):
    for index, b in enumerate(bookmarks):
        if b.id == bookmark_id:
            bookmarks[index] = bookmark
            return bookmark
    return {"error": "Bookmark not found"}, 404

@app.delete("/bookmarks/{bookmark_id}")
def delete_bookmark(bookmark_id: int):
    for index, b in enumerate(bookmarks):
        if b.id == bookmark_id:
            del bookmarks[index]
            return {"status": "deleted"}
    return {"error": "Bookmark not found"}, 404
