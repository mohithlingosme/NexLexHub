"use client";

import { useEffect, useState } from "react";

import { apiBase, apiKey } from "../data";
import { Panel, WorkspaceShell } from "../workspace-shell";

type TimelineEvent = {
  title: string;
  decision_date: string;
  court: string;
};

export default function TimelinePage() {
  const [events, setEvents] = useState<TimelineEvent[]>([]);

  useEffect(() => {
    fetch(`${apiBase}/timeline`, { headers: { "X-API-Key": apiKey } })
      .then((response) => response.json())
      .then((payload) => setEvents(payload as TimelineEvent[]))
      .catch(() => setEvents([]));
  }, []);

  return (
    <WorkspaceShell title="Timeline Explorer" eyebrow="Chronology + Court Activity">
      <Panel title="Judgment chronology" subtitle="Track decision dates, legal developments, and alert-triggering events.">
        <div className="space-y-4">
          {events.map((event) => (
            <div key={`${event.title}-${event.decision_date}`} className="grid gap-3 rounded-2xl border border-white/10 bg-white/5 p-4 md:grid-cols-[180px_1fr]">
              <div className="text-sm text-shell-muted">{event.decision_date}</div>
              <div>
                <h4 className="text-base font-medium text-white">{event.title}</h4>
                <p className="mt-1 text-sm text-shell-muted">{event.court}</p>
              </div>
            </div>
          ))}
        </div>
      </Panel>
    </WorkspaceShell>
  );
}
