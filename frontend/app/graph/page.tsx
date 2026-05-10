import { Panel, WorkspaceShell } from "../workspace-shell";

export default function GraphPage() {
  return (
    <WorkspaceShell title="Citation Graph" eyebrow="Case ↔ Cited By ↔ Relied Upon">
      <div className="grid gap-5 xl:grid-cols-[1.2fr_0.8fr]">
        <Panel title="Graph canvas" subtitle="React Flow / D3 integration surface for precedent and citation topology.">
          <div className="grid min-h-[520px] place-items-center rounded-[28px] border border-dashed border-white/10 bg-shell">
            <div className="text-center">
              <p className="text-sm uppercase tracking-[0.35em] text-shell-muted">Graph viewport</p>
              <p className="mt-3 text-lg text-white">Nodes for cases, courts, and statutes render here.</p>
            </div>
          </div>
        </Panel>
        <Panel title="Graph semantics" subtitle="Treatment-aware edges and source-grounded navigation.">
          <div className="space-y-3 text-sm text-shell-muted">
            <div className="rounded-2xl border border-white/10 bg-white/5 p-4">Cited by</div>
            <div className="rounded-2xl border border-white/10 bg-white/5 p-4">Relied upon</div>
            <div className="rounded-2xl border border-white/10 bg-white/5 p-4">Overruled / distinguished</div>
          </div>
        </Panel>
      </div>
    </WorkspaceShell>
  );
}
