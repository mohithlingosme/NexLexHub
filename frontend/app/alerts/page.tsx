"use client";

import { useEffect, useState } from "react";

import { apiBase, apiKey } from "../data";
import { Panel, WorkspaceShell } from "../workspace-shell";

type Alert = {
  id: number;
  name: string;
  query: string;
  delivery_channel: string;
  is_active: boolean;
};

export default function AlertsPage() {
  const [alerts, setAlerts] = useState<Alert[]>([]);

  useEffect(() => {
    fetch(`${apiBase}/alerts`, { headers: { "X-API-Key": apiKey } })
      .then((response) => response.json())
      .then((payload) => setAlerts(payload as Alert[]))
      .catch(() => setAlerts([]));
  }, []);

  return (
    <WorkspaceShell title="Alerts Center" eyebrow="Saved Queries + Event Monitoring">
      <Panel title="Active alerts" subtitle="Alert rules can be tied to search intent, statutes, and legal event clusters.">
        <div className="space-y-4">
          {alerts.map((alert) => (
            <div key={alert.id} className="rounded-2xl border border-white/10 bg-white/5 p-4">
              <div className="flex flex-wrap items-center gap-3">
                <h4 className="text-base font-medium text-white">{alert.name}</h4>
                <span className="rounded-full border border-white/10 px-3 py-1 text-xs text-shell-muted">
                  {alert.delivery_channel}
                </span>
                <span className="rounded-full border border-emerald-400/20 bg-emerald-400/10 px-3 py-1 text-xs text-emerald-200">
                  {alert.is_active ? "active" : "paused"}
                </span>
              </div>
              <p className="mt-3 text-sm text-shell-muted">{alert.query}</p>
            </div>
          ))}
        </div>
      </Panel>
    </WorkspaceShell>
  );
}
