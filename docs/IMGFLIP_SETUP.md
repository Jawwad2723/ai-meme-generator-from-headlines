# 🖼️ Imgflip Setup Guide

## Why Imgflip?

✅ **100% FREE** - No credit card, no limits, forever!
✅ **Easy API** - Simple REST API, works instantly
✅ **100 requests/day FREE** - More than enough for testing
✅ **Popular templates** - All the viral memes you know
✅ **No rate limiting** - (for free tier usage)

## Step-by-Step Setup

### Step 1: Create Account (30 seconds)

1. Go to: https://imgflip.com/signup
2. Fill in:
   - Username (this is your API username)
   - Email
   - Password (this is your API password)
3. Click "Sign up"
4. **Done!** No email verification needed for API

### Step 2: Get Your Credentials

Your API credentials are:
- **Username:** The username you just created
- **Password:** The password you just created

That's it! No API key needed, just username/password.

### Step 3: Add to .env

Edit your `.env` file:

```bash
IMGFLIP_USERNAME=your-username-here
IMGFLIP_PASSWORD=your-password-here
```

**Important:** 
- Don't use quotes
- Use the SAME username and password you use to login to imgflip.com

### Step 4: Test (Optional)

Visit https://imgflip.com/api and try the example:

```bash
curl -X POST https://api.imgflip.com/caption_image \
  -d template_id=181913649 \
  -d username=YOUR_USERNAME \
  -d password=YOUR_PASSWORD \
  -d text0="TOP TEXT" \
  -d text1="BOTTOM TEXT"
```

Should return JSON with `"success": true`

## Free Tier Details

### What's Included (FREE):

✅ **Unlimited meme generation**
✅ **100+ meme templates**
✅ **Custom text on any template**
✅ **High-quality images**
✅ **No watermark** (on most templates)
✅ **Direct image URLs**
✅ **No expiration** (images stay forever)

### Limits (Generous):

- **100 API requests per day** (per account)
- **Rate limit:** ~1 request per second
- **Image size:** Up to 1000x1000px

For this project:
- Generate 100 memes per day = **FREE**
- Generate 10 memes = only 10 API calls
- **Perfect for development and testing!**

## Popular Templates

Our app includes these templates by default:

| Template Name | Description | Best For |
|---------------|-------------|----------|
| **Drake Hotline Bling** | Drake rejecting/accepting | Comparing two options |
| **Distracted Boyfriend** | Guy looking at another girl | Temptation, distraction |
| **Two Buttons** | Guy can't decide which button | Difficult choices |
| **Expanding Brain** | Intelligence levels | Escalating ideas |
| **Change My Mind** | Guy at table with sign | Controversial opinions |
| **Is This A Pigeon** | Anime guy confused | Misidentifying things |
| **Woman Yelling At Cat** | Split image | Arguments, disagreements |
| **Success Kid** | Baby with fist pump | Small victories |
| **One Does Not Simply** | Boromir from LOTR | Things that are difficult |
| **Ancient Aliens** | Guy with wild hair | Conspiracy theories |

## API Details

### Endpoint

```
POST https://api.imgflip.com/caption_image
```

### Parameters

- `template_id`: Template ID number
- `username`: Your Imgflip username
- `password`: Your Imgflip password
- `text0`: Top text (all caps recommended)
- `text1`: Bottom text (all caps recommended)

### Response

```json
{
  "success": true,
  "data": {
    "url": "https://i.imgflip.com/abc123.jpg",
    "page_url": "https://imgflip.com/i/abc123"
  }
}
```

## Troubleshooting

### "Invalid username or password"

**Check:**
1. Can you login to imgflip.com with same credentials?
2. Are there quotes around values in .env? (Remove them)
3. Are there spaces? (Remove them)
4. Is username spelled correctly?

**Example of correct .env:**
```bash
IMGFLIP_USERNAME=johndoe
IMGFLIP_PASSWORD=mypassword123
```

**Example of WRONG:**
```bash
IMGFLIP_USERNAME="johndoe"  # NO QUOTES!
IMGFLIP_PASSWORD='mypassword123'  # NO QUOTES!
IMGFLIP_USERNAME= johndoe  # NO SPACES!
```

### "Rate limit exceeded"

You've made more than 100 requests in one day.

**Solutions:**
1. Wait 24 hours (resets daily)
2. Create another free account
3. Use caching (save memes, don't regenerate)

### "Template not found"

Using template ID that doesn't exist.

**Solution:**
- Use template names from our default list
- Check https://imgflip.com/memetemplates for valid IDs
- Stick to popular templates (they always work)

## Advanced: Finding More Templates

1. Go to: https://imgflip.com/memetemplates
2. Find a meme you like
3. Click on it
4. Look at the URL: `https://imgflip.com/meme/TEMPLATE-ID`
5. Use that TEMPLATE-ID in API calls

**Example:**
- Drake template URL: https://imgflip.com/meme/181913649
- Template ID: `181913649`

## Best Practices

### 1. Keep Text Short

- Top text: 5-10 words max
- Bottom text: 5-10 words max
- Use ALL CAPS (meme tradition)

### 2. Cache Generated Memes

Don't regenerate same meme multiple times. Save URLs!

```python
# Good: Save meme URLs
meme_cache = {}
if headline in meme_cache:
    return meme_cache[headline]
else:
    url = create_meme(...)
    meme_cache[headline] = url
    return url
```

### 3. Handle Rate Limits

```python
import time

# Add small delay between requests
time.sleep(1)  # 1 second between memes
```

### 4. Test Locally First

Before deploying, test with small batches:
- Start with 1 meme
- Then try 5 memes
- Then scale up

## Upgrading (Optional)

If you outgrow the free tier:

**Imgflip Pro:**
- $9.95/month
- Unlimited API calls
- No rate limits
- Remove watermarks
- Priority support

**For this project:** Free tier is usually enough!

## Summary

✅ **Sign up:** https://imgflip.com/signup (30 seconds)
✅ **Add to .env:** Username and password (no quotes!)
✅ **Start generating:** 100 memes/day FREE forever
✅ **No credit card:** Never needed

**That's it! Imgflip is the easiest part of the setup!** 🎨

---

**Questions?**
- Imgflip API Docs: https://imgflip.com/api
- Imgflip Support: https://imgflip.com/contact