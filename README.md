# Distributed Emergency Alert and Response System (DEARS)

## 📚 Documentation & Reports

**All project documentation, reports, and diagrams can be found in the `docs/` directory:**

### 📋 Main Reports
- **Project Report (PDF)**: [`docs/03_Documents/RAPPORT_PROJET_D&DS.pdf`](docs/03_Documents/RAPPORT_PROJET_D&DS.pdf)
- **Project Report (Word)**: [`docs/03_Documents/RAPPORT_PROJET_D&DS.docx`](docs/03_Documents/RAPPORT_PROJET_D&DS.docx)
- **Project Presentation**: [`docs/03_Documents/Presentation.pptx`](docs/03_Documents/Presentation.pptx)

### 📐 Design & Architecture Diagrams
Located in [`docs/02_Conception/`](docs/02_Conception/):
- **Class Diagrams**: `ClassDiagram.jpg`, `ClassDiagram2.jpg`
- **Use Case Diagram**: `UseCaseDiagram.jpg`
- **Sequence Diagram**: `SequenceDiagram.jpg`
- **Deployment Diagram**: `DeploymentDiagram.jpg`
- **StarUML Project**: `Conception_StarUML.mdj`

### 📖 Project Instructions
- **Project Specifications**: [`docs/01_Instructions/Projet.pdf`](docs/01_Instructions/Projet.pdf)

---

## 🎯 Overview

DEARS (Distributed Emergency Alert and Response System) is a comprehensive distributed system designed to handle emergency alerts and coordinate responses across multiple emergency services. The system enables citizens to report emergencies through a web interface, which are then automatically routed to the appropriate response units (Police, Fire, Medical) based on the emergency type.

### Key Features

- **Multi-Service Architecture**: Distributed microservices for Police, Fire, and Medical emergency responses
- **Central Dispatcher**: Intelligent alert routing and coordination
- **Real-Time Updates**: Live dashboard for responders and administrators
- **Role-Based Access**: Citizen, Responder, and Admin user roles
- **Geographic Tracking**: Location-based emergency reporting and unit assignment
- **Status Management**: Complete alert lifecycle tracking from creation to resolution

---

## 🏗️ System Architecture

The system consists of the following components:

### Backend Services (Microservices)
1. **Dispatcher Service** (Port 8000)
   - Central hub for receiving and routing emergency alerts
   - Coordinates communication between client and response services
   - Manages alert distribution logic

2. **Response Services**
   - **Police Service** (Port 9001)
   - **Fire Service** (Port 9002)
   - **Medical Service** (Port 9003)
   - Each service handles its specific emergency type independently

### Frontend Client
- **Django Web Application** (Port 8080)
  - User-friendly interface for citizens to report emergencies
  - Real-time dashboards for responders and administrators
  - User authentication and profile management
  - Alert status tracking

---

## 🛠️ Technology Stack

### Backend
- **Framework**: Flask (Python)
- **Database**: PostgreSQL (Neon Cloud)
- **ORM**: SQLAlchemy
- **Migrations**: Alembic
- **API**: RESTful architecture

### Frontend
- **Framework**: Django
- **Database**: PostgreSQL
- **Real-time Updates**: HTMX
- **Styling**: Modern CSS with dark/light theme support

### Infrastructure
- **Containerization**: Ready for Docker deployment
- **Process Management**: Multi-service orchestration

---

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- PostgreSQL server (local or cloud)
- Windows Terminal (recommended for Windows users)

### Installation & Running

#### Option 1: Automated Startup (Recommended - Windows)
Simply run the startup script from the project root:
```bat
start_dears.bat
```

