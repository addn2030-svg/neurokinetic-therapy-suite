# 🚀 خريطة النقل الكاملة — Railway / Render + n8n + Supabase + Gemini

> الهدف: تشغيل منظومة **رئيس المكتب الرقمي (Chief of Staff)** على بنية حديثة وسليمة،
> مع بقاء هذا المستودع (موقع NKT التعليمي) منشوراً كموقع ثابت.

---

## 1) البنية المستهدفة

```
┌──────────────────────────────────────────────────────────────────┐
│                    البنية الجديدة بعد النقل                        │
├──────────────────────────────────────────────────────────────────┤
│                                                                  │
│  [Render أو Railway]        [Railway — حاوية Docker]              │
│   موقع NKT الثابت  ────────►  n8n (محرك الأتمتة)                   │
│   (هذا المستودع)             │  • بديل عن engine/proactive.py    │
│                                │  • Webhook بوت تيليجرام           │
│                                │  • جدولة البريف الصباحي (Cron)     │
│                                ▼                                  │
│  [Supabase]              [Gemini Gem / API]                      │
│   • Postgres: state       • System Instruction                   │
│     بدل state.json          (gemini_export/system_instruction.md)│
│   • جدول audit_log        • ملفات المعرفة (RAG)                   │
│     بدل audit.jsonl       • سياق ديناميكي يومي من n8n             │
│                                ▲                                  │
│                                │                                  │
│                          [بوت Telegram]  ← واجهة المستخدم          │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

## 2) جدول الإحلال: القديم ➜ الجديد

| المكوّن القديم | البديل الجديد | أين يعمل |
|---|---|---|
| `engine/proactive.py` (فحص دوري وتنبيهات) | n8n Workflow بجدولة Cron كل 15–30 دقيقة | Railway/Render (Docker) |
| `engine/export_for_chat.py` (تصدير السياق) | n8n Workflow يومي 6:30 صباحاً يقرأ Supabase ويبني ملخص السياق | n8n |
| `state.json` | جدول `agent_state` في Supabase (صف واحد لكل مفتاح أو JSONB) | Supabase Postgres |
| `audit.jsonl` | جدول `audit_log` (append-only) | Supabase Postgres |
| الأسرار في ملفات/بيئة محلية | متغيرات بيئة المنصة (انظر `docs/API_TOKENS_GUIDE.md`) | Railway/Render |
| كود الشخصية والسلوك | **تعليمات سلوكية** في Gemini (لا يُرفع الكود نفسه) | Gemini Gem |

---

## 3) نشر موقع NKT الثابت (هذا المستودع)

### الخيار الموصى به: Render (مجاني، بدون خادم)
1. اربط المستودع: Render → **New → Blueprint** → اختر `neurokinetic-therapy-suite` (يقرأ `render.yaml` تلقائياً).
2. أو يدوياً: **New → Static Site** → Build Command فارغ → Publish Directory `.`
3. أضف `GITHUB_TOKEN`/Deploy Key في إعدادات الحساب إن كان المستودع خاصاً.

### البديل: Railway
1. New Project → Deploy from GitHub repo → يكتشف `railway.json` ويشغّل `python server.py`.
2. المتغير الوحيد المطلوب: `PORT` (يحقنه Railway تلقائياً).

> **متى تختار أياً منهما؟** الموقع الثابت → Render (أسهل ومجاني). الأحمال الدائمة مثل n8n → Railway (دعم Docker + volumes أفضل).

---

## 4) نشر n8n (محرك الأتمتة)

### على Railway (موصى به)
1. أنشئ مشروعاً جديداً من قالب **n8n** الجاهز في Railway.
2. أضف **Volume** على المسار `/home/node/.n8n` (يحفظ قاعدة البيانات المحلية والـ credentials).
3. المتغيرات الأساسية:

| المتغير | القيمة |
|---|---|
| `N8N_ENCRYPTION_KEY` | ناتج `openssl rand -hex 32` — **احفظه في مدير كلمات مرور** |
| `N8N_HOST` / `N8N_PROTOCOL` | نطاق Railway + `https` |
| `WEBHOOK_URL` | `https://نطاقك/` (ضروري لعمل بوت تيليجرام) |
| `GENERIC_TIMEZONE` | `Asia/Riyadh` |
| `DB_TYPE` (اختياري متقدم) | `postgresdb` + `DATABASE_URL` من Supabase لجعل n8n نفسه بلا حالة |

4. فعّل **n8n API** من الإعدادات وأنشئ `N8N_API_KEY`.
5. اربط الـ credentials داخل n8n: Telegram Bot، Google Service Account، Supabase، Gemini.

