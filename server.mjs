import http from 'node:http'; import fs from 'node:fs'; import path from 'node:path'; import os from 'node:os';
const H = os.homedir(), PORT = Number(process.env.PORT || 2300), DIR = path.dirname(new URL(import.meta.url).pathname);
const ROOTS = { g: DIR + '/models', l: DIR + '/lib', v: H + '/downloads/selena_decoded', a: H + '/downloads/selena_decoded_audio', t: DIR + '/thumbs' };
const MIME = { '.png': 'image/png', '.glb': 'model/gltf-binary', '.js': 'text/javascript; charset=utf-8', '.jpg': 'image/jpeg', '.wav': 'audio/wav', '.obj': 'text/plain; charset=utf-8', '.json': 'application/json', '.html': 'text/html; charset=utf-8' };
http.createServer((req, res) => {
  try {
    const u = new URL(req.url, 'http://x'); let p = decodeURIComponent(u.pathname);
    if (p === '/') { res.writeHead(200, { 'content-type': MIME['.html'], 'cache-control': 'no-store' }); return res.end(fs.readFileSync(DIR + '/index.html')); }
    if (p === '/hero') { res.writeHead(200, { 'content-type': MIME['.html'], 'cache-control': 'no-store' }); return res.end(fs.readFileSync(DIR + '/hero.html')); }
    if (p === '/hero.json') { res.writeHead(200, { 'content-type': MIME['.json'], 'cache-control': 'no-cache' }); return res.end(fs.readFileSync(DIR + '/hero.json')); }
    if (p === '/experiment') { res.writeHead(200, { 'content-type': MIME['.html'], 'cache-control': 'no-store' }); return res.end(fs.readFileSync(DIR + '/experiment.html')); }
    if (p === '/experiment.json') { res.writeHead(200, { 'content-type': MIME['.json'], 'cache-control': 'no-cache' }); return res.end(fs.readFileSync(DIR + '/experiment.json')); }
    if (p === '/index.json') { res.writeHead(200, { 'content-type': MIME['.json'], 'cache-control': 'no-cache' }); return res.end(fs.readFileSync(DIR + '/index.json')); }
    const k = p.split('/')[1], root = ROOTS[k]; if (!root) { res.writeHead(404); return res.end('tidak ada'); }
    const full = path.join(root, p.split('/').slice(2).join('/'));
    if (!full.startsWith(root + path.sep) || !fs.existsSync(full) || !fs.statSync(full).isFile()) { res.writeHead(404); return res.end('tidak ada'); }
    const size = fs.statSync(full).size, h = { 'content-type': MIME[path.extname(full)] || 'application/octet-stream', 'accept-ranges': 'bytes', 'cache-control': 'max-age=3600' };
    const m = (req.headers.range || '').match(/bytes=(\d*)-(\d*)/);
    if (m && (m[1] || m[2])) { let s = m[1] ? +m[1] : size - +m[2], e = m[1] && m[2] ? +m[2] : size - 1; e = Math.min(e, size - 1);
      res.writeHead(206, { ...h, 'content-range': `bytes ${s}-${e}/${size}`, 'content-length': e - s + 1 }); return fs.createReadStream(full, { start: s, end: e }).pipe(res); }
    res.writeHead(200, { ...h, 'content-length': size }); fs.createReadStream(full).pipe(res);
  } catch (e) { res.writeHead(500); res.end(String(e.message)); }
}).listen(PORT, '0.0.0.0', () => console.log('mlbb-preview di port ' + PORT));
