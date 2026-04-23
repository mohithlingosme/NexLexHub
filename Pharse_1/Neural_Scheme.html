from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import cm, mm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table,
                                 TableStyle, PageBreak, HRFlowable, KeepTogether)
from reportlab.graphics.shapes import Drawing, Rect, String, Line, Circle, Polygon, Wedge, RoundRect, Arrow
from reportlab.graphics import renderPDF
from reportlab.graphics.charts.barcharts import VerticalBarChart
from reportlab.graphics.charts.piecharts import Pie
from reportlab.platypus.flowables import Flowable
import math

# ─── Color Palette ───────────────────────────────────────────────────────────
NAVY      = colors.HexColor('#0A1628')
COBALT    = colors.HexColor('#1B3A6B')
ROYAL     = colors.HexColor('#2463EB')
CYAN      = colors.HexColor('#06B6D4')
GOLD      = colors.HexColor('#F59E0B')
EMERALD   = colors.HexColor('#10B981')
CRIMSON   = colors.HexColor('#EF4444')
VIOLET    = colors.HexColor('#8B5CF6')
LIGHT_BG  = colors.HexColor('#F0F4FF')
BORDER    = colors.HexColor('#C7D2FE')
DARK_TEXT = colors.HexColor('#1E293B')
MID_TEXT  = colors.HexColor('#475569')
WHITE     = colors.white

PAGE_W, PAGE_H = A4  # 595 x 842

# ─── Styles ──────────────────────────────────────────────────────────────────
def make_styles():
    styles = getSampleStyleSheet()
    s = {}

    s['cover_title'] = ParagraphStyle('cover_title', fontName='Helvetica-Bold',
        fontSize=38, textColor=WHITE, leading=46, alignment=TA_CENTER, spaceAfter=10)
    s['cover_sub'] = ParagraphStyle('cover_sub', fontName='Helvetica',
        fontSize=16, textColor=CYAN, leading=22, alignment=TA_CENTER)
    s['cover_body'] = ParagraphStyle('cover_body', fontName='Helvetica',
        fontSize=11, textColor=colors.HexColor('#CBD5E1'), leading=18, alignment=TA_CENTER)

    s['chapter_num'] = ParagraphStyle('chapter_num', fontName='Helvetica-Bold',
        fontSize=11, textColor=CYAN, spaceAfter=4)
    s['chapter_title'] = ParagraphStyle('chapter_title', fontName='Helvetica-Bold',
        fontSize=22, textColor=NAVY, leading=28, spaceAfter=12)
    s['section_title'] = ParagraphStyle('section_title', fontName='Helvetica-Bold',
        fontSize=14, textColor=COBALT, leading=20, spaceBefore=14, spaceAfter=6)
    s['body'] = ParagraphStyle('body', fontName='Helvetica',
        fontSize=10.5, textColor=DARK_TEXT, leading=17, spaceAfter=8)
    s['caption'] = ParagraphStyle('caption', fontName='Helvetica-Oblique',
        fontSize=9, textColor=MID_TEXT, alignment=TA_CENTER, spaceAfter=16)
    s['callout'] = ParagraphStyle('callout', fontName='Helvetica-Bold',
        fontSize=10, textColor=COBALT, leading=16, leftIndent=14, spaceAfter=6)
    s['bullet'] = ParagraphStyle('bullet', fontName='Helvetica',
        fontSize=10.5, textColor=DARK_TEXT, leading=16, leftIndent=20,
        bulletIndent=8, spaceAfter=4)
    s['metric_label'] = ParagraphStyle('metric_label', fontName='Helvetica-Bold',
        fontSize=9, textColor=MID_TEXT, alignment=TA_CENTER)
    s['metric_val'] = ParagraphStyle('metric_val', fontName='Helvetica-Bold',
        fontSize=22, textColor=ROYAL, alignment=TA_CENTER, leading=26)
    s['table_header'] = ParagraphStyle('table_header', fontName='Helvetica-Bold',
        fontSize=9.5, textColor=WHITE, alignment=TA_CENTER)
    s['table_cell'] = ParagraphStyle('table_cell', fontName='Helvetica',
        fontSize=9, textColor=DARK_TEXT, leading=13)
    s['table_cell_bold'] = ParagraphStyle('table_cell_bold', fontName='Helvetica-Bold',
        fontSize=9, textColor=DARK_TEXT, leading=13)
    s['toc_entry'] = ParagraphStyle('toc_entry', fontName='Helvetica',
        fontSize=11, textColor=DARK_TEXT, leading=20)
    s['toc_page'] = ParagraphStyle('toc_page', fontName='Helvetica-Bold',
        fontSize=11, textColor=COBALT, alignment=TA_RIGHT, leading=20)
    s['disclaimer'] = ParagraphStyle('disclaimer', fontName='Helvetica-Oblique',
        fontSize=8.5, textColor=MID_TEXT, leading=14, alignment=TA_CENTER)
    return s

S = make_styles()

# ─── Helper Flowables ─────────────────────────────────────────────────────────
def chapter_divider(num, title, color=COBALT):
    story = []
    d = Drawing(PAGE_W - 80, 6)
    d.add(Rect(0, 0, PAGE_W - 80, 6, fillColor=color, strokeColor=None))
    story.append(d)
    story.append(Spacer(1, 8))
    story.append(Paragraph(f"CHAPTER {num}", S['chapter_num']))
    story.append(Paragraph(title, S['chapter_title']))
    return story

def section_header(text):
    return Paragraph(f"● {text}", S['section_title'])

def body(text):
    return Paragraph(text, S['body'])

def bullet(text):
    return Paragraph(f"• &nbsp;{text}", S['bullet'])

def rule(color=BORDER, thickness=1):
    return HRFlowable(width="100%", thickness=thickness, color=color, spaceAfter=8, spaceBefore=8)

# ─── Custom Flowable: Pipeline Arrow Diagram ──────────────────────────────────
class PipelineDiagram(Flowable):
    """Horizontal pipeline with labeled boxes and arrows."""
    def __init__(self, stages, width=None, height=100):
        super().__init__()
        self.stages = stages   # list of (label, color, icon_text)
        self.width = width or (PAGE_W - 80)
        self.height = height

    def wrap(self, *args):
        return self.width, self.height

    def draw(self):
        n = len(self.stages)
        box_w = (self.width - (n - 1) * 22) / n
        box_h = 64
        y0 = (self.height - box_h) / 2

        for i, (label, col, icon) in enumerate(self.stages):
            x = i * (box_w + 22)
            # Shadow
            self.canv.setFillColor(colors.HexColor('#00000020'))
            self.canv.roundRect(x + 3, y0 - 3, box_w, box_h, 8, fill=1, stroke=0)
            # Box
            self.canv.setFillColor(col)
            self.canv.roundRect(x, y0, box_w, box_h, 8, fill=1, stroke=0)
            # Icon area (circle)
            cx = x + box_w / 2
            self.canv.setFillColor(colors.HexColor('#FFFFFF30'))
            self.canv.circle(cx, y0 + box_h - 22, 16, fill=1, stroke=0)
            # Icon text
            self.canv.setFillColor(WHITE)
            self.canv.setFont('Helvetica-Bold', 13)
            self.canv.drawCentredString(cx, y0 + box_h - 26, icon)
            # Label
            self.canv.setFont('Helvetica-Bold', 7.5)
            lines = label.split('\n')
            for j, line in enumerate(lines):
                self.canv.drawCentredString(cx, y0 + 16 - j * 10, line)
            # Arrow
            if i < n - 1:
                ax = x + box_w + 2
                ay = y0 + box_h / 2
                self.canv.setFillColor(colors.HexColor('#94A3B8'))
                self.canv.setStrokeColor(colors.HexColor('#94A3B8'))
                self.canv.setLineWidth(2)
                self.canv.line(ax, ay, ax + 16, ay)
                # arrowhead
                self.canv.polygon([ax + 14, ay + 4, ax + 22, ay, ax + 14, ay - 4], fill=1)


class RadarChart(Flowable):
    """Simple radar / spider chart."""
    def __init__(self, labels, values, size=180):
        super().__init__()
        self.labels = labels
        self.values = values  # 0-1 scale
        self.size = size

    def wrap(self, *args):
        return self.size, self.size

    def draw(self):
        cx, cy = self.size / 2, self.size / 2
        r = self.size * 0.38
        n = len(self.labels)

        # Grid rings
        for ring in [0.25, 0.5, 0.75, 1.0]:
            pts = []
            for i in range(n):
                angle = math.pi / 2 + 2 * math.pi * i / n
                pts.extend([cx + r * ring * math.cos(angle),
                             cy + r * ring * math.sin(angle)])
            self.canv.setStrokeColor(BORDER)
            self.canv.setLineWidth(0.5)
            self.canv.polygon(pts, stroke=1, fill=0)

        # Data polygon
        pts = []
        for i, v in enumerate(self.values):
            angle = math.pi / 2 + 2 * math.pi * i / n
            pts.extend([cx + r * v * math.cos(angle),
                         cy + r * v * math.sin(angle)])
        self.canv.setFillColor(colors.HexColor('#2463EB40'))
        self.canv.setStrokeColor(ROYAL)
        self.canv.setLineWidth(1.5)
        self.canv.polygon(pts, stroke=1, fill=1)

        # Labels
        for i, lbl in enumerate(self.labels):
            angle = math.pi / 2 + 2 * math.pi * i / n
            lx = cx + (r + 18) * math.cos(angle)
            ly = cy + (r + 18) * math.sin(angle)
            self.canv.setFont('Helvetica-Bold', 7.5)
            self.canv.setFillColor(DARK_TEXT)
            self.canv.drawCentredString(lx, ly - 4, lbl)


