import { dashboardCards } from "./data";
import { Panel, WorkspaceShell } from "./workspace-shell";

export default function Home() {
  return (
    <WorkspaceShell title="Dashboard" eyebrow="Research Command Center">
      <div className="grid gap-5 xl:grid-cols-[1.4fr_1fr]">
        <Panel
          title="NexLexHub is a legal intelligence workspace"
          subtitle="Built for semantic retrieval, citation-grounded analysis, and precedent-aware navigation."
        >
          <div className="grid gap-4 md:grid-cols-3">
            {dashboardCards.map((card) => (
              <div key={card.title} className="rounded-2xl border border-white/10 bg-white/5 p-4">
                <p className="text-xs uppercase tracking-[0.25em] text-shell-muted">{card.title}</p>
                <p className="mt-3 text-lg font-medium text-white">{card.value}</p>
                <p className="mt-2 text-sm leading-6 text-shell-muted">{card.detail}</p>
              </div>
            ))}
          </div>
        </Panel>
        <Panel title="Workspace Signals" subtitle="Dense layout modeled on research-heavy enterprise SaaS.">
          <div className="space-y-3 text-sm text-shell-muted">
            <div className="rounded-2xl border border-emerald-400/20 bg-emerald-400/10 p-4">
              AI insights are citation-linked and grounded against retrieved judgment chunks.
            </div>
            <div className="rounded-2xl border border-sky-400/20 bg-sky-400/10 p-4">
              Scrapers retain only publisher metadata, snippets, entities, and event hashes.
            </div>
            <div className="rounded-2xl border border-amber-400/20 bg-amber-400/10 p-4">
              Official sources, processing, embeddings, alerts, and conversations sit behind one API surface.
            </div>
          </div>
        </Panel>
      </div>
    </WorkspaceShell>
  );
}
