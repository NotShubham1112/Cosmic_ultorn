export enum RiskLevel {
    SAFE = "safe",       // Read-only, non-sensitive
    LOW = "low",         // Minor changes, reversible
    MEDIUM = "medium",   // Significant changes
    HIGH = "high",       // Destructive or costly
}

export interface ToolArgument {
    name: string;
    type: string;
    description: string;
    required: boolean;
}

export interface Tool {
    name: string;
    description: string;
    args_schema: any; // JSON Schema
    risk_level: RiskLevel;
}

export interface ToolCall {
    tool: string;
    args: Record<string, any>;
    id?: string;
}

export interface ToolResult {
    tool_call_id?: string;
    output: any;
    error?: string;
    success: boolean;
}

export interface MCPConfig {
    enabled_servers: string[];
    local_servers: Record<string, string>; // name -> command
    remote_servers: Record<string, string>; // name -> url
}
