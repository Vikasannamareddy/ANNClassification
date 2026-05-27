# Activate the virtual environment and run Streamlit
$venvPath = "C:\Users\Vikas\OneDrive\Desktop\GenAI\Python\.venv\Scripts\Activate.ps1"
$appPath = "C:\Users\Vikas\OneDrive\Desktop\GenAI\Python\annclassification\ANNapp.py"

# Change to app directory
Set-Location "C:\Users\Vikas\OneDrive\Desktop\GenAI\Python\annclassification"

# Activate venv
& $venvPath

# Run streamlit
streamlit run $appPath
