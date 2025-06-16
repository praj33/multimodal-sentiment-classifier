@echo off
echo 🎭 Multimodal Sentiment Analysis Server
echo =====================================

echo 🔍 Checking Python...
python --version

echo 🔧 Installing uvicorn...
python -m pip install uvicorn[standard] fastapi python-multipart

echo 🚀 Starting server...
echo 📍 Server will be available at: http://127.0.0.1:8000
echo 📚 API Documentation: http://127.0.0.1:8000/docs
echo 🛑 Press Ctrl+C to stop
echo =====================================

python -m uvicorn api:app --host 127.0.0.1 --port 8000 --reload

pause
