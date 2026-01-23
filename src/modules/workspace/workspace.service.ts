// Worspace_service.ts 
// Declare all workspace related feature here

import { Workspace } from "./workspace.model";


export async function updateWorkspaceStreaks(userId: string) {
  const workspaces = await Workspace.find({ user_id: userId });
  const yesterday = new Date();
  yesterday.setDate(yesterday.getDate() - 1);
  const yesterdayStr = yesterday.toISOString().split('T')[0];

  const results = [];
  for (const ws of workspaces) {
    if (ws.last_completed_date) {
      if (ws.last_completed_date < yesterdayStr) {
        ws.streak = 0;
        await ws.save();
      }
    }
    results.push(ws);
  }
  return results;
}


