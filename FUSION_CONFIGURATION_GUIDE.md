# 🔧 Fusion Configuration Guide - Day 3

## 📋 **Overview**

This guide explains how **Gandhar**, **Karthikeya**, **Vedant**, **Rishabh**, and **Shashank** can modify fusion logic, weights, and algorithms **without changing any code**. All configuration is done through the `config/fusion_config.yaml` file.

---

## 🎯 **Team-Specific Quick Start**

### **Gandhar's Team (Avatar Emotions)**
```yaml
# Apply this preset for avatar emotion detection
fusion:
  method: "confidence_weighted"
weights:
  text: 0.3    # Lower text weight
  audio: 0.4   # Higher audio for tone detection
  video: 0.3   # Higher video for facial expressions
```

**Usage:**
```python
from fusion_config_manager import get_fusion_config_manager
manager = get_fusion_config_manager()
manager.apply_team_preset('gandhar_avatar_emotions')
```

### **Vedant/Rishabh's Team (AI Teacher Scoring)**
```yaml
# Apply this preset for educational content analysis
fusion:
  method: "adaptive"
weights:
  text: 0.6    # High text weight for content analysis
  audio: 0.3   # Moderate audio for engagement
  video: 0.1   # Low video weight
```

**Usage:**
```python
manager.apply_team_preset('vedant_teacher_scoring')
```

### **Shashank's Team (Content Moderation)**
```yaml
# Apply this preset for content safety
fusion:
  method: "simple"
weights:
  text: 0.7    # Maximum text focus
  audio: 0.2   # Minimal audio
  video: 0.1   # Minimal video
confidence_threshold: 0.9  # High precision required
```

**Usage:**
```python
manager.apply_team_preset('shashank_content_moderation')
```

---

## ⚙️ **Configuration File Structure**

### **Basic Configuration**
```yaml
# config/fusion_config.yaml

fusion:
  method: "confidence_weighted"  # Fusion algorithm
  enable_dynamic_weights: true   # Allow runtime weight adjustment
  confidence_threshold: 0.7      # Minimum confidence for decisions
  hot_reload: true              # Auto-reload config changes

weights:
  text: 0.5    # Text model weight (0.0 - 1.0)
  audio: 0.25  # Audio model weight
  video: 0.25  # Video model weight
```

### **Advanced Features**
```yaml
# Runtime control (Day 3 feature)
runtime_control:
  enable_config_api: true        # Allow API-based config changes
  config_api_auth: true         # Require authentication
  
  # A/B testing support
  ab_testing:
    enabled: false
    test_groups: ["control", "experimental"]
    traffic_split: [0.5, 0.5]

# Performance monitoring
monitoring:
  track_fusion_performance: true
  performance_window: 1000      # Track last 1000 predictions
  auto_adjust_weights: false    # Auto-optimization
```

---

## 🔄 **Fusion Methods Explained**

### **1. Simple Weighted Average**
```yaml
fusion:
  method: "simple"
```
- **Best for:** Content moderation, consistent results
- **How it works:** `result = w1*text + w2*audio + w3*video`
- **Pros:** Predictable, fast, stable
- **Cons:** Doesn't adapt to confidence levels

### **2. Confidence-Weighted (Recommended)**
```yaml
fusion:
  method: "confidence_weighted"
```
- **Best for:** Avatar emotions, general use
- **How it works:** Weights adjusted based on individual model confidence
- **Pros:** Adapts to model certainty, better accuracy
- **Cons:** Slightly more complex

### **3. Adaptive Learning**
```yaml
fusion:
  method: "adaptive"
```
- **Best for:** AI teacher scoring, learning systems
- **How it works:** Learns optimal weights from performance data
- **Pros:** Self-improving, optimal for specific domains
- **Cons:** Requires training data, slower initial performance

---

## 🎛️ **Runtime Weight Adjustment**

### **Method 1: Direct File Editing**
1. Edit `config/fusion_config.yaml`
2. Save the file
3. Changes apply automatically (if `hot_reload: true`)

```yaml
weights:
  text: 0.6    # Increase text importance
  audio: 0.3   # Moderate audio
  video: 0.1   # Reduce video
```

### **Method 2: Python API**
```python
from fusion_config_manager import get_fusion_config_manager

manager = get_fusion_config_manager()

# Update weights at runtime
new_weights = {
    'text': 0.6,
    'audio': 0.3, 
    'video': 0.1
}
manager.update_weights(new_weights)

# Change fusion method
manager.update_method('confidence_weighted')

# Apply team preset
manager.apply_team_preset('gandhar_avatar_emotions')
```

### **Method 3: Environment Variables**
```bash
# Override weights via environment
export FUSION_TEXT_WEIGHT=0.6
export FUSION_AUDIO_WEIGHT=0.3
export FUSION_VIDEO_WEIGHT=0.1
export FUSION_METHOD=confidence_weighted
```

---

## 📊 **Weight Tuning Guidelines**

