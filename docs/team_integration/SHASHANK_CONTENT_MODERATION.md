# 🛡️ Shashank's Team: Content Moderation Integration Guide

## 📋 **Overview**

This guide provides **Shashank** and the content moderation team with everything needed to integrate the Multimodal Sentiment Analysis API for **content safety and moderation**. The system is optimized for high-precision detection of inappropriate, harmful, or policy-violating content.

---

## 🎯 **Use Case: Content Moderation**

**Goal**: Analyze user-generated content (text, audio, video) to detect policy violations, inappropriate content, and safety concerns with high precision.

**Key Requirements:**
- **High precision** to minimize false positives
- **Text-focused analysis** for policy violation detection
- **Consistent results** for fair moderation decisions
- **Detailed logging** for audit trails and appeals

---

## ⚙️ **Optimal Configuration**

### **Fusion Settings (Pre-configured)**
```yaml
# config/fusion_config.yaml
fusion:
  method: "simple"               # Consistent, predictable results
  confidence_threshold: 0.9      # Very high threshold for safety
  enable_dynamic_weights: false  # Consistent behavior

weights:
  text: 0.7    # Primary: content policy analysis
  audio: 0.2   # Secondary: tone and speech analysis
  video: 0.1   # Minimal: visual content analysis

# Safety-specific settings
modalities:
  text:
    min_confidence: 0.5
    weight_range: [0.6, 0.8]  # High text focus
    
validation:
  require_consensus: false       # Don't require agreement
  fallback_strategy: "text_priority"  # Prioritize text analysis
```

### **Apply Configuration**
```python
from fusion_config_manager import get_fusion_config_manager

# Apply Shashank's preset
manager = get_fusion_config_manager()
success = manager.apply_team_preset('shashank_content_moderation')
print(f"Content moderation config applied: {success}")
```

---

## 🚀 **Integration Examples**

