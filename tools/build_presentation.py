#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Builds the migration step-by-step PowerPoint deck (Arabic, RTL).

Usage:  python3 build_presentation.py  [output.pptx]
Dependency: pip install python-pptx
"""
import sys
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
from pptx.oxml.ns import qn

NAVY  = RGBColor(0x0F, 0x2B, 0x46)
TEAL  = RGBColor(0x0E, 0x83, 0x88)
GOLD  = RGBColor(0xE8, 0xA3, 0x3D)
INK   = RGBColor(0x1F, 0x2D, 0x3D)
GRAY  = RGBColor(0x64, 0x74, 0x84)
LIGHT = RGBColor(0xF2, 0xF6, 0xF8)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
RED   = RGBColor(0xC0, 0x39, 0x2B)
GREEN = RGBColor(0x1E, 0x8E, 0x3E)
PURP  = RGBColor(0x5E, 0x35, 0xB1)
FONT = "Segoe UI"

prs = Presentation()
prs.slide_width, prs.slide_height = Inches(13.333), Inches(7.5)
BLANK = prs.slide_layouts[6]

def _rtl(p, align=PP_ALIGN.RIGHT):
    p.alignment = align
    p._p.get_or_add_pPr().set("rtl", "1")

def _font(run, size=16, bold=False, color=INK, name=FONT, italic=False):
    f = run.font
    f.size, f.bold, f.italic, f.name = Pt(size), bold, italic, name
    f.color.rgb = color
    rPr = run._r.get_or_add_rPr()
    cs = rPr.find(qn("a:cs"))
    if cs is None:
        cs = rPr.makeelement(qn("a:cs"), {}); rPr.append(cs)
    cs.set("typeface", name)

def slide_new(bg=WHITE):
    s = prs.slides.add_slide(BLANK)
    r = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
    r.fill.solid(); r.fill.fore_color.rgb = bg
    r.line.fill.background(); r.shadow.inherit = False
    return s

def footer(s, n, dark=False):
    tb = s.shapes.add_textbox(Inches(0.35), Inches(7.02), Inches(12.6), Inches(0.35))
    p = tb.text_frame.paragraphs[0]; _rtl(p, PP_ALIGN.LEFT)
    _font(p.add_run(), 10, False, WHITE if dark else GRAY)
    p.runs[0].text = f"دليل تنفيذ مشروع النقل — 2026   |   {n:02d}"

def title_bar(s, title, subtitle=None, num=0):
    bar = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, Inches(1.02))
    bar.fill.solid(); bar.fill.fore_color.rgb = NAVY
    bar.line.fill.background(); bar.shadow.inherit = False
    acc = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(12.83), 0, Inches(0.5), Inches(1.02))
    acc.fill.solid(); acc.fill.fore_color.rgb = GOLD
    acc.line.fill.background(); acc.shadow.inherit = False
    tb = s.shapes.add_textbox(Inches(0.5), Inches(0.1), Inches(12.2), Inches(0.9))
    tf = tb.text_frame; tf.word_wrap = True
    p = tf.paragraphs[0]; _rtl(p)
    _font(p.add_run(), 26, True, WHITE); p.runs[0].text = title
    if subtitle:
        p2 = tf.add_paragraph(); _rtl(p2)
        _font(p2.add_run(), 12.5, False, RGBColor(0xBF, 0xD4, 0xE0)); p2.runs[0].text = subtitle
    footer(s, num)

def text_box(s, x, y, w, h, lines, anchor="t"):
    tb = s.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = tb.text_frame; tf.word_wrap = True
    tf.vertical_anchor = {"t": MSO_ANCHOR.TOP, "m": MSO_ANCHOR.MIDDLE, "b": MSO_ANCHOR.BOTTOM}[anchor]
    for i, ln in enumerate(lines):
        txt, size, bold, color = ln[0], ln[1], ln[2], ln[3]
        space = ln[4] if len(ln) > 4 else 6
        align = ln[5] if len(ln) > 5 else PP_ALIGN.RIGHT
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        _rtl(p, align); p.space_after = Pt(space)
        _font(p.add_run(), size, bold, color); p.runs[0].text = txt
    return tb

def box(s, x, y, w, h, fill, line_color=None, shape=MSO_SHAPE.ROUNDED_RECTANGLE):
    b = s.shapes.add_shape(shape, Inches(x), Inches(y), Inches(w), Inches(h))
    b.fill.solid(); b.fill.fore_color.rgb = fill
    if line_color is None: b.line.fill.background()
    else: b.line.color.rgb = line_color; b.line.width = Pt(1.2)
    b.shadow.inherit = False
    return b

def box_label(b, text, size=15, color=WHITE, bold=True, sub=None, sub_color=None):
    tf = b.text_frame; tf.word_wrap = True
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    tf.margin_left = tf.margin_right = Inches(0.08)
    tf.margin_top = tf.margin_bottom = Inches(0.03)
    p = tf.paragraphs[0]; _rtl(p, PP_ALIGN.CENTER)
    _font(p.add_run(), size, bold, color); p.runs[0].text = text
    if sub:
        p2 = tf.add_paragraph(); _rtl(p2, PP_ALIGN.CENTER)
        _font(p2.add_run(), size - 4, False, sub_color or RGBColor(0xDD, 0xEE, 0xF2))
        p2.runs[0].text = sub
    return b

def card(s, x, y, w, h, head, head_color, lines, fill=LIGHT, head_fill=None):
    if head_fill:
        hb = box(s, x, y, w, 0.52, head_fill, shape=MSO_SHAPE.RECTANGLE)
        box_label(hb, head, 15, WHITE, True)
        box(s, x, y + 0.52, w, h - 0.52, fill, shape=MSO_SHAPE.RECTANGLE)
    else:
        box(s, x, y, w, h, fill, shape=MSO_SHAPE.ROUNDED_RECTANGLE)
        text_box(s, x + 0.12, y + 0.08, w - 0.24, 0.4, [(head, 15, True, head_color, 2)])
    ty = y + (0.62 if head_fill else 0.5)
    text_box(s, x + 0.16, ty, w - 0.32, h - (0.72 if head_fill else 0.6), lines)

def num_circle(s, x, y, n, color=TEAL):
    c = s.shapes.add_shape(MSO_SHAPE.OVAL, Inches(x), Inches(y), Inches(0.42), Inches(0.42))
    c.fill.solid(); c.fill.fore_color.rgb = color
    c.line.fill.background(); c.shadow.inherit = False
    tf = c.text_frame; tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    p = tf.paragraphs[0]; _rtl(p, PP_ALIGN.CENTER)
    _font(p.add_run(), 15, True, WHITE); p.runs[0].text = str(n)

def step(s, x, y, w, n, title, desc, color=TEAL):
    num_circle(s, x + w - 0.42, y + 0.02, n, color)
    text_box(s, x, y, w - 0.55, 0.85, [(title, 15, True, INK, 1), (desc, 12, False, GRAY, 0)])

def warn_strip(s, text, y=6.15, color=RED):
    b = box(s, 0.5, y, 12.33, 0.62, RGBColor(0xFD, 0xED, 0xEC))
    b.line.color.rgb = color; b.line.width = Pt(1.2)
    box_label(b, text, 13.5, color, True)

def ok_strip(s, text, y=6.15):
    b = box(s, 0.5, y, 12.33, 0.62, RGBColor(0xE8, 0xF5, 0xEA))
    b.line.color.rgb = GREEN; b.line.width = Pt(1.2)
    box_label(b, text, 13.5, GREEN, True)

# 1 — Title
s = slide_new(NAVY)
box(s, 4.67, 2.62, 4.0, 0.045, GOLD, shape=MSO_SHAPE.RECTANGLE)
text_box(s, 1.0, 1.0, 11.33, 1.0, [("منظومة رئيس المكتب الرقمي — Personal AI Agent", 17, False, GOLD, 0, PP_ALIGN.CENTER)])
text_box(s, 1.0, 1.9, 11.33, 1.3, [("دليل تنفيذ مشروع النقل", 48, True, WHITE, 0, PP_ALIGN.CENTER)])
text_box(s, 1.0, 3.0, 11.33, 1.0, [("خطوة بخطوة إلى:  Railway / Render  +  n8n  +  Supabase  +  Gemini", 22, False, RGBColor(0xC9,0xDE,0xEA), 0, PP_ALIGN.CENTER)])
text_box(s, 1.0, 5.9, 11.33, 1.0, [("2026-09-23   |   كل الملفات جاهزة ومفحوصة — هذا العرض للتنفيذ فقط", 14, False, RGBColor(0x8F,0xAC,0xC0), 0, PP_ALIGN.CENTER)])

# 2 — What & Why
s = slide_new()
title_bar(s, "ما هو المشروع ولماذا؟", "من سكربتات بايثون محلية إلى بنية سحابية مستدامة", 2)
card(s, 6.85, 1.35, 5.98, 4.55, "المشكلة في الوضع الحالي", RED, [
    ("• المحرك البرمجي (proactive.py) يعمل على جهاز محدد ويتوقف بإيقافه", 14, False, INK, 9),
    ("• الحالة مبعثرة في ملفات: state.json و audit.jsonl", 14, False, INK, 9),
    ("• عائق حرج مفتوح: خطأ تيليجرام 502 يعطّل استقبال الأوامر (SYS-BLK-1)", 14, False, INK, 9),
    ("• تأخر مشروع الوكيل الشخصي (PRJ-001) أحد عشر يوماً", 14, False, INK, 9),
    ("• خلط الأسرار والحالة في مكان واحد = مخاطرة أمنية", 14, False, INK, 6),
], fill=RGBColor(0xFB,0xF3,0xF2), head_fill=RGBColor(0xD9,0x53,0x4F))
card(s, 0.5, 1.35, 5.98, 4.55, "الهدف من النقل", TEAL, [
    ("• بنية سحابية تعمل أربعاً وعشرين ساعة دون الاعتماد على جهاز", 14, False, INK, 9),
    ("• أتمتة جاهزة عبر n8n بدلاً من كتابة سكربتات مخصصة", 14, False, INK, 9),
    ("• قاعدة بيانات دائمة في Supabase بدل ملفات الحالة", 14, False, INK, 9),
    ("• شخصية الوكيل وتعليماته في Gemini — منفصلة عن كود التشغيل", 14, False, INK, 9),
    ("• أسرار محكومة في متغيرات بيئة المنصات فقط", 14, False, INK, 6),
], fill=RGBColor(0xEF,0xF7,0xF7), head_fill=TEAL)
ok_strip(s, "النتيجة النهائية: وكيل يعمل دائماً، ذاكرة لا تضيع، وأمان مُدار — بدون كتابة كود جديد", y=6.15)

# 3 — Current state
s = slide_new()
title_bar(s, "الوضع الحالي — نتائج تحليل Git وورقة المهام", "تم التحليل بتاريخ 2026-09-23", 3)
card(s, 9.05, 1.35, 3.78, 4.3, "مستودع Git", NAVY, [
    ("• موقع NKT ثابت مئة بالمئة", 13.5, False, INK, 8),
    ("• فحص الأسرار: نظيف تماماً ✅", 13.5, False, INK, 8),
    ("• 22 ملفاً + صور سريرية 25 م.ب", 13.5, False, INK, 8),
    ("• أُضيف .gitignore لحماية الأسرار", 13.5, False, INK, 8),
    ("• جاهز للنشر فوراً", 13.5, True, GREEN, 6),
], head_fill=NAVY)
card(s, 4.78, 1.35, 3.78, 4.3, "ورقة خطة المهام", TEAL, [
    ("• 10 مهام مفتوحة — إنجاز 75%", 13.5, False, INK, 8),
    ("• عبء ديون 78% وعجز −5,786 ر.س", 13.5, False, INK, 8),
    ("• سقف إنفاق أسبوعي: 2,600 ر.س", 13.5, False, INK, 8),
    ("• حساب خدمة يربط الوكيل بالورقة ✅", 13.5, False, INK, 8),
    ("• PRJ-001 متأخر 11 يوماً", 13.5, True, RED, 6),
], head_fill=TEAL)
card(s, 0.5, 1.35, 3.78, 4.3, "الوكيل الذكي", PURP, [
    ("• متصل ومستقر 🟢", 13.5, False, INK, 8),
    ("• 962 محادثة / 1,370 مدخلة", 13.5, False, INK, 8),
    ("• 2 عادة نشطة / 9 مسجلة", 13.5, False, INK, 8),
    ("• 9 عوائق مفتوحة", 13.5, False, INK, 8),
    ("• الأهم: إصلاح خطأ 502", 13.5, True, RED, 6),
], head_fill=PURP)
ok_strip(s, "🔧 إجراء أمني نُفذ: مشاركة ورقة المهام خُفّضت من «محرّر» إلى «عارض» لأي شخص لديه الرابط", y=5.95)

# 4 — Target architecture
s = slide_new()
title_bar(s, "البنية المستهدفة بعد النقل", "كل مكوّن قديم له بديل جديد — لا حاجة لكتابة كود إضافي", 4)
b = box(s, 5.17, 1.25, 3.0, 0.75, GOLD);  box_label(b, "بوت تيليجرام", 15, WHITE, True, "واجهة المستخدم")
box(s, 6.37, 2.05, 0.6, 0.5, GRAY, shape=MSO_SHAPE.UP_DOWN_ARROW)
b = box(s, 4.17, 2.6, 5.0, 1.0, TEAL);   box_label(b, "n8n — محرك الأتمتة", 17, WHITE, True, "على Railway • بديل عن سكربتات بايثون")
box(s, 6.37, 3.65, 0.6, 0.5, GRAY, shape=MSO_SHAPE.UP_DOWN_ARROW)
b = box(s, 4.17, 4.2, 5.0, 1.0, NAVY);   box_label(b, "Supabase — الذاكرة الدائمة", 17, WHITE, True, "بديل عن state.json و audit.jsonl")
box(s, 9.35, 2.85, 0.85, 0.5, GRAY, shape=MSO_SHAPE.LEFT_RIGHT_ARROW)
b = box(s, 10.35, 2.6, 2.5, 1.0, PURP);  box_label(b, "Gemini", 17, WHITE, True, "الشخصية والتعليمات")
b = box(s, 0.5, 2.6, 2.5, 1.0, GREEN);   box_label(b, "Render / Railway", 15, WHITE, True, "موقع NKT الثابت")
text_box(s, 0.5, 5.5, 12.33, 1.3, [
    ("proactive.py ← الفحص الاستباقي في n8n        |        export_for_chat.py ← سياق اليوم من n8n", 13, False, GRAY, 5, PP_ALIGN.CENTER),
    ("state.json ← جدول agent_state        |        الأسرار ← متغيرات بيئة المنصات (وليس في Git أبداً)", 13, False, GRAY, 0, PP_ALIGN.CENTER),
])

# 5 — Roadmap
s = slide_new()
title_bar(s, "خريطة الطريق — أربع مراحل", "الترتيب مهم: كل مرحلة تبني على سابقتها", 5)
ph = [
    ("المرحلة 0", "التحليل والتجهيز", "✅ مكتملة", "2026-09-23", GREEN),
    ("المرحلة 1", "الأساس: Supabase + n8n + تيليجرام", "🟡 بانتظار التنفيذ", "2026-09-24", GOLD),
    ("المرحلة 2", "الأتمتة: تشغيل الـ 4 workflows", "⬜ لم تبدأ", "2026-09-26", GRAY),
    ("المرحلة 3", "الذكاء: Gemini Gem + نشر الموقع", "⬜ لم تبدأ", "2026-09-27", GRAY),
]
x = 9.55
for t, d, st, dt, c in ph:
    ch = box(s, x, 1.9, 3.35, 1.0, NAVY, shape=MSO_SHAPE.CHEVRON)
    box_label(ch, t, 16, WHITE, True)
    text_box(s, x - 0.15, 3.05, 3.5, 1.4, [
        (d, 13.5, True, INK, 4, PP_ALIGN.CENTER),
        (st, 13, True, c, 3, PP_ALIGN.CENTER),
        (dt, 12, False, GRAY, 0, PP_ALIGN.CENTER),
    ])
    x -= 3.15
card(s, 0.5, 4.7, 12.33, 1.55, "قاعدة التقدم", TEAL, [
    ("• الملفات لكل مرحلة جاهزة مئة بالمئة في المستودع — دورك هو التنفيذ على المنصات فقط", 14, False, INK, 6),
    ("• ورقة «متابعة نقل المنظومة — المراحل والخيارات» هي سجل التقدم: حدّث عمود الحالة بعد كل خطوة", 14, False, INK, 4),
], fill=LIGHT, head_fill=TEAL)

# 6 — Phase 1a Supabase
s = slide_new()
title_bar(s, "المرحلة 1أ — إعداد Supabase (الذاكرة الدائمة)", "الوقت المتوقع: 15 دقيقة", 6)
steps = [
    ("أنشئ مشروعاً جديداً", "في dashboard.supabase.com — اختر أقرب منطقة متاحة للخليج"),
    ("افتح SQL Editor ثم New query", "من القائمة الجانبية في لوحة تحكم المشروع"),
    ("الصق ملف المخطط الكامل", "من المستودع:  deploy/supabase_schema.sql"),
    ("اضغط Run", "سينشئ 4 جداول + 2 views + يرحّل مهامك العشر من الورقة تلقائياً"),
    ("تحقق من النتيجة", "نفّذ:  select count(*) from tasks;  — القيمة المتوقعة: 10"),
    ("انسخ المفاتيح إلى دليل التوكنز", "SUPABASE_URL من الإعدادات العامة + service_role من إعدادات API"),
]
y = 1.3
for i, (t, d) in enumerate(steps, 1):
    step(s, 0.7, y, 11.9, i, t, d); y += 0.78
warn_strip(s, "مفتاح service_role سري جداً: يُستخدم في n8n فقط — ولا يدخل أي واجهة أو Prompt أبداً", y=6.15)

# 7 — Phase 1b n8n
s = slide_new()
title_bar(s, "المرحلة 1ب — نشر n8n على Railway (محرك الأتمتة)", "الوقت المتوقع: 15 دقيقة", 7)
steps = [
    ("أنشئ خدمة من قالب n8n الجاهز", "في Railway:  New Project ← Templates ← n8n"),
    ("أضف Volume دائماً", "على المسار  /home/node/.n8n  — يحمي بياناتك عند كل إعادة نشر"),
    ("ولّد مفتاح التشفير", "في الطرفية:  openssl rand -hex 32  ثم ضعه في  N8N_ENCRYPTION_KEY"),
    ("اضبط متغيرات أساسية", "GENERIC_TIMEZONE=Asia/Riyadh  و  N8N_HOST  بنطاق الخدمة و  https"),
    ("أنشئ مفتاح n8n API", "من داخل واجهة n8n:  Settings ← n8n API  (اختياري للإدارة البرمجية)"),
    ("افتح لوحة n8n وأنشئ حساب المشرف", "ثم انتقل لاستيراد الـ workflows في المرحلة 2"),
]
y = 1.3
for i, (t, d) in enumerate(steps, 1):
    step(s, 0.7, y, 11.9, i, t, d); y += 0.78
warn_strip(s, "🔑 احفظ N8N_ENCRYPTION_KEY في مدير كلمات المرور — فقدانه يعني فقدان كل الـ credentials المخزنة", y=6.15)

# 8 — Phase 1c Telegram
s = slide_new()
title_bar(s, "المرحلة 1ج — بوت تيليجرام ومتغيرات البيئة", "الوقت المتوقع: 10 دقائق — يغلق العائق الحرج SYS-BLK-1", 8)
steps = [
    ("دوّر توكن البوت", "راسل  @BotFather  وأرسل  /token  — التوكن الجديد يلغي القديم المسرّب"),
    ("اعرف رقم محادثتك", "راسل  @userinfobot  وانسخ الـ chat id الخاص بك"),
    ("أضف متغيرات تيليجرام في Railway", "TELEGRAM_ALLOWED_CHAT_IDS=رقمك   و   TELEGRAM_ADMIN_CHAT_ID=رقمك"),
    ("اختبر البوت", "أرسل أي رسالة — سيُستخدم في المرحلة 2 مع الـ workflow رقم 01"),
]
y = 1.3
for i, (t, d) in enumerate(steps, 1):
    step(s, 0.7, y, 11.9, i, t, d); y += 0.78
card(s, 0.7, 4.5, 11.9, 1.4, "القاعدة الذهبية للمتغيرات", GOLD, [
    ("كل الأسرار تُوضع في متغيرات بيئة المنصة (Railway Variables) — وليس في أي ملف داخل المستودع.", 14.5, True, INK, 5),
    ("القالب الجاهز لكل الأسماء والقيم المطلوبة: ملف  .env.example  في جذر المستودع + ورقة دليل التوكنز.", 13, False, GRAY, 0),
], fill=RGBColor(0xFD,0xF6,0xE9), head_fill=GOLD)

# 9 — Phase 2 workflows
s = slide_new()
title_bar(s, "المرحلة 2 — الأتمتة: استيراد الـ 4 workflows", "الوقت المتوقع: 20 دقيقة — ملفات جاهزة ومفحوصة برمجياً", 9)
rows = [
    ("الملف", "الوظيفة", "البديل القديم"),
    ("01_telegram_gateway", "رسالة تيليجرام ← جيميناي ← رد (مع قائمة سماح)", "بوت بايثون"),
    ("02_proactive_scan", "كل 20 دقيقة: تنبيه بالمهام المتأخرة — بدون تكرار", "engine/proactive.py"),
    ("03_morning_brief", "البريف الصباحي 🌅 الساعة 6:30 بتوقيت الرياض", "يدوي"),
    ("04_daily_context_export", "سياق اليوم لـ Gemini الساعة 6:00 صباحاً", "engine/export_for_chat.py"),
]
gf = s.shapes.add_table(5, 3, Inches(0.6), Inches(1.35), Inches(12.13), Inches(2.5))
tbl = gf.table
tbl.columns[0].width = Inches(3.6); tbl.columns[1].width = Inches(6.0); tbl.columns[2].width = Inches(2.53)
for r in range(5):
    for c in range(3):
        cell = tbl.cell(r, c)
        cell.fill.solid()
        cell.fill.fore_color.rgb = TEAL if r == 0 else (LIGHT if r % 2 else WHITE)
        tf = cell.text_frame; tf.word_wrap = True
        p = tf.paragraphs[0]; _rtl(p, PP_ALIGN.CENTER if r == 0 or c != 1 else PP_ALIGN.RIGHT)
        _font(p.add_run(), 13.5 if r else 14, r == 0, WHITE if r == 0 else INK)
        p.runs[0].text = rows[r][c]
text_box(s, 0.6, 4.05, 12.13, 2.0, [
    ("خطوات الاستيراد بالترتيب:", 16, True, NAVY, 8),
    ("1)  أنشئ الـ 3 credentials في n8n بالأسماء:  Telegram Bot (Chief of Staff)  /  Supabase Postgres  /  Gemini API Key", 13.5, False, INK, 7),
    ("2)  Workflows ← Import from File ← اختر الملفات الأربعة من مجلد  deploy/n8n_workflows", 13.5, False, INK, 7),
    ("3)  اختبر رقم 02 بزر Execute Workflow — سيصلك تنبيه المتأخرات مرة واحدة ثم يتوقف التكرار تلقائياً", 13.5, False, INK, 7),
    ("4)  فعّل (Activate) الجميع — التفاصيل الكاملة في  deploy/README.md", 13.5, False, INK, 0),
])

# 10 — Phase 3 Gemini
s = slide_new()
title_bar(s, "المرحلة 3 — إنشاء Gemini Gem (شخصية رئيس المكتب)", "الوقت المتوقع: 20 دقيقة", 10)
steps = [
    ("افتح Gemini ثم Gems ثم إنشاء Gem جديد", "أو استخدم AI Studio إذا تفضلت واجهة المطورين"),
    ("الصق التعليمات النظامية", "محتوى ملف  gemini_export/system_instruction.md  كاملاً في حقل التعليمات"),
    ("ارفع ملفات المعرفة (RAG)", "حسب القائمة في  knowledge/README.md — بعد تطبيق قائمة الإزالة أولاً"),
    ("اختبر الـ Gem بسيناريوهات التدريب", "استخدم حالات التقييم: بريف صباحي، قرار مالي، اجتماع ← مهام"),
    ("الروتين اليومي", "الصق «سياق اليوم» الذي يرسله n8n صباحاً في بداية كل محادثة مهمة"),
]
y = 1.3
for i, (t, d) in enumerate(steps, 1):
    step(s, 0.7, y, 11.9, i, t, d, color=PURP); y += 0.78
ok_strip(s, "ما يُرفع إلى Gemini تعليمات سلوكية ومعرفة معقّمة فقط — لا كود، لا أسرار، لا بيانات حقيقية", y=5.7)

# 11 — Security rules
s = slide_new()
title_bar(s, "القواعد الأمنية الذهبية", "غير قابلة للتفاوض — راجعها قبل كل خطوة", 11)
rules = [
    ("لا أسرار في Git أبداً", "استخدم .env مع الـ .gitignore المرفق، وافحص كل التزام قبل دفعه"),
    ("الأسرار في متغيرات المنصة", "Railway Variables وRender Env — وليس في الكود أو ملفات الإعداد"),
    ("الامتياز الأدنى", "توكن مستقل لكل خدمة بأضيق صلاحية ممكنة"),
    ("التدوير الدوري", "كل 90–180 يوماً — وفوراً عند أي شبهة تسريب"),
    ("مفاتيح لا تدخل أي Prompt", "service_role وN8N_ENCRYPTION_KEY وأي توكن دفع — أبداً"),
    ("راجع صلاحيات المشاركة", "لكل ورقة جديدة قبل مشاركتها (طبّقناها على ورقة المهام ✅)"),
]
pos = [(6.85, 1.4), (6.85, 3.0), (6.85, 4.6), (0.5, 1.4), (0.5, 3.0), (0.5, 4.6)]
for i, ((t, d), (px, py)) in enumerate(zip(rules, pos), 1):
    box(s, px, py, 5.98, 1.45, LIGHT)
    num_circle(s, px + 5.45, py + 0.15, i, RED if i == 5 else TEAL)
    text_box(s, px + 0.2, py + 0.12, 5.15, 1.2, [(t, 15.5, True, INK, 3), (d, 12.5, False, GRAY, 0)])

# 12 — Resources
s = slide_new()
title_bar(s, "المتابعة والموارد — أين تجد كل شيء؟", "أربع مراجع تكفيك طوال المشروع", 12)
res = [
    ("📗 ورقة متابعة النقل — المراحل والخيارات", "سجل تقدمك: حدّث عمود «الحالة» في الـ 22 مهمة بعد كل خطوة، واعتمد الخيارات في جدول القرارات", "في Google Drive"),
    ("🔐 ورقة دليل الوصول إلى APIs والتوكنز", "14 مفتاحاً: مكان الاستخراج، اسم المتغير، مكان التخزين، وسياسة التدوير", "في Google Drive"),
    ("PR رقم 1 على GitHub", "كل ملفات النقل جاهزة للمراجعة والدمج", "المستودع: neurokinetic-therapy-suite"),
    ("📁 مجلدات المستودع", "docs/ للأدلة الثلاثة  •  deploy/ لملف الـ SQL والـ workflows  •  gemini_export/ لحزمة جيميناي", "اطلب من الوكيل أي ملف لتفصيله"),
]
y = 1.35
for t, d, loc in res:
    card(s, 0.5, y, 12.33, 1.12, t, NAVY, [(d + "   —   الموقع: " + loc, 13, False, GRAY, 0)], fill=LIGHT)
    y += 1.27

# 13 — Summary
s = slide_new(NAVY)
text_box(s, 1.0, 0.55, 11.33, 0.8, [("الخلاصة — ما تبقى عليك", 32, True, WHITE, 0, PP_ALIGN.CENTER)])
box(s, 5.67, 1.35, 2.0, 0.04, GOLD, shape=MSO_SHAPE.RECTANGLE)
cards13 = [
    ("1", "ادمج PR رقم 1", "زر واحد في صفحة الـ PR — يجعل كل الملفات في الفرع الرئيسي", "دقيقة واحدة"),
    ("2", "أنشئ المستودع الجديد", "أنشئ مستودعاً فارغاً باسم  personal-ai-agent-gemini  وأبلغ الوكيل ليدفع محتواه فوراً", "3 دقائق"),
    ("3", "نفّذ المراحل على المنصات", "اتبع الشرائح 6 ← 10 بالترتيب: سوبابيس ثم n8n ثم تيليجرام ثم الاستيراد ثم جيميناي", "45–60 دقيقة"),
]
x = 8.75
for n, t, d, tm in cards13:
    b = box(s, x, 1.85, 3.9, 3.1, RGBColor(0x17, 0x3A, 0x5C))
    b.line.color.rgb = TEAL; b.line.width = Pt(1.4)
    text_box(s, x + 0.25, 2.05, 3.4, 2.8, [
        (n + "  |  " + t, 17, True, GOLD, 10),
        (d, 13, False, RGBColor(0xD5, 0xE3, 0xEC), 10),
        ("⏱ " + tm, 12.5, True, RGBColor(0x9F, 0xC5, 0xD8), 0),
    ])
    x -= 4.1
text_box(s, 1.0, 5.45, 11.33, 1.2, [
    ("كل الملفات جاهزة ومفحوصة — التنفيذ لم يعد يحتاج كتابة سطر واحد 🚀", 20, True, WHITE, 6, PP_ALIGN.CENTER),
    ("أنجز أي خطوة وأخبر الوكيل: سيحدّث ورقة المتابعة ويكمل ما يترتب عليها فوراً", 14, False, RGBColor(0x9F, 0xC5, 0xD8), 0, PP_ALIGN.CENTER),
])

out = sys.argv[1] if len(sys.argv) > 1 else "migration-guide-step-by-step.pptx"
prs.core_properties.title = "دليل تنفيذ مشروع النقل — خطوة بخطوة"
prs.core_properties.author = "Arena Agent"
prs.save(out)
print("saved:", out, "| slides:", len(prs.slides._sldIdLst))
