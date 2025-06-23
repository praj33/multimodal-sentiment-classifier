#!/usr/bin/env python3
# test_torch.py - Test PyTorch installation

print("🔍 Testing PyTorch Installation...")
print("=" * 40)

try:
    import torch
    print("✅ PyTorch imported successfully")
    print(f"✅ PyTorch version: {torch.__version__}")
    print(f"✅ CUDA available: {torch.cuda.is_available()}")
    
    # Test basic tensor operations
    x = torch.tensor([1, 2, 3])
    print(f"✅ Basic tensor creation: {x}")
    
    # Test if torch._C is accessible
    import torch._C
    print("✅ torch._C module accessible")
    
except ImportError as e:
    print(f"❌ Import error: {e}")
except Exception as e:
    print(f"❌ Error: {e}")

print("\n🧪 Testing Text Classifier Import...")
print("=" * 40)

try:
    from classifiers.text_classifier import TextClassifier
    print("✅ Text classifier imports successfully")
    
    # Try to initialize the classifier
    classifier = TextClassifier()
    print("✅ Text classifier initialized successfully")
    
except Exception as e:
    print(f"❌ Text classifier error: {e}")

print("\n🚀 Testing API Import...")
print("=" * 40)

try:
    import api
    print("✅ API module imports successfully")
except Exception as e:
    print(f"❌ API import error: {e}")

print("\n🎉 PyTorch Test Complete!")
