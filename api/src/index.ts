import { serve } from "@hono/node-server";
import { Hono } from "hono";
import { exec } from "child_process";
import path from "path";

const app = new Hono();

app.get("/", (c) => {
  return c.text("Hello Hono!");
});

app.post("/query", async (c) => {
  const { question } = await c.req.json();
  // const scriptPath = path.join(__dirname, "scripts", "langchain_script.py");
  return new Promise((resolve) => {
    exec(
      `python ./scripts/langchain_script.py "${question}"}`,
      (error, stdout, stderr) => {
        if (error) {
          console.error(`Error executing Python script: ${error.message}`);
          resolve(c.json({ error: "Internal server error" }, 500));
          return;
        }
        if (stderr) {
          console.error(`Python script error: ${stderr}`);
          resolve(c.json({ error: "Python script error" }, 500));
          return;
        }
        resolve(c.json({ answer: stdout.trim() }));
      },
    );
  });
});

const port = 3000;
console.log(`Server is running on http://localhost:${port}`);

serve({
  fetch: app.fetch,
  port,
});
