# 📚CS Learn Track
A web-based Attendance Tracking System designed to manage student registration, batch creation, and attendance tracking efficiently. The platform provides distinct features for Admins and Students to   streamline academic administration and participation. This solution ensures smooth operations with batch management, session scheduling, and attendance monitoring, promoting organized learning.

## Project Overview
   The system allows admins to manage students, create batches, assign students to batches, and schedule sessions. Students can log in, view schedules, and attend sessions by verifying their ID cards. Attendance is marked automatically upon successful ID verification, providing a reliable record-keeping system

# 🛠️ Features
## Admin Features:
➕ Add Students  
🏷️ Create Batches  
🗓️ Schedule Classes    
👥 Assign Students to Batches  
📋 View Attendance & Reports  
🗂️ Manage Student Profiles  
🗑️ Remove Students  

## 👨‍🎓 Student Features  
🔑 Login  
📸 Upload Images   
🔄 Update Profile & Password  
🗓️ View Class Schedule  
🎓 Attend Sessions  
✅ Check Attendance  

## 🚀 Technology Stack
Frontend: NextJS  
Backend: Django  
Database: PostgreSQL  
Hosting: AWS  

## 📝 Installation Guide

1. Clone the repository,    
    ```
    git clone -b development https://github.com/Cyber-Square-Pro/cs-learn-track-api.git
    ```

2. Goto project directory    
   ```
   cd cs-learn-track-api
   ```

3. Create a virtual environment 
   ```
   python3 -m venv env
   ```
   
4. Activate the virtual environment
       
   On Windows    
   ```
   cd env/scripts
   activate
   ```
   
   On Mac and Ubuntu  
   ```
   cd env/scripts
   source activate
   ```
   
6. Goto to project folder using same terminal and install dependencies 
   ```
   pip install -r requirements.txt
    ```  

7. Migrate:  
    ```
    python manage.py migrate
    ```
8. Start the development server
   ```
   python manage.py runserver
   ```
9. Test the api in Postman by the endpoint  
       http://localhost:8000.
