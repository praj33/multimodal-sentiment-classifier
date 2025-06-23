# cloud_deploy.py - Automated cloud deployment scripts

import os
import json
import subprocess
import sys
from typing import Dict, Any, Optional
import yaml
import time

class CloudDeployer:
    """Automated cloud deployment for multiple platforms"""
    
    def __init__(self, config_file: str = "config/deployment.yaml"):
        self.config_file = config_file
        self.config = self.load_config()
        
    def load_config(self) -> Dict[str, Any]:
        """Load deployment configuration"""
        if os.path.exists(self.config_file):
            with open(self.config_file, 'r') as f:
                return yaml.safe_load(f)
        else:
            return self.create_default_config()
    
    def create_default_config(self) -> Dict[str, Any]:
        """Create default deployment configuration"""
        config = {
            "app_name": "multimodal-sentiment-api",
            "docker_image": "multimodal-sentiment:latest",
            "port": 8000,
            "environment": "production",
            "aws": {
                "region": "us-east-1",
                "instance_type": "t3.medium",
                "min_capacity": 1,
                "max_capacity": 5
            },
            "gcp": {
                "region": "us-central1",
                "machine_type": "e2-medium",
                "min_instances": 1,
                "max_instances": 5
            },
            "azure": {
                "location": "East US",
                "sku": "B2s",
                "min_replicas": 1,
                "max_replicas": 5
            },
            "heroku": {
                "dyno_type": "standard-1x",
                "region": "us"
            },
            "render": {
                "plan": "starter",
                "region": "oregon"
            }
        }
        
        # Save default config
        os.makedirs(os.path.dirname(self.config_file), exist_ok=True)
        with open(self.config_file, 'w') as f:
            yaml.dump(config, f, default_flow_style=False)
        
        return config
    
    def deploy_to_aws_lambda(self) -> Dict[str, Any]:
        """Deploy as AWS Lambda function"""
        print("🚀 Deploying to AWS Lambda...")
        
        # Create Lambda deployment package
        lambda_config = {
            "FunctionName": self.config["app_name"],
            "Runtime": "python3.9",
            "Role": "arn:aws:iam::YOUR_ACCOUNT:role/lambda-execution-role",
            "Handler": "lambda_handler.handler",
            "Code": {
                "ZipFile": "lambda_package.zip"
            },
            "Environment": {
                "Variables": {
                    "ENVIRONMENT": "production"
                }
            },
            "Timeout": 300,
            "MemorySize": 1024
        }
        
        # Create serverless.yml for Serverless Framework
        serverless_config = {
            "service": self.config["app_name"],
            "provider": {
                "name": "aws",
                "runtime": "python3.9",
                "region": self.config["aws"]["region"],
                "timeout": 300,
                "memorySize": 1024
            },
            "functions": {
                "sentiment_api": {
                    "handler": "lambda_handler.handler",
                    "events": [
                        {
                            "http": {
                                "path": "/{proxy+}",
                                "method": "ANY",
                                "cors": True
                            }
                        }
                    ]
                }
            },
            "plugins": ["serverless-python-requirements"]
        }
        
        with open("serverless.yml", "w") as f:
            yaml.dump(serverless_config, f, default_flow_style=False)
        
        return {"status": "configured", "config": lambda_config}
    
    def deploy_to_aws_ecs(self) -> Dict[str, Any]:
        """Deploy to AWS ECS with Fargate"""
        print("🚀 Deploying to AWS ECS...")
        
        # Create ECS task definition
        task_definition = {
            "family": self.config["app_name"],
            "networkMode": "awsvpc",
            "requiresCompatibilities": ["FARGATE"],
            "cpu": "512",
            "memory": "1024",
            "executionRoleArn": "arn:aws:iam::YOUR_ACCOUNT:role/ecsTaskExecutionRole",
            "containerDefinitions": [
                {
                    "name": self.config["app_name"],
                    "image": f"YOUR_ACCOUNT.dkr.ecr.{self.config['aws']['region']}.amazonaws.com/{self.config['docker_image']}",
                    "portMappings": [
                        {
                            "containerPort": self.config["port"],
                            "protocol": "tcp"
                        }
                    ],
                    "environment": [
                        {"name": "ENVIRONMENT", "value": "production"}
                    ],
                    "logConfiguration": {
                        "logDriver": "awslogs",
                        "options": {
                            "awslogs-group": f"/ecs/{self.config['app_name']}",
                            "awslogs-region": self.config["aws"]["region"],
                            "awslogs-stream-prefix": "ecs"
                        }
                    }
                }
            ]
        }
        
        with open("ecs-task-definition.json", "w") as f:
            json.dump(task_definition, f, indent=2)
        
        return {"status": "configured", "task_definition": task_definition}
    
    def deploy_to_gcp_cloud_run(self) -> Dict[str, Any]:
        """Deploy to Google Cloud Run"""
        print("🚀 Deploying to Google Cloud Run...")
        
        # Create Cloud Run service configuration
        service_config = {
            "apiVersion": "serving.knative.dev/v1",
            "kind": "Service",
            "metadata": {
                "name": self.config["app_name"],
                "annotations": {
                    "run.googleapis.com/ingress": "all"
                }
            },
            "spec": {
                "template": {
                    "metadata": {
                        "annotations": {
                            "autoscaling.knative.dev/minScale": str(self.config["gcp"]["min_instances"]),
                            "autoscaling.knative.dev/maxScale": str(self.config["gcp"]["max_instances"])
                        }
                    },
                    "spec": {
                        "containers": [
                            {
                                "image": f"gcr.io/YOUR_PROJECT/{self.config['docker_image']}",
                                "ports": [
                                    {"containerPort": self.config["port"]}
                                ],
                                "env": [
                                    {"name": "ENVIRONMENT", "value": "production"}
                                ],
                                "resources": {
                                    "limits": {
                                        "cpu": "1000m",
                                        "memory": "2Gi"
                                    }
                                }
                            }
                        ]
                    }
                }
            }
        }
        
        with open("cloudrun-service.yaml", "w") as f:
            yaml.dump(service_config, f, default_flow_style=False)
        
        return {"status": "configured", "service_config": service_config}
    
    def deploy_to_azure_container_instances(self) -> Dict[str, Any]:
        """Deploy to Azure Container Instances"""
        print("🚀 Deploying to Azure Container Instances...")
        
        # Create Azure Resource Manager template
        arm_template = {
            "$schema": "https://schema.management.azure.com/schemas/2019-04-01/deploymentTemplate.json#",
            "contentVersion": "1.0.0.0",
            "parameters": {},
            "variables": {},
            "resources": [
                {
                    "type": "Microsoft.ContainerInstance/containerGroups",
                    "apiVersion": "2021-03-01",
                    "name": self.config["app_name"],
                    "location": self.config["azure"]["location"],
                    "properties": {
                        "containers": [
                            {
                                "name": self.config["app_name"],
                                "properties": {
                                    "image": f"YOUR_REGISTRY.azurecr.io/{self.config['docker_image']}",
                                    "ports": [
                                        {"port": self.config["port"]}
                                    ],
                                    "environmentVariables": [
                                        {"name": "ENVIRONMENT", "value": "production"}
                                    ],
                                    "resources": {
                                        "requests": {
                                            "cpu": 1,
                                            "memoryInGB": 2
                                        }
                                    }
                                }
                            }
                        ],
                        "osType": "Linux",
                        "ipAddress": {
                            "type": "Public",
                            "ports": [
                                {
                                    "protocol": "TCP",
                                    "port": self.config["port"]
                                }
                            ]
                        }
                    }
                }
            ]
        }
        
        with open("azure-template.json", "w") as f:
            json.dump(arm_template, f, indent=2)
        
        return {"status": "configured", "template": arm_template}
    
    def deploy_to_heroku(self) -> Dict[str, Any]:
        """Deploy to Heroku"""
        print("🚀 Deploying to Heroku...")
        
        # Create Procfile
        procfile_content = f"web: uvicorn api:app --host 0.0.0.0 --port $PORT"
        with open("Procfile", "w") as f:
            f.write(procfile_content)
        
        # Create app.json for Heroku
        app_json = {
            "name": self.config["app_name"],
            "description": "Multimodal Sentiment Analysis API",
            "image": "heroku/python",
            "addons": ["heroku-postgresql:hobby-dev"],
            "env": {
                "ENVIRONMENT": {
                    "description": "Application environment",
                    "value": "production"
                }
            },
            "formation": {
                "web": {
                    "quantity": 1,
                    "size": self.config["heroku"]["dyno_type"]
                }
            }
        }
        
        with open("app.json", "w") as f:
            json.dump(app_json, f, indent=2)
        
        return {"status": "configured", "app_config": app_json}
    
    def deploy_to_render(self) -> Dict[str, Any]:
        """Deploy to Render"""
        print("🚀 Deploying to Render...")
        
        # Create render.yaml
        render_config = {
            "services": [
                {
                    "type": "web",
                    "name": self.config["app_name"],
                    "env": "python",
                    "plan": self.config["render"]["plan"],
                    "buildCommand": "pip install -r requirements.txt",
                    "startCommand": f"uvicorn api:app --host 0.0.0.0 --port $PORT",
                    "envVars": [
                        {
                            "key": "ENVIRONMENT",
                            "value": "production"
                        }
                    ]
                }
            ]
        }
        
        with open("render.yaml", "w") as f:
            yaml.dump(render_config, f, default_flow_style=False)
        
        return {"status": "configured", "render_config": render_config}
    
    def create_docker_image(self) -> Dict[str, Any]:
        """Build and tag Docker image for deployment"""
        print("🐳 Building Docker image...")
        
        try:
            # Build Docker image
            build_cmd = f"docker build -t {self.config['docker_image']} ."
            result = subprocess.run(build_cmd, shell=True, capture_output=True, text=True)
            
            if result.returncode == 0:
                print("✅ Docker image built successfully")
                return {"status": "success", "image": self.config['docker_image']}
            else:
                print(f"❌ Docker build failed: {result.stderr}")
                return {"status": "error", "error": result.stderr}
                
        except Exception as e:
            print(f"❌ Docker build error: {e}")
            return {"status": "error", "error": str(e)}
    
    def generate_deployment_scripts(self) -> Dict[str, str]:
        """Generate deployment scripts for all platforms"""
        scripts = {}
        
        # AWS deployment script
        scripts["aws_deploy.sh"] = """#!/bin/bash
# AWS Deployment Script
echo "🚀 Deploying to AWS..."

# Build and push Docker image to ECR
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin YOUR_ACCOUNT.dkr.ecr.us-east-1.amazonaws.com
docker build -t multimodal-sentiment .
docker tag multimodal-sentiment:latest YOUR_ACCOUNT.dkr.ecr.us-east-1.amazonaws.com/multimodal-sentiment:latest
docker push YOUR_ACCOUNT.dkr.ecr.us-east-1.amazonaws.com/multimodal-sentiment:latest

# Deploy to ECS
aws ecs register-task-definition --cli-input-json file://ecs-task-definition.json
aws ecs update-service --cluster default --service multimodal-sentiment-service --task-definition multimodal-sentiment-api

echo "✅ AWS deployment complete"
"""
        
        # GCP deployment script
        scripts["gcp_deploy.sh"] = """#!/bin/bash
# GCP Deployment Script
echo "🚀 Deploying to Google Cloud..."

# Build and push to Container Registry
gcloud builds submit --tag gcr.io/YOUR_PROJECT/multimodal-sentiment .

# Deploy to Cloud Run
gcloud run deploy multimodal-sentiment-api \\
    --image gcr.io/YOUR_PROJECT/multimodal-sentiment \\
    --platform managed \\
    --region us-central1 \\
    --allow-unauthenticated

echo "✅ GCP deployment complete"
"""
        
        # Azure deployment script
        scripts["azure_deploy.sh"] = """#!/bin/bash
# Azure Deployment Script
echo "🚀 Deploying to Azure..."

# Build and push to Container Registry
az acr build --registry YOUR_REGISTRY --image multimodal-sentiment .

# Deploy to Container Instances
az deployment group create \\
    --resource-group YOUR_RESOURCE_GROUP \\
    --template-file azure-template.json

echo "✅ Azure deployment complete"
"""
        
        # Save scripts to files
        for filename, content in scripts.items():
            with open(filename, "w") as f:
                f.write(content)
            os.chmod(filename, 0o755)  # Make executable
        
        return scripts
    
    def deploy_all(self) -> Dict[str, Any]:
        """Generate all deployment configurations"""
        print("🚀 Generating deployment configurations for all platforms...")
        
        results = {
            "timestamp": time.time(),
            "docker_image": self.create_docker_image(),
            "aws_lambda": self.deploy_to_aws_lambda(),
            "aws_ecs": self.deploy_to_aws_ecs(),
            "gcp_cloud_run": self.deploy_to_gcp_cloud_run(),
            "azure_aci": self.deploy_to_azure_container_instances(),
            "heroku": self.deploy_to_heroku(),
            "render": self.deploy_to_render(),
            "scripts": self.generate_deployment_scripts()
        }
        
        # Save deployment summary
        with open("deployment_summary.json", "w") as f:
            json.dump(results, f, indent=2)
        
        print("✅ All deployment configurations generated!")
        print("📁 Check the following files:")
        print("   - serverless.yml (AWS Lambda)")
        print("   - ecs-task-definition.json (AWS ECS)")
        print("   - cloudrun-service.yaml (GCP Cloud Run)")
        print("   - azure-template.json (Azure)")
        print("   - Procfile & app.json (Heroku)")
        print("   - render.yaml (Render)")
        print("   - Deployment scripts: *_deploy.sh")
        
        return results

if __name__ == "__main__":
    deployer = CloudDeployer()
    deployer.deploy_all()
