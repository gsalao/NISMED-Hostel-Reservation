# UP NISMED Hostel Reservation System
This is the repository of the Hostel Reservation System for the University of the Philippines National Institute for Science and Mathematics Education Development (UP NISMED) Hostel.

# Development
This project is built on a [Vue.js](https://vuejs.org) frontend with a [Django](https://www.djangoproject.com) backend which uses [PostgreSQL](https://www.postgresql.org) as its database and [Redis](https://redis.io) for its caching.

The website's Vue.js frontend was deployed on [Netlify](https://www.netlify.com). The Django backend and Redis server was hosted on a [DigitalOcean](https://www.digitalocean.com) droplet. The PostgreSQL database that it uses is hosted on [Supabase](https://supabase.com).

## Managing Environment Variables
The backend and frontend have `.env.example` files to ensure that secret variables are maintained.

### Backend `.env` configuration
| **Name**                | **Description**                                                    |
| ----------------------- | ------------------------------------------------------------------ |
| `DB_NAME`               | The name of the database that will be used |
| `DB_USER`               | The user who has access to the database |
| `DB_PASSWORD`           | The password to the `DB_USER` |
| `SECRET_KEY`            | The secret key of the Django app |
| `EMAIL_HOST_USER`       | The email address of the account sending emails |
| `REDIS_URL`             | The URL for redis |
| `FRONTEND_URL`          | The URL for the frontend |
| `GOOGLE_SCRIPT_URL`     | The URL of the Google Script webapp |

### Frontend `.env` configuration
| **Name**                | **Description**                                                    |
| ----------------------- | ------------------------------------------------------------------ |
| `VITE_BACKEND_BASE_URL` | The URL of the Django app (in this case, the `/api` suffix **MUST** be included or it will not work) |
| `VITE_BACKEND_URL` | The URL of the Django app **without** `/api` |

# Project Setup
This part of the README.md assumes a local setup.

## Prerequisites
1. [Node.js](https://nodejs.org/en)
2. [Python](https://www.python.org)
3. [PostgreSQL](https://www.postgresql.org) Database
4. [Docker](https://www.docker.com)

## Backend Setup
1. Create a PostgeSQL database (local or Supabase)
2. Create a [Google Apps Script Project](https://developers.google.com/apps-script) using your `EMAIL_HOST_USER` .
3. Paste in the code of `/backend/Code.gs`
4. Deploy the project with the following configuration: `Execute as:Me` and `Who has access: Anyone` and copy the URL of the webapp
5. Ensure that you are in the `backend` folder
6. Create `.env` file and fill up with necessary details (see above for details)
7. `python3 -m venv env` or `python -m venv env` in order to create the virtual environment for Django
8. Run the `backend_setup.ps1` or `backend_setup.sh` file to prepare the backend (use `.ps1` for Windows devices and `.sh` for POSIX-compliant machines)
9. `docker run -d -p <port>:<port> redis`

## Frontend Setup
1. Ensure that you are in the `frontend` folder
2. Create `.env` folder and fill up with necessary details (see above for details)
3. `npm install` to install dependecies
4. `npm run dev` to run server
5. `npm run build` to type-check, compile, and minify for production (which will be used in Netlify)

# Team
The following are the developers of the project:
1. [Prince Harry Quijano](https://github.com/Harry2166)
2. [Gerard Andrew Salao](https://github.com/gsalao)
