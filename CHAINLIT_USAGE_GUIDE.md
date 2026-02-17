# 🌐 Chainlit Web App Usage Guide
## Clinical Trial Sample Size Calculator

Your multi-agent sample size calculator is now available as a beautiful, user-friendly web application!

## 🚀 **Quick Start**

### **Method 1: Using the Launch Script (Recommended)**

```bash
# Navigate to your RAG directory
cd /homes/chencx29/RAG

# Launch the app
./launch_app.sh
```

### **Method 2: Direct Command**

```bash
# From the RAG directory
/homes/chencx29/miniconda3/envs/PyRAG/bin/chainlit run chainlit_sample_size_app.py --port 8000
```

## 🌐 **Accessing the App**

Once started, open your web browser and navigate to:
- **Local access**: http://localhost:8000
- **Network access**: http://your-server-ip:8000

## 🎯 **App Features & Interface**

### **Welcome Screen**
When you first open the app, you'll see:
- ✅ **System status** (Multi-agent system, R MCP server, AI agents)
- 📊 **Template buttons** for common trial types
- 📝 **Welcome message** with instructions

### **Template Buttons**
Click these for quick setup:

1. **📊 Two-Arm Superiority Trial**
   - Standard placebo-controlled study
   - Simple effect size input
   - Common statistical parameters

2. **📈 Three-Arm Dose Response**
   - Dose-finding studies
   - Multiple effect sizes
   - Complex multiplicity control

3. **🔬 ABBV932 Example Trial**
   - Demonstrates full system capabilities
   - Real-world parameters
   - Comprehensive analysis

4. **⚙️ Custom Trial Design**
   - Any number of arms
   - Complex endpoint structures
   - Advanced configurations

5. **❓ Help & Examples**
   - Detailed usage instructions
   - Parameter explanations
   - Example inputs

## 💬 **Using Natural Language Input**

You can describe your trial in plain English:

### **Example Inputs:**

**Simple Two-Arm:**
```
Calculate sample size for a two-arm superiority trial comparing my drug to placebo. 
I expect a moderate effect size of -0.4 with 80% power and 15% dropout.
```

**Three-Arm Dose Response:**
```
I need a sample size for a three-arm dose-response study with placebo, 5mg, and 10mg. 
Effect sizes should be -0.3 and -0.5 respectively. I need 85% power with 20% dropout.
```

**Complex Multi-Arm:**
```
Design a four-arm trial comparing placebo to three doses (2.5mg, 5mg, 10mg). 
Expect dose-response with effect sizes -0.2, -0.35, -0.5. 
Need 90% power, 2.5% alpha, 25% dropout.
Multiple endpoints with 0.6 correlation.
```

## 📊 **Understanding Results**

### **Key Results Display:**
- **📈 Sample Size per Arm**: e.g., "180 subjects per arm"
- **👥 Total Enrollment**: e.g., "540 subjects total"
- **⚡ Power Achieved**: e.g., "80% power"
- **🔬 Method Used**: "Multi-agent analysis" or "R server calculation"

### **Detailed Reports:**
- **📄 Clinical Interpretation**: Professional regulatory-ready report
- **⚙️ Parameters Used**: Complete parameter summary table
- **📋 Statistical Justification**: Assumptions, limitations, recommendations

### **Interactive Features:**
- **🔄 New Calculation**: Start another analysis
- **⚙️ Modify Parameters**: Adjust existing calculation
- **📤 Export Results**: Download detailed reports

## 🎨 **App Interface Features**

### **Real-Time Processing:**
- **🔄 Processing messages**: Shows which agent is working
- **⏳ Progress updates**: "Calculation Agent: Computing optimal sample size..."
- **✅ Completion confirmations**: Clear success/failure indicators

### **Rich Content Display:**
- **📊 Formatted results** with clear sections
- **📄 Downloadable reports** as markdown files
- **📋 Interactive tables** for parameter summaries
- **🎯 Action buttons** for next steps

### **Error Handling:**
- **❌ Clear error messages** if something goes wrong
- **🔧 Helpful suggestions** for fixing issues
- **🔄 Recovery options** to try alternative approaches

## 🔧 **Advanced Usage**

### **Parameter Modification:**
After getting results, you can:
1. Click "⚙️ Modify Parameters"
2. Specify changes: "Increase power to 90%" or "Change effect size to -0.5"
3. Get updated calculations instantly

### **Multiple Scenarios:**
- Run different scenarios in sequence
- Compare results across different parameters
- Build comprehensive trial portfolios

### **Export & Documentation:**
- Download detailed markdown reports
- Save parameter configurations
- Generate regulatory-ready documentation

## 🛠️ **Troubleshooting**

### **Common Issues:**

**App won't start:**
```bash
# Check if you're in the right directory
pwd  # Should show /homes/chencx29/RAG

# Check if chainlit is available
/homes/chencx29/miniconda3/envs/PyRAG/bin/chainlit --version
```

**"System not initialized" error:**
- Refresh the browser page
- Check that .env file exists
- Verify Python environment

**Slow calculations:**
- ✅ This is normal - complex calculations take 30-60 seconds
- ⚠️ R server issues fall back to reliable simplified methods
- 🔄 Progress messages show system is working

**Natural language not working well:**
- 📊 Use template buttons instead
- 🔧 Be more specific about parameters
- 📝 Include all required information (arms, effect sizes, power, dropout)

### **Performance Tips:**

1. **Use Template Buttons**: Faster setup for common trial types
2. **Be Specific**: Include all key parameters in natural language descriptions
3. **Start Simple**: Begin with two-arm trials, then move to complex designs
4. **Check Progress**: Watch for processing messages to confirm system is working

## 🎯 **Best Practices**

### **For Optimal Results:**
1. **Template First**: Start with templates, then customize
2. **Complete Information**: Always specify effect sizes, power, dropout
3. **Realistic Parameters**: Use clinically meaningful effect sizes
4. **Multiple Scenarios**: Test different assumptions
5. **Save Results**: Download reports for documentation

### **For Different Trial Types:**

**Phase II Dose-Finding:**
- Use 3-4 arm templates
- Conservative effect sizes (-0.2 to -0.4)
- Higher dropout rates (25-30%)
- Moderate power requirements (80%)

**Phase III Confirmatory:**
- Use 2-3 arm templates
- Well-defined effect sizes based on Phase II
- Standard dropout rates (15-20%)
- High power requirements (90%+)

**Regulatory Submission:**
- Use detailed reports feature
- Document all assumptions
- Include sensitivity analyses
- Export comprehensive documentation

## 📱 **Mobile & Remote Access**

The app works on:
- **💻 Desktop browsers** (Chrome, Firefox, Safari, Edge)
- **📱 Mobile devices** (responsive design)
- **🌐 Remote access** (if server is network accessible)

## 🎉 **Summary**

Your Chainlit web app provides:
- **🤖 AI-powered** natural language processing
- **📊 Professional** sample size calculations  
- **🌐 Web-based** easy access from any device
- **📋 Complete** regulatory-ready documentation
- **🔧 Flexible** templates and custom designs
- **⚡ Fast** results in under a minute

---

## 🚀 **Ready to Start?**

1. **Launch the app**: `./launch_app.sh`
2. **Open browser**: http://localhost:8000
3. **Choose template** or describe your trial
4. **Get results** in 30-60 seconds
5. **Download reports** for your documentation

**Happy calculating! 🧮✨**