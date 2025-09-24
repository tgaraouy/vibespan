#!/usr/bin/env python3
"""
Simple Web Interface for Testing Vibespan.ai
Creates a basic HTML interface to test the onboarding flow.
"""

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import uvicorn

app = FastAPI(title="Vibespan.ai Test Interface")

@app.get("/", response_class=HTMLResponse)
async def test_interface():
    """Simple test interface"""
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Vibespan.ai Test Interface</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; background: #f5f5f5; }
            .container { max-width: 800px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
            h1 { color: #2c3e50; text-align: center; }
            .section { margin: 20px 0; padding: 20px; border: 1px solid #ddd; border-radius: 5px; }
            button { background: #3498db; color: white; padding: 10px 20px; border: none; border-radius: 5px; cursor: pointer; margin: 5px; }
            button:hover { background: #2980b9; }
            .result { background: #f8f9fa; padding: 15px; margin: 10px 0; border-radius: 5px; border-left: 4px solid #28a745; }
            .error { border-left-color: #dc3545; }
            input, select { padding: 8px; margin: 5px; border: 1px solid #ddd; border-radius: 3px; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🏥 Vibespan.ai Test Interface</h1>
            <p>Test your health agents onboarding flow for <strong>tgaraouy</strong></p>
            
            <div class="section">
                <h3>1️⃣ Start Onboarding</h3>
                <button onclick="startOnboarding()">Start Onboarding</button>
                <div id="onboarding-result"></div>
            </div>
            
            <div class="section">
                <h3>2️⃣ Connect Data Sources</h3>
                <select id="data-source">
                    <option value="whoop">🏃‍♂️ WHOOP</option>
                    <option value="apple_health">🍎 Apple Health</option>
                    <option value="csv_upload">📊 CSV Upload</option>
                    <option value="manual_entry">✍️ Manual Entry</option>
                </select>
                <button onclick="connectDataSource()">Connect Data Source</button>
                <div id="data-source-result"></div>
            </div>
            
            <div class="section">
                <h3>3️⃣ Set Health Goals</h3>
                <input type="checkbox" id="goal-performance" checked> Performance<br>
                <input type="checkbox" id="goal-recovery" checked> Recovery<br>
                <input type="checkbox" id="goal-longevity" checked> Longevity<br>
                <button onclick="setGoals()">Set Goals</button>
                <div id="goals-result"></div>
            </div>
            
            <div class="section">
                <h3>4️⃣ Activate Agents</h3>
                <input type="checkbox" id="agent-datacollector" checked> DataCollector<br>
                <input type="checkbox" id="agent-patterndetector" checked> PatternDetector<br>
                <input type="checkbox" id="agent-workoutplanner" checked> BasicWorkoutPlanner<br>
                <input type="checkbox" id="agent-nutritionplanner" checked> BasicNutritionPlanner<br>
                <input type="checkbox" id="agent-healthcoach" checked> HealthCoach<br>
                <input type="checkbox" id="agent-safetyofficer" checked> SafetyOfficer<br>
                <button onclick="activateAgents()">Activate Agents</button>
                <div id="agents-result"></div>
            </div>
            
            <div class="section">
                <h3>5️⃣ Complete Onboarding</h3>
                <button onclick="completeOnboarding()">Complete Onboarding</button>
                <div id="complete-result"></div>
            </div>
            
            <div class="section">
                <h3>6️⃣ Test Dashboard</h3>
                <button onclick="testDashboard()">Test Dashboard</button>
                <button onclick="testAgentStatus()">Test Agent Status</button>
                <button onclick="testAgentProcessing()">Test Agent Processing</button>
                <div id="dashboard-result"></div>
            </div>
        </div>
        
        <script>
            const API_BASE = 'http://localhost:8000';
            const HEADERS = {
                'Content-Type': 'application/json',
                'Host': 'tgaraouy.localhost:8000'
            };
            
            function showResult(elementId, message, isError = false) {
                const element = document.getElementById(elementId);
                element.innerHTML = `<div class="result ${isError ? 'error' : ''}">${message}</div>`;
            }
            
            async function startOnboarding() {
                try {
                    const response = await fetch(`${API_BASE}/onboarding/start`, {
                        method: 'GET',
                        headers: HEADERS
                    });
                    const data = await response.json();
                    
                    if (response.ok) {
                        showResult('onboarding-result', `
                            ✅ Onboarding started!<br>
                            Tenant ID: ${data.tenant_id}<br>
                            Status: ${data.onboarding_status}<br>
                            Steps: ${data.steps.length}
                        `);
                    } else {
                        showResult('onboarding-result', `❌ Error: ${data.detail}`, true);
                    }
                } catch (error) {
                    showResult('onboarding-result', `❌ Error: ${error.message}`, true);
                }
            }
            
            async function connectDataSource() {
                const sourceId = document.getElementById('data-source').value;
                const config = {
                    source_id: sourceId,
                    type: 'real_time',
                    config: {
                        webhook_url: `https://tgaraouy.vibespan.ai/webhook/${sourceId}/tgaraouy`
                    }
                };
                
                try {
                    const response = await fetch(`${API_BASE}/onboarding/data-sources/connect`, {
                        method: 'POST',
                        headers: HEADERS,
                        body: JSON.stringify(config)
                    });
                    const data = await response.json();
                    
                    if (response.ok) {
                        showResult('data-source-result', `
                            ✅ ${sourceId} connected successfully!<br>
                            Status: ${data.status}
                        `);
                    } else {
                        showResult('data-source-result', `❌ Error: ${data.detail}`, true);
                    }
                } catch (error) {
                    showResult('data-source-result', `❌ Error: ${error.message}`, true);
                }
            }
            
            async function setGoals() {
                const goals = [];
                if (document.getElementById('goal-performance').checked) goals.push('performance');
                if (document.getElementById('goal-recovery').checked) goals.push('recovery');
                if (document.getElementById('goal-longevity').checked) goals.push('longevity');
                
                const config = {
                    goals: goals,
                    preferences: {
                        workout_frequency: '5-6 times per week',
                        diet_preference: 'balanced',
                        sleep_target: '8 hours'
                    }
                };
                
                try {
                    const response = await fetch(`${API_BASE}/onboarding/goals`, {
                        method: 'POST',
                        headers: HEADERS,
                        body: JSON.stringify(config)
                    });
                    const data = await response.json();
                    
                    if (response.ok) {
                        showResult('goals-result', `
                            ✅ Goals set successfully!<br>
                            Goals: ${data.goals.join(', ')}<br>
                            Preferences: ${Object.keys(data.preferences).length} items
                        `);
                    } else {
                        showResult('goals-result', `❌ Error: ${data.detail}`, true);
                    }
                } catch (error) {
                    showResult('goals-result', `❌ Error: ${error.message}`, true);
                }
            }
            
            async function activateAgents() {
                const agents = [];
                if (document.getElementById('agent-datacollector').checked) agents.push('DataCollector');
                if (document.getElementById('agent-patterndetector').checked) agents.push('PatternDetector');
                if (document.getElementById('agent-workoutplanner').checked) agents.push('BasicWorkoutPlanner');
                if (document.getElementById('agent-nutritionplanner').checked) agents.push('BasicNutritionPlanner');
                if (document.getElementById('agent-healthcoach').checked) agents.push('HealthCoach');
                if (document.getElementById('agent-safetyofficer').checked) agents.push('SafetyOfficer');
                
                const config = { agents: agents };
                
                try {
                    const response = await fetch(`${API_BASE}/onboarding/agents/activate`, {
                        method: 'POST',
                        headers: HEADERS,
                        body: JSON.stringify(config)
                    });
                    const data = await response.json();
                    
                    if (response.ok) {
                        showResult('agents-result', `
                            ✅ Agents activated successfully!<br>
                            Total agents: ${data.total_agents}<br>
                            Agents: ${data.active_agents.join(', ')}
                        `);
                    } else {
                        showResult('agents-result', `❌ Error: ${data.detail}`, true);
                    }
                } catch (error) {
                    showResult('agents-result', `❌ Error: ${error.message}`, true);
                }
            }
            
            async function completeOnboarding() {
                try {
                    const response = await fetch(`${API_BASE}/onboarding/complete`, {
                        method: 'POST',
                        headers: HEADERS
                    });
                    const data = await response.json();
                    
                    if (response.ok) {
                        showResult('complete-result', `
                            🎉 Onboarding completed successfully!<br>
                            Status: ${data.status}<br>
                            Dashboard: ${data.dashboard_url}
                        `);
                    } else {
                        showResult('complete-result', `❌ Error: ${data.detail}`, true);
                    }
                } catch (error) {
                    showResult('complete-result', `❌ Error: ${error.message}`, true);
                }
            }
            
            async function testDashboard() {
                try {
                    const response = await fetch(`${API_BASE}/dashboard`, {
                        method: 'GET',
                        headers: HEADERS
                    });
                    const data = await response.json();
                    
                    if (response.ok) {
                        showResult('dashboard-result', `
                            ✅ Dashboard accessible!<br>
                            Tenant: ${data.tenant_id}<br>
                            Subdomain: ${data.subdomain}<br>
                            Status: ${data.status}<br>
                            Active agents: ${data.agents.length}<br>
                            Data sources: ${data.data_sources.length}
                        `);
                    } else {
                        showResult('dashboard-result', `❌ Error: ${data.detail}`, true);
                    }
                } catch (error) {
                    showResult('dashboard-result', `❌ Error: ${error.message}`, true);
                }
            }
            
            async function testAgentStatus() {
                try {
                    const response = await fetch(`${API_BASE}/agents/status`, {
                        method: 'GET',
                        headers: HEADERS
                    });
                    const data = await response.json();
                    
                    if (response.ok) {
                        showResult('dashboard-result', `
                            ✅ Agent status retrieved!<br>
                            Total agents: ${data.total_agents}<br>
                            Active agents: ${Object.keys(data.agents).join(', ')}
                        `);
                    } else {
                        showResult('dashboard-result', `❌ Error: ${data.detail}`, true);
                    }
                } catch (error) {
                    showResult('dashboard-result', `❌ Error: ${error.message}`, true);
                }
            }
            
            async function testAgentProcessing() {
                const sampleData = {
                    recovery_score: 78,
                    sleep_quality: 8.2,
                    hrv: 47,
                    goals: ['performance', 'recovery']
                };
                
                try {
                    const response = await fetch(`${API_BASE}/agents/process`, {
                        method: 'POST',
                        headers: HEADERS,
                        body: JSON.stringify(sampleData)
                    });
                    const data = await response.json();
                    
                    if (response.ok) {
                        showResult('dashboard-result', `
                            ✅ Agent processing successful!<br>
                            Agents processed: ${data.agents_processed.length}<br>
                            Insights generated: ${data.insights.length}<br>
                            Recommendations: ${data.recommendations.length}<br>
                            Sample insights:<br>
                            • ${data.insights.slice(0, 2).join('<br>• ')}
                        `);
                    } else {
                        showResult('dashboard-result', `❌ Error: ${data.detail}`, true);
                    }
                } catch (error) {
                    showResult('dashboard-result', `❌ Error: ${error.message}`, true);
                }
            }
        </script>
    </body>
    </html>
    """

if __name__ == "__main__":
    print("🌐 Starting Vibespan.ai Test Interface...")
    print("📱 Open your browser and go to: http://localhost:8080")
    print("🏥 Test the onboarding flow for tgaraouy")
    
    uvicorn.run(app, host="0.0.0.0", port=8080)