class ScoreBar(Flowable):
    """Horizontal bar showing scoring tiers."""
    def __init__(self, width=None, height=55):
        super().__init__()
        self.width = width or (PAGE_W - 80)
        self.height = height

    def wrap(self, *args):
        return self.width, self.height

    def draw(self):
        w = self.width
        bar_h = 24
        bar_y = 20

        segments = [
            (0.0, 0.70, CRIMSON, "REJECT\n< 7.0"),
            (0.70, 0.80, GOLD, "REVIEW\n7.0–8.0"),
            (0.80, 1.0, EMERALD, "AUTO-PUBLISH\n> 8.0"),
        ]
        for start, end, col, lbl in segments:
            x1 = start * w
            x2 = end * w
            self.canv.setFillColor(col)
            self.canv.rect(x1, bar_y, x2 - x1, bar_h, fill=1, stroke=0)
            self.canv.setFillColor(WHITE)
            self.canv.setFont('Helvetica-Bold', 7.5)
            mid = (x1 + x2) / 2
            for j, line in enumerate(lbl.split('\n')):
                self.canv.drawCentredString(mid, bar_y + bar_h - 9 - j * 10, line)

        # Tick marks
        for val, label in [(0, '0'), (7, '7'), (8, '8'), (10, '10')]:
            x = (val / 10) * w
            self.canv.setStrokeColor(DARK_TEXT)
            self.canv.setLineWidth(1)
            self.canv.line(x, bar_y - 2, x, bar_y + bar_h + 2)
            self.canv.setFillColor(DARK_TEXT)
            self.canv.setFont('Helvetica-Bold', 8)
            self.canv.drawCentredString(x, bar_y - 12, label)


class ArchitectureMap(Flowable):
    """High-level architecture map showing data flow layers."""
    def __init__(self, width=None, height=300):
        super().__init__()
        self.width = width or (PAGE_W - 80)
        self.height = height

    def wrap(self, *args):
        return self.width, self.height

    def draw(self):
        w, h = self.width, self.height
        layers = [
            ("🌐  DATA SOURCES", "LiveLaw · Bar & Bench · Google News", COBALT, 0.85),
            ("⚙️   INGESTION & CLEANING", "BFS Scraper · BeautifulSoup · MinHash Dedup", colors.HexColor('#1E4D8C'), 0.70),
            ("🔍  AI FILTERING", "InLegalBERT · Semantic Scoring · is_legal: true/false", ROYAL, 0.55),
            ("✂️   SMART CHUNKING", "Semantic Chunks · Clause-Based Splits · Cross-Refs Preserved", colors.HexColor('#7C3AED'), 0.40),
            ("🧠  LLM ENGINE", "DeepSeek-R1 (Tier 1) · Gemma-3 / Aalap (Tier 2)", VIOLET, 0.27),
            ("✅  QA & VALIDATION", "LettuceDetect · LUMINA · Score Formula → Publish / Review / Reject", EMERALD, 0.14),
            ("💾  STORAGE & FRONTEND", "PostgreSQL · ElasticSearch · Vector DB · Next.js UI", colors.HexColor('#0E7490'), 0.02),
        ]

        layer_h = h * 0.12
        for label, desc, col, y_frac in layers:
            bx = 0
            by = h * y_frac
            bw = w
            # Background
            self.canv.setFillColor(col)
            self.canv.roundRect(bx, by, bw, layer_h, 5, fill=1, stroke=0)
            # Label
            self.canv.setFillColor(WHITE)
            self.canv.setFont('Helvetica-Bold', 9)
            self.canv.drawString(bx + 12, by + layer_h - 16, label)
            self.canv.setFont('Helvetica', 8)
            self.canv.setFillColor(colors.HexColor('#FFFFFFCC'))
            self.canv.drawString(bx + 12, by + 5, desc)

            # Connecting arrow
            if y_frac > 0.02:
                ax = w / 2
                ay_top = by - 2
                self.canv.setStrokeColor(colors.HexColor('#94A3B8'))
                self.canv.setFillColor(colors.HexColor('#94A3B8'))
                self.canv.setLineWidth(1.5)
                self.canv.line(ax, ay_top, ax, ay_top - 7)
                self.canv.polygon([ax - 5, ay_top - 5, ax + 5, ay_top - 5, ax, ay_top - 12], fill=1)


class ChunkingDiagram(Flowable):
    def __init__(self, width=None, height=160):
        super().__init__()
        self.width = width or (PAGE_W - 80)
        self.height = height

    def wrap(self, *args):
        return self.width, self.height

    def draw(self):
        w, h = self.width, self.height
        half = w / 2 - 10

        # LEFT: Bad chunking
        self.canv.setFillColor(colors.HexColor('#FEF2F2'))
        self.canv.roundRect(0, 10, half, h - 20, 6, fill=1, stroke=0)
        self.canv.setFillColor(CRIMSON)
        self.canv.setFont('Helvetica-Bold', 9)
        self.canv.drawCentredString(half / 2, h - 20, "❌  SLIDING WINDOW (BAD)")

        # chunks
        for i, (text, col) in enumerate([
            ("...Section 156(3) CrPC states that", colors.HexColor('#FECACA')),
            ("a magistrate may order police...", colors.HexColor('#FCA5A5')),
            ("...investigation. The accused argued", colors.HexColor('#FECACA')),
        ]):
            y = h - 40 - i * 34
            self.canv.setFillColor(col)
            self.canv.roundRect(10, y, half - 20, 28, 4, fill=1, stroke=0)
            self.canv.setFillColor(DARK_TEXT)
            self.canv.setFont('Helvetica', 7.5)
            self.canv.drawString(18, y + 10, text)

        self.canv.setFillColor(CRIMSON)
        self.canv.setFont('Helvetica-Oblique', 8)
        self.canv.drawCentredString(half / 2, 14, "Context SEVERED → AI gets confused")

        # RIGHT: Good chunking
        rx = half + 20
        self.canv.setFillColor(colors.HexColor('#F0FDF4'))
        self.canv.roundRect(rx, 10, half, h - 20, 6, fill=1, stroke=0)
        self.canv.setFillColor(EMERALD)
        self.canv.setFont('Helvetica-Bold', 9)
        self.canv.drawCentredString(rx + half / 2, h - 20, "✅  SEMANTIC CHUNKING (GOOD)")

        chunk_text = [
            "Section 156(3) CrPC / Section 175(3)",
            "BNSS: Magistrate's power to order",
            "police investigation — PRESERVED ✓",
        ]
        self.canv.setFillColor(colors.HexColor('#BBF7D0'))
        self.canv.roundRect(rx + 10, h - 130, half - 20, 80, 4, fill=1, stroke=0)
        self.canv.setFillColor(DARK_TEXT)
        self.canv.setFont('Helvetica', 7.5)
        for i, t in enumerate(chunk_text):
            self.canv.drawString(rx + 18, h - 60 - i * 12, t)

        self.canv.setFillColor(EMERALD)
        self.canv.setFont('Helvetica-Oblique', 8)
        self.canv.drawCentredString(rx + half / 2, 14, "Full context → Accurate AI output")


class CostComparisonChart(Flowable):
    def __init__(self, width=None, height=160):
        super().__init__()
        self.width = width or (PAGE_W - 80)
        self.height = height

    def wrap(self, *args):
        return self.width, self.height

    def draw(self):
        w, h = self.width, self.height
        models = ["OpenAI o1", "DeepSeek-R1", "Gemma-3 27B", "Aalap"]
        costs  = [60.0, 2.19, 0.16, 0.0]
        cols   = [CRIMSON, ROYAL, GOLD, EMERALD]
        max_cost = 60.0
        bar_area_h = h - 50
        bar_w = (w - 60) / len(models) - 10
        base_x = 30

        for i, (m, c, col) in enumerate(zip(models, costs, cols)):
            bh = (c / max_cost) * bar_area_h if max_cost > 0 else 4
            bh = max(bh, 4)
            bx = base_x + i * (bar_w + 10)
            by = 30
            self.canv.setFillColor(col)
            self.canv.roundRect(bx, by, bar_w, bh, 3, fill=1, stroke=0)
            # Value label
            self.canv.setFillColor(DARK_TEXT)
            self.canv.setFont('Helvetica-Bold', 8)
            label = f"${c:.2f}" if c > 0 else "FREE"
            self.canv.drawCentredString(bx + bar_w / 2, by + bh + 4, label)
            # Model name
            self.canv.setFont('Helvetica', 7.5)
            self.canv.drawCentredString(bx + bar_w / 2, by - 12, m)

        # Y-axis label
        self.canv.setFillColor(MID_TEXT)
        self.canv.setFont('Helvetica', 7.5)
        self.canv.drawString(0, h / 2, "$/1M Output Tokens")

        # Title
        self.canv.setFillColor(DARK_TEXT)
        self.canv.setFont('Helvetica-Bold', 8.5)
        self.canv.drawCentredString(w / 2, h - 10, "Output Cost per 1M Tokens — LexNexHub Model Options")


