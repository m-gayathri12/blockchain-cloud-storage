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

- **Frontend & Backend**: Django 2.1.7 (Python Framework)
- **Blockchain Layer**: Simulated or actual Ethereum interaction using Web3.py
- **Storage**: Local file system or IPFS 
- **Language**: Python 3.7.2

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
  - `django`
  - `hashlib`
  - `json`
  - `os`
    
##pip module requirements

Django==2.1.7
PyMySQL==0.9.3
pycryptodome==3.23.0
pyaes==1.6.1
web3==5.31.3
eth-account==0.5.9
eth-abi==2.2.0
eth-utils==1.10.0
eth-keys==0.3.4
rlp==2.0.1
ipfshttpclient==0.4.13.2
multiaddr==0.0.9
varint==1.0.2
jsonschema==4.17.3
numpy==1.21.6
pandas==1.3.5
matplotlib==3.1.1
scikit-learn==0.22.2.post1
joblib==1.3.2
PyPDF2==3.0.1
python-docx==1.1.0

  

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
