# 🚀 Vercel Deployment Guide for Vibespan.ai

## Quick Deployment Steps

### 1. Go to Vercel Dashboard
- Visit [https://vercel.com/dashboard](https://vercel.com/dashboard)
- Click "New Project"

### 2. Import from GitHub
- Select "Import Git Repository"
- Choose `tgaraouy/vibespan`
- Click "Import"

### 3. Configure Project Settings
- **Project Name**: `vibespan`
- **Framework Preset**: `Other`
- **Root Directory**: `./` (leave as default)
- **Build Command**: Leave empty (Vercel will auto-detect)
- **Output Directory**: Leave empty
- **Install Command**: Leave empty

### 4. Environment Variables (Optional)
Add these in Vercel dashboard if you have them:
```
OPENAI_API_KEY=your_openai_key
ANTHROPIC_API_KEY=your_anthropic_key
ENCRYPTION_KEY=your_32_character_key
```

### 5. Deploy
- Click "Deploy"
- Wait for build to complete
- Get your deployment URL

## Troubleshooting

### If Build Fails with Dependencies:
1. **Use Minimal Requirements**: In Vercel settings, change build command to:
   ```bash
   pip install -r requirements-minimal.txt
   ```

2. **Use Simplified Main**: Change entry point to `main_simple.py` in vercel.json:
   ```json
   {
     "builds": [
       {
         "src": "main_simple.py",
         "use": "@vercel/python"
       }
     ]
   }
   ```

### If Still Having Issues:
1. **Check Build Logs**: Look at the build output in Vercel dashboard
2. **Try Different Python Version**: Set Python version in vercel.json:
   ```json
   {
     "functions": {
       "main.py": {
         "runtime": "python3.9"
       }
     }
   }
   ```

## Testing Your Deployment

### 1. Health Check
```bash
curl https://your-app.vercel.app/health
```

### 2. API Status
```bash
curl https://your-app.vercel.app/api/status
```

### 3. Tenant Test
```bash
curl https://your-app.vercel.app/api/tenant/tgaraouy
```

## Domain Setup (Optional)

### 1. Add Custom Domain
- Go to Project Settings → Domains
- Add `vibespan.ai`
- Add wildcard `*.vibespan.ai`

### 2. Configure DNS
Add these DNS records:
```
Type: A
Name: @
Value: 76.76.19.61

Type: CNAME  
Name: *
Value: cname.vercel-dns.com
```

## Success Indicators

✅ **Build Success**: No errors in build logs
✅ **Health Check**: `/health` endpoint returns 200
✅ **API Working**: `/api/status` returns JSON response
✅ **Tenant Access**: `/api/tenant/tgaraouy` works

## Your Repository
- **GitHub**: [https://github.com/tgaraouy/vibespan](https://github.com/tgaraouy/vibespan)
- **Latest Commit**: Vercel deployment fixes applied
- **Ready for Deployment**: All configurations optimized

---

**Your Vibespan.ai platform is ready to deploy! 🏥🤖✨**
