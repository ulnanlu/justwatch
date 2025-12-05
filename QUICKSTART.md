# Quick Start Guide

## Running the Application

### 1. Start the Backend (Terminal 1)
```powershell
cd backend
uv run fastapi dev main.py
```
Backend will be running at: http://localhost:8000

### 2. Start the Frontend (Terminal 2)
```powershell
cd frontend
pnpm dev
```
Frontend will be running at: http://localhost:5173

### 3. Access the Application
Open your browser to: http://localhost:5173

## Using the Application

### Search for Movies/TV Shows
1. Navigate to the home page or click "Search" in the navbar
2. Type a movie or TV show title in the search box
3. Results will appear automatically as you type

### View Streaming Offers
1. Click "View Offers" button on any search result
2. See all available streaming offers across all countries
3. Compare prices in USD
4. Click "Watch" to go directly to the streaming provider

### Change Country
Use the country dropdown in the navigation bar to change your default search country.

## API Documentation

While the backend is running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Example Searches

Try searching for:
- "Breaking Bad"
- "Dune"
- "The Office"
- "Stranger Things"
- "The Matrix"

## Features

✅ **Real-time Search** - Results appear as you type
✅ **Global Offers** - View streaming options from all countries
✅ **Price Comparison** - All prices normalized to USD
✅ **Provider Links** - Direct links to watch on streaming platforms
✅ **Detailed Info** - IMDB/TMDB links, genres, release dates
✅ **Quality Info** - Video/audio technology, languages, subtitles

## Troubleshooting

### Backend won't start
- Make sure Python 3.14+ is installed
- Run `uv sync` to install dependencies

### Frontend won't start
- Make sure Node.js is installed
- Run `pnpm install` to install dependencies

### CORS Errors
- Make sure both backend and frontend are running
- Backend must be on port 8000
- Frontend must be on port 5173

### No search results
- Check your internet connection
- JustWatch API might be temporarily unavailable
- Try a different search query
