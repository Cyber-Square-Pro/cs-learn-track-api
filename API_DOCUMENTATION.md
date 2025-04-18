# API Documentation

---

### POST /student/login/

**Description**: Student login endpoint. Validates student credentials and returns JWT tokens if successful.

**Parameters**:
- **Request Body**:
```json
{
  "admissionNo": "Student's admission number (integer)",
  "studentPassword": "Student's password (string)"
}
```

**Returns**:
- **Status**: 200 OK (others: 400 Bad Request)
- **Response Example**:
```json
{
  "message": "Student logged in successfully",
  "name": "John Doe",
  "status": 200,
  "refresh": "<refresh_token>",
  "access": "<access_token>"
}
```

**Authentication Required**: No  
**Authentication Type**: None

---

### POST /teacher/login/

**Description**: Teacher login endpoint. Validates teacher credentials and returns JWT tokens if successful.

**Parameters**:
- **Request Body**:
```json
{
  "email": "Teacher's email (string)",
  "teacherPassword": "Teacher's password (string)"
}
```

**Returns**:
- **Status**: 200 OK (others: 400 Bad Request)
- **Response Example**:
```json
{
  "message": "Teacher logged in successfully",
  "name": "Jane Smith",
  "status": 200,
  "refresh": "<refresh_token>",
  "access": "<access_token>"
}
```

**Authentication Required**: No  
**Authentication Type**: None

---

### POST /adminendpoint/login/

**Description**: Admin login endpoint. Validates admin credentials.

**Parameters**:
- **Request Body**:
```json
{
  "username": "Admin username (string)",
  "password": "Admin password (string)"
}
```

**Returns**:
- **Status**: 200 OK (others: 400 Bad Request)
- **Response Example**:
```json
{
  "message": "Admin logged in successfully",
  "status": 200
}
```

**Authentication Required**: No  
**Authentication Type**: None

---

### POST /logout/

**Description**: Logs out the current user and blacklists the refresh token.

**Parameters**:
- **Request Body**:
```json
{
  "refresh": "Refresh token (string)"
}
```

**Returns**:
- **Status**: 200 OK (others: 400 Bad Request)
- **Response Example**:
```json
{
  "message": "Logged out successfully",
  "status": 200
}
```

**Authentication Required**: Yes  
**Authentication Type**: Student / Teacher (JWT Token)

---

### POST /token/refresh/

**Description**: Regenerates an access token using a valid refresh token.

**Parameters**:
- **Request Body**:
```json
{
  "refresh": "Refresh token (string)"
}
```

**Returns**:
- **Status**: 200 OK (others: 400 Bad Request)
- **Response Example**:
```json
{
  "access": "<access_token>",
  "status": 200
}
```

**Authentication Required**: No  
**Authentication Type**: None

---

### POST /batch/list/

**Description**: Lists all batches a teacher is in charge of.

**Parameters**:
- **Request Body**: None

**Returns**:
- **Status**: 200 OK
- **Response Example**:
```json
{
  "batches": [
    {"id": 1, "name": "Batch A"},
    {"id": 2, "name": "Batch B"}
  ],
  "status": 200
}
```

**Authentication Required**: Yes  
**Authentication Type**: Teacher Token

---

### POST /CheckUserTypeEndPoint/

**Description**: Checks the type of the current user (teacher or student) based on JWT token.

**Parameters**:
- **Request Body**: None

**Returns**:
- **Status**: 200 OK (others: 400 Bad Request)
- **Response Example**:
```json
{
  "role": "teacher",
  "status": 200
}
```

**Authentication Required**: Yes  
**Authentication Type**: Student / Teacher Token

---

### POST /teacher/data/

**Description**: Retrieves all data for the authenticated teacher.

**Parameters**:
- **Request Body**: None

**Returns**:
- **Status**: 200 OK
- **Response Example**:
```json
{
  "teacher_data": {
    "id": 1,
    "name": "Jane Smith",
    "email": "jane@example.com",
    "contactNo": "1234567890",
    "hireDate": "2025-01-01",
    "teacherPassword": "<hidden>",
    "profilePic": "/media/profile_pictures/jane.jpg"
  },
  "status": 200
}
```

**Authentication Required**: Yes  
**Authentication Type**: Teacher Token

---

### POST /student/data/

**Description**: Retrieves all data for the authenticated student.

**Parameters**:
- **Request Body**: None

**Returns**:
- **Status**: 200 OK
- **Response Example**:
```json
{
  "student_data": {
    "admissionNo": 1001,
    "studentName": "John Doe",
    "rollNo": 1,
    "studentClass": "10A",
    "gender": "Male",
    "fatherName": "Mr. Doe",
    "email": "john@example.com",
    "contactNo": "9876543210",
    "joinedDate": "2025-01-01",
    "studentPassword": "<hidden>",
    "profilePic": "/media/profile_pictures/john.jpg"
  },
  "status": 200
}
```

**Authentication Required**: Yes  
**Authentication Type**: Student Token

---

### POST /teacher/dashboard/

**Description**: Returns dashboard details for the teacher, including total students, active students, and recent students.

**Parameters**:
- **Request Body**: None

**Returns**:
- **Status**: 200 OK
- **Response Example**:
```json
{
  "total_students": 100,
  "active_students": 80,
  "recent_students_details": [
    {"admissionNo": 1001, "studentName": "John Doe", "batch": "Batch A", "email": "john@example.com", "active": true}
  ],
  "status": 200
}
```

