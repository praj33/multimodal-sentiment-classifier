@echo off
echo 🔧 FIXING PYTORCH TORCH._C ERROR
echo ================================

echo 📍 Step 1: Activating virtual environment...
call venv\scripts\activate.bat

echo 📍 Step 2: Checking current PyTorch installation...
pip list | findstr torch

echo 📍 Step 3: Uninstalling existing PyTorch packages...
pip uninstall torch torchvision torchaudio -y

echo 📍 Step 4: Clearing pip cache...
pip cache purge

echo 📍 Step 5: Installing fresh PyTorch (CPU version)...
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu

echo 📍 Step 6: Verifying PyTorch installation...
python -c "import torch; print('✅ PyTorch version:', torch.__version__); print('✅ CUDA available:', torch.cuda.is_available())"

echo 📍 Step 7: Testing text classifier import...
python -c "from classifiers.text_classifier import TextClassifier; print('✅ Text classifier imports successfully')"

echo 🎉 PyTorch fix complete! You can now run: python start_api.py
pause
