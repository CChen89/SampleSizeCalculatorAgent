# 🧮 Clinical Trial Sample Size Calculator - Chainlit Web App

A beautiful web application for clinical trial sample size calculation using AI multi-agent system.

## 🎯 What This App Does

Transform complex statistical calculations into simple web-based interactions:
- **🌐 Beautiful Web Interface**: Professional UI accessible from any browser
- **💬 Natural Language Input**: Describe your trial in plain English
- **🤖 AI-Powered Analysis**: Multi-agent system handles complex calculations
- **📊 Instant Results**: Professional sample size recommendations in 30-60 seconds
- **📋 Regulatory Reports**: Download comprehensive documentation

## 🚀 Quick Start

### 1. Clone Repository
```bash
git clone https://github.com/CChen89/SampleSizeCalculatorAgent.git
cd SampleSizeCalculatorAgent
```

### 2. Install Dependencies
```bash
pip install -r requirements_multiagent.txt
```

### 3. Configure Environment
```bash
cp .env.example .env
# Edit .env with your Azure OpenAI credentials
```

### 4. Launch Web App
```bash
./launch_app.sh
```

### 5. Open Browser
Navigate to: **http://localhost:8000**

## 🌟 Features

### 🎯 **Easy to Use**
- **Template Buttons**: Quick setup for common trial types
- **Natural Language**: "I need sample size for a three-arm dose study..."
- **Interactive Chat**: Ask questions, modify parameters, get explanations
- **Professional Results**: Regulatory-ready reports

### 📊 **Statistically Rigorous**
- **Multi-Arm Trials**: 2-10 treatment arms supported
- **Multiple Endpoints**: Primary and secondary with correlations
- **Graphical Procedures**: Advanced multiplicity control
- **Power Optimization**: Automatic sample size search
- **Dropout Adjustment**: Built-in attrition modeling

### 🤖 **AI-Powered**
- **4 Specialized Agents**: Parameter validation, calculation, visualization, coordination
- **LangChain Integration**: Advanced language understanding
- **LangGraph Workflow**: Robust error handling and state management
- **R Integration**: Optional connection to statistical R server

## 📱 **Web Interface Preview**

When you open the app, you'll see:

```
🧮 Clinical Trial Sample Size Calculator

Welcome! I'm your AI-powered sample size calculator...

[📊 Two-Arm Trial]  [📈 Three-Arm Trial]  [🔬 ABBV932 Example]  [⚙️ Custom Design]  [❓ Help]

💬 Chat: Describe your trial design here...
```

## 🎯 **Example Usage**

### **Template Button Example**
1. Click "📊 Two-Arm Superiority Trial"
2. Type: "Placebo vs Treatment, effect size -0.4, 80% power, 15% dropout"
3. Get result: "116 subjects per arm recommended"

### **Natural Language Example**
Type in chat:
```
I need sample size for a three-arm dose-response study with placebo, 
5mg, and 10mg doses. Effect sizes should be -0.3 and -0.5 respectively. 
I need 85% power with 20% dropout.
```

Get comprehensive analysis with clinical interpretation.

## 📊 **Typical Results**

| Trial Type | Effect Size | Power | Dropout | Result |
|-----------|------------|-------|---------|---------|
| Two-arm | -0.4 | 80% | 15% | ~116 per arm |
| Three-arm | -0.33 | 80% | 20% | ~180 per arm |
| Four-arm | -0.2 to -0.5 | 85% | 25% | ~120-160 per arm |

## 🔧 **System Requirements**

- Python 3.8+
- Azure OpenAI API access (or compatible)
- Web browser (Chrome, Firefox, Safari, Edge)
- 2GB RAM minimum
- Network connection for AI model access

## 📚 **Documentation**

- [**Chainlit Usage Guide**](CHAINLIT_USAGE_GUIDE.md) - Complete web app manual
- [**Quick Start**](QUICK_START.md) - 5-minute tutorial
- [**Deployment Guide**](DEPLOYMENT.md) - Installation and deployment

## 🛠️ **Troubleshooting**

### Common Issues:
- **App won't start**: Check Python environment and dependencies
- **No results**: Verify .env configuration with API credentials
- **Slow responses**: Normal for complex calculations (30-60 seconds)

### Quick Tests:
```bash
# Test core system
python -c "from SampleSizeMultiAgent import MultiAgentSampleSizeCalculator; print('✅ Working')"

# Test web app  
python chainlit_sample_size_app.py --help
```

## 🎉 **Success Story**

This app transforms what used to be:
- ❌ **Hours of manual calculation**
- ❌ **Complex R programming required**  
- ❌ **Error-prone parameter management**
- ❌ **Limited accessibility**

Into:
- ✅ **30-60 second calculations**
- ✅ **Simple web interface**
- ✅ **AI-powered parameter extraction**
- ✅ **Accessible to entire clinical team**

## 📄 **License**

MIT License - see [LICENSE](LICENSE) file for details.

---

## 🚀 **Ready to Calculate Sample Sizes?**

1. **Clone this repository**
2. **Run `./launch_app.sh`**  
3. **Open http://localhost:8000**
4. **Start designing your clinical trials!**

Transform your clinical trial design workflow today! 🎊