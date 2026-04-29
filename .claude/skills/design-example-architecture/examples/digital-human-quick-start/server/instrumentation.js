// Next.js 生命周期钩子
// Lifecycle hook for Next.js
// 播报任务现在通过 /api/broadcast 接口管理
// Broadcast tasks are now managed via /api/broadcast endpoints
export async function register() {
  if (process.env.NEXT_RUNTIME === "nodejs") {
    const { clearAllTasks } = await import("./lib/digitalHuman.js");
    // 服务器启动时清理所有正在运行的数字人任务
    // Clear all running digital human tasks when server starts
    await clearAllTasks();
  }
}