**Authentication Required**: Yes  
**Authentication Type**: Teacher Token

---

### POST /batch/create/

**Description**: Creates a new batch. Only accessible by teachers.

**Parameters**:
- **Request Body**:
```json
{
  "batchName": "Name of the batch (string)",
  "description": "Description (string, optional)"
}
```

**Returns**:
- **Status**: 201 Created (others: 400 Bad Request)
- **Response Example**:
```json
{
  "message": "Batch created successfully",
  "status": 201
}
```

**Authentication Required**: Yes  
**Authentication Type**: Teacher Token

---

### POST /student/register/

**Description**: Registers a new student. Only accessible by teachers.

**Parameters**:
- **Request Body**:
```json
{
  "studentName": "Student's name (string)",
  "studentClass": "Class (string)",
  "division": "Division (string)",
  "gender": "Gender (string)",
  "fatherName": "Father's name (string)",
  "email": "Email (string)",
  "contactNo": "Contact number (string)",
  "joinedDate": "Date joined (YYYY-MM-DD)",
  "studentPassword": "Password (string)",
  "batch": "Batch ID (integer)",
  "profilePic": "Profile picture (file, optional)"
}
```

**Returns**:
- **Status**: 201 Created (others: 400 Bad Request, 500 Internal Server Error)
- **Response Example**:
```json
{
  "message": "Student registered successfully",
  "admissionNo": 1001,
  "status": 201
}
```

**Authentication Required**: Yes  
**Authentication Type**: Teacher Token

---

### POST /teacher/register/

**Description**: Registers a new teacher.

**Parameters**:
- **Request Body**:
```json
{
  "name": "Teacher's name (string)",
  "email": "Email (string)",
  "contactNo": "Contact number (string)",
  "hireDate": "Hire date (YYYY-MM-DD)",
  "teacherPassword": "Password (string)",
  "profilePic": "Profile picture (file, optional)"
}
```

**Returns**:
- **Status**: 201 Created (others: 400 Bad Request, 500 Internal Server Error)
- **Response Example**:
```json
{
  "message": "Teacher registered successfully",
  "status": 201
}
```

**Authentication Required**: No  
**Authentication Type**: None

---

### POST /database/clear/

**Description**: Clears all data from the database (students, batches, teachers, user profiles, users).

**Parameters**:
- **Request Body**: None

**Returns**:
- **Status**: 200 OK
- **Response Example**:
```json
{
  "message": "All data cleared successfully."
}
```

**Authentication Required**: No  
**Authentication Type**: None

---

### GET /test/

**Description**: Test endpoint to verify API is working.

**Parameters**:
- **Request Body**: None

**Returns**:
- **Status**: 200 OK
- **Response Example**:
```json
{
  "message": "Test Succesfull"
}
```

**Authentication Required**: No  
**Authentication Type**: None

---

### POST /batch/list_batch_students/

**Description**: Retrieves the list of students in a given batch. Only accessible by teachers.

**Parameters**:
- **Request Body**:
```json
{
  "batch_id": "Batch ID (integer)"
}
```

**Returns**:
- **Status**: 200 OK (others: 400 Bad Request, 404 Not Found)
- **Response Example**:
```json
{
  "batch": "Batch A",
  "students": [
    {"name": "John Doe", "rollNo": 1, "admissionNo": 1001}
  ]
}
```

**Authentication Required**: Yes  
**Authentication Type**: Teacher Token

---

### POST /batch/teacher_student_list/

**Description**: Retrieves the list of all students in batches where the authenticated teacher is in charge.

**Parameters**:
- **Request Body**: None

**Returns**:
- **Status**: 200 OK (others: 404 Not Found)
- **Response Example**:
```json
{
  "students": [
    {
      "name": "John Doe",
      "rollNo": 1,
      "admissionNo": 1001,
      "batch": "Batch A"
    }
  ]
}
```

**Authentication Required**: Yes  
**Authentication Type**: Teacher Token

---

### POST /batch/remove_student/

**Description**: Removes a student from a batch. Only accessible by teachers.

**Parameters**:
- **Request Body**:
```json
{
  "admissionNo": "Student's admission number (integer)"
}
```

**Returns**:
- **Status**: 200 OK (others: 400 Bad Request, 404 Not Found)
- **Response Example**:
```json
{
  "message": "Student removed from batch"
}
```

**Authentication Required**: Yes  
**Authentication Type**: Teacher Token

---

### POST /teacher/get_student_data/

**Description**: Allows a teacher to retrieve detailed data for a specific student by admission number.

**Parameters**:
- **Request Body**:
```json
{
  "admissionNo": "Student's admission number (integer)"
}
```

**Returns**:
- **Status**: 200 OK (others: 404 Not Found, 403 Forbidden)
- **Response Example**:
```json
{
  "student_data": {
    "admissionNo": 1001,
    "studentName": "John Doe",
    "rollNo": 1,
    "studentClass": "10A",
    "gender": "Male",
    "fatherName": "Mr. Doe",
    "email": "john@example.com",
    "contactNo": "9876543210",
    "joinedDate": "2025-01-01",
    "profilePic": "/media/profile_pictures/john.jpg"
  },
  "status": 200
}
```

**Authentication Required**: Yes  
**Authentication Type**: Teacher Token

---