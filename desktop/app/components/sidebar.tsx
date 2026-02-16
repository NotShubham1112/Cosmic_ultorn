"use client";

import { cn } from "@/lib/utils";
import { Button } from "@/components/ui/button";
import { ScrollArea } from "@/components/ui/scroll-area";
import {
    LayoutDashboard,
    MessageSquare,
    BrainCircuit,
    Puzzle,
    Settings,
    History
} from "lucide-react";

const sidebarItems = [
    { icon: LayoutDashboard, label: "Dashboard", href: "/" },
    { icon: MessageSquare, label: "Chat", href: "/chat" },
    { icon: BrainCircuit, label: "Planner", href: "/planner" },
    { icon: Puzzle, label: "MCP Tools", href: "/mcp" },
    { icon: History, label: "Memory", href: "/memory" },
    { icon: Settings, label: "Settings", href: "/settings" },
];

export function Sidebar({ className }: { className?: string }) {
    return (
        <div className={cn("pb-12 border-r bg-muted/40", className)}>
            <div className="space-y-4 py-4">
                <div className="px-3 py-2">
                    <h2 className="mb-2 px-4 text-lg font-semibold tracking-tight">
                        Cosmic Ultorn
                    </h2>
                    <div className="space-y-1">
                        <ScrollArea className="h-[calc(100vh-80px)] px-1">
                            {sidebarItems.map((item) => (
                                <Button
                                    key={item.label}
                                    variant="ghost"
                                    className="w-full justify-start gap-2"
                                >
                                    <item.icon className="h-4 w-4" />
                                    {item.label}
                                </Button>
                            ))}
                        </ScrollArea>
                    </div>
                </div>
            </div>
        </div>
    );
}
