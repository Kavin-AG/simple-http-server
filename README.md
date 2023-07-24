
# Simple HTTP Server with Authentication and Alphabetical Listing

This Python script sets up a simple HTTP server that serves files from a specified directory and provides authentication functionality. The server also lists the files and directories in alphabetical order when accessed through a web browser. The purpose of this project is to demonstrate how to create a basic HTTP server with authentication and custom directory listing using Python.

## Getting Started

Follow these instructions to set up and run the HTTP server on your local machine.

### Prerequisites

- Python 3.x installed on your system.

### Installation

1. Clone the repository to your local machine.

   ```bash
   git clone https://github.com/your-username/simple-http-server.git
   ```

2. Change the working directory to the cloned repository.

   ```bash
   cd simple-http-server
   ```

### Usage

1. Place the files you want to serve in a folder named `my_folder` inside the cloned repository.

2. Open the `server.py` file and modify the `USERNAME` and `PASSWORD` variables to set your desired authentication credentials. **Note: For demonstration purposes only; do not use sensitive credentials in this file.**

3. Run the HTTP server:

   ```bash
   python server.py
   ```

4. The server will start and display the IP address and port on which it is running (e.g., `Serving at http://192.168.1.10:8000/`).

5. Open your web browser and navigate to `http://localhost:8000/` or `http://<your-machine-IP>:8000/` to access the server. You'll be prompted to enter the authentication credentials set in step 2. After successful authentication, you will see the files and directories listed alphabetically.

### Customization

- You can modify the `BASE_DIRECTORY` variable in `server.py` to serve files from a different folder.

- To customize the appearance of the webpage, you can modify the CSS styles in the `list_directory()` method of the `CustomHandler` class in `server.py`.

### Security Considerations

- This HTTP server is intended for local testing or development. If you plan to make it accessible from the internet, follow proper security measures, such as enabling encryption (HTTPS), using a static IP or dynamic DNS, configuring a firewall, and limiting access to authorized users only.

- **Avoid using sensitive authentication credentials in the code for production scenarios.**

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- This project is inspired by the need to demonstrate how to create a basic HTTP server with authentication and alphabetical listing using Python.

---

Feel free to explore and use this simple HTTP server for your projects. If you encounter any issues or have suggestions for improvement, please create an issue or submit a pull request. Happy coding! 😊
