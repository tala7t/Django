"""Build Postman folder 9 with POST/PATCH/DELETE for every dashboard resource."""
import json
from pathlib import Path

BEARER = {
    "type": "bearer",
    "bearer": [{"key": "token", "value": "{{access_token}}", "type": "string"}],
}


def crud_triplet(section: str, name: str, base_path: str, post_body: str, patch_body: str, post_extra=None):
    """base_path without trailing slash, relative to /api/v1/dashboard/"""
    list_url = f"{{{{base_url}}}}/api/v1/dashboard/{base_path}/"
    detail_url = f"{{{{base_url}}}}/api/v1/dashboard/{base_path}/{{{{sample_id}}}}/"
    items = [
        {
            "name": f"{section} — {name} — POST (إضافة)",
            "request": {
                "method": "POST",
                "auth": BEARER,
                "header": [{"key": "Content-Type", "value": "application/json"}],
                "body": {"mode": "raw", "raw": post_body},
                "url": list_url,
                "description": post_extra or "**POST** على قائمة المورد لإنشاء سجل جديد.",
            },
            "response": [],
        },
        {
            "name": f"{section} — {name} — PATCH (تعديل جزئي)",
            "request": {
                "method": "PATCH",
                "auth": BEARER,
                "header": [{"key": "Content-Type", "value": "application/json"}],
                "body": {"mode": "raw", "raw": patch_body},
                "url": detail_url,
                "description": "**PATCH** `{id}/` — مثال حقول صالحة؛ عيّن `sample_id` لمعرّف موجود.",
            },
            "response": [],
        },
        {
            "name": f"{section} — {name} — DELETE (حذف)",
            "request": {
                "method": "DELETE",
                "auth": BEARER,
                "url": detail_url,
                "description": "**DELETE** `{id}/` — حذف السجل.",
            },
            "response": [],
        },
    ]
    # Replace generic PATCH body for resources where we know one field
    return items