# ─── Page Templates ────────────────────────────────────────────────────────────
def make_cover(canvas, doc):
    canvas.saveState()
    w, h = A4

    # Background gradient simulation
    for i in range(100):
        frac = i / 100
        r = 0x0A + int((0x1B - 0x0A) * frac)
        g = 0x16 + int((0x3A - 0x16) * frac)
        b = 0x28 + int((0x6B - 0x28) * frac)
        canvas.setFillColorRGB(r/255, g/255, b/255)
        canvas.rect(0, h * frac - 1, w, h / 100 + 2, fill=1, stroke=0)

    # Geometric accent circles
    canvas.setFillColor(colors.HexColor('#FFFFFF08'))
    canvas.circle(w * 0.85, h * 0.8, 160, fill=1, stroke=0)
    canvas.circle(w * 0.15, h * 0.2, 120, fill=1, stroke=0)
    canvas.setFillColor(colors.HexColor('#06B6D410'))
    canvas.circle(w * 0.5, h * 0.5, 200, fill=1, stroke=0)

    # Top accent bar
    canvas.setFillColor(CYAN)
    canvas.rect(0, h - 8, w, 8, fill=1, stroke=0)

    # LexNexHub logo area
    canvas.setFillColor(ROYAL)
    canvas.roundRect(w/2 - 60, h - 80, 120, 44, 8, fill=1, stroke=0)
    canvas.setFillColor(WHITE)
    canvas.setFont('Helvetica-Bold', 18)
    canvas.drawCentredString(w/2, h - 62, "LexNexHub")

    # Main title
    canvas.setFillColor(WHITE)
    canvas.setFont('Helvetica-Bold', 36)
    canvas.drawCentredString(w/2, h - 155, "Phase 1 Architecture")
    canvas.setFont('Helvetica-Bold', 28)
    canvas.setFillColor(CYAN)
    canvas.drawCentredString(w/2, h - 190, "Visual Intelligence Guide")

    # Divider
    canvas.setStrokeColor(CYAN)
    canvas.setLineWidth(2)
    canvas.line(w/2 - 140, h - 210, w/2 + 140, h - 210)

    # Subtitle
    canvas.setFillColor(colors.HexColor('#CBD5E1'))
    canvas.setFont('Helvetica', 13)
    canvas.drawCentredString(w/2, h - 234,
        "A Plain-English Visual Breakdown of the AI Legal Pipeline")
    canvas.drawCentredString(w/2, h - 252, "for Non-Technical Decision Makers")

    # Pipeline preview boxes
    labels = ["Scrape", "Filter", "Chunk", "Extract", "QA", "Publish"]
    box_w = 66
    total = len(labels) * box_w + (len(labels)-1) * 8
    start_x = (w - total) / 2
    y_boxes = h - 370
    for i, lbl in enumerate(labels):
        bx = start_x + i * (box_w + 8)
        canvas.setFillColor(colors.HexColor(f'#1B3A6B'))
        canvas.roundRect(bx, y_boxes, box_w, 36, 5, fill=1, stroke=0)
        canvas.setStrokeColor(ROYAL)
        canvas.setLineWidth(1)
        canvas.roundRect(bx, y_boxes, box_w, 36, 5, fill=0, stroke=1)
        canvas.setFillColor(WHITE)
        canvas.setFont('Helvetica-Bold', 9)
        canvas.drawCentredString(bx + box_w/2, y_boxes + 14, lbl)
        if i < len(labels) - 1:
            canvas.setFillColor(CYAN)
            canvas.setFont('Helvetica-Bold', 12)
            canvas.drawCentredString(bx + box_w + 4, y_boxes + 14, "→")

    # Stats row
    stats = [("8-Point", "Output Schema"), ("< 50ms", "Query Latency"), ("96%", "Cost Saving vs. GPT"),
             ("0.9+", "AUROC QA Score")]
    sw = (w - 80) / len(stats)
    sy = h - 490
    for i, (val, lbl) in enumerate(stats):
        sx = 40 + i * sw
        canvas.setFillColor(colors.HexColor('#FFFFFF10'))
        canvas.roundRect(sx, sy, sw - 10, 56, 6, fill=1, stroke=0)
        canvas.setFillColor(GOLD)
        canvas.setFont('Helvetica-Bold', 20)
        canvas.drawCentredString(sx + (sw-10)/2, sy + 34, val)
        canvas.setFillColor(colors.HexColor('#94A3B8'))
        canvas.setFont('Helvetica', 8)
        canvas.drawCentredString(sx + (sw-10)/2, sy + 18, lbl)

    # Disclaimer box
    canvas.setFillColor(colors.HexColor('#FFFFFF12'))
    canvas.roundRect(40, 60, w - 80, 50, 6, fill=1, stroke=0)
    canvas.setFillColor(colors.HexColor('#94A3B8'))
    canvas.setFont('Helvetica-Oblique', 8)
    canvas.drawCentredString(w/2, 96, "DISCLAIMER: This document is for informational and research purposes only.")
    canvas.drawCentredString(w/2, 82, "LexNexHub outputs do not constitute licensed legal advice.")

    # Bottom bar
    canvas.setFillColor(colors.HexColor('#FFFFFF15'))
    canvas.rect(0, 0, w, 55, fill=1, stroke=0)
    canvas.setFillColor(colors.HexColor('#64748B'))
    canvas.setFont('Helvetica', 9)
    canvas.drawCentredString(w/2, 20, "LexNexHub Phase 1  ·  Deep Implementation Plan  ·  2025–2026")

    canvas.restoreState()


def make_page(canvas, doc):
    canvas.saveState()
    w, h = A4

    # Top bar
    canvas.setFillColor(NAVY)
    canvas.rect(0, h - 30, w, 30, fill=1, stroke=0)
    canvas.setFillColor(WHITE)
    canvas.setFont('Helvetica-Bold', 8)
    canvas.drawString(40, h - 18, "LexNexHub Phase 1 — Visual Architecture Guide")
    canvas.setFont('Helvetica', 8)
    canvas.drawRightString(w - 40, h - 18, f"Page {doc.page}")

    # Accent stripe
    canvas.setFillColor(CYAN)
    canvas.rect(0, h - 33, w, 3, fill=1, stroke=0)

    # Footer
    canvas.setFillColor(colors.HexColor('#F8FAFC'))
    canvas.rect(0, 0, w, 28, fill=1, stroke=0)
    canvas.setStrokeColor(BORDER)
    canvas.setLineWidth(0.5)
    canvas.line(40, 28, w - 40, 28)
    canvas.setFillColor(MID_TEXT)
    canvas.setFont('Helvetica-Oblique', 7.5)
    canvas.drawCentredString(w/2, 10, "For informational purposes only · Not legal advice")

    canvas.restoreState()


