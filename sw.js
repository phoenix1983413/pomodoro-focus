/* ============================================================
   番茄工作钟 · Service Worker
   - 离线可用（核心资产 cache-first）
   - HTML 用 network-first，确保更新最快生效
   - 其余请求 stale-while-revalidate
   ============================================================ */
const VERSION = "pomodoro-focus-v2.1.0";
const CORE = [
  "./",
  "./index.html",
  "./manifest.json",
  "./icons/icon-192.png",
  "./icons/icon-512.png",
  "./icons/apple-touch-icon.png"
];

self.addEventListener("install", (event) => {
  event.waitUntil(
    caches.open(VERSION).then((cache) => cache.addAll(CORE)).then(() => self.skipWaiting())
  );
});

self.addEventListener("activate", (event) => {
  event.waitUntil(
    caches.keys().then((keys) =>
      Promise.all(keys.filter((k) => k !== VERSION).map((k) => caches.delete(k)))
    ).then(() => self.clients.claim())
  );
});

self.addEventListener("fetch", (event) => {
  const req = event.request;
  if (req.method !== "GET") return;

  const url = new URL(req.url);
  // 仅处理同源
  if (url.origin !== self.location.origin) return;

  // HTML 文档：network-first，拿到后回填缓存
  if (req.mode === "navigate" || (req.headers.get("accept") || "").includes("text/html")){
    event.respondWith(
      fetch(req).then((res) => {
        const copy = res.clone();
        caches.open(VERSION).then((c) => c.put(req, copy));
        return res;
      }).catch(() => caches.match("./index.html").then((r) => r || new Response("Offline", { status: 503 })))
    );
    return;
  }

  // 其余静态资源：cache-first，回退网络
  event.respondWith(
    caches.match(req).then((cached) => {
      if (cached) return cached;
      return fetch(req).then((res) => {
        if (res && res.ok){
          const copy = res.clone();
          caches.open(VERSION).then((c) => c.put(req, copy));
        }
        return res;
      }).catch(() => {
        // 图标缺失时给一个 1x1 透明 PNG，避免报错
        if (req.destination === "image"){
          return new Response(new Uint8Array([0,0,0,0,0,0,0,0]), { headers: { "Content-Type": "image/png" } });
        }
        return new Response("Offline", { status: 503 });
      });
    })
  );
});

// 监听客户端消息，强制刷新缓存
self.addEventListener("message", (event) => {
  if (event.data === "SKIP_WAITING") self.skipWaiting();
});
