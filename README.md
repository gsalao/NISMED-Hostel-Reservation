# UP NISMED Hostel Reservation System
This is the repository of the Hostel Reservation System for the University of the Philippines National Institute for Science and Mathematics Education Development (UP NISMED) Hostel.

# Development
This project is built on a [Vue.js](https://vuejs.org) frontend with a [Django](https://www.djangoproject.com) backend which uses [PostgreSQL](https://www.postgresql.org) as its database.

## Managing Environment Variables
The backend and frontend have `.env.example` files to ensure that secret variables are maintained.

### Backend `.env` configuration
| **Name**                | **Description**                                                    |
| ----------------------- | ------------------------------------------------------------------ |
| `DB_NAME`               | The name of the database that will be used |
| `DB_USER`               | The user who has access to the database |
| `DB_PASSWORD`           | The password to the `DB_USER` |
| `SECRET_KEY`            | The secret key of the Django app |
| `EMAIL_HOST_USER`       | The email address of the account sending the verification codes |
| `EMAIL_HOST_PASSWORD`   | The generated app password for the email |
| `REDIS_URL`             | The URL for redis |
| `FRONTEND_URL`          | The URL for the frontend |

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
1. Create a PostgeSQL database local in your machine
2. Ensure that you are in the `backend` folder
3. Create `.env` file and fill up with necessary details (see above for details)
4. `python3 -m venv env` or `python -m venv env` in order to create the virtual environment for Django
5. Run the `backend_setup.ps1` file to prepare the backend
6. `docker run -d -p <port>:<port> redis`

## Frontend Setup
1. Ensure that you are in the `frontend` folder
2. Create `.env` folder and fill up with necessary details (see above for details)
3. `npm install` to install dependecies
4. `npm run dev` to run server
5. `npm run build` to type-check, compile, and minify for production

# Team
The following are the developers of the project:
1. [Prince Harry Quijano](https://github.com/Harry2166)
2. [Gerard Andrew Salao](https://github.com/gsalao)
