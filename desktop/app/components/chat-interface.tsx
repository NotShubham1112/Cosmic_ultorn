"use client";

import { useState, useEffect } from "react";
import { Send, User, Bot, Paperclip, Loader2, CheckCircle2, Circle } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { ScrollArea } from "@/components/ui/scroll-area";

export function ChatInterface() {
    const [messages, setMessages] = useState([
        { role: "assistant", content: "Hello! I'm your AI co-worker. I've connected all MCP systems, including the Indexer. How can I help you today?" }
    ]);
    const [input, setInput] = useState("");
    const [isPlanning, setIsPlanning] = useState(false);
    const [currentPlan, setCurrentPlan] = useState<any>(null);

    const handleSend = async () => {
        if (!input.trim() || isPlanning) return;

        const userMsg = input;
        setMessages(prev => [...prev, { role: "user", content: userMsg }]);
        setInput("");
        setIsPlanning(true);

        try {
            if (window.electron) {
                // 1. Create Plan
                const plan = await window.electron.agent.createPlan(userMsg);
                setCurrentPlan(plan);

                setMessages(prev => [...prev, {
                    role: "assistant",
                    content: `I've created a plan with ${plan.steps.length} steps to achieve your goal. Starting execution now...`
                }]);

                // 2. Execute Plan
                const result = await window.electron.agent.executeTask({
                    ...plan,
                    id: `task-${Date.now()}`
                });

                setCurrentPlan(result);

                setMessages(prev => [...prev, {
                    role: "assistant",
                    content: result.status === "completed"
                        ? "Task completed successfully! All steps have been verified."
                        : "Task execution encountered an issue. Please review the inspector panel."
                }]);
            } else {
                // Mock fallback for browser dev
                setTimeout(() => {
                    setMessages(prev => [...prev, { role: "assistant", content: "Agent is offline (No Electron bridge detected)." }]);
                }, 1000);
            }
        } catch (e: any) {
            setMessages(prev => [...prev, { role: "assistant", content: `Error: ${e.message}` }]);
        } finally {
            setIsPlanning(false);
        }
    };

    return (
        <div className="flex flex-col h-full bg-background border-r">
            <ScrollArea className="flex-1 p-4 space-y-4">
                {messages.map((msg, idx) => (
                    <div key={idx} className={`flex gap-3 ${msg.role === "user" ? "flex-row-reverse" : ""}`}>
                        <div className={`p-2 rounded-full h-fit ${msg.role === "user" ? "bg-primary text-primary-foreground" : "bg-muted"}`}>
                            {msg.role === "user" ? <User className="h-4 w-4" /> : <Bot className="h-4 w-4" />}
                        </div>
                        <Card className={`p-3 max-w-[80%] ${msg.role === "user" ? "bg-primary text-primary-foreground" : "bg-muted/50"}`}>
                            <p className="text-sm leading-relaxed">{msg.content}</p>
                        </Card>
                    </div>
                ))}

                {currentPlan && (
                    <div className="mt-4 p-4 rounded-lg bg-muted/30 border border-primary/20">
                        <h4 className="text-xs font-semibold mb-3 flex items-center gap-2">
                            {isPlanning ? <Loader2 className="h-3 w-3 animate-spin" /> : <CheckCircle2 className="h-3 w-3 text-green-500" />}
                            Current Plan: {currentPlan.goal}
                        </h4>
                        <div className="space-y-2">
                            {currentPlan.steps.map((step: any) => (
                                <div key={step.id} className="flex items-center gap-2 text-[11px]">
                                    {step.status === "completed" ? (
                                        <CheckCircle2 className="h-3 w-3 text-green-500" />
                                    ) : step.status === "running" ? (
                                        <Loader2 className="h-3 w-3 animate-spin text-primary" />
                                    ) : (
                                        <Circle className="h-3 w-3 text-muted-foreground" />
                                    )}
                                    <span className={step.status === "completed" ? "text-muted-foreground line-through" : ""}>
                                        {step.description}
                                    </span>
                                </div>
                            ))}
                        </div>
                    </div>
                )}
            </ScrollArea>

            <div className="p-4 border-t bg-muted/20">
                <div className="flex gap-2 relative">
                    <Button variant="ghost" size="icon" className="h-10 w-10">
                        <Paperclip className="h-4 w-4" />
                    </Button>
                    <input
                        className="flex-1 bg-muted/50 border rounded-md px-4 text-sm focus:outline-none focus:ring-1 focus:ring-primary"
                        placeholder={isPlanning ? "Agent is working..." : "Type your message..."}
                        disabled={isPlanning}
                        value={input}
                        onChange={(e) => setInput(e.target.value)}
                        onKeyDown={(e) => e.key === "Enter" && handleSend()}
                    />
                    <Button size="icon" className="h-10 w-10" onClick={handleSend} disabled={isPlanning}>
                        {isPlanning ? <Loader2 className="h-4 w-4 animate-spin" /> : <Send className="h-4 w-4" />}
                    </Button>
                </div>
                <p className="text-[10px] text-center text-muted-foreground mt-2">
                    Agent 24/7 • Local Context Enabled • Mistral Medium
                </p>
            </div>
        </div>
    );
}
