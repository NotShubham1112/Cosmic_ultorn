import { ChatOpenAI } from "@langchain/openai";
import { ChatPromptTemplate } from "@langchain/core/prompts";
import { StructuredOutputParser } from "@langchain/core/output_parsers";
import { z } from "zod";
import * as dotenv from "dotenv";
import { ToolRegistry } from "./mcp/registry";
import { ToolCall } from "./mcp/schemas";

dotenv.config();

const StepSchema = z.object({
    id: z.number(),
    action: z.enum(["create", "modify", "delete", "run_command", "review", "tool_call"]),
    path: z.string().optional().default(""),
    description: z.string(),
    content: z.string().optional(),
    tool_call: z.custom<ToolCall>().optional(),
    status: z.enum(["pending", "running", "completed", "failed"]).default("pending"),
});

const PlanSchema = z.object({
    goal: z.string(),
    steps: z.array(StepSchema),
});

export type Step = z.infer<typeof StepSchema>;
export type Plan = z.infer<typeof PlanSchema>;

export class Planner {
    private registry: ToolRegistry;

    constructor() {
        this.registry = ToolRegistry.getInstance();
    }

    async createPlan(goal: string): Promise<Plan> {
        const apiKey = process.env.OPENAI_API_KEY;

        if (apiKey && apiKey.startsWith("sk-")) {
            try {
                const llm = new ChatOpenAI({
                    openAIApiKey: apiKey,
                    modelName: "gpt-4o",
                    temperature: 0,
                });

                const parser = StructuredOutputParser.fromZodSchema(PlanSchema);

                const tools = this.registry.listTools();
                const toolsDesc = tools.map(t => `- ${t.name}: ${t.description}`).join("\n");

                const systemPrompt = `You are an expert AI software architect.
Create a detailed, step-by-step implementation plan.

Available Tools:
${toolsDesc}

For each step, specify:
- action: 'tool_call' (PREFERRED) or legacy actions ('create', 'modify', 'run_command', 'review')
- tool_call: If action is 'tool_call', provide the tool name and arguments.
- description: brief explanation of what to do
- path: if applicable (e.g. for file operations)

Ensure dependencies are handled first.`;

                const prompt = ChatPromptTemplate.fromMessages([
                    ["system", systemPrompt],
                    ["user", "{goal}\n\n{format_instructions}"],
                ]);

                const chain = prompt.pipe(llm).pipe(parser);

                const result = await chain.invoke({
                    goal: goal,
                    format_instructions: parser.getFormatInstructions(),
                });

                return result as Plan;
            } catch (error) {
                console.warn(`[Warning] LLM planning failed: ${error}. Falling back to mock.`);
            }
        } else {
            console.info("[Info] No OpenAI API key found. Using mock planner.");
        }

        // Mock Plan Fallback
        return {
            goal: goal,
            steps: [
                {
                    id: 1,
                    action: "create",
                    path: "desktop/src/test-mock.ts",
                    content: "console.log('Hello from Node Mock Planner')",
                    description: "Create a test file",
                    status: "pending"
                },
                {
                    id: 2,
                    action: "run_command",
                    path: "",
                    description: "Run a safe command",
                    status: "pending"
                },
            ],
        };
    }
}
