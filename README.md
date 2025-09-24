# 🏥 Vibespan.ai - Health Agents in a Box

**Your personal AI health companion for a vibrant, long life.**

Vibespan.ai is a multi-tenant AI health platform that provides personalized health agents to optimize your wellness journey. Each user gets their own secure, private health intelligence system with AI agents that analyze your data and provide actionable insights.

## 🌟 Features

### 🤖 Core AI Agents
- **DataCollector**: Collects and normalizes health data from various sources
- **PatternDetector**: Finds correlations and trends in your health data
- **BasicWorkoutPlanner**: Provides personalized workout recommendations
- **BasicNutritionPlanner**: Offers nutrition guidance based on your health data
- **HealthCoach**: Provides general health coaching and motivation
- **SafetyOfficer**: Monitors your health data for safety concerns and alerts

### 📊 Data Integration
- **WHOOP v2**: Real-time recovery, sleep, and strain data
- **Apple Health**: Comprehensive health and fitness data
- **CSV Upload**: Historical health data import
- **Manual Entry**: Custom health tracking
- **Webhook Support**: Real-time data ingestion

### 🔒 Security & Privacy
- **Multi-tenant Architecture**: Each user gets isolated subdomain (`userid.vibespan.ai`)
- **Data Encryption**: PHI/PII data encrypted at rest
- **FHIR Compliance**: Standardized health data format
- **Audit Logging**: Complete activity tracking
- **3-Year Data Retention**: Automated cleanup policies

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Git

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/tgaraouy/vibespan.git
   cd vibespan
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   ```bash
   cp env.example .env
   # Edit .env with your API keys
   ```

4. **Run the application**
   ```bash
   python main.py
   ```

5. **Access your health dashboard**
   - Open `http://localhost:8000` in your browser
   - Use Host header `tgaraouy.localhost:8000` for tenant access

## 🧪 Testing

### Run Tests
```bash
# Test basic functionality
python simple_test.py

# Test with real health data
python test_with_real_data.py

# Test complete onboarding flow
python test_tgaraouy_onboarding.py
```

### Browser Testing
Open `browser_test.html` in your browser to test the web interface.

## 📡 API Documentation

Once the server is running, visit:
- **API Docs**: `http://localhost:8000/docs`
- **Interactive Testing**: Use the Swagger UI

### Key Endpoints

#### Onboarding
- `GET /onboarding/start` - Start onboarding process
- `GET /onboarding/data-sources` - Get available data sources
- `POST /onboarding/data-sources/connect` - Connect data source
- `POST /onboarding/goals` - Set health goals
- `POST /onboarding/agents/activate` - Activate agents
- `POST /onboarding/complete` - Complete onboarding

#### Agents
- `GET /agents/status` - Get agent status
- `POST /agents/process` - Process health data
- `GET /agents/insights` - Get health insights
- `POST /agents/chat` - Chat with agents

#### Webhooks
- `POST /webhook/whoop/{tenant_id}` - WHOOP v2 webhook
- `POST /webhook/apple-health/{tenant_id}` - Apple Health webhook
- `POST /webhook/test/{tenant_id}` - Test webhook

## 🏗️ Architecture

### Multi-Tenant Design
```
vibespan.ai/
├── tgaraouy.vibespan.ai/     # Your personal subdomain
├── user2.vibespan.ai/        # Another user's subdomain
└── user3.vibespan.ai/        # Third user's subdomain
```

### Agent Orchestration
```
Supervisor Agent
├── DataCollector Agent
├── PatternDetector Agent
├── BasicWorkoutPlanner Agent
├── BasicNutritionPlanner Agent
├── HealthCoach Agent
└── SafetyOfficer Agent
```

### Data Flow
```
Health Data Sources → Data Ingestion → FHIR Normalization → Agent Processing → Insights & Recommendations
```

## 🔧 Development

### Project Structure
```
vibespan/
├── src/
│   ├── api/                  # API routes
│   ├── agents/               # AI agents
│   ├── auth/                 # Authentication & tenant management
│   ├── data/                 # Data processing
│   ├── middleware/           # Custom middleware
│   └── models/               # Data models
├── schemas/                  # FHIR schemas
├── mappings/                 # Data source mappings
├── tests/                    # Test files
├── main.py                   # Application entry point
└── requirements.txt          # Dependencies
```

### Adding New Agents
1. Create agent class in `src/agents/`
2. Implement `BaseAgent` interface
3. Add to agent factory
4. Update tenant configuration

### Adding New Data Sources
1. Create mapping in `mappings/`
2. Add ingestion logic in `src/data/`
3. Update webhook routes
4. Test with sample data

## 🚀 Deployment

### Vercel Deployment
1. **Connect to Vercel**
   - Import repository from GitHub
   - Configure build settings

2. **Environment Variables**
   - Set API keys in Vercel dashboard
   - Configure database connections

3. **Domain Setup**
   - Point `*.vibespan.ai` to Vercel
   - SSL certificates auto-configured

### Environment Variables
```bash
# LLM Providers
OPENAI_API_KEY=your_openai_key
ANTHROPIC_API_KEY=your_anthropic_key

# Database
DATABASE_URL=your_database_url

# Security
ENCRYPTION_KEY=your_encryption_key

# Webhooks
WHOOP_WEBHOOK_SECRET=your_whoop_secret
```

## 📊 Your Health Data

### Current Data Sources
- **WHOOP Data**: 742 records (recovery, sleep, strain)
- **Workout Data**: 607 records (exercises, performance)
- **Food Data**: 371 records (nutrition tracking)
- **Health Data**: 371 records (general health metrics)
- **Supplements**: 86 records (supplement tracking)

### Data Processing
- **Total Records**: 2,178+ health data points
- **Real-time Processing**: Webhook ingestion active
- **Pattern Detection**: 3+ significant health patterns identified
- **Insights Generated**: 18+ personalized insights per analysis

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

- **Documentation**: Check the `/docs` folder
- **Issues**: Report bugs on GitHub Issues
- **Discussions**: Join GitHub Discussions

## 🎯 Roadmap

### Phase 1: Core Platform ✅
- [x] Multi-tenant architecture
- [x] Core AI agents
- [x] Data ingestion
- [x] Basic insights

### Phase 2: Advanced Features 🚧
- [ ] Premium agents (MedicationSpecialist, SleepOptimizer)
- [ ] Advanced pattern detection
- [ ] Mobile app
- [ ] Social features

### Phase 3: Enterprise 🎯
- [ ] Healthcare provider integration
- [ ] Clinical decision support
- [ ] Population health analytics
- [ ] Compliance certifications

---

**Built with ❤️ for your health and wellness journey**

*Vibespan.ai - Where AI meets your health data to optimize your life.*