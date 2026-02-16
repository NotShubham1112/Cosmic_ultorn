import { spawn, ChildProcessWithoutNullStreams } from "child_process";
import { Tool, ToolCall, ToolResult } from "./schemas";

export interface MCPClient {
    connect(): Promise<void>;
    listTools(): Promise<Tool[]>;
    callTool(call: ToolCall): Promise<ToolResult>;
}

export class StdioMCPClient implements MCPClient {
    private command: string;
    private args: string[];
    private env?: Record<string, string>;
    private process: ChildProcessWithoutNullStreams | null = null;
    private nextId = 1;
    private pendingRequests: Map<number, { resolve: (val: any) => void; reject: (err: any) => void }> = new Map();

    constructor(command: string, args: string[], env?: Record<string, string>) {
        this.command = command;
        this.args = args;
        this.env = env;
    }

    async connect(): Promise<void> {
        return new Promise((resolve, reject) => {
            try {
                this.process = spawn(this.command, this.args, {
                    env: { ...process.env, ...this.env },
                    shell: false,
                });

                this.process.stdout.on("data", (data) => this.handleData(data));
                this.process.stderr.on("data", (data) => console.error(`[MCP Error] ${data}`));

                this.process.on("error", (err) => {
                    console.error(`[MCP] Failed to start process: ${err.message}`);
                    reject(err);
                });

                this.process.on("close", (code) => {
                    console.log(`[MCP] Process exited with code ${code}`);
                });

                console.log(`[MCP] Connected to stdio server: ${this.command}`);
                resolve();
            } catch (e) {
                reject(e);
            }
        });
    }

    private handleData(data: Buffer) {
        const lines = data.toString().split("\n").filter((l) => l.trim());
        for (const line of lines) {
            try {
                const response = JSON.parse(line);
                if (response.id && this.pendingRequests.has(response.id)) {
                    const { resolve } = this.pendingRequests.get(response.id)!;
                    this.pendingRequests.delete(response.id);
                    resolve(response);
                }
            } catch (e) {
                console.warn(`[MCP] Failed to parse response: ${line}`);
            }
        }
    }

    async listTools(): Promise<Tool[]> {
        const response = await this.sendRequest("list_tools", {});
        return response.result || [];
    }

    async callTool(call: ToolCall): Promise<ToolResult> {
        const response = await this.sendRequest("call_tool", {
            name: call.tool,
            arguments: call.args,
        });

        if (response.error) {
            return {
                success: false,
                output: response.error.message || "Unknown error",
                error: response.error.code?.toString(),
            };
        }

        return {
            success: true,
            output: response.result,
        };
    }

    private async sendRequest(method: string, params: any): Promise<any> {
        if (!this.process) throw new Error("MCP Client not connected");

        const id = this.nextId++;
        const request = {
            jsonrpc: "2.0",
            id,
            method,
            params,
        };

        return new Promise((resolve, reject) => {
            this.pendingRequests.set(id, { resolve, reject });
            this.process!.stdin.write(JSON.stringify(request) + "\n");
        });
    }
}
