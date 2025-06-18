# 🚀 **DEVELOPER QUICK REFERENCE CARD**
*Essential commands and concepts for daily use*

---

## 🐳 **DOCKER ESSENTIALS**

### **Core Commands:**
```bash
# Build image
docker build -t myapp .

# Run container
docker run -p 8000:8000 myapp

# List containers
docker ps

# Stop container
docker stop <container-id>

# Docker Compose
docker-compose up -d
docker-compose down
```

### **Dockerfile Template:**
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["python", "app.py"]
```

---

## ⚙️ **CONFIGURATION CHECKLIST**

### **Environment Variables (.env):**
```bash
DATABASE_URL=postgresql://localhost/db
API_KEY=your-secret-key
DEBUG=false
PORT=8000
```

### **In Code:**
```python
import os
from dotenv import load_dotenv

load_dotenv()
db_url = os.getenv('DATABASE_URL')
```

---

## 🚀 **API DESIGN CHECKLIST**

### **HTTP Methods:**
- `GET` - Retrieve data
- `POST` - Create new resource
- `PUT` - Update entire resource
- `PATCH` - Update partial resource
- `DELETE` - Remove resource

### **Status Codes:**
- `200` - OK
- `201` - Created
- `400` - Bad Request
- `401` - Unauthorized
- `404` - Not Found
- `500` - Server Error

### **URL Structure:**
```
GET    /api/v1/users
GET    /api/v1/users/123
POST   /api/v1/users
PUT    /api/v1/users/123
DELETE /api/v1/users/123
```

---

## 🏗️ **PROJECT STRUCTURE**

```
📁 project/
├── 📁 api/           # Endpoints
├── 📁 services/      # Business logic
├── 📁 models/        # Data structures
├── 📁 utils/         # Helpers
├── 📁 config/        # Configuration
├── 📁 tests/         # Tests
├── .env              # Environment variables
├── requirements.txt  # Dependencies
├── Dockerfile        # Container config
└── README.md         # Documentation
```

---

## 🔒 **SECURITY CHECKLIST**

### **Input Validation:**
```python
# ✅ Always validate
if not filename.endswith('.txt'):
    raise ValueError("Invalid file type")

# ✅ Use parameterized queries
cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))

# ✅ Escape HTML
from html import escape
safe_text = escape(user_input)
```

### **Environment Variables:**
```python
# ✅ Never hardcode secrets
API_KEY = os.getenv('API_KEY')  # Good
API_KEY = "secret123"           # Bad
```

---

## 📊 **LOGGING TEMPLATE**

```python
import logging

# Setup
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Usage
logger.info("User %s logged in", user_id)
logger.error("Database error: %s", error)
```

---

## 🧪 **TESTING TEMPLATE**

```python
import pytest

def test_user_creation():
    user = create_user({'name': 'John', 'email': 'john@test.com'})
    assert user.name == 'John'

def test_invalid_email():
    with pytest.raises(ValueError):
        create_user({'name': 'John', 'email': 'invalid'})
```

---

## 🎯 **PROFESSIONAL QUESTIONS**

**Before writing code, ask:**
1. What happens when this fails?
2. How will someone else understand this?
3. How will this scale?
4. Is this secure?
5. How will I test this?
6. How will I debug this in production?

---

## 📚 **DAILY PRACTICES**

### **Code Quality:**
- [ ] Write readable code
- [ ] Add error handling
- [ ] Include logging
- [ ] Write tests
- [ ] Document functions
- [ ] Use environment variables

### **Git Workflow:**
```bash
git add .
git commit -m "feat: add user authentication"
git push origin feature-branch
```

### **Deployment:**
```bash
# Local development
docker-compose up -d

# Production deployment
docker build -t myapp .
docker run -p 8000:8000 --env-file .env myapp
```

---

## 🚨 **RED FLAGS TO AVOID**

- [ ] Hardcoded passwords/API keys
- [ ] No error handling
- [ ] No input validation
- [ ] No logging
- [ ] No tests
- [ ] Unclear variable names
- [ ] Giant functions (>50 lines)
- [ ] No documentation

---

## 🏆 **CAREER PROGRESSION**

### **Junior → Mid-Level:**
- Master Docker & APIs
- Learn database design
- Understand security basics
- Write comprehensive tests

### **Mid-Level → Senior:**
- System design skills
- Performance optimization
- Mentoring others
- Business understanding

### **Senior → Lead:**
- Technical strategy
- Team leadership
- Cross-functional collaboration
- Architecture decisions

---

## 🎯 **WEEKLY LEARNING PLAN**

### **Week 1-2: Docker Mastery**
- Multi-stage builds
- Docker Compose
- Container orchestration

### **Week 3-4: Database Skills**
- SQL optimization
- Database design
- Migrations

### **Week 5-6: Cloud Deployment**
- Choose AWS/GCP/Azure
- Deploy applications
- Set up monitoring

### **Week 7-8: Testing & Quality**
- Unit testing
- Integration testing
- Code quality tools

---

## 📞 **EMERGENCY DEBUGGING**

### **Production Issues:**
1. **Check logs first**
2. **Verify environment variables**
3. **Test database connections**
4. **Check external API status**
5. **Monitor resource usage**

### **Common Fixes:**
```bash
# Restart container
docker-compose restart

# Check logs
docker-compose logs -f

# Check container status
docker ps

# Access container shell
docker exec -it <container> /bin/bash
```

---

## 🎭 **MINDSET REMINDERS**

- **"It works on my machine"** → **"It works everywhere"**
- **"I'll fix it later"** → **"I'll do it right now"**
- **"Good enough"** → **"Professional quality"**
- **"Just make it work"** → **"Make it work reliably"**

---

**🎯 Keep this handy for daily reference!**

*Print this out or bookmark it - these are the fundamentals that separate professional developers from the rest.*
