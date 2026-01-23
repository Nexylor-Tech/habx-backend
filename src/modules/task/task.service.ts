import { Task } from "./task.model";

export async function getTask(workspaceId: string) {
  return await Task.find({ workspace_id: workspaceId }).lean();
}

export async function createTask(workspaceId: string, title: string, deadline?: string) {
  const newTask = await Task.create({
    workspace_id: workspaceId,
    title,
    deadline
  });
  return newTask.toObject();
}

export async function updateTask(taskId: string, body: any) {
  await Task.findByIdAndUpdate(taskId, { $set: body });
  return { message: "Updated" };
}
