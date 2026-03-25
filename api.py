from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Optional
from database import Database
import sqlite3


app = FastAPI(title="Student Management API", version="1.0")


class StudentCreate(BaseModel):
    roll_no: int
    name: str
    course: str

class StudentUpdate(BaseModel):
    name: str

class StudentResponse(BaseModel):
    id: int
    roll_no: int
    name: str
    course: str

# Dependency to get database instance per request
def get_db():
    """create a new database connection for each request """
    db = Database()
    try:
        yield db
    finally:
        db.close()



@app.get("/", tags=["Root"])
def read_root():
    """Welcome endpoint"""
    return {"message": "Welcome to Student Management API"}

@app.get("/students", response_model=List[StudentResponse], tags=["Students"])
def get_all_students(db: Database = Depends(get_db)):
    """Get all students"""
    try:
        result = db.execute("SELECT id, roll_no, name, course FROM students")
        rows = result.fetchall()
        
        if not rows:
            return []
        
        students = [
            {"id": row[0], "roll_no": row[1], "name": row[2], "course": row[3]}
            for row in rows
        ]
        return students
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/students/{roll_no}", response_model=List[StudentResponse], tags=["Students"])
def search_by_roll(roll_no: int, db: Database = Depends(get_db)):
    """Search student by roll number"""
    try:
        result = db.execute(
            "SELECT id, roll_no, name, course FROM students WHERE roll_no=?",
            (roll_no,)
        )
        rows = result.fetchall()
        
        if not rows:
            raise HTTPException(status_code=404, detail=f"No student found with roll number {roll_no}")
        
        students = [
            {"id": row[0], "roll_no": row[1], "name": row[2], "course": row[3]}
            for row in rows
        ]
        return students
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/students/search/name/{name}", response_model=List[StudentResponse], tags=["Students"])
def search_by_name(name: str, db: Database = Depends(get_db)):
    """Search student by name"""
    try:
        result = db.execute(
            "SELECT id, roll_no, name, course FROM students WHERE name LIKE ?",
            ("%" + name + "%",)
        )
        rows = result.fetchall()
        
        if not rows:
            raise HTTPException(status_code=404, detail=f"No student found with name '{name}'")
        
        students = [
            {"id": row[0], "roll_no": row[1], "name": row[2], "course": row[3]}
            for row in rows
        ]
        return students
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/students/course/{course}", response_model=List[StudentResponse], tags=["Students"])
def filter_by_course(course: str, db: Database = Depends(get_db)):
    """Filter students by course"""
    try:
        result = db.execute(
            "SELECT id, roll_no, name, course FROM students WHERE course LIKE ?",
            ("%" + course + "%",)
        )
        rows = result.fetchall()
        
        if not rows:
            raise HTTPException(status_code=404, detail=f"No student found in course '{course}'")
        
        students = [
            {"id": row[0], "roll_no": row[1], "name": row[2], "course": row[3]}
            for row in rows
        ]
        return students
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



@app.post("/students", response_model=dict, tags=["Students"])
def add_student(student: StudentCreate, db: Database = Depends(get_db)):
    """Add a new student"""
    try:
        db.execute(
            "INSERT INTO students(roll_no, name, course) VALUES (?, ?, ?)",
            (student.roll_no, student.name, student.course)
        )
        return {"message": "Student added successfully", "student": student.dict()}
    except sqlite3.IntegrityError:
        raise HTTPException(
            status_code=400,
            detail="Student with this roll number already exists in this course"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



@app.put("/students/{roll_no}/{course}", response_model=dict, tags=["Students"])
def update_student(roll_no: int, course: str, student_update: StudentUpdate, db: Database = Depends(get_db)):
    """Update student name by roll number and course"""
    try:
        # Check if student exists
        result = db.execute(
            "SELECT * FROM students WHERE roll_no=? AND course=?",
            (roll_no, course)
        )
        existing = result.fetchone()
        
        if not existing:
            raise HTTPException(
                status_code=404,
                detail=f"No student found with roll no {roll_no} in course {course}"
            )
        
        # Update student
        db.execute(
            "UPDATE students SET name=? WHERE roll_no=? AND course=?",
            (student_update.name, roll_no, course)
        )
        return {"message": "Student updated successfully", "roll_no": roll_no, "course": course, "new_name": student_update.name}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



@app.delete("/students/{roll_no}/{course}", response_model=dict, tags=["Students"])
def delete_student(roll_no: int, course: str, db: Database = Depends(get_db)):
    """Delete student by roll number and course"""
    try:
        # Check if student exists
        result = db.execute(
            "SELECT * FROM students WHERE roll_no=? AND course=?",
            (roll_no, course)
        )
        existing = result.fetchone()
        
        if not existing:
            raise HTTPException(
                status_code=404,
                detail=f"No student found with roll no {roll_no} in course {course}"
            )
        
    
        db.execute(
            "DELETE FROM students WHERE roll_no=? AND course=?",
            (roll_no, course)
        )
        return {"message": "Student deleted successfully", "roll_no": roll_no, "course": course}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
