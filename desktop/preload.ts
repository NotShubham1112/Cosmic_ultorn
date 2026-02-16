import { contextBridge, ipcRenderer } from 'electron';

contextBridge.exposeInMainWorld('electron', {
    ping: () => ipcRenderer.invoke('ping'),
    mcp: {
        listTools: () => ipcRenderer.invoke('mcp:listTools'),
    },
    agent: {
        createPlan: (goal: string) => ipcRenderer.invoke('agent:createPlan', goal),
        executeTask: (task: any) => ipcRenderer.invoke('agent:executeTask', task),
    },
});
