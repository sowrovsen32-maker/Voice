# VoxFree TTS — ফ্রি নিউরাল ভয়েস স্টুডিও

Edge TTS-এর ফ্রি নিউরাল কণ্ঠ (বাংলা / হিন্দি / ইংরেজি, ছেলে-মেয়ে, দেশভিত্তিক) দিয়ে
স্ক্রিপ্ট → ভয়েস। কোনো API কী লাগে না, কোনো টাকা লাগে না।

## ফাইল
- `index.html` — পুরো অ্যাপ (এক ফাইল)। HopWeb/Chrome-এ খুলুন।
- `server/app.py` — ফ্রি backend (edge-tts proxy)।
- `server/requirements.txt`, `server/Dockerfile`

## Backend চালু করার ৩টি উপায়

### A) নিজের কম্পিউটার / VPS
pip install -r server/requirements.txt
uvicorn app:app --host 0.0.0.0 --port 8000 --app-dir server
→ অ্যাপে URL: http://আইপি:8000

### B) Render (ফ্রি web service)
- New → Web Service → এই GitHub রিপো কানেক্ট করুন
- Root Directory: server
- Build Command: pip install -r requirements.txt
- Start Command: uvicorn app:app --host 0.0.0.0 --port $PORT

### C) Hugging Face Spaces (ফ্রি, Docker)
- New Space → SDK: Docker → `server/` ফোল্ডারের ফাইলগুলো আপলোড করুন
- URL হবে: https://<user>-<space>.hf.space

### D) কোড ছাড়াই (রেডিমেড Cloudflare Worker)
- https://github.com/DIYgod/cloudflare-edge-tts ডিপ্লয় করুন (ফ্রি প্ল্যানে দিনে ১,০০,০০০ রিকোয়েস্ট)
- পাওয়া URL অ্যাপে বসান। Worker-এ CORS হেডার না থাকলে ব্রাউজার ব্লক করতে পারে —
  `Access-Control-Allow-Origin: *` যোগ করে নিন।

## গুরুত্বপূর্ণ
- ২০২৬-১০-১০ থেকে Microsoft পুরনো টোকেন রিজেক্ট করে (HTTP 403)। তাই edge-tts আপডেট রাখুন:
  `pip install -U edge-tts` (৭.৩+ লাইনে নতুন v2 টোকেন আছে)।
- ফ্রি হোস্টের লিমিট/শর্ত সময়ে সময়ে বদলায় — ডিপ্লয়ের আগে নিজে দেখে নিন।
- এই টুল Microsoft-এর অনানুষ্ঠানিক এন্ডপয়েন্ট ব্যবহার করে; বাণিজ্যিক বড় কাজে নিজের ঝুঁকি আছে।
