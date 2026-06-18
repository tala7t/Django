"""One-off script to insert quick-guide folder into Postman collection. Run: python postman/_update_postman_guide.py"""
import json
from pathlib import Path

path = Path(__file__).resolve().parent / "JDU_Backend_API.postman_collection.json"
data = json.loads(path.read_text(encoding="utf-8"))

bearer = {
    "type": "bearer",
    "bearer": [{"key": "token", "value": "{{access_token}}", "type": "string"}],
}


def req(name, method, url, desc, body=None, headers=None):
    r = {"method": method, "auth": bearer, "url": url, "description": desc}
    if headers:
        r["header"] = headers
    if body:
        r["body"] = body
    return {"name": name, "request": r, "response": []}


quick_guide = {
    "name": "0 — دليل سريع (بحث · ترقيم · إضافة خبر)",
    "description": (
        "**ابدأ من هنا.** إضافة خبر، الترقيم (pagination)، البحث (search)، والفلترة. "
        "في طلبات **GET** افتح تبويب **Params** لرؤية كل المعاملات.\n\n"
        "**مهم:** نفّذ أولًا مجلد «1 — المصادقة» وانسخ `access` إلى المتغير `access_token`."
    ),
    "item": [
        req(
            "⭐ إضافة خبر — POST (JSON)",
            "POST",
            "{{base_url}}/api/v1/dashboard/news/articles/",
            "**إنشاء خبر جديد.** Body: JSON. حقول: `university` (رقم)، `title_ar`, `title_en`, `content`.",
            headers=[{"key": "Content-Type", "value": "application/json"}],
            body={
                "mode": "raw",
                "raw": (
                    "{\n"
                    '  "university": 1,\n'
                    '  "title_ar": "خبر تجريبي",\n'
                    '  "title_en": "Sample news",\n'
                    '  "content": "نص الخبر الكامل هنا."\n'
                    "}"
                ),
            },
        ),
        req(
            "⭐ إضافة خبر — POST (صورة multipart)",
            "POST",
            "{{base_url}}/api/v1/dashboard/news/articles/",
            "form-data: نص + ملف `image` (اختياري إن وُجدت صورة).",
            body={
                "mode": "formdata",
                "formdata": [
                    {"key": "university", "value": "1", "type": "text"},
                    {"key": "title_ar", "value": "خبر مع صورة", "type": "text"},
                    {"key": "title_en", "value": "News with image", "type": "text"},
                    {"key": "content", "value": "النص...", "type": "text"},
                    {"key": "image", "type": "file", "src": []},
                ],
            },
        ),
        req(
            "ترقيم (pagination) — page + page_size",
            "GET",
            {
                "raw": "{{base_url}}/api/v1/dashboard/news/articles/?page=2&page_size=10&ordering=-publish_date",
                "query": [
                    {"key": "page", "value": "2", "description": "رقم الصفحة"},
                    {
                        "key": "page_size",
                        "value": "10",
                        "description": "عدد العناصر (افتراضي السيرفر 20، أقصى 100)",
                    },
                    {
                        "key": "ordering",
                        "value": "-publish_date",
                        "description": "فرز تنازلي حسب تاريخ النشر",
                    },
                ],
            },
            "**الرد:** `count`, `next`, `previous`, `results`.",
        ),
        req(
            "بحث (search) في العنوان والمحتوى",
            "GET",
            {
                "raw": "{{base_url}}/api/v1/dashboard/news/articles/?search=مؤتمر&page=1",
                "query": [
                    {
                        "key": "search",
                        "value": "مؤتمر",
                        "description": "يبحث في title_ar, title_en, content",
                    },
                    {"key": "page", "value": "1"},
                ],
            },
            "غيّر قيمة **search** كما تريد.",
        ),
        req(
            "فلترة — جامعة + تاريخ النشر",
            "GET",
            {
                "raw": "{{base_url}}/api/v1/dashboard/news/articles/?university=1&publish_date_from=2026-01-01&publish_date_to=2026-12-31",
                "query": [
                    {"key": "university", "value": "1", "description": "معرّف الجامعة"},
                    {"key": "publish_date_from", "value": "2026-01-01", "description": "YYYY-MM-DD"},
                    {"key": "publish_date_to", "value": "2026-12-31", "description": "YYYY-MM-DD"},
                ],
            },
            "يمكن الجمع مع search و page في نفس الطلب.",
        ),
        req(
            "تعديل خبر — PATCH",
            "PATCH",
            "{{base_url}}/api/v1/dashboard/news/articles/{{sample_id}}/",
            "حدّث `sample_id` بمعرّف حقيقي من القائمة.",
            headers=[{"key": "Content-Type", "value": "application/json"}],
            body={"mode": "raw", "raw": '{\n  "title_ar": "عنوان بعد التعديل"\n}'},
        ),
        req(
            "حذف خبر — DELETE",
            "DELETE",
            "{{base_url}}/api/v1/dashboard/news/articles/{{sample_id}}/",
            "احذف بالمعرف.",
        ),
        {
            "name": "📖 مرجع: باراميترات أي قائمة في الداشبورد",
            "request": {
                "method": "GET",
                "header": [],
                "url": "{{base_url}}/api/v1/dashboard/news/articles/",
                "description": (
                    "**تنطبق على أغلب مسارات GET تحت** `/api/v1/dashboard/...`\n\n"
                    "| المعامل | المعنى |\n"
                    "|---------|--------|\n"
                    "| `page` | رقم الصفحة |\n"
                    "| `page_size` | حجم الصفحة (حتى 100) |\n"
                    "| `search` | بحث (الحقول تختلف حسب المورد) |\n"
                    "| `ordering` | فرز، مثل `-publish_date` |\n\n"
                    "فلاتر إضافية حسب الجدول (مثل `university`, `publish_date_from`). "
                    "تفاصيلها في مجلدات **8.1–8.6** أو في `filters.py` بالمشروع."
                ),
            },
            "response": [],
        },
    ],
}

items = data["item"]
# Replace or insert folder 0
idx = next(
    (i for i, x in enumerate(items) if isinstance(x, dict) and str(x.get("name", "")).startswith("0 —")),
    None,
)
if idx is not None:
    items[idx] = quick_guide
else:
    items.insert(0, quick_guide)

prefix = "**→ للداشبورد:** افتح أولًا المجلد **«0 — دليل سريع»** (إضافة خبر، pagination، search).\n\n"
desc = data["info"]["description"]
if prefix.strip() not in desc:
    data["info"]["description"] = prefix + desc

path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
print("Updated:", path)
