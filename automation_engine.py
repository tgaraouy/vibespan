#!/usr/bin/env python3
"""
Automation Engine for Vibespan.ai Managed Services
Handles automated health workflows, proactive monitoring, and service management.
"""

import asyncio
import json
import logging
from typing import Dict, Any, List, Optional, Callable
from datetime import datetime, timedelta
from enum import Enum
import schedule
import time

logger = logging.getLogger(__name__)

class AutomationTrigger(Enum):
    """Types of automation triggers"""
    SCHEDULED = "scheduled"
    DATA_RECEIVED = "data_received"
    THRESHOLD_BREACH = "threshold_breach"
    PATTERN_DETECTED = "pattern_detected"
    USER_ACTION = "user_action"
    EXTERNAL_EVENT = "external_event"

class AutomationAction(Enum):
    """Types of automation actions"""
    SEND_NOTIFICATION = "send_notification"
    UPDATE_PLAN = "update_plan"
    TRIGGER_ANALYSIS = "trigger_analysis"
    SCHEDULE_CHECKUP = "schedule_checkup"
    ADJUST_RECOMMENDATIONS = "adjust_recommendations"
    ESCALATE_ALERT = "escalate_alert"
    COLLECT_DATA = "collect_data"
    GENERATE_REPORT = "generate_report"

class AutomationRule:
    """Represents an automation rule"""
    
    def __init__(self, rule_id: str, name: str, description: str, 
                 trigger: AutomationTrigger, conditions: Dict[str, Any],
                 actions: List[AutomationAction], priority: int = 1):
        self.rule_id = rule_id
        self.name = name
        self.description = description
        self.trigger = trigger
        self.conditions = conditions
        self.actions = actions
        self.priority = priority
        self.enabled = True
        self.last_triggered = None
        self.trigger_count = 0
        self.created_at = datetime.now()
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "rule_id": self.rule_id,
            "name": self.name,
            "description": self.description,
            "trigger": self.trigger.value,
            "conditions": self.conditions,
            "actions": [action.value for action in self.actions],
            "priority": self.priority,
            "enabled": self.enabled,
            "last_triggered": self.last_triggered.isoformat() if self.last_triggered else None,
            "trigger_count": self.trigger_count,
            "created_at": self.created_at.isoformat()
        }

class HealthWorkflow:
    """Represents a health workflow automation"""
    
    def __init__(self, workflow_id: str, name: str, description: str,
                 steps: List[Dict[str, Any]], schedule_config: Dict[str, Any] = None):
        self.workflow_id = workflow_id
        self.name = name
        self.description = description
        self.steps = steps
        self.schedule_config = schedule_config or {}
        self.enabled = True
        self.last_run = None
        self.next_run = None
        self.run_count = 0
        self.success_count = 0
        self.failure_count = 0
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "workflow_id": self.workflow_id,
            "name": self.name,
            "description": self.description,
            "steps": self.steps,
            "schedule_config": self.schedule_config,
            "enabled": self.enabled,
            "last_run": self.last_run.isoformat() if self.last_run else None,
            "next_run": self.next_run.isoformat() if self.next_run else None,
            "run_count": self.run_count,
            "success_count": self.success_count,
            "failure_count": self.failure_count
        }

