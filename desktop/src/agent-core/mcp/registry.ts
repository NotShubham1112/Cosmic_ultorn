import { Tool, ToolCall, ToolResult } from "./schemas";
import { MCPClient } from "./client";
import { PermissionManager } from "./permissions";

export class ToolRegistry {
    private static instance: ToolRegistry;
    private clients: Map<string, MCPClient> = new Map();
    private tools: Map<string, Tool> = new Map();
    private toolToServer: Map<string, string> = new Map();
    private permissionManager: PermissionManager = new PermissionManager();

    private constructor() { }

    public static getInstance(): ToolRegistry {
        if (!ToolRegistry.instance) {
            ToolRegistry.instance = new ToolRegistry();
        }
        return ToolRegistry.instance;
    }

    public registerServer(name: string, client: MCPClient) {
        this.clients.set(name, client);
    }

    public registerTool(serverName: string, tool: Tool) {
        this.tools.set(tool.name, tool);
        this.toolToServer.set(tool.name, serverName);
    }

    public listTools(): Tool[] {
        return Array.from(this.tools.values());
    }

    public getTool(name: string): Tool | undefined {
        return this.tools.get(name);
    }

    public async executeTool(call: ToolCall): Promise<ToolResult> {
        const toolName = call.tool;
        const toolDef = this.getTool(toolName);

        if (!toolDef) {
            return {
                success: false,
                output: `Tool '${toolName}' not found.`,
                error: "ToolNotFound",
            };
        }

        // 1. Permission Check
        if (!this.permissionManager.checkPermission(toolDef, call)) {
            return {
                success: false,
                output: `Tool '${toolName}' requires user confirmation or was blocked.`,
                error: "PermissionDenied",
            };
        }

        // 2. Routing
        const serverName = this.toolToServer.get(toolName);
        if (!serverName) {
            return {
                success: false,
                output: `No server found for tool '${toolName}'`,
                error: "ServerNotFound",
            };
        }

        const client = this.clients.get(serverName);
        if (!client) {
            return {
                success: false,
                output: `Client for server '${serverName}' not found`,
                error: "ClientNotFound",
            };
        }

        // 3. Execution
        try {
            return await client.callTool(call);
        } catch (e: any) {
            return {
                success: false,
                output: e.message,
                error: "ExecutionError",
            };
        }
    }
}
