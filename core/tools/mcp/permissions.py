from typing import Dict, Optional, List
from .schemas import ToolCall, RiskLevel, Tool

class PermissionConfig:
    def __init__(self, default_risk: RiskLevel = RiskLevel.MEDIUM):
        self.default_risk = default_risk
        # Map tool name -> RiskLevel override
        self.overrides: Dict[str, RiskLevel] = {}

    def set_risk(self, tool_name: str, risk: RiskLevel):
        self.overrides[tool_name] = risk

    def get_risk(self, tool_name: str) -> RiskLevel:
        return self.overrides.get(tool_name, self.default_risk)

class PermissionManager:
    def __init__(self, config: Optional[PermissionConfig] = None):
        if config is None:
            # Default configuration: conservative
            config = PermissionConfig(default_risk=RiskLevel.MEDIUM)
            # Safe tools (examples)
            config.set_risk("read_file", RiskLevel.SAFE)
            config.set_risk("list_dir", RiskLevel.SAFE)
            config.set_risk("get_weather", RiskLevel.SAFE)
            # High risk tools (examples)
            config.set_risk("delete_file", RiskLevel.HIGH)
            config.set_risk("deploy_prod", RiskLevel.HIGH)
            config.set_risk("push_code", RiskLevel.HIGH)

        self.config = config

    def check_permission(self, tool: Tool, call: ToolCall) -> bool:
        """
        Returns True if the tool can be executed automatically.
        Returns False if user confirmation is required.
        """
        # 1. Check Tool's intrinsic risk level (from definition)
        risk = tool.risk_level
        
        # 2. Check override from configuration
        conf_risk = self.config.get_risk(tool.name)
        
        # Take the stricter of the two risk levels
        # (Assuming risk order: SAFE < LOW < MEDIUM < HIGH)
        # We can implement a comparison logic, or just use config primarily.
        
        # Let's say config overrides definition if set explicitly.
        risk = conf_risk
        
        should_auto_execute = risk in [RiskLevel.SAFE, RiskLevel.LOW]
        
        if not should_auto_execute:
            print(f"[SECURITY] Tool '{tool.name}' requires confirmation (Risk: {risk})")
            return False
            
        return True

    def requires_confirmation(self, tool_name: str) -> bool:
        risk = self.config.get_risk(tool_name)
        return risk not in [RiskLevel.SAFE, RiskLevel.LOW]