class AutomationEngine:
    """Core automation engine for managed health services"""
    
    def __init__(self, tenant_id: str):
        self.tenant_id = tenant_id
        self.rules: Dict[str, AutomationRule] = {}
        self.workflows: Dict[str, HealthWorkflow] = {}
        self.action_handlers: Dict[AutomationAction, Callable] = {}
        self.trigger_handlers: Dict[AutomationTrigger, Callable] = {}
        self.logger = logging.getLogger(f"automation.{tenant_id}")
        
        # Initialize default automation rules
        self._initialize_default_rules()
        self._initialize_default_workflows()
        self._setup_action_handlers()
    
    def _initialize_default_rules(self):
        """Initialize default automation rules for health management"""
        
        # Recovery monitoring rule
        recovery_rule = AutomationRule(
            "recovery_monitoring",
            "Recovery Score Monitoring",
            "Monitor recovery scores and trigger actions when low",
            AutomationTrigger.THRESHOLD_BREACH,
            {
                "metric": "recovery_score",
                "threshold": 30,
                "operator": "<",
                "duration_minutes": 60
            },
            [AutomationAction.SEND_NOTIFICATION, AutomationAction.ADJUST_RECOMMENDATIONS],
            priority=1
        )
        self.rules["recovery_monitoring"] = recovery_rule
        
        # Sleep pattern detection
        sleep_rule = AutomationRule(
            "sleep_pattern_detection",
            "Sleep Pattern Analysis",
            "Detect sleep pattern changes and provide recommendations",
            AutomationTrigger.PATTERN_DETECTED,
            {
                "pattern_type": "sleep_duration",
                "change_threshold": 0.2,
                "lookback_days": 7
            },
            [AutomationAction.TRIGGER_ANALYSIS, AutomationAction.SEND_NOTIFICATION],
            priority=2
        )
        self.rules["sleep_pattern_detection"] = sleep_rule
        
        # Workout recovery optimization
        workout_rule = AutomationRule(
            "workout_recovery_optimization",
            "Workout Recovery Optimization",
            "Optimize workout intensity based on recovery metrics",
            AutomationTrigger.DATA_RECEIVED,
            {
                "data_type": "recovery_score",
                "workout_scheduled": True
            },
            [AutomationAction.UPDATE_PLAN, AutomationAction.ADJUST_RECOMMENDATIONS],
            priority=1
        )
        self.rules["workout_recovery_optimization"] = workout_rule
        
        # Health alert escalation
        alert_rule = AutomationRule(
            "health_alert_escalation",
            "Health Alert Escalation",
            "Escalate critical health alerts",
            AutomationTrigger.THRESHOLD_BREACH,
            {
                "metric": "heart_rate_variability",
                "threshold": 15,
                "operator": "<",
                "duration_minutes": 30
            },
            [AutomationAction.ESCALATE_ALERT, AutomationAction.SEND_NOTIFICATION],
            priority=0  # Highest priority
        )
        self.rules["health_alert_escalation"] = alert_rule
    
    def _initialize_default_workflows(self):
        """Initialize default health workflows"""
        
        # Daily health check workflow
        daily_check_workflow = HealthWorkflow(
            "daily_health_check",
            "Daily Health Check",
            "Comprehensive daily health assessment and recommendations",
            [
                {
                    "step": 1,
                    "action": "collect_metrics",
                    "description": "Collect all available health metrics",
                    "timeout": 300
                },
                {
                    "step": 2,
                    "action": "analyze_patterns",
                    "description": "Analyze patterns and trends",
                    "timeout": 180
                },
                {
                    "step": 3,
                    "action": "generate_recommendations",
                    "description": "Generate personalized recommendations",
                    "timeout": 120
                },
                {
                    "step": 4,
                    "action": "update_daily_plan",
                    "description": "Update daily action plan",
                    "timeout": 60
                },
                {
                    "step": 5,
                    "action": "send_summary",
                    "description": "Send daily health summary",
                    "timeout": 30
                }
            ],
            {
                "schedule": "daily",
                "time": "07:00",
                "timezone": "UTC"
            }
        )
        self.workflows["daily_health_check"] = daily_check_workflow
        
        # Weekly optimization workflow
        weekly_optimization_workflow = HealthWorkflow(
            "weekly_optimization",
            "Weekly Health Optimization",
            "Weekly deep analysis and optimization",
            [
                {
                    "step": 1,
                    "action": "collect_weekly_data",
                    "description": "Collect and aggregate weekly data",
                    "timeout": 600
                },
                {
                    "step": 2,
                    "action": "pattern_analysis",
                    "description": "Deep pattern analysis",
                    "timeout": 900
                },
                {
                    "step": 3,
                    "action": "optimize_plans",
                    "description": "Optimize workout and nutrition plans",
                    "timeout": 300
                },
                {
                    "step": 4,
                    "action": "generate_insights",
                    "description": "Generate weekly insights report",
                    "timeout": 180
                },
                {
                    "step": 5,
                    "action": "update_goals",
                    "description": "Update and adjust health goals",
                    "timeout": 120
                }
            ],
            {
                "schedule": "weekly",
                "day": "monday",
                "time": "08:00",
                "timezone": "UTC"
            }
        )
        self.workflows["weekly_optimization"] = weekly_optimization_workflow
        
        # Proactive monitoring workflow
        proactive_monitoring_workflow = HealthWorkflow(
            "proactive_monitoring",
            "Proactive Health Monitoring",
            "Continuous monitoring and early intervention",
            [
                {
                    "step": 1,
                    "action": "monitor_metrics",
                    "description": "Monitor real-time health metrics",
                    "timeout": 30
                },
                {
                    "step": 2,
                    "action": "check_thresholds",
                    "description": "Check against health thresholds",
                    "timeout": 15
                },
                {
                    "step": 3,
                    "action": "trigger_alerts",
                    "description": "Trigger alerts if needed",
                    "timeout": 10
                },
                {
                    "step": 4,
                    "action": "update_recommendations",
                    "description": "Update real-time recommendations",
                    "timeout": 20
                }
            ],
            {
                "schedule": "interval",
                "interval_minutes": 15
            }
        )
        self.workflows["proactive_monitoring"] = proactive_monitoring_workflow
    
    def _setup_action_handlers(self):
        """Setup action handlers for automation"""
        self.action_handlers = {
            AutomationAction.SEND_NOTIFICATION: self._handle_send_notification,
            AutomationAction.UPDATE_PLAN: self._handle_update_plan,
            AutomationAction.TRIGGER_ANALYSIS: self._handle_trigger_analysis,
            AutomationAction.SCHEDULE_CHECKUP: self._handle_schedule_checkup,
            AutomationAction.ADJUST_RECOMMENDATIONS: self._handle_adjust_recommendations,
            AutomationAction.ESCALATE_ALERT: self._handle_escalate_alert,
            AutomationAction.COLLECT_DATA: self._handle_collect_data,
            AutomationAction.GENERATE_REPORT: self._handle_generate_report
        }
    
    async def trigger_rule(self, rule_id: str, trigger_data: Dict[str, Any]) -> Dict[str, Any]:
        """Trigger a specific automation rule"""
        if rule_id not in self.rules:
            return {"status": "error", "message": f"Rule {rule_id} not found"}
        
        rule = self.rules[rule_id]
        if not rule.enabled:
            return {"status": "skipped", "message": f"Rule {rule_id} is disabled"}
        
        # Check conditions
        if not self._check_conditions(rule.conditions, trigger_data):
            return {"status": "conditions_not_met", "message": "Rule conditions not satisfied"}
        
        # Execute actions
        results = []
        for action in rule.actions:
            try:
                handler = self.action_handlers.get(action)
                if handler:
                    result = await handler(trigger_data)
                    results.append({"action": action.value, "result": result})
                else:
                    results.append({"action": action.value, "result": "no_handler"})
            except Exception as e:
                self.logger.error(f"Error executing action {action.value}: {e}")
                results.append({"action": action.value, "result": "error", "error": str(e)})
        
        # Update rule stats
        rule.last_triggered = datetime.now()
        rule.trigger_count += 1
        
        return {
            "status": "executed",
            "rule_id": rule_id,
            "trigger_data": trigger_data,
            "results": results,
            "triggered_at": rule.last_triggered.isoformat()
        }
    
    async def execute_workflow(self, workflow_id: str) -> Dict[str, Any]:
        """Execute a health workflow"""
        if workflow_id not in self.workflows:
            return {"status": "error", "message": f"Workflow {workflow_id} not found"}
        
        workflow = self.workflows[workflow_id]
        if not workflow.enabled:
            return {"status": "skipped", "message": f"Workflow {workflow_id} is disabled"}
        
        workflow.last_run = datetime.now()
        workflow.run_count += 1
        
        results = []
        for step in workflow.steps:
            try:
                step_result = await self._execute_workflow_step(step)
                results.append(step_result)
                
                if step_result.get("status") == "error":
                    workflow.failure_count += 1
                    return {
                        "status": "failed",
                        "workflow_id": workflow_id,
                        "failed_at_step": step["step"],
                        "results": results
                    }
            except Exception as e:
                self.logger.error(f"Error executing workflow step {step['step']}: {e}")
                workflow.failure_count += 1
                return {
                    "status": "error",
                    "workflow_id": workflow_id,
                    "error": str(e),
                    "results": results
                }
        
        workflow.success_count += 1
        return {
            "status": "completed",
            "workflow_id": workflow_id,
            "results": results,
            "completed_at": workflow.last_run.isoformat()
        }
    
    def _check_conditions(self, conditions: Dict[str, Any], trigger_data: Dict[str, Any]) -> bool:
        """Check if automation conditions are met"""
        # Simplified condition checking - in production, this would be more sophisticated
        for key, expected_value in conditions.items():
            if key in trigger_data:
                actual_value = trigger_data[key]
                if isinstance(expected_value, dict) and "operator" in expected_value:
                    operator = expected_value["operator"]
                    threshold = expected_value.get("threshold", expected_value.get("value"))
                    
                    if operator == "<" and actual_value >= threshold:
                        return False
                    elif operator == ">" and actual_value <= threshold:
                        return False
                    elif operator == "==" and actual_value != threshold:
                        return False
                elif actual_value != expected_value:
                    return False
            else:
                return False
        return True
    
    async def _execute_workflow_step(self, step: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a single workflow step"""
        action = step.get("action")
        timeout = step.get("timeout", 60)
        
        # Simulate step execution
        await asyncio.sleep(0.1)  # Simulate processing time
        
        return {
            "step": step["step"],
            "action": action,
            "status": "completed",
            "description": step.get("description", ""),
            "execution_time": 0.1
        }
    
    # Action handlers
    async def _handle_send_notification(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Handle send notification action"""
        return {"status": "notification_sent", "message": "Health notification sent"}
    
    async def _handle_update_plan(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Handle update plan action"""
        return {"status": "plan_updated", "message": "Health plan updated"}
    
    async def _handle_trigger_analysis(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Handle trigger analysis action"""
        return {"status": "analysis_triggered", "message": "Health analysis started"}
    
    async def _handle_schedule_checkup(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Handle schedule checkup action"""
        return {"status": "checkup_scheduled", "message": "Health checkup scheduled"}
    
    async def _handle_adjust_recommendations(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Handle adjust recommendations action"""
        return {"status": "recommendations_adjusted", "message": "Recommendations updated"}
    
    async def _handle_escalate_alert(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Handle escalate alert action"""
        return {"status": "alert_escalated", "message": "Health alert escalated"}
    
    async def _handle_collect_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Handle collect data action"""
        return {"status": "data_collected", "message": "Health data collected"}
    
    async def _handle_generate_report(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Handle generate report action"""
        return {"status": "report_generated", "message": "Health report generated"}
    
    def get_automation_status(self) -> Dict[str, Any]:
        """Get automation engine status"""
        return {
            "tenant_id": self.tenant_id,
            "rules_count": len(self.rules),
            "workflows_count": len(self.workflows),
            "enabled_rules": len([r for r in self.rules.values() if r.enabled]),
            "enabled_workflows": len([w for w in self.workflows.values() if w.enabled]),
            "total_triggers": sum(rule.trigger_count for rule in self.rules.values()),
            "total_workflow_runs": sum(workflow.run_count for workflow in self.workflows.values()),
            "last_updated": datetime.now().isoformat()
        }
    
    def add_custom_rule(self, rule: AutomationRule) -> Dict[str, Any]:
        """Add a custom automation rule"""
        self.rules[rule.rule_id] = rule
        return {"status": "rule_added", "rule_id": rule.rule_id}
    
    def add_custom_workflow(self, workflow: HealthWorkflow) -> Dict[str, Any]:
        """Add a custom health workflow"""
        self.workflows[workflow.workflow_id] = workflow
        return {"status": "workflow_added", "workflow_id": workflow.workflow_id}

# Global automation engines per tenant
_automation_engines: Dict[str, AutomationEngine] = {}

def get_automation_engine(tenant_id: str) -> AutomationEngine:
    """Get automation engine for tenant"""
    if tenant_id not in _automation_engines:
        _automation_engines[tenant_id] = AutomationEngine(tenant_id)
    return _automation_engines[tenant_id]
