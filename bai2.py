from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel

app = FastAPI()

enrollments = [
    {
        "id": 1,
        "student_id": "SV001",
        "course_id": 1
    },
    {
        "id": 2,
        "student_id": "SV002",
        "course_id": 1
    }
]

class EnrollmentCreate(BaseModel):
    student_id: str
    course_id: int


@app.post("/enrollments", status_code=status.HTTP_201_CREATED)
def create_enrollment(enrollment: EnrollmentCreate):

    # Kiểm tra học viên đã đăng ký khóa học hay chưa
    for item in enrollments:
        if (
            item["student_id"] == enrollment.student_id
            and item["course_id"] == enrollment.course_id
        ):
            raise HTTPException(
                status_code=400,
                detail="Student already enrolled in this course"
            )

    new_enrollment = {
        "id": len(enrollments) + 1,
        "student_id": enrollment.student_id,
        "course_id": enrollment.course_id
    }

    enrollments.append(new_enrollment)

    return {
        "message": "Enroll successfully",
        "data": new_enrollment
    }
  # LỖI:
    # API tạo bản ghi đăng ký mới ngay mà không kiểm tra
    # học viên (student_id) đã đăng ký khóa học (course_id) này hay chưa.
    # Vì vậy một học viên có thể đăng ký cùng một khóa học nhiều lần,
    # làm dữ liệu đăng ký bị trùng.

    # CÁCH SỬA:
    # Trước khi thêm bản ghi mới, duyệt danh sách enrollments.
    # Nếu tồn tại bản ghi có cùng student_id và course_id
    # thì raise HTTPException(status_code=400,
    # detail="Student already enrolled in this course").
    # Nếu chưa tồn tại thì mới thêm đăng ký mới.
    # Đồng thời trả về HTTP status code 201 Created.