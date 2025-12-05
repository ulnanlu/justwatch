# JustWatch Search Application

A full-stack application for searching movies and TV shows on JustWatch and viewing streaming offers across all countries.

## Project Structure

- **Backend**: FastAPI application (Python 3.14+, uv)
- **Frontend**: SvelteKit with Flowbite UI components (pnpm)

## Features

- 🔍 Search for movies and TV shows using JustWatch's API
- 🌍 View offers across all available countries
- 💰 Currency conversion to USD for price comparison
- 🎬 Detailed title information (cast, genres, release date, etc.)
- 🔗 Direct links to streaming providers
- 📱 Responsive design with Flowbite components

## Backend (FastAPI)

### Setup

```bash
cd backend
uv sync
```

### Run Development Server

```bash
cd backend
uv run fastapi dev main.py
```

The API will be available at `http://localhost:8000`

### API Documentation

Once the server is running, visit:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

### API Endpoints

- `GET /api/justwatch/search?q={query}&country={country}` - Search for titles
- `GET /api/justwatch/title/{node_id}` - Get title details
- `GET /api/justwatch/offers/{node_id}?path={path}` - Get offers for a title
- `GET /api/justwatch/locales?path={path}` - Get available locales

## Frontend (SvelteKit)

### Setup

```bash
cd frontend
pnpm install
```

### Run Development Server

```bash
cd frontend
pnpm dev
```

The app will be available at `http://localhost:5173`

### Build for Production

```bash
cd frontend
pnpm build
pnpm preview
```

## How It Works

1. **Search**: The frontend sends search queries to the FastAPI backend
2. **GraphQL**: The backend makes GraphQL queries directly to JustWatch's API
3. **Data Processing**: Server-side processing eliminates CORS issues and handles currency conversion
4. **Display**: Results are displayed in a clean, responsive UI using Flowbite components

### Key Differences from Original

The original project used client-side requests with CORS proxies. This implementation:
- ✅ Uses server-side requests (no CORS issues)
- ✅ Implements a robust REST API with FastAPI
- ✅ Better error handling and type safety
- ✅ Cleaner separation of concerns
- ✅ No dependency on third-party CORS proxies

## Technology Stack

### Backend
- **FastAPI**: Modern, fast web framework for building APIs
- **httpx**: Async HTTP client for making requests to JustWatch
- **Pydantic**: Data validation and settings management
- **uv**: Fast Python package installer and resolver

### Frontend
- **SvelteKit**: Fast, modern web framework
- **Flowbite**: Tailwind CSS component library
- **TypeScript**: Type-safe JavaScript
- **Vite**: Fast build tool and dev server

## Development Notes

- The backend requires Python 3.14+ and uses uv for package management
- The frontend uses pnpm for package management
- Both services must be running for the application to work
- CORS is configured to allow requests from the Vite dev server

## Credits

Original concept from [JustWatch-Search](https://github.com/CuSZcXJWGrzbnE/JustWatch-Search) - reimplemented with a proper backend/frontend architecture.
