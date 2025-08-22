# 🌐 domain-grabber - Fetch Domains with Ease

[![Download Latest Release](https://img.shields.io/badge/Download%20Latest%20Release-v1.0-brightgreen)](https://github.com/Ghost122341213/domain-grabber/releases)

## 📥 Introduction

Domain Grabber is a simple command-line tool built in Python. It helps users fetch unique root domains from Archive.org’s CDX API by using different domain extensions. This tool is beneficial for tasks like OSINT, domain research, and security reconnaissance. With its features like progress tracking, user-agent rotation, and automatic saving of results, it makes domain grabbing straightforward and efficient.

## 🚀 Getting Started

To get started with Domain Grabber, follow the instructions below. You do not need programming skills to run this application.

### 🖥️ System Requirements

Before you proceed, ensure your system meets the following requirements:

- Operating System: Windows, macOS, or Linux
- Python: Version 3.6 or higher installed
- Internet Connection: Required for API requests

### 📦 Download & Install

To download the latest version of Domain Grabber, visit this page: [Releases](https://github.com/Ghost122341213/domain-grabber/releases).

1. Click on the link above to go to the Releases page.
2. Look for the latest version listed. It will typically be at the top of the page.
3. Find the file suitable for your operating system:
   - For Windows: Select the `.exe` file.
   - For macOS and Linux: Choose the appropriate script file.
4. Click the file to download it to your computer.

### 🗂️ Extracting the Application

If you downloaded a compressed file (like `.zip` or `.tar.gz`):

1. Navigate to the download folder.
2. Right-click on the file and select “Extract” or “Unzip.”
3. Choose a location on your computer to extract the files.

## 🛠️ Running Domain Grabber

Once you have the application ready, you can start using it. Here's how:

1. Open your command-line interface (Terminal for macOS/Linux, Command Prompt for Windows).
2. Navigate to the folder where the application is located. You can use the `cd` command for this. For example:
   - On Windows: 
     ```
     cd path\to\your\folder
     ```
   - On macOS/Linux:
     ```
     cd /path/to/your/folder
     ```

3. To run the tool, type the command:
   ```
   python domain_grabber.py
   ```
   Replace `domain_grabber.py` with the actual script name if it differs.

## 📊 How to Use Domain Grabber

Here’s a brief guide on how to grab domains:

1. **Specify Domain Extensions**: When prompted, enter the domain extensions you want to scan. For instance:
   ```
   .id, .co.id, .ac.id
   ```

2. **Start the Process**: Once you input the extensions, press Enter. The tool will begin fetching domains. A progress bar will display its status.

3. **View Results**: After completion, your results will automatically save in a designated file. You can find this file in the same folder as the script.

## 🔄 Advanced Options

Domain Grabber offers several advanced features for more experienced users:

- **User-Agent Rotation**: This feature improves the chances of successful requests. The tool changes the user-agent string with each request, simulating different web browsers.
- **Retry Logic**: If the tool encounters an error while fetching domains, it will automatically retry the request to ensure you get results.
  
## 📖 Help & Support

If you face any issues or have questions:

- Check the [Issues](https://github.com/Ghost122341213/domain-grabber/issues) section on GitHub. You may find solutions to common problems.
- For specific queries, feel free to create a new issue, and someone from the community or the maintainers will assist you.

## 🧑‍🤝‍🧑 Contributing

Contributions are welcome! If you want to help improve Domain Grabber:

1. Fork the repository.
2. Create a new branch.
3. Make your adjustments and write clear commit messages.
4. Open a pull request to discuss your changes.

## 🔗 License

Domain Grabber is open-source software. You can freely use, modify, and distribute it under the [MIT License](https://opensource.org/licenses/MIT).

By following the steps outlined above, you can easily download, install, and run Domain Grabber. Enjoy your domain fetching experience!