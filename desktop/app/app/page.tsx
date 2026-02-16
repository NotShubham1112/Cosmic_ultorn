import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import {
  Zap,
  ShieldCheck,
  Cpu,
  Terminal as TerminalIcon,
  Activity,
  Plus
} from "lucide-react";

export default function DashboardPage() {
  return (
    <div className="p-8 space-y-8 animate-in fade-in duration-500">
      <header className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold tracking-tight">Agent Dashboard</h1>
          <p className="text-muted-foreground">
            Welcome back. Your agentic co-worker is online and active.
          </p>
        </div>
        <Button className="gap-2">
          <Plus className="h-4 w-4" /> New Task
        </Button>
      </header>

      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
        <Card className="bg-muted/50">
          <CardHeader className="flex flex-row items-center justify-between pb-2 space-y-0">
            <CardTitle className="text-sm font-medium">Memory Nodes</CardTitle>
            <Zap className="h-4 w-4 text-yellow-500" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">1,284</div>
            <p className="text-xs text-muted-foreground">+12 since yesterday</p>
          </CardContent>
        </Card>
        <Card className="bg-muted/50">
          <CardHeader className="flex flex-row items-center justify-between pb-2 space-y-0">
            <CardTitle className="text-sm font-medium">MCP Tools</CardTitle>
            <ShieldCheck className="h-4 w-4 text-green-500" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">42 Active</div>
            <p className="text-xs text-muted-foreground">All systems guarding</p>
          </CardContent>
        </Card>
        <Card className="bg-muted/50">
          <CardHeader className="flex flex-row items-center justify-between pb-2 space-y-0">
            <CardTitle className="text-sm font-medium">CPU Usage</CardTitle>
            <Cpu className="h-4 w-4 text-blue-500" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">14%</div>
            <p className="text-xs text-muted-foreground">Running local Mistral</p>
          </CardContent>
        </Card>
        <Card className="bg-muted/50">
          <CardHeader className="flex flex-row items-center justify-between pb-2 space-y-0">
            <CardTitle className="text-sm font-medium">Active Tasks</CardTitle>
            <Activity className="h-4 w-4 text-purple-500" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">3 Running</div>
            <p className="text-xs text-muted-foreground">Sub-agents processing</p>
          </CardContent>
        </Card>
      </div>

      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-7">
        <Card className="col-span-4 bg-muted/30">
          <CardHeader>
            <CardTitle>Recent Activity</CardTitle>
            <CardDescription>
              Your agent has performed 18 actions in the last hour.
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {[1, 2, 3].map((i) => (
                <div key={i} className="flex items-center gap-4">
                  <div className="p-2 rounded-full bg-primary/10">
                    <TerminalIcon className="h-4 w-4 text-primary" />
                  </div>
                  <div className="space-y-1">
                    <p className="text-sm font-medium leading-none">
                      Modified core/planner.py
                    </p>
                    <p className="text-xs text-muted-foreground">
                      Optimized task decomposition logic
                    </p>
                  </div>
                  <div className="ml-auto text-xs text-muted-foreground">
                    {i * 12}m ago
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
        <Card className="col-span-3 bg-muted/30">
          <CardHeader>
            <CardTitle>System Health</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              <div className="flex items-center justify-between">
                <span className="text-sm">Ollama (Local)</span>
                <span className="text-xs px-2 py-0.5 rounded-full bg-green-500/10 text-green-500 font-medium">
                  CONNECTED
                </span>
              </div>
              <div className="flex items-center justify-between">
                <span className="text-sm">Mistral API</span>
                <span className="text-xs px-2 py-0.5 rounded-full bg-green-500/10 text-green-500 font-medium">
                  CONNECTED
                </span>
              </div>
              <div className="flex items-center justify-between">
                <span className="text-sm">Vector DB</span>
                <span className="text-xs px-2 py-0.5 rounded-full bg-green-500/10 text-green-500 font-medium">
                  OPTIMIZED
                </span>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
