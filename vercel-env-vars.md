# Vercel Environment Variables Setup

## Required Environment Variables for Vibespan.ai

### 1. **LLM APIs** (for AI agents)
```
OPENAI_API_KEY=sk-your-openai-api-key-here
ANTHROPIC_API_KEY=sk-ant-your-anthropic-api-key-here
```

### 2. **GitHub OAuth** (for authentication)
```
GITHUB_CLIENT_ID=your-github-oauth-app-client-id
GITHUB_CLIENT_SECRET=your-github-oauth-app-client-secret
```

### 3. **WHOOP v2 Integration** (for real-time health data)
```
WHOOP_CLIENT_ID=your-whoop-client-id
WHOOP_CLIENT_SECRET=your-whoop-client-secret
WHOOP_WEBHOOK_SECRET=your-whoop-webhook-secret
WHOOP_WEBHOOK_TOKEN=your-whoop-webhook-token
WHOOP_V2_BASE_URL=https://api.prod.whoop.com
```

### 4. **Security & Encryption**
```
JWT_SECRET_KEY=your-super-secret-jwt-key-here-make-it-long-and-random
ENCRYPTION_KEY=your-32-byte-encryption-key-here
```

### 5. **Environment Configuration**
```
ENVIRONMENT=production
DEBUG=false
BASE_URL=https://vibespan.ai
```

## How to Add Environment Variables in Vercel:

1. **Go to your Vercel dashboard**
2. **Select your project** (vibespan)
3. **Go to Settings** → **Environment Variables**
4. **Add each variable** with the following settings:
   - **Name**: The variable name (e.g., `OPENAI_API_KEY`)
   - **Value**: Your actual API key or secret
   - **Environment**: Select `Production`, `Preview`, and `Development`
5. **Click "Save"** for each variable
6. **Redeploy** your application

## Important Notes:

- **Never commit real API keys** to your repository
- **Use strong, random secrets** for JWT_SECRET_KEY and ENCRYPTION_KEY
- **Test with development keys first** before using production keys
- **Environment variables are encrypted** in Vercel and only accessible at runtime

## Quick Start (Minimum Required):

For basic functionality, you only need:
```
OPENAI_API_KEY=sk-your-openai-key
JWT_SECRET_KEY=your-random-secret-key
ENVIRONMENT=production
```

## Security Best Practices:

1. **Generate strong secrets**:
   ```bash
   # For JWT_SECRET_KEY (32+ characters)
   openssl rand -base64 32
   
   # For ENCRYPTION_KEY (32 bytes)
   openssl rand -hex 32
   ```

2. **Use different keys** for different environments
3. **Rotate keys regularly** for production
4. **Monitor usage** through API provider dashboards
