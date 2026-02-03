// Service Worker para EBSERH TI Study App
const CACHE_NAME = 'ebserh-ti-study-v1.0.0';
const RUNTIME_CACHE = 'ebserh-ti-runtime-v1.0.0';

// Assets para cache estático
const STATIC_ASSETS = [
  '/',
  '/static/css/bootstrap.min.css',
  '/static/js/bootstrap.bundle.min.js',
  '/static/fontawesome/css/all.min.css',
  '/static/fontawesome/webfonts/fa-solid-900.woff2',
  '/static/fontawesome/webfonts/fa-regular-400.woff2',
  '/static/fontawesome/webfonts/fa-brands-400.woff2',
  '/manifest.json',
  '/static/icons/icon-192x192.png',
  '/static/icons/icon-512x512.png'
];

// Páginas para cache
const PAGES_TO_CACHE = [
  '/',
  '/questoes',
  '/plano',
  '/simulado',
  '/desempenho',
  '/admin'
];

// Instalação do Service Worker
self.addEventListener('install', event => {
  console.log('[SW] Instalando Service Worker...');
  
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => {
        console.log('[SW] Cacheando assets estáticos...');
        return cache.addAll(STATIC_ASSETS);
      })
      .then(() => {
        console.log('[SW] Instalação concluída');
        return self.skipWaiting();
      })
      .catch(error => {
        console.error('[SW] Erro na instalação:', error);
      })
  );
});

// Ativação do Service Worker
self.addEventListener('activate', event => {
  console.log('[SW] Ativando Service Worker...');
  
  event.waitUntil(
    caches.keys()
      .then(cacheNames => {
        return Promise.all(
          cacheNames.map(cacheName => {
            if (cacheName !== CACHE_NAME && cacheName !== RUNTIME_CACHE) {
              console.log('[SW] Removendo cache antigo:', cacheName);
              return caches.delete(cacheName);
            }
          })
        );
      })
      .then(() => {
        console.log('[SW] Ativação concluída');
        return self.clients.claim();
      })
  );
});

// Estratégia de cache: Cache First para assets estáticos
self.addEventListener('fetch', event => {
  const request = event.request;
  const url = new URL(request.url);
  
  // Ignorar requisições Chrome Extension
  if (url.protocol === 'chrome-extension:') {
    return;
  }
  
  // Estratégia para assets estáticos (Cache First)
  if (STATIC_ASSETS.some(asset => request.url.includes(asset)) || 
      request.url.includes('/static/') ||
      request.destination === 'script' ||
      request.destination === 'style' ||
      request.destination === 'image') {
    
    event.respondWith(
      caches.match(request)
        .then(response => {
          if (response) {
            return response;
          }
          
          return fetch(request)
            .then(response => {
              if (!response || response.status !== 200 || response.type !== 'basic') {
                return response;
              }
              
              const responseToCache = response.clone();
              caches.open(CACHE_NAME)
                .then(cache => {
                  cache.put(request, responseToCache);
                });
              
              return response;
            })
            .catch(() => {
              // Retornar página offline para navegação
              if (request.destination === 'document') {
                return caches.match('/offline.html');
              }
            });
        })
    );
    return;
  }
  
  // Estratégia para páginas HTML (Network First, fallback para cache)
  if (request.destination === 'document' || 
      PAGES_TO_CACHE.some(page => request.url.includes(page))) {
    
    event.respondWith(
      fetch(request)
        .then(response => {
          if (!response || response.status !== 200) {
            return caches.match(request);
          }
          
          const responseToCache = response.clone();
          caches.open(RUNTIME_CACHE)
            .then(cache => {
              cache.put(request, responseToCache);
            });
          
          return response;
        })
        .catch(() => {
          return caches.match(request)
            .then(cachedResponse => {
              if (cachedResponse) {
                return cachedResponse;
              }
              
              // Retornar página offline
              return caches.match('/offline.html');
            });
        })
    );
    return;
  }
  
  // Estratégia para APIs (Network First, timeout curto)
  if (request.url.includes('/api/') || 
      request.url.includes('/ia/') || 
      request.url.includes('/admin/')) {
    
    event.respondWith(
      Promise.race([
        fetch(request),
        new Promise((_, reject) => 
          setTimeout(() => reject(new Error('Timeout')), 3000)
        )
      ])
      .then(response => {
        if (!response || response.status !== 200) {
          throw new Error('Resposta inválida');
        }
        
        // Cache de respostas bem-sucedidas por 5 minutos
        const responseToCache = response.clone();
        caches.open(RUNTIME_CACHE)
          .then(cache => {
            cache.put(request, responseToCache);
          });
        
        return response;
      })
      .catch(() => {
        // Tentar obter do cache
        return caches.match(request)
          .then(cachedResponse => {
            if (cachedResponse) {
              return cachedResponse;
            }
            
            // Retornar resposta offline para APIs
            return new Response(
              JSON.stringify({
                error: 'Offline',
                message: 'Sem conexão com a internet',
                cached: false
              }),
              {
                status: 503,
                headers: {
                  'Content-Type': 'application/json'
                }
              }
            );
          });
      })
    );
    return;
  }
  
  // Para outras requisições, usar Network First
  event.respondWith(
    fetch(request)
      .catch(() => {
        return caches.match(request);
      })
  );
});

// Sincronização em background (para futuro uso)
self.addEventListener('sync', event => {
  if (event.tag === 'sync-performance') {
    event.waitUntil(syncPerformanceData());
  }
});

// Notificações push (para futuro uso)
self.addEventListener('push', event => {
  const options = {
    body: event.data ? event.data.text() : 'Nova atualização disponível!',
    icon: '/static/icons/icon-192x192.png',
    badge: '/static/icons/icon-72x72.png',
    vibrate: [100, 50, 100],
    data: {
      dateOfArrival: Date.now(),
      primaryKey: 1
    },
    actions: [
      {
        action: 'explore',
        title: 'Abrir App',
        icon: '/static/icons/icon-96x96.png'
      },
      {
        action: 'close',
        title: 'Fechar',
        icon: '/static/icons/icon-96x96.png'
      }
    ]
  };

  event.waitUntil(
    self.registration.showNotification('EBSERH TI Study', options)
  );
});

// Função para sincronizar dados de performance (offline)
async function syncPerformanceData() {
  try {
    const offlineData = await getOfflineData();
    
    for (const data of offlineData) {
      await fetch('/api/sync-performance', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
      });
    }
    
    await clearOfflineData();
    console.log('[SW] Dados sincronizados com sucesso');
  } catch (error) {
    console.error('[SW] Erro na sincronização:', error);
  }
}

// Funções auxiliares para armazenamento offline
async function getOfflineData() {
  // Implementar lógica para obter dados offline do IndexedDB
  return [];
}

async function clearOfflineData() {
  // Implementar lógica para limpar dados offline do IndexedDB
  console.log('[SW] Dados offline limpos');
}

// Limpeza periódica do cache
self.addEventListener('message', event => {
  if (event.data && event.data.type === 'SKIP_WAITING') {
    self.skipWaiting();
  }
  
  if (event.data && event.data.type === 'CACHE_CLEANUP') {
    event.waitUntil(
      caches.open(RUNTIME_CACHE)
        .then(cache => {
          return cache.keys()
            .then(keys => {
              return Promise.all(
                keys.map(key => {
                  if (Date.now() - new Date(key.headers.get('date')).getTime() > 24 * 60 * 60 * 1000) {
                    return cache.delete(key);
                  }
                })
              );
            });
        })
    );
  }
});