# ─── BUILD STORY ───────────────────────────────────────────────────────────────
def build():
    doc = SimpleDocTemplate("/mnt/user-data/outputs/LexNexHub_Visual_Guide.pdf",
        pagesize=A4,
        leftMargin=40, rightMargin=40,
        topMargin=50, bottomMargin=40,
        title="LexNexHub Phase 1 — Visual Guide",
        author="LexNexHub Architecture Team")

    story = []

    # ─── COVER ───────────────────────────────────────────────────────────────
    story.append(PageBreak())   # triggers cover

    # ─── TABLE OF CONTENTS ───────────────────────────────────────────────────
    story.extend(chapter_divider("—", "Table of Contents", COBALT))
    toc_items = [
        ("1", "What is LexNexHub?", "The Big Picture Explained"),
        ("2", "The 8-Point Output Schema", "What the System Produces"),
        ("3", "Data Ingestion & Cleaning", "How Legal Articles Are Collected"),
        ("4", "AI-Powered Legal Filtering", "InLegalBERT — The Brain at the Gate"),
        ("5", "Smart Chunking", "How Long Documents Are Split Without Losing Meaning"),
        ("6", "The LLM Processing Engine", "DeepSeek-R1, Gemma-3 & Aalap"),
        ("7", "Quality Assurance", "Hallucination Detection & Scoring"),
        ("8", "DevSecOps & Security", "How the System Defends Itself"),
        ("9", "Storage & Infrastructure", "Where Data Lives"),
        ("10", "Cost & Model Comparison", "Economics of the Pipeline"),
    ]
    toc_data = []
    for num, title, sub in toc_items:
        toc_data.append([
            Paragraph(f"<b>{num}.</b> {title}", S['toc_entry']),
            Paragraph(f"<i>{sub}</i>", ParagraphStyle('s', fontName='Helvetica-Oblique',
                fontSize=9, textColor=MID_TEXT)),
        ])
    toc_table = Table(toc_data, colWidths=[280, 200])
    toc_table.setStyle(TableStyle([
        ('ROWBACKGROUNDS', (0,0), (-1,-1), [WHITE, LIGHT_BG]),
        ('TOPPADDING', (0,0), (-1,-1), 7),
        ('BOTTOMPADDING', (0,0), (-1,-1), 7),
        ('LEFTPADDING', (0,0), (0,-1), 10),
        ('LINEBELOW', (0,-1), (-1,-1), 1, BORDER),
    ]))
    story.append(toc_table)
    story.append(PageBreak())

    # ─── CH 1: WHAT IS LEXNEXHUB ─────────────────────────────────────────────
    story.extend(chapter_divider("1", "What Is LexNexHub?"))
    story.append(body(
        "LexNexHub is an <b>automated AI pipeline</b> that continuously reads legal news websites, "
        "extracts key information from court judgments and legal articles, and transforms that "
        "unstructured text into a clean, structured format that lawyers, researchers, and legal "
        "professionals can instantly understand and search through."))
    story.append(Spacer(1, 10))
    story.append(body(
        "Think of it like a highly intelligent legal researcher who never sleeps — "
        "reading thousands of court rulings every day, extracting the important points, "
        "checking every fact for accuracy, and filing everything neatly in a searchable database."))
    story.append(Spacer(1, 14))

    story.append(section_header("The End-to-End Journey of One Legal Article"))
    story.append(body(
        "Here is how a single article travels through the LexNexHub pipeline, "
        "from a raw news URL to a structured, verified legal record:"))
    story.append(Spacer(1, 10))

    stages = [
        ("🌐\nSCRAPE", COBALT, "🌐"),
        ("🧹\nCLEAN", colors.HexColor('#1E4D8C'), "🧹"),
        ("🔍\nFILTER", ROYAL, "🔍"),
        ("✂️\nCHUNK", VIOLET, "✂"),
        ("🧠\nEXTRACT", colors.HexColor('#7C3AED'), "🧠"),
        ("✅\nVALIDATE", EMERALD, "✅"),
        ("💾\nPUBLISH", colors.HexColor('#0E7490'), "💾"),
    ]
    pipe = PipelineDiagram(
        [(lbl, col, ico) for lbl, col, ico in stages],
        width=PAGE_W - 80, height=110
    )
    story.append(pipe)
    story.append(Paragraph("Figure 1.1 — The 7-Stage LexNexHub Processing Pipeline", S['caption']))
    story.append(Spacer(1, 10))

    story.append(section_header("Why Does This Matter?"))
    story.append(body(
        "Indian law is undergoing a massive transformation. The old Indian Penal Code (IPC) "
        "has been replaced by the Bharatiya Nyaya Sanhita (BNS). The old CrPC has become the "
        "Bharatiya Nagarik Suraksha Sanhita (BNSS). Keeping up with these changes manually "
        "is nearly impossible. LexNexHub automates this intelligence gathering at scale."))
    story.append(Spacer(1, 8))

    # Metrics table
    metrics = [
        ["Metric", "Target", "What It Means"],
        ["Daily Processing Capacity", "1,000s of articles/day", "High-volume legal news covered automatically"],
        ["Query Response Time", "< 50 milliseconds", "Instant search results for the user"],
        ["Cost Savings vs. OpenAI", "~96% cheaper", "DeepSeek-R1 at $2.19/M vs $60/M output tokens"],
        ["QA Score Threshold (Auto-Publish)", "> 8.0 / 10", "Only highly accurate results reach the public"],
        ["Hallucination Detection AUROC", "> 0.90", "Industry-leading accuracy in catching AI errors"],
    ]
    mt = Table(metrics, colWidths=[175, 130, 190])
    mt.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), COBALT),
        ('TEXTCOLOR', (0,0), (-1,0), WHITE),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,0), 9),
        ('FONTNAME', (0,1), (-1,-1), 'Helvetica'),
        ('FONTSIZE', (0,1), (-1,-1), 9),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [WHITE, LIGHT_BG]),
        ('GRID', (0,0), (-1,-1), 0.5, BORDER),
        ('ALIGN', (1,1), (1,-1), 'CENTER'),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(mt)
    story.append(Paragraph("Table 1.1 — LexNexHub Key Performance Targets", S['caption']))
    story.append(PageBreak())

    # ─── CH 2: 8-POINT SCHEMA ─────────────────────────────────────────────────
    story.extend(chapter_divider("2", "The 8-Point Output Schema", ROYAL))
    story.append(body(
        "Every legal article processed by LexNexHub is transformed into a standardised "
        "<b>8-Point Schema</b>. This structured format makes it easy for users to quickly "
        "understand a court judgment without reading the entire document."))
    story.append(Spacer(1, 10))

    schema_items = [
        ("1", "Title", "The formal case heading and court name", COBALT),
        ("2", "Summary Intro", "A 2-3 sentence plain-English overview of the ruling", ROYAL),
        ("3", "Background", "The original dispute — how the case began", colors.HexColor('#1E4D8C')),
        ("4", "Court Reasoning", "The logic the judge used to reach the decision", VIOLET),
        ("5", "Legal Principles", "The specific laws and rules the court applied", colors.HexColor('#7C3AED')),
        ("6", "Case References", "Past judgments cited as precedent (e.g., Bhajan Lal)", colors.HexColor('#059669')),
        ("7", "Final Ruling", "What the court decided — the outcome", EMERALD),
        ("8", "Conclusion", "Broader implications for the legal system", GOLD),
    ]
    schema_data = [
        [
            Paragraph(f'<font color="white"><b>{n}</b></font>', ParagraphStyle('cn', fontName='Helvetica-Bold', fontSize=14, textColor=WHITE, alignment=TA_CENTER)),
            Paragraph(f'<b>{t}</b>', S['table_cell_bold']),
            Paragraph(desc, S['table_cell']),
        ]
        for n, t, desc, _ in schema_items
    ]
    schema_table = Table(schema_data, colWidths=[36, 120, 330])
    schema_style = [
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('LEFTPADDING', (0,0), (-1,-1), 10),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('GRID', (0,0), (-1,-1), 0.5, BORDER),
    ]
    for i, (_, _, _, col) in enumerate(schema_items):
        schema_style.append(('BACKGROUND', (0,i), (0,i), col))
        schema_style.append(('BACKGROUND', (1,i), (-1,i), LIGHT_BG if i%2==0 else WHITE))
    schema_table.setStyle(TableStyle(schema_style))
    story.append(schema_table)
    story.append(Paragraph("Figure 2.1 — The Mandatory 8-Point Output Schema", S['caption']))
    story.append(Spacer(1, 12))

    story.append(section_header("Real-World Example"))
    story.append(body(
        "Consider this real article: <i>\"Magistrate's Order For Investigation Can't Be Quashed "
        "By Relying On Accused's Defence: Supreme Court.\"</i> Below is how LexNexHub maps the "
        "raw article to the 8-point schema:"))
    story.append(Spacer(1, 8))

    example_data = [
        [Paragraph("<b>Schema Field</b>", S['table_header']),
         Paragraph("<b>Extracted Content</b>", S['table_header'])],
        ["Title", "Magistrate's Order For Investigation Can't Be Quashed By Relying On Accused's Defence"],
        ["Summary Intro", "Supreme Court clarified the scope of a Magistrate's power under Section 175(3) BNSS"],
        ["Background", "Civil transaction turned criminal; dispute over whether Magistrate's order was valid"],
        ["Court Reasoning", "Evaluating defence evidence at preliminary stage improperly interferes with investigation"],
        ["Legal Principles", "Rules governing Section 175(3) BNSS (formerly Section 156(3) CrPC)"],
        ["Case References", "State of Haryana v. Bhajan Lal; Priyanka Srivastava; Anil Kumar v. M.K. Aiyappa"],
        ["Final Ruling", "Magistrate's original order was restored; High Court's quashing order overturned"],
        ["Conclusion", "Magistrates cannot be blocked from ordering investigation based on accused's defence"],
    ]
    et = Table(example_data, colWidths=[130, 360])
    et.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), NAVY),
        ('TEXTCOLOR', (0,0), (-1,0), WHITE),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [LIGHT_BG, WHITE]),
        ('FONTNAME', (0,1), (-1,-1), 'Helvetica'),
        ('FONTSIZE', (0,0), (-1,-1), 9),
        ('GRID', (0,0), (-1,-1), 0.5, BORDER),
        ('FONTNAME', (0,1), (0,-1), 'Helvetica-Bold'),
        ('TEXTCOLOR', (0,1), (0,-1), COBALT),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    story.append(et)
    story.append(Paragraph("Table 2.1 — Live Example: Supreme Court IPC/BNS Ruling", S['caption']))
    story.append(PageBreak())

    # ─── CH 3: DATA INGESTION ─────────────────────────────────────────────────
    story.extend(chapter_divider("3", "Data Ingestion & Cleaning", COBALT))
    story.append(body(
        "Before any AI processing can begin, LexNexHub must continuously collect and clean "
        "raw legal text from across the web. This is the 'factory floor' of the pipeline — "
        "it handles the messy, real-world problem of getting clean data in bulk."))
    story.append(Spacer(1, 10))

    story.append(section_header("How the Scraper Works: Breadth-First Search (BFS)"))
    story.append(body(
        "Imagine a legal news website as a map. The scraper starts at the homepage (the "
        "most important point) and explores <b>outward in layers</b> — first reading all "
        "the latest articles, then going into categories, then into archives. "
        "This \"Breadth-First\" approach ensures the most recent content is always captured "
        "before diving into historical records."))
    story.append(Spacer(1, 10))

    # BFS visual
    d = Drawing(PAGE_W - 80, 140)
    # Homepage node
    d.add(Circle(240, 100, 28, fillColor=COBALT, strokeColor=None))
    d.add(String(240, 95, "Homepage", textAnchor='middle', fontName='Helvetica-Bold',
                 fontSize=7.5, fillColor=WHITE))
    # Category nodes
    cats = [("LiveLaw", 80, 55), ("Bar&Bench", 160, 30), ("High Ct.", 320, 30), ("SC News", 400, 55)]
    for lbl, x, y in cats:
        d.add(Line(240, 100, x + 25, y + 18, strokeColor=ROYAL, strokeWidth=1.5))
        d.add(RoundRect(x, y, 50, 36, 5, fillColor=ROYAL, strokeColor=None))
        d.add(String(x + 25, y + 14, lbl, textAnchor='middle', fontName='Helvetica-Bold',
                     fontSize=7, fillColor=WHITE))
    # Article nodes
    arts = [(50, 10), (100, 10), (140, 10), (210, 10), (300, 10), (360, 10), (410, 10), (450, 10)]
    art_parents = [(80,55), (80,55), (160,30), (160,30), (320,30), (320,30), (400,55), (400,55)]
    for (ax, ay), (px, py) in zip(arts, art_parents):
        d.add(Line(px + 25, py + 18, ax + 15, ay + 10, strokeColor=BORDER, strokeWidth=0.8))
        d.add(RoundRect(ax, ay, 30, 20, 3, fillColor=colors.HexColor('#E0E7FF'), strokeColor=None))
        d.add(String(ax + 15, ay + 7, "Art.", textAnchor='middle', fontName='Helvetica',
                     fontSize=6, fillColor=DARK_TEXT))
    story.append(d)
    story.append(Paragraph("Figure 3.1 — Breadth-First Search: Scraping Layer by Layer", S['caption']))

    story.append(section_header("Deduplication: Never Processing the Same Article Twice"))
    dedup_data = [
        [Paragraph("<b>Method</b>", S['table_header']),
         Paragraph("<b>How It Works</b>", S['table_header']),
         Paragraph("<b>Use Case</b>", S['table_header'])],
        ["HashSet (Exact Match)", "Stores a unique fingerprint (hash) of every URL seen. Rejects exact duplicates instantly.",
         "Stops the same LiveLaw URL being processed 10 times"],
        ["MinHash (Near-Duplicate)", "Compares how similar two articles are in meaning (Jaccard similarity). Rejects reworded copies.",
         "Stops aggregator sites that copy news with minor edits"],
    ]
    dt = Table(dedup_data, colWidths=[130, 220, 145])
    dt.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), NAVY), ('TEXTCOLOR', (0,0), (-1,0), WHITE),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'), ('FONTSIZE', (0,0), (-1,-1), 9),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [LIGHT_BG, WHITE]),
        ('FONTNAME', (0,1), (-1,-1), 'Helvetica'), ('GRID', (0,0), (-1,-1), 0.5, BORDER),
        ('TOPPADDING', (0,0), (-1,-1), 7), ('BOTTOMPADDING', (0,0), (-1,-1), 7),
        ('LEFTPADDING', (0,0), (-1,-1), 8), ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    story.append(dt)
    story.append(Paragraph("Table 3.1 — Deduplication Strategies", S['caption']))

    story.append(section_header("Text Cleaning: From Noisy HTML to Pure Text"))
    story.append(body(
        "Raw web pages contain advertisements, menus, social media buttons, and hundreds "
        "of hidden code tags. The cleaning layer strips all of this noise using "
        "<b>BeautifulSoup</b> and regular expressions, leaving only the pure legal text."))
    story.append(Spacer(1, 6))
    story.append(body(
        "<b>Special Note on Legal Stopwords:</b> In normal text processing, common words like "
        "\"and\", \"or\", \"the\" are removed to save space. However, in legal text, these words "
        "can completely change the meaning of a statute. LexNexHub uses a <b>custom legal "
        "stopword list</b> that preserves structural connectors critical to accurate interpretation."))
    story.append(PageBreak())

    # ─── CH 4: FILTERING ──────────────────────────────────────────────────────
    story.extend(chapter_divider("4", "AI-Powered Legal Filtering (InLegalBERT)", ROYAL))
    story.append(body(
        "Not every article scraped from the web is actually a legal document. Political opinions, "
        "celebrity news, and sports coverage might all appear on aggregator sites. "
        "LexNexHub uses a specialized AI model — <b>InLegalBERT</b> — to act as a highly "
        "accurate gatekeeper, only allowing genuine legal content to proceed."))
    story.append(Spacer(1, 10))

    story.append(section_header("What Makes InLegalBERT Special?"))
    story.append(body(
        "InLegalBERT was trained on <b>5.4 million Indian legal documents</b> totalling "
        "27 gigabytes of text. It has deeply internalized the patterns, terminology, and "
        "structure of Indian court language. When it reads a text, it intuitively "
        "recognises legal language at a level that generic AI models cannot match."))
    story.append(Spacer(1, 10))

    # Comparison table
    comp_data = [
        [Paragraph("<b>Feature</b>", S['table_header']),
         Paragraph("<b>Generic BERT</b>", S['table_header']),
         Paragraph("<b>InLegalBERT</b>", S['table_header'])],
        ["Training Data", "General internet text", "5.4M Indian legal documents (27GB)"],
        ["Legal Terminology", "Basic understanding", "Deep specialization in Indian statutes"],
        ["Accuracy on Legal Tasks", "Moderate", "Significantly higher F1 score"],
        ["Understanding of IPC/BNS", "Limited", "Native understanding of Indian legal codes"],
        ["Cost", "Low", "Free (open-source on Hugging Face)"],
    ]
    ct = Table(comp_data, colWidths=[160, 165, 170])
    ct.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), NAVY), ('TEXTCOLOR', (0,0), (-1,0), WHITE),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'), ('FONTSIZE', (0,0), (-1,-1), 9),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [LIGHT_BG, WHITE]),
        ('FONTNAME', (0,1), (-1,-1), 'Helvetica'),
        ('FONTNAME', (0,1), (0,-1), 'Helvetica-Bold'),
        ('GRID', (0,0), (-1,-1), 0.5, BORDER),
        ('TOPPADDING', (0,0), (-1,-1), 7), ('BOTTOMPADDING', (0,0), (-1,-1), 7),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('BACKGROUND', (2,1), (2,-1), colors.HexColor('#EFF6FF')),
        ('TEXTCOLOR', (2,1), (2,-1), COBALT),
        ('FONTNAME', (2,1), (2,-1), 'Helvetica-Bold'),
    ]))
    story.append(ct)
    story.append(Paragraph("Table 4.1 — Generic BERT vs. InLegalBERT", S['caption']))
    story.append(Spacer(1, 12))

    story.append(section_header("The Filtering Decision Process"))
    story.append(body(
        "The filtering system makes a binary YES/NO decision on every article. "
        "The decision is expressed as a confidence score from 0 to 1:"))
    story.append(Spacer(1, 8))

    # Filter flow diagram
    fd = Drawing(PAGE_W - 80, 100)
    # Input box
    fd.add(RoundRect(0, 35, 100, 40, 5, fillColor=COBALT, strokeColor=None))
    fd.add(String(50, 52, "Article Text", textAnchor='middle', fontName='Helvetica-Bold', fontSize=8, fillColor=WHITE))
    # Arrow
    fd.add(Line(100, 55, 130, 55, strokeColor=MID_TEXT, strokeWidth=1.5))
    fd.add(Polygon([128, 59, 136, 55, 128, 51], fillColor=MID_TEXT, strokeColor=None))
    # InLegalBERT box
    fd.add(RoundRect(136, 28, 120, 54, 5, fillColor=ROYAL, strokeColor=None))
    fd.add(String(196, 59, "InLegalBERT", textAnchor='middle', fontName='Helvetica-Bold', fontSize=9, fillColor=WHITE))
    fd.add(String(196, 44, "Score: 0.0 – 1.0", textAnchor='middle', fontName='Helvetica', fontSize=7.5, fillColor=colors.HexColor('#BFDBFE')))
    # Arrow to decision
    fd.add(Line(256, 55, 286, 55, strokeColor=MID_TEXT, strokeWidth=1.5))
    fd.add(Polygon([284, 59, 292, 55, 284, 51], fillColor=MID_TEXT, strokeColor=None))
    # Decision diamond
    fd.add(Polygon([340,80, 390,55, 340,30, 290,55], fillColor=GOLD, strokeColor=None))
    fd.add(String(340, 52, "Score", textAnchor='middle', fontName='Helvetica-Bold', fontSize=8, fillColor=DARK_TEXT))
    fd.add(String(340, 41, "> 0.85?", textAnchor='middle', fontName='Helvetica-Bold', fontSize=8, fillColor=DARK_TEXT))
    # YES path
    fd.add(Line(390, 55, 420, 55, strokeColor=EMERALD, strokeWidth=1.5))
    fd.add(Polygon([418, 59, 426, 55, 418, 51], fillColor=EMERALD, strokeColor=None))
    fd.add(RoundRect(426, 35, 70, 40, 5, fillColor=EMERALD, strokeColor=None))
    fd.add(String(461, 58, "is_legal:", textAnchor='middle', fontName='Helvetica-Bold', fontSize=8, fillColor=WHITE))
    fd.add(String(461, 45, "true  →", textAnchor='middle', fontName='Helvetica-Bold', fontSize=8, fillColor=WHITE))
    fd.add(String(468, 32, "PROCEED", textAnchor='middle', fontName='Helvetica-Bold', fontSize=6.5, fillColor=WHITE))
    # NO path
    fd.add(Line(340, 30, 340, 10, strokeColor=CRIMSON, strokeWidth=1.5))
    fd.add(RoundRect(290, 0, 100, 20, 4, fillColor=CRIMSON, strokeColor=None))
    fd.add(String(340, 7, "DISCARD (non-legal)", textAnchor='middle', fontName='Helvetica-Bold', fontSize=7, fillColor=WHITE))
    # Labels
    fd.add(String(406, 65, "YES", textAnchor='middle', fontName='Helvetica-Bold', fontSize=7, fillColor=EMERALD))
    fd.add(String(350, 18, "NO", textAnchor='middle', fontName='Helvetica-Bold', fontSize=7, fillColor=CRIMSON))
    story.append(fd)
    story.append(Paragraph("Figure 4.1 — InLegalBERT Classification Decision Flow", S['caption']))
    story.append(PageBreak())

    # ─── CH 5: CHUNKING ───────────────────────────────────────────────────────
    story.extend(chapter_divider("5", "Smart Chunking: Splitting Without Losing Meaning", VIOLET))
    story.append(body(
        "AI models can only read a limited amount of text at one time — like a person who "
        "can only hold 10 pages in their working memory. A 50-page Supreme Court judgment "
        "must therefore be split into smaller pieces (\"chunks\"). The challenge is doing "
        "this <b>without cutting through the middle of a legal argument</b>."))
    story.append(Spacer(1, 10))

    story.append(ChunkingDiagram(width=PAGE_W - 80, height=165))
    story.append(Paragraph("Figure 5.1 — Sliding Window (Bad) vs. Semantic Chunking (Good)", S['caption']))
    story.append(Spacer(1, 10))

    story.append(section_header("Method 1: Semantic Chunking"))
    story.append(body(
        "The system converts each sentence into a mathematical vector (a list of numbers "
        "that represents its meaning). It then checks how similar each consecutive pair of "
        "sentences is to each other using <b>cosine similarity</b>. When the similarity "
        "drops sharply, it means the document is switching topics — so a chunk boundary "
        "is placed there. The result is chunks that each represent one complete legal idea."))
    story.append(Spacer(1, 8))

    story.append(section_header("Method 2: Clause-Based Chunking"))
    story.append(body(
        "Indian legal documents reference specific laws by section number (e.g., "
        "\"Section 156(3) CrPC\"). The system uses pattern recognition to find these "
        "references and ensure that when a section is mentioned alongside its new-law "
        "counterpart (e.g., \"Section 175(3) BNSS\"), <b>both references always remain in "
        "the same chunk</b>. This is critical because the AI model needs both pieces of "
        "context to understand the legal argument correctly."))
    story.append(Spacer(1, 10))

    # IPC to BNS mapping
    story.append(section_header("India's New Legal Codes: Mapping Old to New"))
    story.append(body(
        "LexNexHub is specifically engineered to handle India's landmark 2024 legislative "
        "transition. On July 1, 2024, three new codes replaced the colonial-era framework:"))
    story.append(Spacer(1, 6))

    law_data = [
        [Paragraph("<b>Old Law (Colonial Era)</b>", S['table_header']),
         Paragraph("<b>New Law (2024)</b>", S['table_header']),
         Paragraph("<b>What It Governs</b>", S['table_header'])],
        ["Indian Penal Code (IPC)", "Bharatiya Nyaya Sanhita (BNS)", "Criminal offences and punishments"],
        ["Code of Criminal Procedure (CrPC)", "Bharatiya Nagarik Suraksha Sanhita (BNSS)", "Criminal court procedures"],
        ["Indian Evidence Act (IEA)", "Bharatiya Sakshya Adhiniyam (BSA)", "Evidence rules in court"],
    ]
    lt = Table(law_data, colWidths=[165, 175, 155])
    lt.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), COBALT), ('TEXTCOLOR', (0,0), (-1,0), WHITE),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'), ('FONTSIZE', (0,0), (-1,-1), 9),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.HexColor('#FFF7ED'), colors.HexColor('#FFFBEB')]),
        ('FONTNAME', (0,1), (-1,-1), 'Helvetica'),
        ('FONTNAME', (0,1), (0,-1), 'Helvetica-Bold'),
        ('TEXTCOLOR', (0,1), (0,-1), CRIMSON),
        ('FONTNAME', (1,1), (1,-1), 'Helvetica-Bold'),
        ('TEXTCOLOR', (1,1), (1,-1), EMERALD),
        ('GRID', (0,0), (-1,-1), 0.5, BORDER),
        ('TOPPADDING', (0,0), (-1,-1), 8), ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(lt)
    story.append(Paragraph("Table 5.1 — India's 2024 Legislative Transition", S['caption']))
    story.append(PageBreak())

    # ─── CH 6: LLM ENGINE ────────────────────────────────────────────────────
    story.extend(chapter_divider("6", "The LLM Processing Engine", colors.HexColor('#7C3AED')))
    story.append(body(
        "The LLM (Large Language Model) Engine is the brain of LexNexHub. It reads the "
        "chunked legal text and extracts all 8 structured fields. Rather than using a "
        "single model for everything, LexNexHub uses a <b>2-tier routing architecture</b> — "
        "sending complex tasks to the powerful model and simple tasks to the fast, "
        "cheap model. This is like having a senior partner and a junior associate: "
        "the senior handles complex analysis, the junior handles formatting."))
    story.append(Spacer(1, 10))

    # Tier diagram
    td = Drawing(PAGE_W - 80, 130)
    # Tier 1 box
    td.add(RoundRect(0, 55, (PAGE_W-90)*0.48, 72, 8, fillColor=colors.HexColor('#1E1B4B'), strokeColor=None))
    td.add(String(130, 115, "TIER 1: HEAVY REASONING", textAnchor='middle', fontName='Helvetica-Bold', fontSize=9, fillColor=CYAN))
    td.add(String(130, 100, "DeepSeek-R1", textAnchor='middle', fontName='Helvetica-Bold', fontSize=13, fillColor=WHITE))
    td.add(String(130, 85, "Chain-of-Thought · Self-Reflection", textAnchor='middle', fontName='Helvetica', fontSize=7.5, fillColor=colors.HexColor('#A5B4FC')))
    td.add(String(130, 73, "Court Reasoning · Legal Principles · Precedents", textAnchor='middle', fontName='Helvetica', fontSize=7, fillColor=colors.HexColor('#818CF8')))
    td.add(String(130, 62, "$0.14/1M input  ·  $2.19/1M output", textAnchor='middle', fontName='Helvetica-Bold', fontSize=7.5, fillColor=GOLD))

    # Arrow between
    mid_x = (PAGE_W - 90) * 0.5
    td.add(Line(mid_x - 14, 90, mid_x + 14, 90, strokeColor=MID_TEXT, strokeWidth=1.5))
    td.add(String(mid_x, 96, "OR", textAnchor='middle', fontName='Helvetica-Bold', fontSize=9, fillColor=MID_TEXT))

    # Tier 2 box
    rx = (PAGE_W - 90) * 0.52
    td.add(RoundRect(rx, 55, (PAGE_W-90)*0.48, 72, 8, fillColor=colors.HexColor('#052E16'), strokeColor=None))
    td.add(String(rx + 130, 115, "TIER 2: FAST EXTRACTION", textAnchor='middle', fontName='Helvetica-Bold', fontSize=9, fillColor=EMERALD))
    td.add(String(rx + 130, 100, "Gemma-3 27B  /  Aalap", textAnchor='middle', fontName='Helvetica-Bold', fontSize=13, fillColor=WHITE))
    td.add(String(rx + 130, 85, "Fast · Low VRAM · Indian Legal Fine-tune", textAnchor='middle', fontName='Helvetica', fontSize=7.5, fillColor=colors.HexColor('#6EE7B7')))
    td.add(String(rx + 130, 73, "Summaries · HTML Formatting · Quick Extractions", textAnchor='middle', fontName='Helvetica', fontSize=7, fillColor=colors.HexColor('#34D399')))
    td.add(String(rx + 130, 62, "Gemma: $0.08/1M input  ·  Aalap: FREE", textAnchor='middle', fontName='Helvetica-Bold', fontSize=7.5, fillColor=GOLD))

    # Routing label
    td.add(RoundRect(mid_x - 50, 10, 100, 26, 5, fillColor=COBALT, strokeColor=None))
    td.add(String(mid_x, 20, "Smart Router", textAnchor='middle', fontName='Helvetica-Bold', fontSize=8, fillColor=WHITE))
    td.add(Line(mid_x, 36, mid_x - 70, 55, strokeColor=ROYAL, strokeWidth=1))
    td.add(Line(mid_x, 36, mid_x + 70, 55, strokeColor=EMERALD, strokeWidth=1))
    story.append(td)
    story.append(Paragraph("Figure 6.1 — Two-Tier LLM Routing Architecture", S['caption']))
    story.append(Spacer(1, 8))

    story.append(CostComparisonChart(width=PAGE_W - 80, height=165))
    story.append(Paragraph("Figure 6.2 — Output Cost Comparison: $60/M (OpenAI o1) vs $2.19/M (DeepSeek-R1)", S['caption']))
    story.append(Spacer(1, 8))

    story.append(section_header("What is Chain-of-Thought (CoT) Reasoning?"))
    story.append(body(
        "Standard AI models predict the next word statistically. DeepSeek-R1 uses "
        "an internal \"thinking\" phase where it works through problems step-by-step — "
        "like a lawyer drafting an argument before writing the final brief. This means "
        "it checks its own reasoning, spots contradictions, and adapts its strategy "
        "before producing the final answer. For complex legal analysis, this makes "
        "a significant difference in output quality."))
    story.append(PageBreak())

    # ─── CH 7: QA ─────────────────────────────────────────────────────────────
    story.extend(chapter_divider("7", "Quality Assurance & Hallucination Detection", EMERALD))
    story.append(body(
        "A hallucination in legal AI is not just an error — it is a <b>catastrophic failure</b>. "
        "If the system invents a legal precedent, fabricates a judge's ruling, or misquotes "
        "a statute, legal professionals relying on this data could be seriously misled. "
        "LexNexHub's QA Engine uses two specialized frameworks to catch these errors "
        "before anything reaches the public."))
    story.append(Spacer(1, 10))

    story.append(section_header("Framework 1: LettuceDetect (Word-Level Fact Checking)"))
    story.append(body(
        "LettuceDetect reads the original source article and the AI-generated output "
        "simultaneously. It highlights every word or phrase in the AI output that "
        "<b>cannot be found or supported in the original source</b>. It does this at "
        "the token level — individual words — making it extremely precise."))
    story.append(Spacer(1, 6))
    story.append(body(
        "<b>Key Stats:</b> Processes 30–60 documents per second on a single GPU. "
        "Handles documents up to 8,192 tokens (far more than older models). "
        "Achieves 79.22% F1 accuracy at example level and outperforms much larger "
        "models (like Llama-2-13B) at a fraction of the computing cost."))
    story.append(Spacer(1, 10))

    story.append(section_header("Framework 2: LUMINA (Statistical Behavior Analysis)"))
    story.append(body(
        "While LettuceDetect checks specific words, LUMINA looks at the AI model's "
        "<b>behavior patterns</b>. It answers the question: \"Did the model use the "
        "provided article to write its answer, or did it rely on its own internal memory?\" "
        "If the model ignored the source material and wrote from memory (which may be "
        "outdated or incorrect), LUMINA flags the output. It achieves AUROC scores above "
        "0.90 — the gold standard for detection quality."))
    story.append(Spacer(1, 10))

    story.append(section_header("The Scoring Formula"))
    story.append(body(
        "Every AI-generated output receives a <b>composite quality score out of 10</b>, "
        "calculated using five weighted factors:"))
    story.append(Spacer(1, 8))

    score_data = [
        [Paragraph("<b>Factor</b>", S['table_header']),
         Paragraph("<b>Weight</b>", S['table_header']),
         Paragraph("<b>What Is Measured</b>", S['table_header']),
         Paragraph("<b>Measured By</b>", S['table_header'])],
        ["A — Accuracy", "35%", "Are all facts grounded in the source? Zero hallucinations?", "LettuceDetect + LUMINA"],
        ["R — Relevance", "20%", "Is this actually a legal article? Confirmed legal domain?", "InLegalBERT confidence"],
        ["C — Completeness", "20%", "Are all 8 schema sections present and fully populated?", "Structural check"],
        ["Cl — Clarity", "15%", "Is the language clear, readable, and well-formatted?", "NLP Readability Index"],
        ["Ct — Citations", "10%", "Are case references (e.g., Bhajan Lal) correctly formatted?", "Regex + Span-level check"],
    ]
    st_table = Table(score_data, colWidths=[105, 50, 220, 120])
    st_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), NAVY), ('TEXTCOLOR', (0,0), (-1,0), WHITE),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'), ('FONTSIZE', (0,0), (-1,-1), 8.5),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [LIGHT_BG, WHITE]),
        ('FONTNAME', (0,1), (-1,-1), 'Helvetica'),
        ('FONTNAME', (0,1), (0,-1), 'Helvetica-Bold'), ('TEXTCOLOR', (0,1), (0,-1), COBALT),
        ('FONTNAME', (1,1), (1,-1), 'Helvetica-Bold'), ('TEXTCOLOR', (1,1), (1,-1), ROYAL),
        ('ALIGN', (1,0), (1,-1), 'CENTER'),
        ('GRID', (0,0), (-1,-1), 0.5, BORDER),
        ('TOPPADDING', (0,0), (-1,-1), 7), ('BOTTOMPADDING', (0,0), (-1,-1), 7),
        ('LEFTPADDING', (0,0), (-1,-1), 8), ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    story.append(st_table)
    story.append(Paragraph("Table 7.1 — QA Scoring Formula: Final Score = (0.35×A) + (0.20×R) + (0.20×C) + (0.15×Cl) + (0.10×Ct)", S['caption']))
    story.append(Spacer(1, 10))

    story.append(section_header("Publishing Tiers Based on Score"))
    story.append(ScoreBar(width=PAGE_W - 80))
    story.append(Paragraph("Figure 7.1 — Automatic Publishing Decision Based on QA Score", S['caption']))
    story.append(Spacer(1, 8))

    tier_data = [
        [Paragraph("<b>Score Range</b>", S['table_header']),
         Paragraph("<b>Action</b>", S['table_header']),
         Paragraph("<b>Meaning</b>", S['table_header'])],
        ["Score > 8.0", "AUTO-PUBLISH", "Highly accurate. Goes straight to database and live website."],
        ["Score 7.0 – 8.0", "HUMAN REVIEW", "Minor issues detected. Sent to admin dashboard for manual check."],
        ["Score < 7.0", "REJECT & RETRY", "Failed validation. Logged, flagged, re-processed with tighter parameters."],
    ]
    tier_table = Table(tier_data, colWidths=[110, 110, 275])
    tier_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), NAVY), ('TEXTCOLOR', (0,0), (-1,0), WHITE),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'), ('FONTSIZE', (0,0), (-1,-1), 9),
        ('BACKGROUND', (0,1), (-1,1), colors.HexColor('#ECFDF5')),
        ('BACKGROUND', (0,2), (-1,2), colors.HexColor('#FFFBEB')),
        ('BACKGROUND', (0,3), (-1,3), colors.HexColor('#FEF2F2')),
        ('TEXTCOLOR', (1,1), (1,1), EMERALD), ('TEXTCOLOR', (1,2), (1,2), GOLD), ('TEXTCOLOR', (1,3), (1,3), CRIMSON),
        ('FONTNAME', (0,1), (-1,-1), 'Helvetica'), ('FONTNAME', (1,1), (1,-1), 'Helvetica-Bold'),
        ('GRID', (0,0), (-1,-1), 0.5, BORDER),
        ('TOPPADDING', (0,0), (-1,-1), 8), ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('LEFTPADDING', (0,0), (-1,-1), 10), ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(tier_table)
    story.append(Paragraph("Table 7.2 — Three-Tier Publishing Decision System", S['caption']))
    story.append(PageBreak())

    # ─── CH 8: SECURITY ───────────────────────────────────────────────────────
    story.extend(chapter_divider("8", "DevSecOps & Self-Healing Security", CRIMSON))
    story.append(body(
        "LexNexHub handles sensitive legal data at scale. A single security breach "
        "could expose confidential case strategies or allow poisoned data into the pipeline. "
        "The security architecture doesn't just defend — it <b>learns, detects, and heals itself</b>."))
    story.append(Spacer(1, 10))

    sec_data = [
        [Paragraph("<b>Threat</b>", S['table_header']),
         Paragraph("<b>Detection Method</b>", S['table_header']),
         Paragraph("<b>Auto-Response</b>", S['table_header'])],
        ["DDoS / Brute Force Attacks", "Token Bucket Algorithm — limits requests per second", "Block + rate-limit the source IP automatically"],
        ["Sophisticated Scraping / Injection", "Isolation Forest ML — detects unusual traffic patterns", "Risk score generated; anomalous session blocked"],
        ["Lateral Attack Paths", "Graph Neural Networks (GNN) — maps infrastructure topology", "Highlight vulnerable paths; alert sent to ops team"],
        ["XSS Payload in Scraped HTML", "LSTM Log Classifier — reads sequential logs for threat signals", "Auto-sanitize; blocklist domain; scale Kubernetes pods"],
        ["Code Changes & Vulnerabilities", "GitHub Actions CI/CD — SAST + unit tests on every commit", "Block deployment if tests fail; no-downtime patching"],
    ]
    sect = Table(sec_data, colWidths=[130, 175, 190])
    sect.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#7F1D1D')),
        ('TEXTCOLOR', (0,0), (-1,0), WHITE),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'), ('FONTSIZE', (0,0), (-1,-1), 8.5),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.HexColor('#FFF1F2'), WHITE]),
        ('FONTNAME', (0,1), (-1,-1), 'Helvetica'),
        ('FONTNAME', (0,1), (0,-1), 'Helvetica-Bold'), ('TEXTCOLOR', (0,1), (0,-1), CRIMSON),
        ('GRID', (0,0), (-1,-1), 0.5, BORDER),
        ('TOPPADDING', (0,0), (-1,-1), 7), ('BOTTOMPADDING', (0,0), (-1,-1), 7),
        ('LEFTPADDING', (0,0), (-1,-1), 8), ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    story.append(sect)
    story.append(Paragraph("Table 8.1 — Security Threats, Detection Methods & Auto-Responses", S['caption']))
    story.append(PageBreak())

    # ─── CH 9: STORAGE ────────────────────────────────────────────────────────
    story.extend(chapter_divider("9", "Storage, MLOps & Infrastructure", colors.HexColor('#0E7490')))
    story.append(body(
        "LexNexHub uses a <b>polyglot persistence</b> strategy — meaning different types "
        "of data are stored in different database systems, each optimized for its specific job. "
        "Think of it like a building: raw materials go to the warehouse, finished products go "
        "to the showroom, and the search catalog stays at the front desk."))
    story.append(Spacer(1, 10))

    storage_data = [
        [Paragraph("<b>Storage System</b>", S['table_header']),
         Paragraph("<b>What It Stores</b>", S['table_header']),
         Paragraph("<b>Why This System</b>", S['table_header']),
         Paragraph("<b>Performance Target</b>", S['table_header'])],
        ["Amazon S3 + Glacier", "Raw HTML, unprocessed JSON scrape results", "Cheap, infinite-scale archival storage", "Long-term cold storage"],
        ["PostgreSQL", "Final 8-point structured output, user accounts, access roles", "Reliable, structured relational data", "Consistent reads/writes"],
        ["ElasticSearch", "All text for full-text search across judgments", "BM25 ranking — returns best matches instantly", "< 50ms query latency"],
        ["Vector Database (FAISS/Milvus)", "AI embeddings (mathematical meaning-vectors)", "Enables semantic search by meaning, not just keywords", "Future: meaning-based search"],
    ]
    stor_table = Table(storage_data, colWidths=[110, 155, 155, 75])
    stor_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#0E4B5C')),
        ('TEXTCOLOR', (0,0), (-1,0), WHITE),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'), ('FONTSIZE', (0,0), (-1,-1), 8.5),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.HexColor('#ECFEFF'), WHITE]),
        ('FONTNAME', (0,1), (-1,-1), 'Helvetica'),
        ('FONTNAME', (0,1), (0,-1), 'Helvetica-Bold'), ('TEXTCOLOR', (0,1), (0,-1), colors.HexColor('#0E7490')),
        ('GRID', (0,0), (-1,-1), 0.5, BORDER),
        ('TOPPADDING', (0,0), (-1,-1), 7), ('BOTTOMPADDING', (0,0), (-1,-1), 7),
        ('LEFTPADDING', (0,0), (-1,-1), 8), ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    story.append(stor_table)
    story.append(Paragraph("Table 9.1 — Polyglot Persistence: Four Database Systems, Four Jobs", S['caption']))
    story.append(Spacer(1, 10))

    story.append(section_header("MLOps: Keeping the AI Up-to-Date"))
    story.append(body(
        "AI models can become outdated as language and legal terminology evolve — a phenomenon "
        "called <b>data drift</b>. For example, as courts shift from IPC to BNS language, "
        "a model trained only on old documents may miss new patterns."))
    story.append(Spacer(1, 6))
    story.append(body(
        "LexNexHub manages this with a continuous retraining loop: every time a human reviewer "
        "corrects an article in the Admin Dashboard, that corrected data is automatically fed "
        "back into the training pipeline via <b>Apache Airflow</b> and <b>MLflow</b>. "
        "The models improve continuously over time with no manual intervention required."))
    story.append(PageBreak())

    # ─── CH 10: COST TABLE ────────────────────────────────────────────────────
    story.extend(chapter_divider("10", "Cost & Model Summary", GOLD))
    story.append(body(
        "One of LexNexHub's most important architectural decisions is the choice of AI models. "
        "By selecting open-source and low-cost alternatives to proprietary models, "
        "the system achieves comparable — or superior — performance at a <b>fraction of the cost</b>."))
    story.append(Spacer(1, 10))

    models_data = [
        [Paragraph("<b>Model</b>", S['table_header']),
         Paragraph("<b>Role in LexNexHub</b>", S['table_header']),
         Paragraph("<b>Cost</b>", S['table_header']),
         Paragraph("<b>Why Chosen</b>", S['table_header'])],
        ["InLegalBERT", "Legal/Non-legal classifier at ingestion gate",
         "FREE\n(Open Source)", "5.4M Indian legal docs training; superior domain accuracy"],
        ["DeepSeek-R1", "Tier 1: Complex reasoning, precedent extraction, court logic",
         "$0.14–$0.55/1M in\n$2.19/1M out", "96% cheaper than OpenAI o1; equivalent performance; CoT reasoning"],
        ["DeepSeek V4", "Large-context general tasks (up to 1M token window)",
         "$0.30/1M in\n$0.50/1M out", "Massive context window for very long documents"],
        ["Gemma-3 27B", "Tier 2: Fast summaries, HTML formatting, structuring",
         "$0.08/1M in\n$0.16/1M out", "Low VRAM; fast inference; excellent quality for formatting tasks"],
        ["Aalap (Mistral 7B)", "Indian legal entity extraction (on-premise option)",
         "FREE\n(Self-hosted)", "Fine-tuned specifically on Indian legal datasets; offline deployment"],
        ["LettuceDetect", "Token-level hallucination detection in QA engine",
         "FREE\n(MIT License)", "30–60 docs/sec; 8K context; outperforms larger models; ModernBERT base"],
        ["LUMINA", "Statistical validation of context vs. memory usage",
         "FREE\n(Open Source)", "AUROC > 0.90; detects when model ignores source material"],
    ]
    model_table = Table(models_data, colWidths=[90, 160, 90, 155])
    model_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), NAVY), ('TEXTCOLOR', (0,0), (-1,0), WHITE),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'), ('FONTSIZE', (0,0), (-1,-1), 8.5),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [LIGHT_BG, WHITE]),
        ('FONTNAME', (0,1), (-1,-1), 'Helvetica'),
        ('FONTNAME', (0,1), (0,-1), 'Helvetica-Bold'), ('TEXTCOLOR', (0,1), (0,-1), COBALT),
        ('FONTNAME', (2,1), (2,-1), 'Helvetica-Bold'),
        ('ALIGN', (2,0), (2,-1), 'CENTER'),
        ('GRID', (0,0), (-1,-1), 0.5, BORDER),
        ('TOPPADDING', (0,0), (-1,-1), 7), ('BOTTOMPADDING', (0,0), (-1,-1), 7),
        ('LEFTPADDING', (0,0), (-1,-1), 8), ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    story.append(model_table)
    story.append(Paragraph("Table 10.1 — Complete Model & Framework Summary", S['caption']))
    story.append(Spacer(1, 14))

    # Full architecture map
    story.append(section_header("Full Architecture Overview"))
    story.append(body("The diagram below shows all seven processing layers from data source to end-user:"))
    story.append(Spacer(1, 8))
    story.append(ArchitectureMap(width=PAGE_W - 80, height=300))
    story.append(Paragraph("Figure 10.1 — Complete LexNexHub Phase 1 Architecture Stack", S['caption']))
    story.append(Spacer(1, 10))

    # Closing
    story.append(rule(COBALT, 2))
    story.append(Spacer(1, 8))
    story.append(Paragraph(
        "<b>LexNexHub Phase 1</b> establishes a fault-tolerant, self-improving AI ecosystem "
        "purpose-built for the Indian legal landscape. By combining domain-specialized AI "
        "models, advanced hallucination prevention, and intelligent cost management, "
        "it delivers trustworthy, structured legal intelligence at scale — while remaining "
        "rigorously aligned with India's evolving judicial framework.",
        ParagraphStyle('closing', fontName='Helvetica', fontSize=11, textColor=COBALT,
                       leading=18, alignment=TA_CENTER, borderPad=10)))
    story.append(Spacer(1, 12))
    story.append(Paragraph(
        "For informational and research purposes only. This system does not constitute "
        "formal, licensed legal advice, nor does it substitute for the professional counsel "
        "of a qualified attorney.",
        S['disclaimer']))

    # ─── BUILD ────────────────────────────────────────────────────────────────
    def first_page(canvas, doc):
        make_cover(canvas, doc)

    def later_pages(canvas, doc):
        make_page(canvas, doc)

    doc.build(story, onFirstPage=first_page, onLaterPages=later_pages)
    print("PDF built successfully!")

build()