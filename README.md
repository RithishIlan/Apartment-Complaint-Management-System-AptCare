🏢 AptCare: Intelligent Residential Management & Emergency Response System
(Tip: Replace the above link with an actual screenshot or logo of your dashboard!)

📖 Overview
Managing modern residential communities often relies on fragmented communication channels and manual tracking, leading to a breakdown in facility maintenance and resident satisfaction. Without a centralized system, routine maintenance requests are frequently delayed, while critical safety emergencies lack an immediate escalation route.

AptCare is a centralized, data-driven web application designed to modernize apartment complex management. It bridges the communication gap between residents, administrative staff, and maintenance teams by offering a real-time ticketing system, automated SLA (Service Level Agreement) tracking, and an instant SOS emergency alert network.

✨ Key Features
🚨 Real-Time SOS Emergency Radar
Instant Alerts: A dedicated SOS button for residents bypasses standard queues.

Live Admin Polling: The Admin "Command Center" continuously monitors the database, triggering an unavoidable, flashing red pop-up within seconds of an SOS activation.

Smart Routing: Automatically detects keywords (e.g., "Fire", "Intruder") to route the emergency to the correct department (Security, Fire & Gas, etc.).

🎫 Smart Complaint Ticketing & SLAs
Automated Triage: Calculates a Priority Score (Critical, High, Medium, Low) based on the Impact Scope and Safety Risk inputs.

SLA Enforcement: Attaches specific resolution deadlines to every ticket (e.g., 2 hours for Critical, 48 hours for Low).

Live Timeline: Residents can track their ticket's journey from "Submitted" to "Resolved" with a clean, visual pipeline.

📈 Data-Driven Dashboards
Admin Command Center: Displays active loads, overdue SLA breaches, and staff efficiency metrics.

Analytics & Reports: Features continuous timeline trend charts and department volume analysis powered by Chart.js.

Staff Performance Monitor: Tracks on-time resolution percentages and aggregates 5-star user feedback (crediting both Primary and Assisting staff).

👥 Secure Resident Management
Seamlessly add, edit, or safely deactivate resident accounts.

Auto-generates standard usernames (e.g., Block-FlatNumber) and emails temporary credentials directly to new residents.

🛠️ Technology Stack
Frontend:

HTML5, CSS3, Vanilla JavaScript

Bootstrap 5 (Responsive UI, Modals, Offcanvas Drawers)

Chart.js (Data Visualization)

SweetAlert2 (Interactive alerts)

Backend:

Python 3.x

Django & Django REST Framework (DRF)

Token-based Authentication

Database:

SQLite (Development) / PostgreSQL or MySQL (Production ready)

🚀 Installation & Setup
Follow these steps to get the AptCare environment running on your local machine.

1. Clone the repository
Bash
git clone https://github.com/yourusername/AptCare.git
cd AptCare
2. Set up a Virtual Environment
Bash
python -m venv env
# On Windows:
env\Scripts\activate
# On macOS/Linux:
source env/bin/activate
3. Install Dependencies
Bash
pip install -r requirements.txt
4. Database Migrations
Bash
python manage.py makemigrations
python manage.py migrate
5. Create a Superuser (Admin Account)
Bash
python manage.py createsuperuser
6. Run the Development Server
Bash
python manage.py runserver
Navigate to http://127.0.0.1:8000/ in your browser.

📂 Project Structure (Frontend Focus)
UserDashboard.html: Resident portal featuring live ticket status, notification bell, and the SOS trigger.

AdminDashboard.html: The command center with active load charts, urgent escalations, and the Live SOS Radar.

neg_esc.html: Neglect & Escalation monitor tracking SLA breaches.

analytics.html: Interactive charts mapping timeline trends and department efficiencies.

staff_performance.html: Team management, efficiency scoring, and user feedback aggregation.

resident_management.html: Secure CRUD operations for apartment inhabitants.

🤝 Contributing
Contributions are welcome! If you have ideas for new features or find a bug, please open an issue or submit a pull request.

Fork the Project

Create your Feature Branch (git checkout -b feature/AmazingFeature)

Commit your Changes (git commit -m 'Add some AmazingFeature')

Push to the Branch (git push origin feature/AmazingFeature)

Open a Pull Request

📄 License
Distributed under the MIT License. See LICENSE for more information.