def main():
    path = Path(__file__).resolve().parent / "JDU_Backend_API.postman_collection.json"
    data = json.loads(path.read_text(encoding="utf-8"))

    subs = []

    # Core
    subs.append(
        {
            "name": "9.1 Core — CRUD",
            "description": "مسار الأساس: `/api/v1/dashboard/core/`",
            "item": []
            + crud_triplet(
                "Core",
                "universities",
                "core/universities",
                '{\n  "name_ar": "جامعة",\n  "name_en": "University",\n  "location": "المدينة",\n  "email": "info@uni.edu",\n  "phone": "+963..."\n}',
                '{\n  "location": "موقع محدث"\n}',
            )
            + crud_triplet(
                "Core",
                "languages",
                "core/languages",
                '{\n  "code": "ar",\n  "label": "العربية"\n}',
                '{\n  "label": "اللغة العربية"\n}',
            )
            + crud_triplet(
                "Core",
                "social-media",
                "core/social-media",
                '{\n  "university": 1,\n  "platform": "facebook",\n  "url": "https://facebook.com/..."\n}',
                '{\n  "url": "https://facebook.com/page"\n}',
            )
            + crud_triplet(
                "Core",
                "branches",
                "core/branches",
                '{\n  "university": 1,\n  "name": "فرع",\n  "address": "العنوان"\n}',
                '{\n  "name": "اسم فرع محدث"\n}',
            )
            + crud_triplet(
                "Core",
                "pages",
                "core/pages",
                '{\n  "slug": "about-us",\n  "title_ar": "من نحن",\n  "title_en": "About",\n  "content_ar": "...",\n  "content_en": "...",\n  "page_type": "about"\n}',
                '{\n  "title_ar": "عنوان محدث"\n}',
            )
            + crud_triplet(
                "Core",
                "contact-messages",
                "core/contact-messages",
                '{\n  "sender_name": "اسم",\n  "sender_email": "a@b.com",\n  "subject": "موضوع",\n  "message": "نص"\n}',
                '{\n  "status": "read"\n}',
                "يمكن للموظف أيضًا إنشاء رسالة من الداشبورد (نفس الحقول).",
            ),
        }
    )

    subs.append(
        {
            "name": "9.2 Academics — CRUD",
            "description": "`/api/v1/dashboard/academics/`",
            "item": []
            + crud_triplet(
                "Academics",
                "colleges",
                "academics/colleges",
                '{\n  "university": 1,\n  "name_ar": "كلية",\n  "name_en": "College",\n  "description": ""\n}',
                '{\n  "description": "وصف محدث"\n}',
            )
            + crud_triplet(
                "Academics",
                "departments",
                "academics/departments",
                '{\n  "college": 1,\n  "name_ar": "قسم",\n  "name_en": "Department"\n}',
                '{\n  "name_ar": "قسم محدث"\n}',
            )
            + crud_triplet(
                "Academics",
                "programs",
                "academics/programs",
                '{\n  "department": 1,\n  "name_ar": "برنامج",\n  "name_en": "Program",\n  "level": "bachelor"\n}',
                '{\n  "name_ar": "اسم برنامج محدث"\n}',
                "لرفع `study_plan` استخدم multipart على نفس المسار.",
            )
            + crud_triplet(
                "Academics",
                "staff",
                "academics/staff",
                '{\n  "department": 1,\n  "full_name": "د. اسم",\n  "title": "أستاذ",\n  "bio": "...",\n  "email": "p@uni.edu",\n  "staff_type": "Academic"\n}',
                '{\n  "title": "أستاذ محدث"\n}',
                "للصورة `photo` استخدم multipart.",
            )
            + crud_triplet(
                "Academics",
                "research",
                "academics/research",
                '{\n  "staff": 1,\n  "title": "عنوان بحث",\n  "abstract": "ملخص",\n  "published_date": "2026-01-15",\n  "url": "https://..."\n}',
                '{\n  "abstract": "ملخص محدث"\n}',
            ),
        }
    )

    news_article_crud = [
        {
            "name": "News — articles — POST (multipart · صورة إلزامية)",
            "request": {
                "method": "POST",
                "auth": BEARER,
                "body": {
                    "mode": "formdata",
                    "formdata": [
                        {"key": "university", "value": "1", "type": "text"},
                        {"key": "title_ar", "value": "خبر", "type": "text"},
                        {"key": "title_en", "value": "News", "type": "text"},
                        {"key": "content", "value": "نص الخبر", "type": "text"},
                        {"key": "image", "type": "file", "src": [], "description": "إلزامي"},
                    ],
                },
                "url": "{{base_url}}/api/v1/dashboard/news/articles/",
                "description": "**إنشاء خبر:** استخدم `multipart/form-data` مع حقل **`image`** (إلزامي). طلب JSON بدون صورة يُرفض.",
            },
            "response": [],
        },
        {
            "name": "News — articles — PATCH (تعديل نص دون تغيير الصورة)",
            "request": {
                "method": "PATCH",
                "auth": BEARER,
                "header": [{"key": "Content-Type", "value": "application/json"}],
                "body": {"mode": "raw", "raw": '{\n  "title_ar": "عنوان محدث"\n}'},
                "url": "{{base_url}}/api/v1/dashboard/news/articles/{{sample_id}}/",
                "description": "**PATCH** جزئي — لتحديث الصورة أرسل multipart مع حقل `image`.",
            },
            "response": [],
        },
        {
            "name": "News — articles — DELETE",
            "request": {
                "method": "DELETE",
                "auth": BEARER,
                "url": "{{base_url}}/api/v1/dashboard/news/articles/{{sample_id}}/",
                "description": "**DELETE**",
            },
            "response": [],
        },
    ]

    news_event_crud = [
        {
            "name": "News — events — POST (multipart · صورة إلزامية)",
            "request": {
                "method": "POST",
                "auth": BEARER,
                "body": {
                    "mode": "formdata",
                    "formdata": [
                        {"key": "university", "value": "1", "type": "text"},
                        {"key": "title_ar", "value": "فعالية", "type": "text"},
                        {"key": "title_en", "value": "Event", "type": "text"},
                        {"key": "event_date", "value": "2026-06-01T10:00:00Z", "type": "text"},
                        {"key": "location", "value": "قاعة المحاضرات", "type": "text"},
                        {"key": "description", "value": "تفاصيل الفعالية", "type": "text"},
                        {"key": "image", "type": "file", "src": [], "description": "إلزامي"},
                    ],
                },
                "url": "{{base_url}}/api/v1/dashboard/news/events/",
                "description": "**إنشاء فعالية:** `multipart` مع **`image`** إلزامي (أضف ملفًا في Postman).",
            },
            "response": [],
        },
        {
            "name": "News — events — PATCH",
            "request": {
                "method": "PATCH",
                "auth": BEARER,
                "header": [{"key": "Content-Type", "value": "application/json"}],
                "body": {"mode": "raw", "raw": '{\n  "location": "قاعة محدثة"\n}'},
                "url": "{{base_url}}/api/v1/dashboard/news/events/{{sample_id}}/",
                "description": "**PATCH** — تحديث موقع أو نص؛ لصورة جديدة استخدم multipart.",
            },
            "response": [],
        },
        {
            "name": "News — events — DELETE",
            "request": {
                "method": "DELETE",
                "auth": BEARER,
                "url": "{{base_url}}/api/v1/dashboard/news/events/{{sample_id}}/",
                "description": "**DELETE**",
            },
            "response": [],
        },
    ]

    subs.append(
        {
            "name": "9.3 News — CRUD",
            "description": "`/api/v1/dashboard/news/` — **الأخبار والفعاليات:** الإنشاء عبر **multipart** لأن **الصورة إلزامية**.",
            "item": []
            + news_article_crud
            + news_event_crud
            + crud_triplet(
                "News",
                "announcements",
                "news/announcements",
                '{\n  "university": 1,\n  "title": "إعلان",\n  "body": "نص الإعلان"\n}',
                '{\n  "title": "عنوان إعلان محدث"\n}',
            ),
        }
    )

    subs.append(
        {
            "name": "9.4 Careers — CRUD",
            "description": "`/api/v1/dashboard/careers/`",
            "item": []
            + crud_triplet(
                "Careers",
                "postings",
                "careers/postings",
                '{\n  "university": 1,\n  "title": "وظيفة",\n  "job_type": "Full-time",\n  "description": "...",\n  "requirements": "...",\n  "deadline": "2026-12-31",\n  "status": "open"\n}',
                '{\n  "status": "closed"\n}',
            )
            + [
                {
                    "name": "Careers — applications — POST (إضافة + ملف CV)",
                    "request": {
                        "method": "POST",
                        "auth": BEARER,
                        "body": {
                            "mode": "formdata",
                            "formdata": [
                                {"key": "job", "value": "1", "type": "text"},
                                {"key": "applicant_name", "value": "اسم", "type": "text"},
                                {"key": "applicant_email", "value": "e@mail.com", "type": "text"},
                                {"key": "cv", "type": "file", "src": []},
                            ],
                        },
                        "url": "{{base_url}}/api/v1/dashboard/careers/applications/",
                        "description": "**POST** multipart — الحقل `cv` ملف إلزامي في النموذج.",
                    },
                    "response": [],
                },
                {
                    "name": "Careers — applications — PATCH",
                    "request": {
                        "method": "PATCH",
                        "auth": BEARER,
                        "header": [{"key": "Content-Type", "value": "application/json"}],
                        "body": {"mode": "raw", "raw": '{\n  "status": "reviewed"\n}'},
                        "url": "{{base_url}}/api/v1/dashboard/careers/applications/{{sample_id}}/",
                        "description": "**PATCH** حالة الطلب.",
                    },
                    "response": [],
                },
                {
                    "name": "Careers — applications — DELETE",
                    "request": {
                        "method": "DELETE",
                        "auth": BEARER,
                        "url": "{{base_url}}/api/v1/dashboard/careers/applications/{{sample_id}}/",
                        "description": "**DELETE**",
                    },
                    "response": [],
                },
            ],
        }
    )

    subs.append(
        {
            "name": "9.5 Admissions — CRUD",
            "description": "`/api/v1/dashboard/admissions/`",
            "item": []
            + crud_triplet(
                "Admissions",
                "students",
                "admissions/students",
                '{\n  "full_name": "طالب",\n  "email": "unique@mail.com",\n  "national_id": "00000000000",\n  "status": "active"\n}',
                '{\n  "status": "inactive"\n}',
                "البريد والرقم الوطني يجب أن يكونا فريدين.",
            )
            + crud_triplet(
                "Admissions",
                "info (قبول/برنامج)",
                "admissions/info",
                '{\n  "program": 1,\n  "requirements": "...",\n  "procedure": "...",\n  "tuition_fee": "5000.00",\n  "academic_calendar": "..."\n}',
                '{\n  "tuition_fee": "5500.00"\n}',
                "برنامج واحد = سجل قبول واحد (OneToOne).",
            )
            + [
                {
                    "name": "Admissions — applications — POST (JSON أو ملف)",
                    "request": {
                        "method": "POST",
                        "auth": BEARER,
                        "header": [{"key": "Content-Type", "value": "application/json"}],
                        "body": {
                            "mode": "raw",
                            "raw": '{\n  "student": 1,\n  "program": 1,\n  "status": "pending"\n}',
                        },
                        "url": "{{base_url}}/api/v1/dashboard/admissions/applications/",
                        "description": 'لرفع `form_file` استخدم multipart بنفس المسار مع حقول student, program، والملف.',
                    },
                    "response": [],
                },
                {
                    "name": "Admissions — applications — PATCH",
                    "request": {
                        "method": "PATCH",
                        "auth": BEARER,
                        "header": [{"key": "Content-Type", "value": "application/json"}],
                        "body": {"mode": "raw", "raw": '{\n  "status": "accepted"\n}'},
                        "url": "{{base_url}}/api/v1/dashboard/admissions/applications/{{sample_id}}/",
                        "description": "**PATCH**",
                    },
                    "response": [],
                },
                {
                    "name": "Admissions — applications — DELETE",
                    "request": {
                        "method": "DELETE",
                        "auth": BEARER,
                        "url": "{{base_url}}/api/v1/dashboard/admissions/applications/{{sample_id}}/",
                        "description": "**DELETE**",
                    },
                    "response": [],
                },
            ],
        }
    )

    subs.append(
        {
            "name": "9.6 Services — CRUD",
            "description": "`/api/v1/dashboard/services/` — المسار `list` = الخدمات.",
            "item": []
            + crud_triplet(
                "Services",
                "list (خدمات)",
                "services/list",
                '{\n  "name_ar": "خدمة",\n  "name_en": "Service",\n  "service_type": "general",\n  "url": "https://...",\n  "description": "..."\n}',
                '{\n  "description": "وصف محدث"\n}',
            )
            + crud_triplet(
                "Services",
                "library",
                "services/library",
                '{\n  "university": 1,\n  "name": "المكتبة المركزية",\n  "location": "المبنى أ",\n  "access_url": "https://..."\n}',
                '{\n  "location": "مبنى محدث"\n}',
            ),
        }
    )

    folder_9 = {
        "name": "9 — Dashboard CRUD كامل (إضافة · تعديل · حذف)",
        "description": (
            "كل الطلبات تحتاج **JWT** + **`is_staff`**. "
            "لكل مورد في الداشبورد: **POST** على مسار القائمة لإنشاء، **PATCH** و **DELETE** على `{id}/`. "
            "الـ ViewSets كلها `ModelViewSet` في الكود — هذا المجلد يغطي **كل** الموارد."
        ),
        "item": subs,
    }

    items = data["item"]
    idx = next(
        (i for i, x in enumerate(items) if isinstance(x, dict) and str(x.get("name", "")).startswith("9 —")),
        None,
    )
    if idx is not None:
        items[idx] = folder_9
    else:
        items.append(folder_9)

    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    print("OK — folder 9 written")


if __name__ == "__main__":
    main()
