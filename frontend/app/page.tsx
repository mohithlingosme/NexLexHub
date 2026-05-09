const cards = [
  {
    title: "Semantic Search",
    body: "Issue-first retrieval across judgments, statutes, and citation-linked chunks.",
  },
  {
    title: "Precedent Explorer",
    body: "Trace citing chains, treatment signals, and related authorities from one pane.",
  },
  {
    title: "Verified Analysis",
    body: "Citation-grounded legal intelligence reports with compliance scoring.",
  },
];

export default function Home() {
  return (
    <main className="min-h-screen px-6 py-10 md:px-12">
      <section className="mx-auto max-w-6xl rounded-[2rem] border border-black/10 bg-white/70 p-8 shadow-2xl backdrop-blur">
        <div className="grid gap-8 md:grid-cols-[1.3fr_1fr]">
          <div>
            <p className="mb-3 text-sm uppercase tracking-[0.3em] text-brief">NexLexHub 2.0</p>
            <h1 className="font-display text-5xl leading-tight md:text-7xl">
              Legal intelligence, not rewritten journalism.
            </h1>
            <p className="mt-6 max-w-2xl text-lg leading-8 text-black/75">
              Build research workflows on top of official sources, semantic chunks, citation graphs,
              and verification-first RAG.
            </p>
          </div>
          <div className="rounded-[1.5rem] bg-ink p-6 text-parchment">
            <p className="text-sm uppercase tracking-[0.25em] text-parchment/70">Platform Lenses</p>
            <ul className="mt-5 space-y-4 text-sm leading-7">
              <li>Official source retrieval for courts, tribunals, gazette notifications, and statutes.</li>
              <li>Hybrid vector plus lexical search over citation-aware judgment chunks.</li>
              <li>Compliance engine that avoids article reconstruction and enforces attribution.</li>
            </ul>
          </div>
        </div>
        <section className="mt-10 grid gap-5 md:grid-cols-3">
          {cards.map((card) => (
            <article key={card.title} className="rounded-[1.25rem] border border-black/10 bg-parchment p-5">
              <h2 className="font-display text-2xl">{card.title}</h2>
              <p className="mt-3 leading-7 text-black/75">{card.body}</p>
            </article>
          ))}
        </section>
      </section>
    </main>
  );
}
