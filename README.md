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
- Git (for cloning the repository)

### Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/chenmis/mnist.git
   cd mnist
2. **Run the Service:
  Navigate to the project directory.
  Execute the run.sh script to start both the service and client in separate Docker containers.
  ```bash
  ./run.sh