### Workflows الجاهزة للبناء — 📦 **متوفرة الآن كملفات JSON جاهزة للاستيراد في `deploy/n8n_workflows/`** (التعليمات في `deploy/README.md`)، وتعادل محركات بايثون القديمة:
| الـ Workflow | الزناد | الوظيفة |
|---|---|---|
| `telegram-webhook` | Webhook POST | استقبال أوامر المستخدم → توجيهها إلى Gemini → الرد (يغلق SYS-BLK-1 بعد النشر) |
| `proactive-scan` | Cron كل 20 دقيقة | فحص المهام المتأخرة في ورقة المهام/Supabase → تنبيه تيليجرام (بدون تكرار: سجل المعرّفات المرسلة في `audit_log`) |
| `morning-brief` | Cron 6:30 صباحاً | بناء البريف الصباحي من السياق وإرساله لتيليجرام/الإيميل |
| `daily-context-export` | Cron 6:00 صباحاً | تصدير سياق اليوم (مهام مفتوحة + متأخرات) كملف/رسالة تُطعم لـ Gemini |

---

## 5) إعداد Supabase (الذاكرة الدائمة)

1. أنشئ مشروعاً (اختر أقرب منطقة، مثلاً `me-central-1` إن توفرت).
2. من SQL Editor نفّذ الملف الجاهز **`deploy/supabase_schema.sql`** — يتضمن الجداول الأربعة + الـ Views + دالة التدقيق + **ترحيل مهام ورقة المهام الحالية (10 مهام مزروعة مسبقاً)**. المخطط للاطلاع:

```sql
-- حالة الوكيل (بديل state.json)
create table agent_state (
  key text primary key,
  value jsonb not null,
  updated_at timestamptz default now()
);

-- سجل التدقيق (بديل audit.jsonl)
create table audit_log (
  id bigint generated always as identity primary key,
  ts timestamptz default now(),
  actor text,          -- 'telegram' | 'n8n' | 'gemini' | 'user'
  action text,
  payload jsonb
);

-- مهام/تنبيهات سبق إرسالها لمنع التكرار
create table sent_notifications (
  event_key text primary key,
  sent_at timestamptz default now()
);
```

3. فعّل **RLS** على الجداول وسياسة وصول عبر `service_role` فقط من جهة الخادم.
4. خزّن `SUPABASE_URL` + `SUPABASE_SERVICE_ROLE_KEY` في متغيرات n8n.

---

## 6) إعداد Gemini (شخصية رئيس المكتب)

البنية جاهزة في مجلد **`gemini_export/`** بهذا المستودع:

```
gemini_export/
├── README.md                # خطوات الاستيراد في Gemini
├── system_instruction.md    # ✅ الرسالة/التعليمات النظامية الجاهزة
├── removal_checklist.md     # ✅ ما يجب إزالته قبل الرفع (الأسرار/الكود/البيانات)
└── knowledge/README.md      # قائمة ملفات المهارات التي تُرفع كـ RAG
```

**الخطوات:**
1. افتح Gemini → **Gems → New Gem** (أو AI Studio).
2. الصق محتوى `gemini_export/system_instruction.md` في حقل System Instructions.
3. ارفع ملفات المهارات (`clinical-intelligence.md`, `negotiation.md`, …) كملفات معرفة حسب `knowledge/README.md`.
4. اختبر الـ Gem بحالات `training/rcjy-chief-of-staff-scenarios.md` كحالات تقييم.
5. السياق اليومي الديناميكي (المهام المفتوحة/المتأخرات) يرسله لك n8n صباحاً لتلصقه، أو يُمرر عبر API.

> **المستودع الجديد:** حسب خطتك، انقل مجلد `gemini_export/` لاحقاً إلى مستودع مستقل باسم `personal-ai-agent-gemini` لفصل الـ Prompts عن كود التشغيل.

---

## 7) تسلسل التنفيذ المقترح (3 مراحل)

**المرحلة 1 — الأساس (يوم 1):**
مفاتيح Supabase + جداوله ← نشر n8n على Railway ← متغيرات البيئة ← اختبار اتصال تيليجرام (يغلق SYS-BLK-1).

**المرحلة 2 — الأتمتة (يوم 2–3):**
بناء الـ Workflows الأربعة ← ترحيل بيانات `state.json` إلى `agent_state` ← إيقاف محركات بايثون القديمة تدريجياً.

**المرحلة 3 — الذكاء (يوم 3–4):**
إنشاء Gemini Gem بالتعليمات وملفات المعرفة ← ربط ردود الـ Workflow بـ Gemini API ← اختبارات السيناريوهات ← نشر موقع NKT الثابت على Render.

---

## 8) مراجع سريعة من داخل المستودع
- 📗 لوحة متابعة النقل (المراحل + المهام + الخيارات): [ورقة جوجل](https://docs.google.com/spreadsheets/d/1XACtIdLXdz7eNM0bjeMns575gXbmXLALZtSp78nva3c/edit)
- تحليل الوضع الحالي: `docs/ANALYSIS.md`
- جدول التوكنز الكامل: `docs/API_TOKENS_GUIDE.md` + ورقة Google الجديدة
- قالب متغيرات البيئة: `.env.example`
- إعداد Render: `render.yaml` | إعداد Railway: `railway.json` + `server.py`
