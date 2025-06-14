📚 Campus Blog – Flask Web App
A blog-style web application built using Flask that displays global news, sports updates, and weather info via APIs, while allowing admin users to manage IIT campus blog posts.

🚀 Features
🌐 View Global News (via News API)

🏀 Sports News Feed

🌤️ Real-Time Weather Updates

🏫 Admin-Managed IIT Campus Blog

🔐 Simple User Login System

💾 Blog storage using JSON files

🎨 Red and White themed responsive UI

🛠️ Tech Stack
Category	Technology
Backend	Python (Flask)
Frontend	HTML, CSS
APIs	News API, Weather API
Storage	JSON File
Authentication	Flask Sessions
Version Control	Git + GitHub

📂 Project Structure
pgsql
Copy
Edit
📁 campus-blog/
├── app.py
├── blogs.json
├── newsapi_key.py
├── templates/
│   ├── layout.html
│   ├── index.html
│   ├── blog.html
│   └── edit_blog.html
├── static/
│   └── css/
│       └── style.css
└── README.md
🧪 How to Run the Project
Clone the repo:

bash
Copy
Edit
git clone https://github.com/devdulina/ssssssssssss.git
cd ssssssssssss
Install dependencies:

bash
Copy
Edit
pip install flask requests
Add your API key in newsapi_key.py:

python
Copy
Edit
NEWS_API_KEY = 'your_api_key_here'
Run the app:

bash
Copy
Edit
python app.py
Open in browser:
Navigate to http://127.0.0.1:5000

🔐 Default Admin Login
Field	Value
Email	student.dulina@edu.com
Password	passwords@123
