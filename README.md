# 🎨 AI Meme Generator

A production-ready pipeline that automatically generates viral memes from trending news headlines using AI.

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [How It Works](#how-it-works)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [API Documentation](#api-documentation)
- [Free Tier Information](#free-tier-information)
- [Examples](#examples)
- [Troubleshooting](#troubleshooting)
- [Project Structure](#project-structure)

## 🎯 Overview

This project automatically:
1. **Scrapes** trending news headlines from 8+ sources
2. **Generates** funny meme text using OpenAI GPT-4
3. **Creates** meme images with Imgflip API
4. **Optionally posts** to Twitter/Reddit
5. **Exposes** everything through a FastAPI endpoint

**Built with:** Python 3.10+, FastAPI, OpenAI GPT-4, Imgflip API

## ✨ Features

- ✅ **Fully Automated** - One API call does everything
- ✅ **AI-Powered Humor** - GPT-4 generates witty meme text
- ✅ **10+ Meme Templates** - Drake, Distracted Boyfriend, etc.
- ✅ **Free Tier Friendly** - Imgflip API is 100% FREE
- ✅ **Multi-Source Scraping** - 8 news sources with fallback
- ✅ **Social Media Ready** - Optional Twitter/Reddit posting
- ✅ **Production Quality** - Error handling, logging, docs

## 🔄 How It Works

```
News Sites → Scraper → GPT-4 → Meme Creator → Image URL
    ↓           ↓         ↓          ↓            ↓
8+ sources  Headlines  Funny text  Imgflip API  Share!
```

### The Pipeline:

1. **News Scraping** (10-20 seconds)
   - Scrapes from BBC, TechCrunch, The Verge, Reuters, etc.
   - Extracts clean headlines
   - Filters for meme-worthy content

2. **AI Text Generation** (20-30 seconds)
   - GPT-4 analyzes headlines
   - Creates funny, relatable meme text
   - Selects best template for the joke

3. **Image Creation** (5-10 seconds)
   - Calls Imgflip API
   - Generates meme with text overlay
   - Returns shareable image URL

4. **Optional Posting** (5 seconds)
   - Can post to Twitter automatically
   - Can post to Reddit (r/memes)
   - Returns post URLs

**Total Time:** ~40-60 seconds per meme

## 📦 Prerequisites

- **Python 3.10 or higher**
- **OpenAI API Key** ([Get free $5 credit](https://platform.openai.com/api-keys))
- **Imgflip Account** ([Free signup](https://imgflip.com/signup)) - **100% FREE, no limits!**
- Optional: Twitter/Reddit API keys (for posting)

## 🚀 Installation

### Step 1: Clone/Download Project

```bash
cd ai-meme-generator
```

### Step 2: Create Virtual Environment

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

## ⚙️ Configuration

### Step 1: Get API Keys

#### OpenAI API Key (Required)
1. Go to [OpenAI Platform](https://platform.openai.com/api-keys)
2. Sign up or log in
3. Click "Create new secret key"
4. Copy the key (starts with `sk-proj-`)

**Cost:** ~$0.01-0.02 per meme (very cheap!)

#### Imgflip Account (Required - 100% FREE!)
1. Go to [Imgflip](https://imgflip.com/signup)
2. Create FREE account
3. Go to [API page](https://imgflip.com/api)
4. Note your username and password

**Cost:** **$0** - Completely FREE! No limits!

#### Twitter API (Optional)
1. Apply at [Twitter Developer](https://developer.twitter.com/)
2. Create app and get keys
3. Add to `.env`

**Cost:** FREE for basic posting

#### Reddit API (Optional)
1. Go to [Reddit Apps](https://www.reddit.com/prefs/apps)
2. Click "Create App"
3. Select "script" type
4. Get client ID and secret

**Cost:** FREE

### Step 2: Configure Environment

```bash
# Copy example environment file
cp .env.example .env

# Edit .env with your favorite editor
nano .env  # or vim, code, notepad, etc.
```

Add your keys:
```bash
# REQUIRED
OPENAI_API_KEY=sk-proj-your-actual-key-here
IMGFLIP_USERNAME=your-username
IMGFLIP_PASSWORD=your-password

# OPTIONAL (for posting)
TWITTER_API_KEY=your-key
TWITTER_API_SECRET=your-secret
# ... etc
```

Save and close.

## 🎬 Usage

### Start the Server

```bash
# Easy way (if you have run.sh)
./run.sh

# OR manually
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Server will start at: `http://localhost:8000`

### Generate Memes

#### Option 1: Using Swagger UI (Easiest)

1. Open browser: http://localhost:8000/docs
2. Click `POST /generate-memes`
3. Click "Try it out"
4. Set `num_memes` (1-10)
5. Click "Execute"
6. Get meme URLs!

#### Option 2: Using cURL

```bash
curl -X POST "http://localhost:8000/generate-memes?num_memes=3"
```

#### Option 3: Using Python

```python
import requests

response = requests.post(
    "http://localhost:8000/generate-memes",
    params={"num_memes": 5}
)

data = response.json()

for meme in data['memes']:
    print(f"Headline: {meme['headline']}")
    print(f"Meme: {meme['image_url']}")
    print()
```

### Example Response

```json
{
  "status": "success",
  "memes": [
    {
      "headline": "Tech CEO Says AI Will Replace All Jobs",
      "meme_text_top": "TECH CEO: AI WILL REPLACE ALL JOBS",
      "meme_text_bottom": "ALSO TECH CEO: WHY IS NOBODY BUYING OUR PRODUCTS",
      "template_name": "Drake Hotline Bling",
      "image_url": "https://i.imgflip.com/8abc12.jpg",
      "created_at": "2026-02-05T10:30:45.123456"
    }
  ],
  "generated_at": "2026-02-05T10:30:45.123456",
  "count": 1
}
```

## 📚 API Documentation

### Endpoints

#### 1. Generate Memes
```
POST /generate-memes?num_memes=5
```

**Parameters:**
- `num_memes` (optional): Number of memes (1-10, default: 5)
- `news_category` (optional): Filter by category (tech, business, sports)

**Response:** List of generated memes with URLs

**Time:** ~40-60 seconds

#### 2. Get Meme Templates
```
GET /meme-templates
```

Returns list of available meme templates

#### 3. Post to Social Media
```
POST /post-meme
```

**Body:**
```json
{
  "meme_url": "https://i.imgflip.com/...",
  "caption": "When the news hits different 😂",
  "platform": "twitter"
}
```

Posts meme to Twitter or Reddit

#### 4. Health Check
```
GET /health
```

Checks API status and configuration

#### 5. Test Components
```
GET /test-components
```

Verifies all API keys are configured

### Complete API Docs

Visit `http://localhost:8000/docs` when server is running for interactive documentation.

## 💰 Free Tier Information

### What's FREE:

✅ **Imgflip API** - 100% FREE, unlimited memes!
✅ **OpenAI** - $5 free credit (500+ memes)
✅ **Twitter API** - FREE basic posting
✅ **Reddit API** - Completely FREE

### Costs (After Free Tier):

| Service | Free Tier | After Free | Per Meme |
|---------|-----------|------------|----------|
| **Imgflip** | ♾️ Unlimited | ♾️ Still FREE | **$0** |
| **OpenAI** | $5 credit | Pay-as-you-go | $0.01-0.02 |
| **Twitter** | FREE | FREE | **$0** |
| **Reddit** | FREE | FREE | **$0** |

**Total per meme:** $0.01-0.02 (just OpenAI)

### With Free Tiers:

- Imgflip: **Unlimited FREE memes** forever!
- OpenAI $5 credit: **~500 memes** before paying
- Can generate **hundreds of memes for free!**

## 🎨 Examples

### Real Meme Examples

**Input:** "Bitcoin Crashes 20% Overnight"

**Output:**
```
Template: Drake Hotline Bling
Top: "BUYING BITCOIN AT $60K"
Bottom: "BUYING BITCOIN AT $12K"
```

**Input:** "Scientists Discover New Planet"

**Output:**
```
Template: Ancient Aliens
Top: "NEW PLANET DISCOVERED"
Bottom: "ALIENS"
```

**Input:** "Gas Prices Hit Record High"

**Output:**
```
Template: Distracted Boyfriend
Boyfriend: Gas Prices
Girlfriend: $5/gallon
Other Girl: $8/gallon
```

## 🐛 Troubleshooting

### "OpenAI authentication failed"
**Fix:** Check `OPENAI_API_KEY` in `.env`

### "Imgflip error: Invalid username/password"
**Fix:** Verify `IMGFLIP_USERNAME` and `IMGFLIP_PASSWORD`
- Make sure no quotes around values
- Try logging into imgflip.com with same credentials

### "Failed to scrape headlines"
**Fix:** 
- Check internet connection
- System tries 8+ sources automatically
- Usually works on retry

### "No module named 'app'"
**Fix:**
```bash
# Make sure you're in project directory
cd ai-meme-generator

# Make sure virtual environment is activated
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows
```

## 📁 Project Structure

```
ai-meme-generator/
│
├── app/
│   ├── __init__.py              # Package initialization
│   ├── main.py                  # FastAPI app & endpoints
│   ├── config.py                # Configuration management
│   ├── news_scraper.py          # News headline scraping
│   ├── text_generator.py        # GPT-4 meme text generation
│   ├── meme_creator.py          # Imgflip meme creation
│   └── social_poster.py         # Twitter/Reddit posting (optional)
│
├── docs/
│   ├── code_explanation.md      # Line-by-line explanations
│   ├── API_EXAMPLES.md          # API usage examples
│   └── IMGFLIP_SETUP.md         # Imgflip setup guide
│
├── .env.example                 # Environment variables template
├── requirements.txt             # Python dependencies
├── README.md                    # This file
├── QUICKSTART.md                # 5-minute setup guide
└── run.sh                       # Startup script
```

## 🎓 Learning Resources

- [OpenAI API Docs](https://platform.openai.com/docs)
- [Imgflip API Docs](https://imgflip.com/api)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Meme Culture Guide](https://knowyourmeme.com/)

## 🤝 Contributing

Want to add features?
- More meme templates
- Different news sources
- New social platforms
- Better humor algorithms

## 📝 License

This project is for educational and demonstration purposes.

## 🎉 Have Fun!

Make memes, share laughs, go viral! 🚀

---

**Questions?** Check the [QUICKSTART.md](QUICKSTART.md) or [docs/](docs/) folder.

**Issues?** See [Troubleshooting](#troubleshooting) section above.

**Built with ❤️ using FastAPI, OpenAI GPT-4, and Imgflip**