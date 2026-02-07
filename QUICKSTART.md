# 🚀 Quick Start Guide - AI Meme Generator

Get viral memes running in **5 minutes**!

## ⚡ Super Fast Setup

### 1. Install Python Dependencies (1 minute)

```bash
cd ai-meme-generator
python3 -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
```

### 2. Get API Keys (2 minutes)

#### OpenAI (Required - $5 free credit)
1. Visit: https://platform.openai.com/api-keys
2. Click "Create new secret key"
3. Copy key (starts with `sk-proj-`)

#### Imgflip (Required - 100% FREE!)
1. Visit: https://imgflip.com/signup
2. Create account (takes 30 seconds)
3. Username = your email
4. Password = what you chose

### 3. Configure (.env file) (1 minute)

```bash
cp .env.example .env
nano .env  # or any editor
```

Add:
```bash
OPENAI_API_KEY=sk-proj-YOUR-KEY-HERE
IMGFLIP_USERNAME=your-username
IMGFLIP_PASSWORD=your-password
```

Save and exit.

### 4. Start Server (30 seconds)

```bash
./run.sh
# OR
uvicorn app.main:app --reload
```

### 5. Generate Your First Meme! (1 minute)

Open browser: http://localhost:8000/docs

1. Click `POST /generate-memes`
2. Click "Try it out"
3. Click "Execute"
4. Wait ~40 seconds
5. Get meme URL! 🎉

---

## 💡 First Time Tips

### Test Your Setup

```bash
# Check if server is running
curl http://localhost:8000/health

# Check if APIs are configured
curl http://localhost:8000/test-components
```

### Generate 1 Meme (Quick Test)

```bash
curl -X POST "http://localhost:8000/generate-memes?num_memes=1"
```

### Common First-Time Issues

**"Module not found"**
```bash
# Make sure virtual environment is activated
source venv/bin/activate
pip install -r requirements.txt
```

**"OpenAI authentication failed"**
```bash
# Check .env file
cat .env | grep OPENAI_API_KEY
# Make sure key has no quotes
```

**"Imgflip error"**
```bash
# Test login at imgflip.com with same credentials
# Make sure no quotes in .env
```

---

## 🎯 What You Can Do Now

✅ Generate memes from trending news
✅ Pick number of memes (1-10)
✅ Get shareable image URLs
✅ Save memes locally
✅ Share on social media

---

## 📚 Next Steps

- Read full [README.md](README.md) for all features
- Check [API_EXAMPLES.md](docs/API_EXAMPLES.md) for integration
- See [code_explanation.md](docs/code_explanation.md) to understand code

---

**That's it! You're making AI memes! 🎨**