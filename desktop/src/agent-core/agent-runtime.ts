import { ToolRegistry } from "./mcp/registry";
import { ToolCall, ToolResult } from "./mcp/schemas";

export interface AgentTask {
    id: string;
    goal: string;
    status: "pending" | "running" | "completed" | "failed";
    steps: AgentStep[];
}

export interface AgentStep {
    id: number;
    description: string;
    action: "tool_call" | "logic" | "completion" | "create" | "modify" | "delete" | "run_command" | "review";
    tool_call?: ToolCall;
    result?: ToolResult;
    status: "pending" | "running" | "completed" | "failed";
}

export class AgentRuntime {
    private registry: ToolRegistry;

    constructor() {
        this.registry = ToolRegistry.getInstance();
    }

    async executeTask(task: AgentTask): Promise<AgentTask> {
        console.log(`[Runtime] Starting task: ${task.goal}`);
        task.status = "running";

        for (const step of task.steps) {
            step.status = "running";
            console.log(`[Runtime] Executing step: ${step.description}`);

            if (step.action === "tool_call" && step.tool_call) {
                step.result = await this.registry.executeTool(step.tool_call);
                step.status = step.result.success ? "completed" : "failed";
            } else {
                // Handle other action types
                step.status = "completed";
            }

            if (step.status === "failed") {
                task.status = "failed";
                return task;
            }
        }

        task.status = "completed";
        return task;
    }
}
