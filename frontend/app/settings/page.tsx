import { Panel, WorkspaceShell } from "../workspace-shell";

export default function SettingsPage() {
  return (
    <WorkspaceShell title="User Settings" eyebrow="Preferences + Access">
      <div className="grid gap-5 md:grid-cols-2">
        <Panel title="Workspace defaults" subtitle="Model provider, citation style, and retrieval preferences.">
          <div className="space-y-3 text-sm text-shell-muted">
            <div className="rounded-2xl border border-white/10 bg-white/5 p-4">Preferred provider: OpenAI-compatible / Ollama</div>
            <div className="rounded-2xl border border-white/10 bg-white/5 p-4">Citation style: neutral + reporter</div>
            <div className="rounded-2xl border border-white/10 bg-white/5 p-4">Default grounding: official-source only</div>
          </div>
        </Panel>
        <Panel title="Access" subtitle="JWT sessions, API keys, and role-bound features.">
          <div className="space-y-3 text-sm text-shell-muted">
            <div className="rounded-2xl border border-white/10 bg-white/5 p-4">Role-aware access: reader / analyst / admin</div>
            <div className="rounded-2xl border border-white/10 bg-white/5 p-4">Rate limit guardrails</div>
            <div className="rounded-2xl border border-white/10 bg-white/5 p-4">Conversation retention settings</div>
          </div>
        </Panel>
      </div>
    </WorkspaceShell>
  );
}
