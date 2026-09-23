-- ============================================================================
-- Personal AI Agent (Chief of Staff) — Supabase Schema v1
-- ----------------------------------------------------------------------------
-- التنفيذ: dashboard.supabase.com → SQL Editor → New query → الصق → Run
-- هذا المخطط هو البديل الدائم لملفي state.json و audit.jsonl القديمين،
-- ويشمل ترحيل المهام المفتوحة من ورقة «خطة المهام و الانجاز» (بتاريخ 2026-09-23).
-- ============================================================================

create extension if not exists pgcrypto;

-- ----------------------------------------------------------------------------
-- 1) حالة الوكيل (بديل state.json) — مفتاح/قيمة JSON
-- ----------------------------------------------------------------------------
create table if not exists agent_state (
  key        text primary key,
  value      jsonb not null,
  updated_at timestamptz not null default now()
);

-- ----------------------------------------------------------------------------
-- 2) المهام (مرآة عمود الأولويات في ورقة المهام)
-- ----------------------------------------------------------------------------
create table if not exists tasks (
  id          text primary key,
  title       text not null,
  domain      text,                    -- مهني | شخصي | مالي | تقني | ذكاء اصطناعي
  importance  text check (importance in ('عالي','متوسط','منخفض')) default 'متوسط',
  urgency     text check (urgency   in ('عالي','متوسط','منخفض')) default 'متوسط',
  project     text,
  status      text not null default 'open'
              check (status in ('open','in_progress','blocked','waiting','done','closed')),
  next_action text,
  risk        text,
  due_date    date,
  source      text,                    -- المصدر/التبويب في الورقة
  daily_action text,
  created_at  timestamptz not null default now(),
  updated_at  timestamptz not null default now()
);

-- ----------------------------------------------------------------------------
-- 3) سجل التدقيق (بديل audit.jsonl) — للكتابة فقط
-- ----------------------------------------------------------------------------
create table if not exists audit_log (
  id      bigint generated always as identity primary key,
  ts      timestamptz not null default now(),
  actor   text not null,               -- telegram | n8n | gemini | user | system
  action  text not null,
  payload jsonb
);

-- ----------------------------------------------------------------------------
-- 4) التنبيهات المرسلة — لمنع التكرار (قاعدة الحوكمة: منع التكرار)
-- ----------------------------------------------------------------------------
create table if not exists sent_notifications (
  event_key text primary key,
  sent_at   timestamptz not null default now()
);

-- ----------------------------------------------------------------------------
-- Views جاهزة لـ n8n و Gemini
-- ----------------------------------------------------------------------------
create or replace view v_open_tasks as
select * from tasks
where status not in ('done','closed')
order by case importance when 'عالي' then 0 when 'متوسط' then 1 else 2 end,
         due_date asc nulls last;

create or replace view v_overdue_tasks as
select * from tasks
where status not in ('done','closed') and due_date < now()
order by due_date;

-- ----------------------------------------------------------------------------
-- دالة مساعدة لتسجيل التدقيق
-- ----------------------------------------------------------------------------
create or replace function log_audit(p_actor text, p_action text, p_payload jsonb default null)
returns void language sql as $$
  insert into audit_log (actor, action, payload) values (p_actor, p_action, p_payload);
$$;

-- ----------------------------------------------------------------------------
-- الأمان: تفعيل RLS على كل الجداول بدون أي سياسات
-- = الوصول فقط عبر service_role من جهة الخادم (n8n)، ولا وصول من المتصفح
-- ----------------------------------------------------------------------------
alter table agent_state        enable row level security;
alter table tasks              enable row level security;
alter table audit_log          enable row level security;
alter table sent_notifications enable row level security;

-- ----------------------------------------------------------------------------
-- بذور الحالة الأولية (من ورقة المهام — أرقام غير سرية فقط)
-- ----------------------------------------------------------------------------
insert into agent_state (key, value) values
  ('weekly_spending_cap', '{"cap_sar": 2600, "note": "سقف الإنفاق الأسبوعي — مهمة FIN-001"}'),
  ('agent_profile',       '{"name": "Chief of Staff", "platform": "gemini", "autonomy_default": "L1"}'),
  ('sheet_tasks_id',      '{"id": "1ZXmC_3_OTYYtXglNMXRQiSWu2rjDDIzoqaK0SQuWcWc"}')
