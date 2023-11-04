# Todo List Application Setup Guide

This document provides the instructions for setting up the environment for the Todo List application, which is split into two main parts: the backend (Python) and the frontend (React).

## Prerequisites

Ensure you have the following prerequisites installed before proceeding with the setup:
- Python 3.6 or later
- Node.js (which includes npm)
- Git

## Backend Setup

To set up the backend server, follow these steps:

### 1. Clone the Backend Repository

Clone the backend code from the GitHub repository.

```bash
git clone https://github.com/liviuorehovschi/todo-list.git
```

### 2. Create the Virtual Environment

Isolate your Python environment by creating a virtual environment.

```bash
python3 -m venv todo-list
```

### 3. Activate the Virtual Environment

Activate the created virtual environment.

Unix or MacOS
```bash
source todo-list/bin/activate
```

Windows
```bash
todo-list\Scripts\activate
```

### 4. Install the Requirements

Install the necessary Python packages defined in requirements.txt.

```bash
pip3 install -r requirements.txt
```

### 5. Run the Backend Server

Execute the following command to run the backend server.

```bash
python run.py
```

## Frontend Setup

Set up the frontend part of the application with these steps:

### 1. Clone the Frontend Repository

Clone the frontend code from the GitHub repository.

```bash
git clone https://github.com/liviuorehovschi/todo-list-front.git
```

### 2. Navigate to the Frontend Directory

Change into the directory of the cloned frontend repository.

```bash
cd todo-list-front
```

### 3. Install Node Packages

Install the required npm packages.

```bash
npm install
```

### 4. Start the Frontend Server

Finally, start the frontend server which will make the interface accessible.

```bash
npm start
```