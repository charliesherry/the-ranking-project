import sys
sys.path.append("src")

from app import app
import student_controllers,lab_controllers



PORT = 3000
app.run("0.0.0.0", PORT, debug=True)