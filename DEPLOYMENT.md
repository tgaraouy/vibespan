# 🚀 Vibespan.ai Deployment Guide

This guide covers deploying your Vibespan.ai platform to production using Vercel.

## 📋 Prerequisites

- GitHub repository: [https://github.com/tgaraouy/vibespan](https://github.com/tgaraouy/vibespan)
- Vercel account
- Domain name: `vibespan.ai` (or your preferred domain)

## 🌐 Vercel Deployment

### Step 1: Connect to Vercel

1. **Go to [Vercel Dashboard](https://vercel.com/dashboard)**
2. **Click "New Project"**
3. **Import from GitHub**: Select `tgaraouy/vibespan`
4. **Configure Project**:
   - Project Name: `vibespan`
   - Framework Preset: `Other`
   - Root Directory: `./`
   - Build Command: `pip install -r requirements.txt`
   - Output Directory: `./`

### Step 2: Environment Variables

Add these environment variables in Vercel dashboard:

```bash
# LLM Providers (Optional - for enhanced features)
OPENAI_API_KEY=your_openai_key_here
ANTHROPIC_API_KEY=your_anthropic_key_here

# Security
ENCRYPTION_KEY=your_32_character_encryption_key

# Database (Optional - for production)
DATABASE_URL=your_database_connection_string

# Webhook Secrets
WHOOP_WEBHOOK_SECRET=your_whoop_webhook_secret
APPLE_HEALTH_SECRET=your_apple_health_secret

# Application Settings
ENVIRONMENT=production
DEBUG=false
```

### Step 3: Build Configuration

Create `vercel.json` in your project root:

```json
{
  "version": 2,
  "builds": [
    {
      "src": "main.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "main.py"
    }
  ],
  "env": {
    "PYTHONPATH": "$PYTHONPATH:."
  }
}
```

### Step 4: Deploy

1. **Click "Deploy"** in Vercel
2. **Wait for build** to complete
3. **Get your deployment URL**: `https://vibespan-xxx.vercel.app`

## 🌍 Domain Configuration

### Step 1: Add Domain to Vercel

1. **Go to Project Settings** → **Domains**
2. **Add Domain**: `vibespan.ai`
3. **Add Wildcard**: `*.vibespan.ai`
4. **Configure DNS** as instructed by Vercel

### Step 2: DNS Configuration

Add these DNS records to your domain provider:

```
Type: A
Name: @
Value: 76.76.19.61

Type: CNAME
Name: www
Value: cname.vercel-dns.com

Type: CNAME
Name: *
Value: cname.vercel-dns.com
```

### Step 3: SSL Certificate

Vercel automatically provides SSL certificates for your domain.

## 🔧 Production Configuration

### Update Environment Variables

```bash
# Production settings
ENVIRONMENT=production
DEBUG=false
LOG_LEVEL=INFO

# Security
SECRET_KEY=your_production_secret_key
ALLOWED_HOSTS=vibespan.ai,*.vibespan.ai

# Database (if using external database)
DATABASE_URL=postgresql://user:pass@host:port/dbname

# Redis (for caching)
REDIS_URL=redis://host:port
```

### Update CORS Settings

In `main.py`, update CORS middleware:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://vibespan.ai", "https://*.vibespan.ai"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)
```

## 📊 Monitoring & Analytics

### Vercel Analytics

1. **Enable Vercel Analytics** in project settings
2. **Monitor performance** and user behavior
3. **Set up alerts** for errors and downtime

### Health Monitoring

Your platform includes built-in health monitoring:

- **Agent Status**: Monitor AI agent health
- **Data Processing**: Track data ingestion rates
- **Error Logging**: Automatic error detection
- **Performance Metrics**: Response times and throughput

## 🔒 Security Checklist

### Production Security

- [ ] **Environment Variables**: All secrets in Vercel env vars
- [ ] **HTTPS Only**: SSL certificates configured
- [ ] **CORS**: Restricted to your domain
- [ ] **Rate Limiting**: Implement API rate limits
- [ ] **Input Validation**: All inputs validated
- [ ] **Error Handling**: No sensitive data in error messages
- [ ] **Audit Logging**: All actions logged
- [ ] **Data Encryption**: PHI/PII encrypted at rest

### Webhook Security

- [ ] **Signature Verification**: Verify webhook signatures
- [ ] **IP Whitelisting**: Restrict webhook sources
- [ ] **Rate Limiting**: Prevent webhook spam
- [ ] **Payload Validation**: Validate all webhook data

## 🧪 Testing Production

### Health Check

```bash
curl https://vibespan.ai/health
```

### API Testing

```bash
# Test root endpoint
curl https://vibespan.ai/

# Test tenant dashboard (replace with your subdomain)
curl -H "Host: tgaraouy.vibespan.ai" https://vibespan.ai/dashboard

# Test API documentation
open https://vibespan.ai/docs
```

### Webhook Testing

```bash
# Test webhook endpoint
curl -X POST https://vibespan.ai/webhook/test/tgaraouy \
  -H "Content-Type: application/json" \
  -d '{"test": "data"}'
```

## 📈 Scaling Considerations

### Performance Optimization

- **Caching**: Implement Redis caching for frequent queries
- **Database**: Use connection pooling for database connections
- **CDN**: Use Vercel's global CDN for static assets
- **Monitoring**: Set up performance monitoring

### Multi-Tenant Scaling

- **Database Sharding**: Partition data by tenant
- **Load Balancing**: Distribute load across instances
- **Caching Strategy**: Tenant-specific caching
- **Resource Limits**: Per-tenant resource quotas

## 🆘 Troubleshooting

### Common Issues

1. **Build Failures**
   - Check Python version compatibility
   - Verify all dependencies in `requirements.txt`
   - Check build logs in Vercel dashboard

2. **Environment Variables**
   - Ensure all required env vars are set
   - Check variable names match exactly
   - Verify no typos in values

3. **Domain Issues**
   - Verify DNS propagation (can take 24-48 hours)
   - Check SSL certificate status
   - Ensure wildcard domain is configured

4. **API Errors**
   - Check CORS configuration
   - Verify subdomain routing
   - Check middleware configuration

### Support Resources

- **Vercel Documentation**: [https://vercel.com/docs](https://vercel.com/docs)
- **GitHub Issues**: Report bugs and feature requests
- **Community**: Join discussions for help

## 🎉 Launch Checklist

### Pre-Launch

- [ ] **Domain configured** and SSL active
- [ ] **Environment variables** set in production
- [ ] **Health checks** passing
- [ ] **API endpoints** responding correctly
- [ ] **Webhook endpoints** functional
- [ ] **Error monitoring** configured
- [ ] **Backup strategy** in place

### Post-Launch

- [ ] **Monitor performance** for first 24 hours
- [ ] **Check error logs** for any issues
- [ ] **Verify user onboarding** flow works
- [ ] **Test data ingestion** with real data
- [ ] **Monitor agent processing** performance
- [ ] **Set up alerts** for critical issues

---

**Your Vibespan.ai platform is now live and ready to optimize health journeys! 🏥🤖✨**
