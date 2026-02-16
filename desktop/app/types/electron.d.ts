export interface ElectronBridge {
    ping: () => Promise<string>;
    mcp: {
        listTools: () => Promise<any[]>;
    };
    agent: {
        createPlan: (goal: string) => Promise<any>;
        executeTask: (task: any) => Promise<any>;
    };
}

declare global {
    interface Window {
        electron: ElectronBridge;
    }
}
