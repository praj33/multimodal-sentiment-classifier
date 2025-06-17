import os
import yaml

# Get absolute path to the config.yaml file
base_dir = os.path.dirname(os.path.abspath(__file__))
config_path = os.path.join(base_dir, "config", "config.yaml")

print("Looking for:", config_path)

if not os.path.exists(config_path):
    print("❌ File NOT found")
    exit()

# Load the config
with open(config_path, "r") as file:
    config = yaml.safe_load(file)

print("Enabled Models:")
for model_name, enabled in config["model"].items():
    if enabled:
        print(f"  ✅ {model_name.capitalize()}")