# 🚀 FASTAPI CLI (Zackry CLI)

**ZACKRY CLI** is a Python command-line tool that helps developers quickly bootstrap **FastAPI projects**, manage **encryption**, **Docker workflows**, **requests**, and **development utilities** using best practices and simple interactive commands.

Built to be **clean**, **interactive**, and **production-ready**.

---

## ✨ Features

* ⚡ FastAPI project scaffolding
* 🔐 Encryption utilities (.env safe encryption)
* 🐳 Docker build & deployment helpers
* 🎫 Request management → Excel export
* 📦 Pip & virtual environment guide
* 🧭 Interactive CLI (arrow-key selection)
* 🧑‍💻 Beginner-friendly, production-ready

---

## 📦 Installation

```bash
pip install dev-cli
```

Verify installation:

```bash
dev --help
```
![test2](https://github.com/user-attachments/assets/5f1e54e0-5b14-4aa4-adfb-7394820cffd0)

---

## 🧭 CLI Commands Overview

| Command              | Description                  |
| -------------------- | ---------------------------- |
| `dev i` / `dev init` | Initialize FastAPI project   |
| `dev e`              | Encryption tools 🔐          |
| `dev b`              | Docker build tools 🐳        |
| `dev d`              | Docker deployment            |
| `dev g`              | Component generator          |
| `dev r`              | Request management system 🎫 |
| `dev zackry`         | Developer guide & pip help   |

---

## 🏗️ Project Structure

Generated FastAPI structure:

```
app/
├── main.py                 # FastAPI entry point
├── core/
│   └── config.py           # App configuration (.env)
├── routers/
│   └── health.py           # Health check endpoint
├── services/               # Business logic
├── models/                 # ORM models
├── schemas/                # Pydantic schemas
├── utils/
│   └── encryption.py       # Encryption helpers
├── db/                     # Database (only if enabled)
tests/
.env
requirements.txt
Dockerfile
pip.conf
README.md
```

📝 **Note:**
If you select **No DB**, the `db/` folder will NOT be created.

---

## ⚡ Quick Start

### 1️⃣ Initialize a project

```bash
dev i
```

You’ll be asked:

```
? Do you need DB connection? (Y/n)
```

---

### 2️⃣ Run FastAPI (Development)

```bash
uvicorn app.main:app --reload
```

Visit:

```
http://127.0.0.1:8000/health
```

---

<img width="3024" height="306" alt="image" src="https://github.com/user-attachments/assets/6ec0e652-303e-4c32-938b-34864f4e7c51" />

## 🔐 Encryption Guide

### Generate encryption key

```bash
dev e
→ Generate Key
```

✔ Automatically saved at **line 1** of `.env`:

```env
KEY=xxxxxxx
```

---

### Encrypt a value

```bash
dev e
→ Encrypt Value
```

✔ Uses `KEY` from `.env` automatically
✔ No manual key input needed

---

### Encrypt entire `.env`

```bash
dev e
→ Encrypt Entire .env File
```

* `KEY` is **never encrypted**
* Preview shown before encrypt
* Confirmation required (Y/n)

Example:

```env
KEY=xxxx
ENABLE_LOG_REQUEST_HEADER=gAAAAAB...
DEBUG_MODE=gAAAAAB...
```

---

<img width="3022" height="274" alt="image" src="https://github.com/user-attachments/assets/9959d660-d428-40dd-b021-eeea7fca4079" />
<img width="3018" height="416" alt="image" src="https://github.com/user-attachments/assets/dfc6a30b-8b17-4f04-b8cd-6683a649b84b" />

## 🎫 Request Management (Excel)

```bash
dev r
```

✔ Interactive input
✔ Generates Excel file
✔ Structure:

```
DEV | UAT | PROD
Name | Value
```

✔ Output path defaults to **current directory**

---

## 🐳 Docker

### Build image

```bash
dev b
```
<img width="3024" height="222" alt="image" src="https://github.com/user-attachments/assets/dd6cd802-c0d2-42d5-8287-5b432e9e2048" />

### Production run

```bash
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker
```

### Worker guide

* `-w 1` → Development
* `-w 2` → Small traffic
* `-w 4` → Recommended default
* `-w N` → CPU cores × 2 + 1

---

## 📦 Pip & Environment Guide

```bash
dev zackry
```

Includes:

* Clean requirements generation
* Virtualenv best practices
* Common pip commands
* FastAPI debugging tips
* Testing examples

---

## 🧪 Testing

Quick health test:

```bash
python -c "import requests; print(requests.get('http://127.0.0.1:8000/health').json())"
```

Run tests:

```bash
pytest tests/
```

---

## 🧑‍💻 Author

**Created by Hour Zackry**

* 🔗 LinkedIn:
  [https://www.linkedin.com/in/pho-keanghour-27133b21b/](https://www.linkedin.com/in/pho-keanghour-27133b21b/)
* 🌐 Website:
  [https://keanghour.github.io/keanghour.me/](https://keanghour.github.io/keanghour.me/)

---

## ⭐ Philosophy

> Simple tools.
> Clean structure.
> Production mindset.

Happy coding 🚀

---

If you want, next I can:

* Optimize GitLab badges
* Add screenshots
* Add CI/CD `.gitlab-ci.yml`
* Rename dev → Zackry CLI fully

<img width="1040" height="362" alt="image" src="https://github.com/user-attachments/assets/e377d6b3-9b1f-4650-9caf-52b02ba813ff" />



