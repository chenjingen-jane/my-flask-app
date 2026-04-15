# AI Lifestyle Assistant

A full-stack Flask web application that combines weather data, personal spending logs, mood tracking, and user authentication into one smart lifestyle dashboard.

## Live Demo
(Add your Render link here after deployment)

## Features

- User Registration and Login
- Secure password hashing using Werkzeug
- Session-based authentication
- Personalized dashboard for each user
- Weather data integration using OpenWeather API
- Daily spending tracker
- Mood logging
- Smart lifestyle advice based on spending + weather
- Spending history table
- Spending analytics chart using Chart.js
- Logout system

## Tech Stack

### Backend
- Python
- Flask
- SQLite3

### Frontend
- HTML
- CSS
- Jinja2 Templates
- Chart.js

### APIs
- OpenWeather API

### Security
- Password hashing
- Flask sessions

---

## Project Structure

```text
project1/
│── app.py
│── data.db
│── requirements.txt
│── Procfile
│── templates/
│   │── index.html
│   │── login.html
│   │── register.html
