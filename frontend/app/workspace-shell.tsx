"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import type { ReactNode } from "react";

const navItems = [
  { href: "/", label: "Dashboard" },
  { href: "/search", label: "Semantic Search" },
  { href: "/cases", label: "Case Explorer" },
  { href: "/graph", label: "Citation Graph" },
  { href: "/timeline", label: "Timeline" },
  { href: "/workspace", label: "AI Workspace" },
  { href: "/statutes", label: "Statutes" },
  { href: "/alerts", label: "Alerts" },
  { href: "/settings", label: "Settings" },
  { href: "/admin", label: "Admin" },
];

export function WorkspaceShell({
  title,
  eyebrow,
  children,
}: {
  title: string;
  eyebrow: string;
  children: ReactNode;
}) {
  const pathname = usePathname();

  return (
    <main className="min-h-screen bg-shell text-shell-foreground">
      <div className="mx-auto grid min-h-screen max-w-[1600px] grid-cols-1 gap-6 px-4 py-4 lg:grid-cols-[260px_minmax(0,1fr)]">
        <aside className="rounded-[28px] border border-white/10 bg-panel/90 p-5 shadow-panel backdrop-blur">
          <div className="border-b border-white/10 pb-5">
            <p className="text-[11px] uppercase tracking-[0.35em] text-shell-muted">NexLexHub</p>
            <h1 className="mt-3 text-2xl font-semibold tracking-tight text-white">Legal Intelligence OS</h1>
            <p className="mt-2 text-sm leading-6 text-shell-muted">
              Citation-grounded research, semantic retrieval, and verified legal analysis.
            </p>
          </div>
          <nav className="mt-5 space-y-2">
            {navItems.map((item) => {
              const active = pathname === item.href;
              return (
                <Link
                  key={item.href}
                  href={item.href}
                  className={`block rounded-2xl px-4 py-3 text-sm transition ${
                    active
                      ? "bg-accent text-white shadow-glow"
                      : "text-shell-muted hover:bg-white/5 hover:text-white"
                  }`}
                >
                  {item.label}
                </Link>
              );
            })}
          </nav>
        </aside>
        <section className="rounded-[28px] border border-white/10 bg-panel-strong/90 shadow-panel backdrop-blur">
          <header className="border-b border-white/10 px-6 py-5">
            <p className="text-[11px] uppercase tracking-[0.35em] text-shell-muted">{eyebrow}</p>
            <div className="mt-3 flex flex-col gap-3 md:flex-row md:items-end md:justify-between">
              <div>
                <h2 className="text-3xl font-semibold tracking-tight text-white">{title}</h2>
                <p className="mt-2 max-w-3xl text-sm leading-6 text-shell-muted">
                  Production workspace connected to FastAPI, PostgreSQL/pgvector, retrieval, and streaming analysis.
                </p>
              </div>
              <div className="grid grid-cols-3 gap-3 text-xs text-shell-muted">
                <Metric label="Mode" value="Grounded" />
                <Metric label="Database" value="pgvector" />
                <Metric label="API" value="FastAPI" />
              </div>
            </div>
          </header>
          <div className="p-6">{children}</div>
        </section>
      </div>
    </main>
  );
}

function Metric({ label, value }: { label: string; value: string }) {
  return (
    <div className="rounded-2xl border border-white/10 bg-white/5 px-3 py-2">
      <div>{label}</div>
      <div className="mt-1 font-medium text-white">{value}</div>
    </div>
  );
}

export function Panel({
  title,
  subtitle,
  children,
}: {
  title: string;
  subtitle?: string;
  children: ReactNode;
}) {
  return (
    <section className="rounded-[24px] border border-white/10 bg-card p-5">
      <div className="flex items-start justify-between gap-4">
        <div>
          <h3 className="text-lg font-semibold text-white">{title}</h3>
          {subtitle ? <p className="mt-1 text-sm text-shell-muted">{subtitle}</p> : null}
        </div>
      </div>
      <div className="mt-5">{children}</div>
    </section>
  );
}
