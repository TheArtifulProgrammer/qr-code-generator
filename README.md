# 🔗 Custom QR Code Generator

A sleek, modern web application for generating custom QR codes with logos, custom colors, and branding options. Built with FastAPI and featuring a beautiful, responsive user interface.

![QR Code Generator](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white)
![CSS3](https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black)

## ✨ Features

- 🎨 **Custom Colors**: Choose any color for QR code and background.
- 🖼️ **Logo Integration**: Upload and embed logos in the center of QR codes.
- 🎯 **High Error Correction**: Ensures QR codes work even with logos.
- 📱 **Responsive Design**: Works perfectly on desktop, tablet, and mobile.
- ⚡ **Fast Generation**: Instant QR code creation.
- 💾 **Easy Download**: One-click download of generated QR codes.
- 🔧 **Customizable Border**: Optional circular border around logos.
- 🌐 **Modern UI**: Clean, intuitive interface with smooth animations.

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/TheArtifulProgrammer/qr-code-generator.git
cd qr-code-generator
```
Create a virtual environment (recommended)

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

Create required directories

```bash
mkdir -p static/generated uploads
```

Run the application

```bash
uvicorn main:app --reload
```

Open your browser and navigate to http://localhost:8000