### **Basic Content Moderation**
```python
from sdk.python.sentiment_client import SentimentClient
import logging

# Initialize client
client = SentimentClient(base_url="http://localhost:8000")

class ContentModerator:
    """Content moderation system with safety focus"""
    
    def __init__(self):
        self.client = client
        self.moderation_log = logging.getLogger('content_moderation')
        self.policy_thresholds = {
            'harassment': 0.9,
            'hate_speech': 0.95,
            'violence': 0.9,
            'adult_content': 0.85,
            'spam': 0.8
        }
    
    def moderate_content(self, content, content_type='text', user_id=None):
        """Moderate content with comprehensive safety analysis"""
        
        # Analyze content based on type
        if content_type == 'text':
            result = self.client.analyze_text(content)
        elif content_type in ['audio', 'video']:
            result = self.client.analyze_multimodal(content)
        else:
            raise ValueError(f"Unsupported content type: {content_type}")
        
        # Perform safety assessment
        safety_assessment = self.assess_content_safety(result, content)
        
        # Log moderation decision
        self.log_moderation_decision(safety_assessment, user_id, content_type)
        
        return safety_assessment
    
    def assess_content_safety(self, analysis_result, original_content):
        """Assess content safety with detailed analysis"""
        
        # Extract key metrics
        sentiment = analysis_result['sentiment']
        confidence = analysis_result['confidence']
        
        # Determine safety status
        is_safe = self.determine_safety_status(sentiment, confidence, original_content)
        
        # Calculate risk level
        risk_level = self.calculate_risk_level(sentiment, confidence)
        
        # Determine moderation action
        action = self.determine_moderation_action(is_safe, risk_level, confidence)
        
        return {
            'is_safe': is_safe,
            'risk_level': risk_level,
            'action': action,
            'confidence': confidence,
            'sentiment': sentiment,
            'reasoning': self.generate_reasoning(sentiment, confidence, is_safe),
            'requires_human_review': confidence < 0.9 or risk_level == 'high',
            'model_version': analysis_result.get('model_version', {}),
            'timestamp': time.time()
        }
    
    def determine_safety_status(self, sentiment, confidence, content):
        """Determine if content is safe based on analysis"""
        
        # High confidence negative sentiment indicates potential issues
        if sentiment == 'negative' and confidence >= 0.9:
            return False
        
        # Check for specific policy violations
        if self.check_policy_violations(content):
            return False
        
        # Default to safe if no clear violations
        return True
    
    def check_policy_violations(self, content):
        """Check for specific policy violations in text content"""
        
        # Define violation patterns (simplified for example)
        violation_patterns = {
            'harassment': ['harassment', 'bullying', 'threatening'],
            'hate_speech': ['hate', 'discrimination', 'slur'],
            'violence': ['violence', 'harm', 'attack'],
            'adult_content': ['explicit', 'inappropriate'],
            'spam': ['spam', 'promotional', 'advertisement']
        }
        
        content_lower = content.lower()
        violations = []
        
        for category, patterns in violation_patterns.items():
            for pattern in patterns:
                if pattern in content_lower:
                    violations.append(category)
                    break
        
        return violations
    
    def calculate_risk_level(self, sentiment, confidence):
        """Calculate risk level for content"""
        
        if sentiment == 'negative' and confidence >= 0.95:
            return 'high'
        elif sentiment == 'negative' and confidence >= 0.8:
            return 'medium'
        elif sentiment == 'negative' and confidence >= 0.6:
            return 'low'
        else:
            return 'minimal'
    
    def determine_moderation_action(self, is_safe, risk_level, confidence):
        """Determine appropriate moderation action"""
        
        if not is_safe and risk_level == 'high' and confidence >= 0.9:
            return 'block'
        elif not is_safe and risk_level in ['medium', 'high']:
            return 'flag_for_review'
        elif not is_safe and confidence < 0.8:
            return 'human_review'
        elif risk_level == 'minimal':
            return 'approve'
        else:
            return 'monitor'
    
    def generate_reasoning(self, sentiment, confidence, is_safe):
        """Generate human-readable reasoning for moderation decision"""
        
        if is_safe:
            return f"Content appears safe (sentiment: {sentiment}, confidence: {confidence:.2f})"
        else:
            return f"Content flagged as potentially unsafe (sentiment: {sentiment}, confidence: {confidence:.2f})"
    
    def log_moderation_decision(self, assessment, user_id, content_type):
        """Log moderation decision for audit trail"""
        
        log_entry = {
            'user_id': user_id,
            'content_type': content_type,
            'action': assessment['action'],
            'risk_level': assessment['risk_level'],
            'confidence': assessment['confidence'],
            'requires_review': assessment['requires_human_review'],
            'timestamp': assessment['timestamp']
        }
        
        self.moderation_log.info(f"Moderation decision: {log_entry}")

# Example usage
moderator = ContentModerator()

# Moderate text content
text_result = moderator.moderate_content(
    "This is a sample user comment",
    content_type='text',
    user_id='user_123'
)

print(f"Content is safe: {text_result['is_safe']}")
print(f"Action: {text_result['action']}")
print(f"Risk level: {text_result['risk_level']}")
```

### **Batch Content Moderation**
```python
def moderate_content_batch(content_items, batch_size=10):
    """Moderate multiple content items efficiently"""
    
    moderator = ContentModerator()
    results = []
    
    # Process in batches for efficiency
    for i in range(0, len(content_items), batch_size):
        batch = content_items[i:i + batch_size]
        
        batch_results = []
        for item in batch:
            try:
                result = moderator.moderate_content(
                    content=item['content'],
                    content_type=item['type'],
                    user_id=item.get('user_id')
                )
                batch_results.append({
                    'item_id': item['id'],
                    'moderation_result': result
                })
            except Exception as e:
                batch_results.append({
                    'item_id': item['id'],
                    'error': str(e)
                })
        
        results.extend(batch_results)
        
        # Small delay to avoid overwhelming the API
        time.sleep(0.1)
    
    return results

# Generate batch summary
def generate_moderation_summary(batch_results):
    """Generate summary of batch moderation results"""
    
    total_items = len(batch_results)
    actions = {}
    risk_levels = {}
    
    for result in batch_results:
        if 'moderation_result' in result:
            mod_result = result['moderation_result']
            action = mod_result['action']
            risk = mod_result['risk_level']
            
            actions[action] = actions.get(action, 0) + 1
            risk_levels[risk] = risk_levels.get(risk, 0) + 1
    
    return {
        'total_items': total_items,
        'action_breakdown': actions,
        'risk_breakdown': risk_levels,
        'items_requiring_review': len([r for r in batch_results 
                                     if 'moderation_result' in r and 
                                     r['moderation_result']['requires_human_review']])
    }
```

