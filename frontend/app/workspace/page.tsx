"use client";

import { FormEvent, useState } from "react";

import { apiBase } from "../data";
import { Panel, WorkspaceShell } from "../workspace-shell";

export default function WorkspacePage() {
  const [query, setQuery] = useState("Summarize the Section 7 execution-principle cases with citations.");
  const [token, setToken] = useState("");
  const [stream, setStream] = useState("");

  async function login() {
    const response = await fetch(`${apiBase}/auth/login`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email: "analyst@nexlexhub.local", password: "analyst123" }),
    });
    const payload = (await response.json()) as { access_token?: string };
    setToken(payload.access_token ?? "");
  }

  async function onSubmit(event: FormEvent) {
    event.preventDefault();
    if (!token) {
      await login();
    }
    setStream("");
    const response = await fetch(`${apiBase}/ai/chat`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token || (await getFreshToken())}`,
      },
      body: JSON.stringify({ query, title: "Workspace query" }),
    });
    const reader = response.body?.getReader();
    const decoder = new TextDecoder();
    if (!reader) {
      return;
    }
    while (true) {
      const { done, value } = await reader.read();
      if (done) {
        break;
      }
      setStream((current) => current + decoder.decode(value, { stream: true }));
    }
  }

  async function getFreshToken() {
    const response = await fetch(`${apiBase}/auth/login`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email: "analyst@nexlexhub.local", password: "analyst123" }),
    });
    const payload = (await response.json()) as { access_token?: string };
    const nextToken = payload.access_token ?? "";
    setToken(nextToken);
    return nextToken;
  }

  return (
    <WorkspaceShell title="AI Workspace" eyebrow="Streaming, Grounded Legal Analysis">
      <div className="grid gap-5 xl:grid-cols-[1.1fr_0.9fr]">
        <Panel title="Assistant prompt" subtitle="Streaming POST /ai/chat with JWT auth.">
          <form onSubmit={onSubmit} className="space-y-4">
            <textarea
              value={query}
              onChange={(event) => setQuery(event.target.value)}
              className="min-h-40 w-full rounded-2xl border border-white/10 bg-shell px-4 py-4 text-sm text-white outline-none"
            />
            <button className="rounded-2xl bg-accent px-5 py-3 text-sm font-medium text-white">Stream analysis</button>
          </form>
        </Panel>
        <Panel title="Grounded response stream" subtitle="SSE tokens from the backend conversation endpoint.">
          <pre className="min-h-40 whitespace-pre-wrap rounded-2xl border border-white/10 bg-shell p-4 text-xs text-shell-muted">
            {stream || "No streamed answer yet."}
          </pre>
        </Panel>
      </div>
    </WorkspaceShell>
  );
}
