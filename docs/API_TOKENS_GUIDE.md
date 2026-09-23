# 🔐 دليل الوصول إلى APIs والتوكنز

> نسخة المستودع من ورقة Google الجديدة: [**«دليل الوصول إلى APIs والتوكنز — Railway · Render · n8n · Supabase»**](https://docs.google.com/spreadsheets/d/1JGmdxE6nzsCDWod2mWvWljCn3hQxRx_2UNdRA7_AEsI/edit)
> القاعدة الذهبية: **التوكن يعيش فقط في متغيرات بيئة المنصة — أبداً في Git أو في أي Prompt ذكاء اصطناعي.**

---

## جدول المفاتيح والتوكنز المطلوب تجهيزها

| # | الخدمة / المنصة | المفتاح / التوكن | الغرض | مكان الاستخراج | اسم متغير البيئة | مكان التخزين الآمن | الصلاحيات | سياسة التدوير | الحالة |
|---|---|---|---|---|---|---|---|---|---|
| 1 | GitHub | Fine-grained PAT أو Deploy Key | سحب المستودع للنشر التلقائي في Render/Railway | github.com → Settings → Developer settings → Fine-grained tokens | `GITHUB_TOKEN` | Render/Railway Variables | `contents:read` فقط على هذا المستودع | 90 يوماً | ⬜ |
| 2 | Render | API Key | إدارة النشر برمجياً (اختياري) | dashboard.render.com → Account Settings → API Keys | `RENDER_API_KEY` | محلي / n8n credential | قراءة+كتابة حساب | 180 يوماً | ⬜ |
| 3 | Railway | `RAILWAY_TOKEN` | نشر وإدارة مشروع n8n عبر CLI/API | railway.com → Account Settings → Tokens | `RAILWAY_TOKEN` | محلي / CI | نطاق الحساب | 180 يوماً | ⬜ |
| 4 | Supabase | Project Ref / URL | تعريف المشروع | dashboard.supabase.com → Project Settings → General | `SUPABASE_URL` | كل الخدمات | عام (غير سري) | — | ⬜ |
| 5 | Supabase | anon key | اتصال العميل/الواجهة (آمن مع تفعيل RLS) | Project Settings → API | `SUPABASE_ANON_KEY` | الواجهة + n8n | **RLS مفعّل إلزامياً** | — | ⬜ |
| 6 | Supabase | 🔴 service_role key | تجاوز RLS — عمليات الخادم فقط | Project Settings → API | `SUPABASE_SERVICE_ROLE_KEY` | n8n/Backend فقط — **ليس في الواجهة أبداً** | كاملة | فوراً عند أي تسريب | ⬜ |
| 7 | Supabase | سلسلة اتصال قاعدة البيانات | اتصال Postgres مباشر (n8n، نسخ احتياطي) | Project Settings → Database → Connection string | `DATABASE_URL` | n8n credentials | SSL إلزامي | تغيير كلمة مرور DB كل 180 يوماً | ⬜ |
| 8 | n8n | 🔴 `N8N_ENCRYPTION_KEY` | تشفير جميع الـ credentials المخزنة | توليد محلي: `openssl rand -hex 32` | `N8N_ENCRYPTION_KEY` | Railway Variables فقط | لا يُشارك إطلاقاً | **لا تغيّره أبداً بدون نسخة احتياطية** (يفقدك كل الـ credentials) | ⬜ |
| 9 | n8n | API Key | إدارة الـ workflows برمجياً | واجهة n8n → Settings → n8n API | `N8N_API_KEY` | محلي / سكربتات الإدارة | قراءة+كتابة workflows | 180 يوماً | ⬜ |
| 10 | Telegram | Bot Token | بوت "رئيس المكتب" — استقبال وإرسال | ‎@BotFather → `/newbot` أو `/token` | `TELEGRAM_BOT_TOKEN` | n8n Variables | البوت فقط + تقييد بـ `TELEGRAM_ALLOWED_CHAT_IDS` | فوراً عند التسريب | 🟡 نشط حالياً (مهمة SYS-BLK-1: إصلاح 502) |
| 11 | Google Cloud | Service Account JSON | قراءة/كتابة ورقة المهام + Drive عبر API | console.cloud.google.com → IAM & Admin → Service Accounts → Keys | `GOOGLE_SERVICE_ACCOUNT_JSON` | n8n credentials | تفعيل Sheets API + Drive API + **مشاركة الورقة مع إيميل الـ SA** | تدوير المفتاح كل 180 يوماً | 🟢 نشط (`personal-ai-agent-sheets@…`) |
| 12 | Google Sheets | Sheet ID | تحديد ورقة المهام | من رابط الورقة نفسه | `SHEET_TASKS_ID` | n8n Variables | قراءة/كتابة حسب الحاجة | — | 🟢 القيمة: `1ZXmC_3_OTYYtXglNMXRQiSWu2rjDDIzoqaK0SQuWcWc` |
| 13 | Gemini | `GEMINI_API_KEY` | شخصية "رئيس المكتب" عبر Gem / API | aistudio.google.com → Get API Key | `GEMINI_API_KEY` | n8n / Backend | الطبقة المجانية كافية للبداية | 180 يوماً | ⬜ |
| 14 | بريد (اختياري) | SMTP | إرسال البريف اليومي بالإيميل | Gmail App Password أو Resend | `SMTP_HOST/USER/PASS` | n8n credentials | إرسال فقط | 180 يوماً | ⬜ اختياري |

---

## 🛡️ القواعد الأمنية الذهبية (غير قابلة للتفاوض)

1. **لا أسرار في Git أبداً** — استخدم `.env` + الـ `.gitignore` المرفق. افحص أي التزام قبل دفعه.
2. **الأسرار في متغيرات المنصة** — Railway Variables / Render Environment Variables — وليس في الكود أو ملفات الإعداد.
3. **مبدأ الامتياز الأدنى** — توكن مستقل لكل خدمة بأضيق صلاحية ممكنة.
4. **التدوير الدوري** — كل 90–180 يوماً، وفوراً عند أي شبهة تسريب.
5. **✅ نُفّذ (2026-09-23):** كانت ورقة «خطة المهام» مشاركة "أي شخص لديه الرابط = محرّر" — خُفّضت إلى «عارض». راجع أي ورقة جديدة قبل مشاركتها.
6. **مفاتيح لا تدخل أي Prompt أو Gem:** `service_role key` و `N8N_ENCRYPTION_KEY` وأي توكن دفع — لا توضع في تعليمات Gemini ولا في ملفات المعرفة إطلاقاً.

---

## ✅ قائمة تحقق سريعة قبل التشغيل

- [ ] إنشاء مشروع Supabase وجلب المفاتيح (بنود 4–7)
- [ ] توليد `N8N_ENCRYPTION_KEY` وحفظه في مكان آمن خارج المستودع (بند 8)
- [ ] إنشاء/تدوير توكن بوت Telegram واختبار الـ Webhook (بند 10 — يغلق SYS-BLK-1)
- [ ] توليد `GEMINI_API_KEY` من AI Studio (بند 13)
- [ ] رفع كل القيم في متغيرات بيئة المنصة المستهدفة
- [x] تخفيف صلاحية مشاركة ورقة المهام — **تم التنفيذ 2026-09-23** (الرابط الآن: عارض فقط)
