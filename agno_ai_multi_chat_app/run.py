import streamlit.web.cli as stcli
import sys
import os

def main():
    # Get the directory where your app.py is located
    current_dir = os.path.dirname(os.path.abspath(__file__))
    app_path = os.path.join(current_dir, "launch_ui/app.py")
    
    # Set up Streamlit command
    sys.argv = ["streamlit", "run", app_path]
    sys.exit(stcli.main())

if __name__ == "__main__":
    main()