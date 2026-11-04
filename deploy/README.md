# 📦 حزمة النشر الجاهزة — Supabase + n8n

## 1) قاعدة البيانات: `supabase_schema.sql`

**التنفيذ:**
1. افتح [dashboard.supabase.com](https://dashboard.supabase.com) → مشروعك → **SQL Editor** → New query.
2. الصق محتوى `supabase_schema.sql` كاملاً → **Run**.
3. تحقق: `select count(*) from tasks;` → المتوقع **10 مهام مرحّلة من ورقة المهام**.

**ماذا ينشئ؟**
| الكائن | الوظيفة |
|---|---|
| `agent_state` | حالة الوكيل (بديل `state.json`) |
| `tasks` | المهام — **مزروعة مسبقاً بمهام الورقة الحالية** |
| `audit_log` | سجل التدقيق (بديل `audit.jsonl`) |
| `sent_notifications` | منع تكرار التنبيهات |
| `v_open_tasks` / `v_overdue_tasks` | Views جاهزة لـ n8n وGemini |
| RLS مفعّل بدون سياسات | الوصول فقط عبر `service_role` من جهة الخادم |

---

## 2) أتمتة n8n: `n8n_workflows/`

**الاستيراد:** واجهة n8n → **Workflows → ⋯ → Import from File** → اختر كل ملف بالترتيب.

| الملف | الوظيفة | البديل القديم |
|---|---|---|
| `01_telegram_gateway.json` | استقبال رسائل تيليجرام → Gemini → رد (مع قائمة سماح) | بوت بايثون |
| `02_proactive_scan.json` | كل 20 دقيقة: تنبيه بالمهام المتأخرة (بدون تكرار) | `engine/proactive.py` |
| `03_morning_brief.json` | 6:30 صباحاً: البريف الصباحي 🌅 | يدوي |
| `04_daily_context_export.json` | 6:00 صباحاً: سياق اليوم للصقه في Gemini | `engine/export_for_chat.py` |

### بعد الاستيراد، جهّز 3 أشياء في كل ملف:

**أ) الـ Credentials (أنشئها مرة واحدة في n8n وبنفس الأسماء):**
| الاسم في الـ Workflow | النوع | المحتوى |
|---|---|---|
| `Telegram Bot (Chief of Staff)` | Telegram API | البوت توكن من @BotFather |
| `Supabase Postgres` | Postgres | من Supabase: Project Settings → Database → Connection string (فعّل **SSL**) |
| `Gemini API Key (x-goog-api-key)` | Header Auth | Header: `x-goog-api-key` ← القيمة: `GEMINI_API_KEY` |

**ب) متغيرات بيئة n8n (Railway Variables):**
```
TELEGRAM_ALLOWED_CHAT_IDS=رقم-محادثتك-فقط
TELEGRAM_ADMIN_CHAT_ID=رقم-محادثتك
GENERIC_TIMEZONE=Asia/Riyadh
```
> للحصول على رقم محادثتك: راسل بوت `@userinfobot`.

**ج) فعّل (Activate) كل الـ workflows بعد اختبارها بـ Execute Workflow.**

---

## 3) تسلسل الاختبار المقترح

1. نفّذ `supabase_schema.sql` وتحقق من المهام المزروعة.
2. استورد `02` واضغط **Execute Workflow** → يجب أن يصلك تنبيه بالمهام المتأخرة العشر (ثم يتوقف التكرار تلقائياً بسبب `sent_notifications`).
3. استورد `03` و`04` واختبرهما يدوياً قبل تفعيل الجدولة.
4. استورد `01` أخيراً — فهو يحتاج كل المفاتيح جاهزة، واختبره برسالة من حسابك.
