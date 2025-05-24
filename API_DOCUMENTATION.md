# CS Learn Track API Documentation

---

## Authentication

### `POST /add_face_encoding/`
**Auth Required:** Yes — JWT Bearer (student)

**Request Body:**
```json
{
  "face_image": "string (required, base64-encoded image)"
}
```
Response (200 OK):
```json
{
  "message": "Face encoding added successfully",
  "status": 200
}
```
Status Codes:

- 200 OK
- 400 Bad Request (invalid data, no face detected, or error processing image)
- 403 Forbidden (only students can add face encoding)
- 401 Unauthorized (missing/invalid token)

---

### `POST /student/login_face/`
**Auth Required:** No

**Request Body:**
```json
{
  "admissionNo": "integer (required)",
  "login_image": "string (required, base64-encoded image)"
}
```
Response (200 OK):
```json
{
  "message": "Student logged in successfully",
  "name": "string",
  "status": 200,
  "refresh": "string",
  "access": "string"
}
```
Status Codes:

- 200 OK
- 400 Bad Request (invalid data, student not found, face encoding not found, no face detected, or face does not match)

---

**Note:** For all face recognition endpoints, the image must be sent as a base64-encoded string. If using a data URL, only the base64 part is required, but the API can handle both formats.

---

### `POST /student/login/`
**Auth Required:** No

**Request Body:**
```json
{
  "admissionNo": "integer (required)",
  "studentPassword": "string (required)"
}
```
Response (200 OK):
```json
{
  "message": "Student logged in successfully",
  "name": "string",
  "status": 200,
  "refresh": "string",
  "access": "string"
}
```
Status Codes:

- 200 OK
- 400 Bad Request (invalid data, student not found, or wrong password)

---

### `POST /teacher/login/`
**Auth Required:** No

**Request Body:**
```json
{
  "email": "string (required)",
  "teacherPassword": "string (required)"
}
```
Response (200 OK):
```json
{
  "message": "Teacher logged in successfully",
  "name": "string",
  "status": 200,
  "refresh": "string",
  "access": "string"
}
```
Status Codes:

- 200 OK
- 400 Bad Request (invalid data, teacher not found, or wrong password)

---

### `POST /adminendpoint/login/`
**Auth Required:** No

**Request Body:**
```json
{
  "username": "string (required)",
  "password": "string (required)"
}
```
Response (200 OK):
```json
{
  "message": "Admin logged in successfully",
  "status": 200
}
```
Status Codes:

- 200 OK
- 400 Bad Request (invalid data, admin not found, or wrong password)

---

### `POST /logout/`
**Auth Required:** Yes — JWT Bearer (student/teacher)

**Request Body:**
```json
{
  "refresh": "string (optional)"
}
```
Response (200 OK):
```json
{
  "message": "Logged out successfully",
  "status": 200
}
```
Status Codes:

- 200 OK
- 400 Bad Request (invalid token)
- 401 Unauthorized (missing/invalid token)

---

### `POST /token/refresh/`
**Auth Required:** No

**Request Body:**
```json
{
  "refresh": "string (required)"
}
```
Response (200 OK):
```json
{
  "access": "string",
  "status": 200
}
```
Status Codes:

- 200 OK
- 400 Bad Request (invalid token)

---

## User Management

### `POST /student/register/`
**Auth Required:** Yes — JWT Bearer (teacher)

**Request Body:**
```json
{
  "studentName": "string (required)",
  "studentClass": "string (required)",
  "division": "string (required)",
  "gender": "string (required)",
  "fatherName": "string (required)",
  "email": "string (required)",
  "contactNo": "string (required)",
  "joinedDate": "date (required)",
  "studentPassword": "string (required)",
  "batch": "integer (required)",
  "profilePic": "file (optional)"
}
```
Response (201 Created):
```json
{
  "message": "Student registered successfully",
  "admissionNo": "integer",
  "status": 201
}
```
Status Codes:

- 201 Created
- 400 Bad Request (invalid data, batch not found)
- 401 Unauthorized (missing/invalid token)
- 403 Forbidden (wrong role)

---

### `POST /teacher/register/`
**Auth Required:** No

**Request Body:**
```json
{
  "name": "string (required)",
  "email": "string (required)",
  "contactNo": "string (required)",
  "hireDate": "date (required)",
  "teacherPassword": "string (required)",
  "profilePic": "file (optional)"
}
```
Response (201 Created):
```json
{
  "message": "Teacher registered successfully",
  "status": 201
}
```
Status Codes:

- 201 Created
- 400 Bad Request (invalid data)

---

### `POST /CheckUserTypeEndPoint/`
**Auth Required:** Yes — JWT Bearer (teacher/student)

**Request Body:**
```json
{}
```
Response (200 OK):
```json
{
  "role": "teacher|student",
  "status": 200
}
```
Status Codes:

- 200 OK
- 400 Bad Request (invalid token)
- 401 Unauthorized (missing/invalid token)

---

### `POST /teacher/data/`
**Auth Required:** Yes — JWT Bearer (teacher)

**Request Body:**
```json
{}
```
Response (200 OK):
```json
{
  "teacher_data": {
    "id": "integer",
    "name": "string",
    "email": "string",
    "contactNo": "string",
    "hireDate": "date",
    "teacherPassword": "string",
    "profilePic": "string|null"
  },
  "status": 200
}
```
Status Codes:

- 200 OK
- 401 Unauthorized (missing/invalid token)
- 403 Forbidden (wrong role)

---

### `POST /student/data/`
**Auth Required:** Yes — JWT Bearer (student)

**Request Body:**
```json
{}
```
Response (200 OK):
```json
{
  "student_data": {
    "admissionNo": "integer",
    "studentName": "string",
    "rollNo": "integer",
    "studentClass": "string",
    "gender": "string",
    "fatherName": "string",
    "email": "string",
    "contactNo": "string",
    "joinedDate": "date",
    "studentPassword": "string",
    "profilePic": "string|null"
  },
  "status": 200
}
```
Status Codes:

- 200 OK
- 401 Unauthorized (missing/invalid token)
- 403 Forbidden (wrong role)

---

### `POST /teacher/student/data/`
**Auth Required:** Yes — JWT Bearer (teacher)

**Request Body:**
```json
{
  "admissionNo": "integer (required)"
}
```
Response (200 OK):
```json
{
  "student_data": {
    "admissionNo": "integer",
    "studentName": "string",
    "rollNo": "integer",
    "studentClass": "string",
    "gender": "string",
    "fatherName": "string",
    "email": "string",
    "contactNo": "string",
    "joinedDate": "date",
    "studentPassword": "string",
    "profilePic": "string|null"
  },
  "status": 200
}
```
Status Codes:

- 200 OK
- 400 Bad Request (missing admissionNo)
- 404 Not Found (student not found)
- 401 Unauthorized (missing/invalid token)
- 403 Forbidden (wrong role)

---

### `POST /student/update/`
**Auth Required:** Yes — JWT Bearer (teacher/student)

**Request Body:**
```json
{
  "admission_no": "integer (required for teacher, ignored for student)",
  "studentName": "string (optional)",
  "gender": "string (optional)",
  "fatherName": "string (optional)",
  "email": "string (optional)",
  "contactNo": "string (optional)",
  "joinedDate": "date (optional)",
  "studentPassword": "string (optional)",
  "profilePic": "file (optional)"
}
```
Response (200 OK):
```json
{
  "admissionNo": "integer",
  "studentName": "string",
  "rollNo": "integer",
  "studentClass": "string",
  "division": "string",
  "gender": "string",
  "fatherName": "string",
  "email": "string",
  "contactNo": "string",
  "joinedDate": "date",
  "accountStatus": "boolean",
  "studentPassword": "string",
  "batch": "integer",
  "createdAt": "datetime",
  "profilePic": "string|null"
}
```
Status Codes:

- 200 OK
- 400 Bad Request (invalid data, missing admission_no for teacher)
- 404 Not Found (student not found)
- 401 Unauthorized (missing/invalid token)

---

### `POST /teacher/update/`
**Auth Required:** Yes — JWT Bearer (teacher)

**Request Body:**
```json
{
  "name": "string (optional)",
  "subject": "string (optional)",
  "contactNo": "string (optional)",
  "profilePic": "file (optional)"
}
```
Response (200 OK):
```json
{
  "name": "string",
  "subject": "string",
  "contactNo": "string",
  "profilePic": "string|null"
}
```
Status Codes:

- 200 OK
- 400 Bad Request (invalid data)
- 404 Not Found (teacher not found)
- 401 Unauthorized (missing/invalid token)

---

## Batch Management

### `POST /batch/create/`
**Auth Required:** Yes — JWT Bearer (teacher)