### **Real-time Content Monitoring**
```python
import asyncio
import websockets

async def monitor_live_content(websocket_url):
    """Monitor live content streams for real-time moderation"""
    
    moderator = ContentModerator()
    
    async with websockets.connect(websocket_url) as websocket:
        
        while True:
            try:
                # Receive content from live stream
                message = await websocket.recv()
                content_data = json.loads(message)
                
                # Moderate content
                result = moderator.moderate_content(
                    content=content_data['content'],
                    content_type=content_data['type'],
                    user_id=content_data.get('user_id')
                )
                
                # Take immediate action if needed
                if result['action'] == 'block':
                    await websocket.send(json.dumps({
                        'action': 'block_content',
                        'content_id': content_data['id'],
                        'reason': result['reasoning']
                    }))
                elif result['requires_human_review']:
                    await websocket.send(json.dumps({
                        'action': 'flag_for_review',
                        'content_id': content_data['id'],
                        'priority': result['risk_level']
                    }))
                
            except Exception as e:
                print(f"Error in live monitoring: {e}")
                await asyncio.sleep(1)
```

---

## 🎛️ **Configuration Tuning**

### **For Different Content Types**

**Text-Heavy Platforms (Forums, Comments):**
```python
# Maximum text focus for policy detection
manager.update_weights({
    'text': 0.8,   # Maximum text analysis
    'audio': 0.1,  # Minimal audio
    'video': 0.1   # Minimal video
})
```

**Video Platforms:**
```python
# Balanced for video content analysis
manager.update_weights({
    'text': 0.6,   # Text/captions
    'audio': 0.2,  # Audio track
    'video': 0.2   # Visual content
})
```

**High-Risk Content:**
```python
# Ultra-conservative settings
manager.config['fusion']['confidence_threshold'] = 0.95
manager.update_weights({
    'text': 0.9,   # Almost pure text focus
    'audio': 0.05,
    'video': 0.05
})
```

---

## 📊 **Moderation Analytics**

```python
class ModerationAnalytics:
    """Analytics for content moderation performance"""
    
    def __init__(self):
        self.moderation_history = []
    
    def generate_daily_report(self, date):
        """Generate daily moderation report"""
        
        day_results = self.get_results_for_date(date)
        
        return {
            'total_content_reviewed': len(day_results),
            'actions_taken': self.count_actions(day_results),
            'risk_distribution': self.count_risk_levels(day_results),
            'false_positive_rate': self.calculate_false_positive_rate(day_results),
            'human_review_rate': self.calculate_human_review_rate(day_results),
            'average_confidence': self.calculate_average_confidence(day_results)
        }
    
    def track_moderation_accuracy(self, predictions, ground_truth):
        """Track moderation accuracy against human reviewers"""
        
        correct_predictions = 0
        total_predictions = len(predictions)
        
        for pred, truth in zip(predictions, ground_truth):
            if pred['is_safe'] == truth['is_safe']:
                correct_predictions += 1
        
        accuracy = correct_predictions / total_predictions
        return {
            'accuracy': accuracy,
            'total_cases': total_predictions,
            'correct_predictions': correct_predictions
        }
```

---

## 🔧 **Troubleshooting**

### **Common Issues**

**High False Positive Rate:**
```python
# Lower confidence threshold slightly
if false_positive_rate > 0.1:  # 10%
    manager.config['fusion']['confidence_threshold'] = 0.85
```

**Missing Policy Violations:**
```python
# Increase text weight for better detection
if false_negative_rate > 0.05:  # 5%
    manager.update_weights({'text': 0.8, 'audio': 0.1, 'video': 0.1})
```

**Inconsistent Decisions:**
```python
# Ensure simple fusion method for consistency
manager.update_method('simple')
```

---

## 🔒 **Security & Compliance**

### **Audit Trail**
```python
# Ensure all moderation decisions are logged
logging.basicConfig(
    filename='moderation_audit.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
```

### **Data Privacy**
```python
# Anonymize user data in logs
def anonymize_user_data(user_id):
    return hashlib.sha256(user_id.encode()).hexdigest()[:8]
```

---

## ✅ **Quick Checklist**

- [ ] Applied `shashank_content_moderation` preset
- [ ] Tested with sample policy-violating content
- [ ] Configured high-precision thresholds
- [ ] Set up batch processing for content queues
- [ ] Implemented audit logging
- [ ] Created human review workflow
- [ ] Established false positive monitoring

**🛡️ Ready to protect your platform with AI-powered moderation!**
