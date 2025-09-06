## Tech Stack

- **Frontend**: React with Vite, Shadcn UI
- **Backend**: Django REST Framework
- **Database**: PostgreSQL
- **Authentication**: JWT tokens

## Prerequisites

Before running this application, make sure you have the following installed:

- **Docker** (for backend and database)
- **Node.js** (v16 or higher) - for frontend
- **npm** (comes with Node.js)
- **Git**

## Installation & Setup

### Quick Start (Recommended)

1. **Clone the repository:**
```bash
git clone https://github.com/chidanandgowda/week1-clonefest.git
cd week1-clonefest
```

2. **Start Backend and Database with Docker:**
```bash
docker-compose up -d
```

3. **Run database migrations:**
```bash
docker-compose exec backend python manage.py makemigrations accounts
docker-compose exec backend python manage.py makemigrations blog
docker-compose exec backend python manage.py makemigrations feathers
docker-compose exec backend python manage.py makemigrations modules
docker-compose exec backend python manage.py migrate
```

4. **Create a superuser:**
```bash
docker-compose exec backend python manage.py createsuperuser
```

5. **Install and start Frontend:**
```bash
cd frontend
npm install
npm run dev
```

6. **Access the application:**
   - Frontend: http://localhost:5173
   - Admin: http://localhost:8000/admin


## Usage

1. Access the admin panel at `http://localhost:8000/admin` to manage content
2. Visit `http://localhost:5173` to view the blog
3. Create posts using different Feather types
4. Customize themes and modules as needed
