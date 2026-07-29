const C='bcu12m-v2';
self.addEventListener('install',e=>{e.waitUntil(caches.open(C).then(c=>c.addAll(['./','./index.html'])));self.skipWaiting()});
self.addEventListener('activate',e=>{e.waitUntil(caches.keys().then(ks=>Promise.all(ks.filter(k=>k!==C).map(k=>caches.delete(k)))));self.clients.claim()});
self.addEventListener('fetch',e=>{e.respondWith(caches.match(e.request).then(r=>r||fetch(e.request).then(n=>{if(e.request.method==='GET'&&n.ok){const cl=n.clone();caches.open(C).then(c=>c.put(e.request,cl))}return n}).catch(()=>caches.match('./index.html'))))});