### **For Avatar Emotions (Gandhar's Team)**
```yaml
# Emotional nuance requires balanced multimodal input
weights:
  text: 0.3    # Text provides context
  audio: 0.4   # Audio captures tone, emotion
  video: 0.3   # Video shows facial expressions

# Recommended settings
confidence_threshold: 0.8  # Higher threshold for emotion accuracy
consensus_boost: 0.2      # Boost when all modalities agree
```

**Tuning Tips:**
- **Increase audio weight** for tone-based emotions (happy, sad, angry)
- **Increase video weight** for visual emotions (surprise, disgust)
- **Use confidence_weighted method** for nuanced emotion detection

### **For AI Teacher Scoring (Vedant/Rishabh's Team)**
```yaml
# Educational content prioritizes text with audio context
weights:
  text: 0.6    # Primary: content analysis
  audio: 0.3   # Secondary: engagement, clarity
  video: 0.1   # Minimal: visual aids

# Recommended settings
method: "adaptive"         # Learn from scoring patterns
confidence_threshold: 0.75 # Moderate threshold for education
```

**Tuning Tips:**
- **High text weight** for content accuracy assessment
- **Moderate audio weight** for student engagement detection
- **Use adaptive method** to improve scoring over time

### **For Content Moderation (Shashank's Team)**
```yaml
# Safety requires high precision and text focus
weights:
  text: 0.7    # Primary: text content analysis
  audio: 0.2   # Secondary: tone analysis
  video: 0.1   # Minimal: visual content

# Recommended settings
method: "simple"           # Consistent, predictable results
confidence_threshold: 0.9  # Very high threshold for safety
```

**Tuning Tips:**
- **Maximum text weight** for content policy detection
- **High confidence threshold** to minimize false positives
- **Simple method** for consistent moderation decisions

---

## 🔧 **Advanced Configuration**

### **Custom Confidence Thresholds**
```yaml
modalities:
  text:
    min_confidence: 0.3
    weight_range: [0.2, 0.7]
    fallback_weight: 0.4
  
  audio:
    min_confidence: 0.2
    weight_range: [0.1, 0.5]
    fallback_weight: 0.3
```

### **Dynamic Weight Adjustment**
```yaml
dynamic_weights:
  confidence_scaling:
    enabled: true
    min_confidence: 0.3
    max_confidence: 0.95
    scaling_factor: 1.5
  
  consensus_scaling:
    enabled: true
    agreement_threshold: 0.8
    consensus_boost: 0.15
```

### **Environment-Specific Settings**
```yaml
environments:
  development:
    fusion:
      method: "simple"
      enable_dynamic_weights: false
    logging:
      debug_mode: true
  
  production:
    fusion:
      method: "confidence_weighted"
      hot_reload: false
    monitoring:
      track_fusion_performance: true
```

---

## 🚀 **Quick Configuration Recipes**

### **Recipe 1: High Accuracy (Research/Analysis)**
```yaml
fusion:
  method: "confidence_weighted"
  confidence_threshold: 0.85
weights:
  text: 0.5
  audio: 0.25
  video: 0.25
```

### **Recipe 2: Fast Processing (Real-time)**
```yaml
fusion:
  method: "simple"
  enable_dynamic_weights: false
weights:
  text: 0.6
  audio: 0.2
  video: 0.2
```

### **Recipe 3: Emotion-Focused (Avatar)**
```yaml
fusion:
  method: "confidence_weighted"
  confidence_threshold: 0.8
weights:
  text: 0.2
  audio: 0.4
  video: 0.4
```

### **Recipe 4: Content-Focused (Education/Moderation)**
```yaml
fusion:
  method: "simple"
  confidence_threshold: 0.9
weights:
  text: 0.8
  audio: 0.15
  video: 0.05
```

---

## 🔍 **Monitoring and Debugging**

### **Enable Performance Tracking**
```yaml
monitoring:
  track_fusion_performance: true
  performance_window: 1000
  auto_adjust_weights: false
```

### **Enable Debug Logging**
```yaml
logging:
  log_fusion_decisions: true
  log_weight_adjustments: true
  log_confidence_scores: true
  debug_mode: true
```

### **Check Configuration Status**
```python
from fusion_config_manager import get_fusion_config_manager

manager = get_fusion_config_manager()

# Get current configuration
print("Current method:", manager.get_fusion_method())
print("Current weights:", manager.get_weights())
print("Confidence threshold:", manager.get_confidence_threshold())

# Get team-specific notes
notes = manager.get_integration_notes('gandhar_team')
print("Integration notes:", notes)
```

---

## ⚠️ **Important Notes**

1. **Weight Validation**: Weights must sum to 1.0 (auto-normalized if not)
2. **Hot Reload**: Changes apply within 30 seconds when enabled
3. **Backup**: Original config is backed up before changes
4. **Environment**: Use environment-specific settings for dev/staging/prod
5. **Authentication**: Config API changes require authentication in production

---

## 📞 **Support**

- **Configuration Issues**: Check `logs/fusion_config.log`
- **Performance Problems**: Enable monitoring and check metrics
- **Team Integration**: See team-specific sections above
- **Advanced Features**: Contact the development team

**Remember**: All changes can be made without touching any Python code! 🎉
