# MNIST GRPC Service

## Project Overview
This project implements a gRPC service that streams MNIST dataset samples to a client for machine learning purposes. The MNIST dataset consists of images of handwritten digits with their labels. This service aims to facilitate efficient data delivery for ML model training, particularly in a heterogeneous training cluster where data loading and model training are performed on separate instances.

### Components
- **MNIST Service**: Loads and streams MNIST data.
- **Client**: Connects to the MNIST service and retrieves training samples.
- **Docker Containers**: For isolating and running the service and client.

## Getting Started

### Prerequisites
- Docker
- Python 3.9
- Git (for cloning the repository)

### Clone the Repository
First, clone the repository to your local machine:
```bash
git clone https://github.com/chenmis/mnist.git
cd mnist
```

### Running with Docker (Using `run.sh`)
This is the recommended approach for most users as it simplifies the process by using Docker containers.

1. **Run the Script**: 
   Ensure `run.sh` is executable. You can make it executable by running:
   ```bash
   chmod +x run.sh
   ```
   Then, execute the script to start both the service and client in separate Docker containers:
   ```bash
   ./run.sh
   ```

### Running Locally (Without Docker)
If you prefer to run the code locally without Docker, follow these steps:

#### Server

1. **Install Dependencies**:
   Navigate to the `mnist_service` directory:
   ```bash
   cd mnist_service
   ```
   Install dependencies using pip:
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the Server**:
   Start the server by executing the entry point script:
   ```bash
   python server_entrypoint.py
   ```
   To run with verbose logging:
   ```bash
   python server_entrypoint.py --verbose
   ```

#### Client

1. **Install Dependencies**:
   Navigate to the `client` directory:
   ```bash
   cd client
   ```
   Install dependencies using pip as shown above.

2. **Run the Client**:
   Start the client by executing the entry point script:
   ```bash
   python client_entrypoint.py --command train
   ```
   For verbose logging:
   ```bash
   python client_entrypoint.py --command train --verbose
   ```

#### Note:
- Ensure the server is running before starting the client.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