on conflict (key) do nothing;

-- ----------------------------------------------------------------------------
-- ترحيل المهام المفتوحة من ورقة «خطة المهام و الانجاز»
-- ----------------------------------------------------------------------------
insert into tasks (id, title, domain, importance, urgency, project, status, next_action, risk, due_date, source) values
  ('T-FIN-FILES',   'استكمال الملفات المالية',                          'مهني',               'عالي',   'عالي',   'خطة التعافي المالي',   'in_progress', 'تحديد الخطوة الأولى لضبط العجز المالي',          'حرج (عجز -5,786 ر.س)',        '2026-09-05', 'خطة الإنجاز والمهام'),
  ('PRJ-001',       'Personal AI Agent',                                'ذكاء اصطناعي وأتمتة','عالي',   'عالي',   'Personal AI Agent',  'in_progress', 'اختبار الأوامر الجديدة في Telegram',             'متوسط (تأخر 11 يوماً)',        '2026-09-07', 'Projects'),
  ('T-SAVE',        'تفعيل جانب الادخار',                               'شخصي',               'عالي',   'متوسط',  'الأصول والادخار',    'in_progress', 'تحديد مبلغ مستهدف شهري للاقتطاع',               'مرتفع (مرتبط بالعجز)',        '2026-09-08', 'خطة الإنجاز والمهام'),
  ('T-STATS-APP',   'البرمجة لفكرة مشروع البحث عن الإحصائيين والأطباء','مهني',               'عالي',   'متوسط',  'منصة الاستشارات',    'in_progress', 'تصميم هيكل البيانات وقائمة الأطباء',            'متوسط',                       '2026-09-10', 'خطة الإنجاز والمهام'),
  ('T-LEAN',        'Lean Management',                                  'مهني',               'عالي',   'متوسط',  'التطوير المهني',     'in_progress', 'تطبيق نموذج Fishbone على مشكلة قائمة',          'متوسط',                       '2026-09-06', 'التطوير الشخصي'),
  ('T-FAMILY',      'Family time in the market',                        'شخصي',               'عالي',   'عالي',   'الجانب الأسري',      'in_progress', 'تنسيق وقت التسوق مع الأسرة',                    'منخفض',                       '2026-09-05', 'خطة الإنجاز والمهام'),
  ('SYS-BLK-1',     'معالجة خطأ اتصال تيليجرام HTTP 502',               'تقني / AI',          'عالي',   'عالي',   'Personal AI Agent',  'blocked',     'إعادة تهيئة Webhook ومراجعة السجلات',           'حرج (يعطل استقبال الأوامر)',  '2026-09-04', 'حالة الوكيل'),
  ('FIN-001',       'الالتزام بسقف الإنفاق الأسبوعي (2,600 ر.س)',       'مالي',               'عالي',   'عالي',   'خطة التعافي المالي', 'in_progress', 'متابعة مصاريف المعيشة اليومية دون تجاوز',      'حرج (العجز التراكمي)',        '2026-09-07', 'التحليل المالي المختصر'),
  ('HAB-002',       'بناء الوكلاء والأتمتة',                            'ذكاء اصطناعي',       'عالي',   'متوسط',  'Personal AI Agent',  'in_progress', 'كتابة المتطلبات والنموذج الأولي',               'متوسط',                       '2026-09-08', 'التطوير الشخصي'),
  ('T-HOME-CARE',   'استكمال الملف التعريفي بخدمة الرعاية المنزلية',    'مهني',               'متوسط',  'متوسط',  'خدمات الرعاية',      'open',        'مراجعة مسودة الملف وصياغة نطاق الخدمات',       'متوسط',                       '2026-09-12', 'خطة الإنجاز والمهام')
on conflict (id) do nothing;

select log_audit('system', 'schema_v1_applied', '{"tasks_seeded": 10, "source": "sheet 2026-09-23"}');

-- ============================================================================
-- تحقق سريع بعد التنفيذ:
--   select count(*) from tasks;            -- المتوقع: 10
--   select * from v_overdue_tasks;         -- المهام المتأخرة الآن
-- ============================================================================