**Request Body:**
```json
{
  "batchName": "string (required)",
  "description": "string (optional)"
}
```
Response (201 Created):
```json
{
  "message": "Batch created successfully",
  "status": 201
}
```
Status Codes:

- 201 Created
- 400 Bad Request (invalid data)
- 401 Unauthorized (missing/invalid token)
- 403 Forbidden (wrong role)

---

### `POST /batch/list/`
**Auth Required:** Yes — JWT Bearer (teacher)

**Request Body:**
```json
{}
```
Response (200 OK):
```json
{
  "batches": [
    {"id": "integer", "name": "string"},
    ...
  ],
  "status": 200
}
```
Status Codes:

- 200 OK
- 401 Unauthorized (missing/invalid token)
- 403 Forbidden (wrong role)

---

### `POST /batch/list_batch_students/`
**Auth Required:** Yes — JWT Bearer (teacher)

**Request Body:**
```json
{
  "batch_id": "integer (required)"
}
```
Response (200 OK):
```json
{
  "batch": "string",
  "students": [
    {"name": "string", "email": "string", "admissionNo": "integer"},
    ...
  ]
}
```
Status Codes:

- 200 OK
- 400 Bad Request (missing batch_id)
- 404 Not Found (batch not found)
- 401 Unauthorized (missing/invalid token)
- 403 Forbidden (wrong role)

---

### `POST /batch/remove_student/`
**Auth Required:** Yes — JWT Bearer (teacher)

**Request Body:**
```json
{
  "admissionNo": "integer (required)"
}
```
Response (200 OK):
```json
{
  "message": "Student removed from batch"
}
```
Status Codes:

- 200 OK
- 400 Bad Request (missing admissionNo)
- 404 Not Found (student not found)
- 401 Unauthorized (missing/invalid token)
- 403 Forbidden (wrong role)

---

### `POST /batch/teacher_student_list/`
**Auth Required:** Yes — JWT Bearer (teacher)

**Request Body:**
```json
{}
```
Response (200 OK):
```json
{
  "students": [
    {"name": "string", "rollNo": "integer", "admissionNo": "integer", "batch": "string"},
    ...
  ]
}
```
Status Codes:

- 200 OK
- 404 Not Found (teacher not found)
- 401 Unauthorized (missing/invalid token)
- 403 Forbidden (wrong role)

---

### `POST /batch/update/`
**Auth Required:** Yes — JWT Bearer (teacher)

**Request Body:**
```json
{
  "batch_id": "integer (required)",
  "batchName": "string (optional)",
  "description": "string (optional)",
  "batchStatus": "boolean (optional)",
  "batchIncharge": "integer (optional)",
  "teachers": ["integer", ...] (optional)
}
```
Response (200 OK):
```json
{
  "id": "integer",
  "batchName": "string",
  "description": "string",
  "batchStatus": "boolean",
  "createdAt": "datetime",
  "batchIncharge": "integer|null",
  "teachers": ["integer", ...]
}
```
Status Codes:

- 200 OK
- 400 Bad Request (invalid data, missing batch_id)
- 404 Not Found (batch not found)
- 401 Unauthorized (missing/invalid token)

---

## Session Management

### `POST /batch/create_session/`
**Auth Required:** Yes — JWT Bearer (teacher)

**Request Body:**
```json
{
  "sessionName": "string (required)",
  "batch_id": "integer (required)",
  "startDateTime": "datetime (required)",
  "endDateTime": "datetime (required)"
}
```
Response (201 Created):
```json
{
  "id": "integer",
  "sessionName": "string",
  "batch_id": "integer",
  "startDateTime": "datetime",
  "endDateTime": "datetime"
}
```
Status Codes:

- 201 Created
- 400 Bad Request (missing/invalid fields)
- 404 Not Found (batch not found)
- 409 Conflict (session time conflict)
- 401 Unauthorized (missing/invalid token)
- 403 Forbidden (wrong role)

---

### `POST /batch/get_batch_sessions/`
**Auth Required:** Yes — JWT Bearer (teacher/student)

**Request Body:**
```json
{
  "batch_id": "integer (required for teacher, ignored for student)"
}
```
Response (200 OK):
```json
{
  "batch_name": "string",
  "batch_id": "integer",
  "sessions": [
    {
      "id": "integer",
      "sessionName": "string",
      "startDateTime": "datetime",
      "endDateTime": "datetime",
      "createdBy": "string|null"
    },
    ...
  ]
}
```
Status Codes:

- 200 OK
- 400 Bad Request (missing batch_id for teacher)
- 404 Not Found (batch or student not found)
- 401 Unauthorized (missing/invalid token)

---

### `POST /session/update/`
**Auth Required:** Yes — JWT Bearer (teacher)

**Request Body:**
```json
{
  "session_id": "integer (required)",
  "sessionName": "string (optional)",
  "batch": "integer (optional)",
  "startDateTime": "datetime (optional)",
  "endDateTime": "datetime (optional)"
}
```
Response (200 OK):
```json
{
  "id": "integer",
  "sessionName": "string",
  "batch": "integer",
  "createdBy": "integer|null",
  "startDateTime": "datetime",
  "endDateTime": "datetime"
}
```
Status Codes:

- 200 OK
- 400 Bad Request (invalid data, missing session_id)
- 404 Not Found (session not found)
- 401 Unauthorized (missing/invalid token)

---

## Attendance Management

### `POST /session/attendance/`
**Auth Required:** Yes — JWT Bearer (teacher)

**Request Body:**
```json
{
  "session_id": "integer (required)"
}
```
Response (200 OK):
```json
{
  "attendance_data": [
    {"admissionNo": "integer", "studentName": "string", "status": "boolean"},
    ...
  ],
  "status": 200
}
```
Status Codes:

- 200 OK
- 400 Bad Request (missing session_id)
- 404 Not Found (session not found)
- 401 Unauthorized (missing/invalid token)
- 403 Forbidden (wrong role)

---

### `POST /attendance/history/`
**Auth Required:** Yes — JWT Bearer (teacher/student)

**Request Body:**
```json
{
  "admission_no": "integer (required for teacher, ignored for student)"
}
```
Response (200 OK):
```json
{
  "attendance_history": [
    {
      "sessionName": "string",
      "startDateTime": "datetime",
      "endDateTime": "datetime",
      "status": "boolean"
    },
    ...
  ],
  "status": 200
}
```
Status Codes:

- 200 OK
- 400 Bad Request (missing admission_no for teacher)
- 404 Not Found (student not found)
- 401 Unauthorized (missing/invalid token)

---

### `POST /batch/mark_attendance/`
**Auth Required:** Yes — JWT Bearer (teacher)

**Request Body:**
```json
{
  "session_id": "integer (required)",
  "attendance": ["integer", ...] (required, list of admission numbers present)
}
```
Response (200 OK):
```json
{
  "message": "Attendance marked successfully"
}
```
Status Codes:

- 200 OK
- 400 Bad Request (missing session_id or attendance data)
- 404 Not Found (session or batch not found)
- 401 Unauthorized (missing/invalid token)
- 403 Forbidden (wrong role)

---

## Dashboards

### `POST /teacher/dashboard/`
**Auth Required:** Yes — JWT Bearer (teacher)

**Request Body:**
```json
{}
```
Response (200 OK):
```json
{
  "total_students": "integer",
  "active_students": "integer",
  "recent_students_details": [
    {
      "admissionNo": "integer",
      "studentName": "string",
      "batch": "string",
      "email": "string",
      "active": "boolean"
    },
    ...
  ],
  "attendance_data": [
    {"date": "string", "percentage": "float"},
    ...
  ],
  "status": 200
}
```
Status Codes:

- 200 OK
- 401 Unauthorized (missing/invalid token)
- 403 Forbidden (wrong role)

---

## Administration & Testing

### `POST /database/clear/`
**Auth Required:** No

**Request Body:**
```json
{}
```
Response (200 OK):
```json
{
  "message": "All data cleared successfully."
}
```
Status Codes:

- 200 OK

---

### `GET /test/`
**Auth Required:** No

**Request Body:**
_None_

Response (200 OK):
```json
{
  "message": "Test Succesfull"
}
```
Status Codes:

- 200 OK

---


# Notes
- All endpoints that require authentication expect a JWT Bearer token in the `Authorization` header.
- If a view uses `isTeacher`, only teachers can access. If it uses `isStudent`, only students can access. If both, both roles can access but logic may differ (see endpoint description).
- For update endpoints, only fields provided in the request body are updated (partial update).
- For endpoints returning nested objects, see the response examples for structure.
- Status codes 401 and 403 are returned for missing/invalid tokens or wrong roles, respectively.
