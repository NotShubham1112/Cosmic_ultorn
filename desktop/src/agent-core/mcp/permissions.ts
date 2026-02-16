import { Tool, ToolCall, RiskLevel } from "./schemas";

export class PermissionManager {
    checkPermission(tool: Tool, call: ToolCall): boolean {
        // 1. Safe tools are always allowed
        if (tool.risk_level === RiskLevel.SAFE) {
            return true;
        }

        // 2. In a real desktop app, we would emit an event to the UI
        // to prompt the user for confirmation for Medium/High risk tools.
        // For now, we simulate a 'Requires User' state if not Safe.

        // Placeholder logic: Always allow for now during dev, 
        // but in production this would be more strict.
        console.log(`[Permissions] Checking tool: ${tool.name} (Risk: ${tool.risk_level})`);

        if (tool.risk_level === RiskLevel.HIGH) {
            return false; // Force block high risk in auto mode for now.
        }

        return true;
    }
}
