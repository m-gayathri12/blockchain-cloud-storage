# Blockchain-Based Decentralized Cloud Storage with Reliable Deduplication and Storage Balancing

## 📝 Abstract

This project presents a blockchain-powered decentralized cloud storage system designed to overcome the limitations of centralized storage. By integrating reliable deduplication and intelligent storage balancing, the system ensures enhanced security, performance, and space efficiency. Blockchain provides transparency, immutability, and decentralized trust, while distributed storage architecture improves fault tolerance and availability.

---

## 🚀 Features

- 🔐 **Secure Encryption**: User data is encrypted before storage.
- 🧱 **Blockchain Integration**: Ensures data immutability and traceability.
- 🧮 **Reliable Deduplication**: Removes redundant files using hashing techniques without exposing sensitive content.
- ⚖️ **Intelligent Load Balancing**: Smart contracts monitor node capacity and distribute data dynamically.
- 🖥️ **User-Friendly UI**: Allows users to upload/download files and interact with the system seamlessly.

---

## 🏗️ System Architecture

- **User Interface Module**
- **Deduplication Module**
- **Encryption Module**
- **Blockchain Logging Module**
- **Smart Contract Balancer**

> 📊 UML diagrams: Class, Use Case, Sequence, and Collaboration diagrams are used to model and plan the system structure.

---

## 💻 Tech Stack

- **Frontend**: Basic UI in Python (Tkinter/Flask GUI depending on implementation)
- **Backend**: Python
- **Blockchain Layer**: Simulated blockchain structure using Python data structures
- **Database/Storage**: Local file storage across simulated nodes

---

## ⚙️ System Requirements

### Hardware
- Processor: Intel i3 or higher
- RAM: 4 GB
- Disk: 250 GB

### Software
- OS: Windows (or Linux)
- Language: Python 3.8+
- Required Libraries:
  - `flask`
  - `hashlib`
  - `json`
  - `os`
  - `shutil`

---

## 🛠️ Installation & Run

```bash
# Clone the repository
git clone https://github.com/your-username/decentralized-cloud-storage.git

# Navigate to the project directory
cd decentralized-cloud-storage

# Install dependencies (if using Flask UI or other external modules)
pip install -r requirements.txt

# Run the main application
python main.py