This will open Windows Terminal with all services in separate tabs:
- Tab 1: Dispatcher Service (http://localhost:8000)
- Tab 2: Police Service (Port 9001)
- Tab 3: Fire Service (Port 9002)
- Tab 4: Medical Service (Port 9003)
- Tab 5: Django Client (http://localhost:8080)

#### Option 2: Manual Setup

**1. Set up Backend Services**
```bash
cd app/servers
# For Linux/macOS:
./setup_env.sh
# For Windows:
setup_env.bat

# Configure environment variables
# Copy .env.example to .env in each service directory and configure
```

**2. Set up Django Client**
```bash
cd app/client
pip install -r requirements.txt

# Configure environment variables
cp .env.example .env
# Edit .env with your database credentials

# Run migrations
python manage.py migrate

# Create superuser (optional)
python manage.py createsuperuser
```

**3. Start Services**

For backend services:
```bash
cd app/servers
# Linux/macOS:
./start_all.sh
# Windows:
start_all.bat
```

For Django client:
```bash
cd app/client
python manage.py runserver 8080
```

---

## 📱 Usage

### For Citizens
1. Navigate to http://localhost:8080
2. Register or log in
3. Click "Declare Emergency"
4. Fill in emergency details (type, location, description)
5. Submit and receive alert ID for tracking
6. Check status page for updates

### For Responders
1. Log in with responder credentials
2. Access responder dashboard
3. View assigned alerts
4. Update alert status (En Route, On Scene, Resolved)
5. Add response notes

### For Administrators
1. Log in with admin credentials
2. Access admin dashboard
3. View all alerts across all services
4. Manage response units
5. Monitor system-wide statistics
6. Perform CRUD operations on alerts and units

---

## 🗄️ Database Schema

The system uses PostgreSQL with the following main models:

### Client (Django)
- **User**: Django authentication
- **UserProfile**: Extended user information with roles
- **Alert**: Emergency alert records
- **ResponseUnit**: Emergency response teams

### Services (Flask/SQLAlchemy)
- **Alert**: Service-specific alert records
- **ResponseUnit**: Service-specific response units
- **AlertHistory**: Alert status change tracking

See the Class Diagrams in `docs/02_Conception/` for detailed relationships.

---

## 🔧 Configuration

### Environment Variables

Each service requires a `.env` file with the following variables:

**Backend Services:**
```env
DATABASE_URL=postgresql://user:password@host:port/database
SERVICE_PORT=9001  # Varies by service
DISPATCHER_URL=http://localhost:8000
```

**Django Client:**
```env
DATABASE_URL=postgresql://user:password@host:port/database
SECRET_KEY=your-secret-key
DEBUG=True
DISPATCHER_SERVICE_URL=http://localhost:8000
```

See `.env.example` files in each service directory for complete configuration options.

---

## 📊 API Endpoints

### Dispatcher Service (Port 8000)
- `POST /alerts` - Create new alert
- `GET /alerts/<id>` - Get alert details
- `PUT /alerts/<id>` - Update alert status
- `GET /health` - Service health check

### Response Services (Ports 9001-9003)
- `POST /alerts` - Receive alert from dispatcher
- `GET /alerts` - List all alerts
- `PUT /alerts/<id>` - Update alert status
- `GET /units` - List response units

See individual service READMEs in `app/servers/` for detailed API documentation.

---

## 🧪 Testing

### Verify System Setup
```bash
# Check database connections
cd app/client
python verify_users.py

# Check coordinate validation
cd ../..
python check_coordinates.py
```

### Test Alert Flow
1. Create an alert through the web interface
2. Check dispatcher logs for routing
3. Verify alert appears in appropriate response service
4. Update status from responder dashboard
5. Confirm status updates propagate back to client

---

## 📁 Project Structure

```
Distributed-Emergency-Alert-and-Response-System-DEARS/
├── app/
│   ├── client/                      # Django web application
│   │   ├── alerts/                  # Main Django app
│   │   ├── dears_project/           # Django project settings
│   │   ├── manage.py
│   │   └── requirements.txt
│   └── servers/                     # Backend microservices
│       ├── dispatcher_service/      # Central dispatcher
│       ├── response_services/       # Emergency response services
│       │   ├── police_service/
│       │   ├── fire_service/
│       │   └── medical_service/
│       └── requirements.txt
├── docs/                            # All documentation
│   ├── 01_Instructions/             # Project specifications
│   ├── 02_Conception/               # UML diagrams
│   └── 03_Documents/                # Reports and presentations
├── start_dears.bat                  # Windows startup script
└── README.md                        # This file
```

---

## 🔐 Default Credentials

### Admin User
- **Username**: admin
- **Password**: admin

### Test Citizen User
- **Username**: user
- **Password**: user

**⚠️ Important**: Change these credentials in production environments!

---

## 🐛 Troubleshooting

### Services Won't Start
- Verify PostgreSQL is running
- Check `.env` files are properly configured
- Ensure all ports (8000, 8080, 9001-9003) are available
- Activate virtual environment before running services

### Database Connection Errors
- Verify DATABASE_URL in `.env` files
- Check PostgreSQL credentials
- Ensure database exists
- Run migrations: `python manage.py migrate`

### Alerts Not Appearing
- Check dispatcher service logs
- Verify response services are running
- Confirm emergency type matches available services
- Check network connectivity between services

### Template or UI Issues
```bash
# Run template fix script
python fix_all_template_issues.py
```

---

## 📈 Future Enhancements

- Real-time WebSocket notifications
- Mobile application (iOS/Android)
- SMS/Email alert notifications
- Advanced analytics and reporting
- Machine learning for alert prioritization
- Integration with external emergency services APIs
- Multi-language support
- Enhanced geographic mapping with route optimization

---

## 👥 User Roles

### Citizen
- Report emergencies
- Track alert status
- View personal alert history
- Update profile information

### Responder
- View assigned alerts
- Update alert status
- Add response notes
- Manage response unit availability

### Administrator
- Full system access
- Manage all alerts and units
- View system statistics
- User management
- System configuration

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🤝 Contributing

This is an academic project for distributed systems coursework. For questions or contributions, please refer to the project documentation in the `docs/` directory.

---

## 📞 Support

For detailed technical information, please refer to:
- **Main Report**: `docs/03_Documents/RAPPORT_PROJET_D&DS.pdf`
- **Architecture Diagrams**: `docs/02_Conception/`
- **Service Documentation**: `app/servers/README.md`
- **Client Documentation**: `app/client/AUTHENTICATION_IMPLEMENTATION.md`

---

**Last Updated**: December 2025
