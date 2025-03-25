# 42-pong

This web application provides a classic Pong game with user authentication features.

![demo](images/demo.gif)

## Requires

- Docker
- Docker Compose

## Usage

1. Create a `.env` file based on `.env.example`.
2. Run `make`
3. Open your browser and visit `https://localhost:8080/`

## Adding Mock Users and Games

### Adding Mock Users

To add mock users, execute the following commands. You can specify the number of users by setting the `NUM` variable.

```sh
make exec-be  # Enter the backend container.
make create_mock_players NUM=5
exit  # Exit the backend container.
```

Each mock user will have the following credentials, where {id} starts at 1 and increases by 1 for each user.

- Email: mock{id}@example.com
- Password: test12345

### Adding Mock Tournaments

To add a mock tournament, execute the following commands. This will simulate the end-of-tournament state.

```sh
make exec-be  # Enter the backend container.
make create_mock_games
exit  # Exit the backend container.
```

## Technology Stack

- Containerization: Docker, Docker Compose
- Web Server, Reverse Proxy: Nginx
- CI/CD: GitHub Actions

### Frontend

- Vanilla JS
- Toolkit: Bootstrap
- SPA
- WebSocket

### Backend

- Django
- Database: PostgreSQL
- Game: WebSocket, Redis
- API: REST API (built with Django REST Framework)
- Development: Adminer (a helper tool for database management)

## Main Features

- Game
  - Local Match
    - 1 vs 1 single match
  - Remote Tournament
    - 4 participants, 1 vs 1 in 3 matches
    - Random Match
    - Create and join rooms
    - Chat
  - Server-side logic and progress management
  - Dashboard
    - View various game statistics, including win rates, scoring details, and previous match history.
  - 3D graphics
- Account
  - Registration
  - Login/Logout
  - OAuth 2.0 authentication
    - 42 authentication
- User Management
  - Display name
  - Avatar image
    - Default image
    - Upload
  - Add/Remove friends
  - Friend online status
  - Add/Remove blocks
  - Match results (win/loss count)
- Security
  - JWT
    - Access token
    - Refresh token
  - Two-Factor Authentication (2FA)
    - TOTP (Time-based One-Time password)
    - QR code setup with authenticator apps
- Other
  - Multi-browser support
  - Multi-language support
    - English
    - Japanese
    - French
    - Chinese
    - Spanish
    - Korean
