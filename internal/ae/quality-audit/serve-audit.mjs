// Audit-only, read-only server. Does not expose the source PDFs or review APIs.
import http from 'node:http';
import fs from 'node:fs';
import path from 'node:path';
const root=process.cwd();
const mime={'.html':'text/html','.mjs':'text/javascript','.js':'text/javascript','.css':'text/css','.json':'application/json','.png':'image/png','.svg':'image/svg+xml','.woff2':'font/woff2'};
http.createServer((req,res)=>{
 try{
  const pathname=decodeURIComponent(new URL(req.url,'http://localhost').pathname);
  if(req.method!=='GET'){res.writeHead(405);res.end();return;}
  const relative=pathname==='/audit'?'internal/ae/quality-audit/browser.html':pathname==='/audit.js'?'internal/ae/quality-audit/browser.mjs':/^\/(?:data|js|css|figures|assets)\//.test(pathname)?pathname.slice(1):null;
  const file=relative&&path.resolve(root,relative);
  if(!file||!file.startsWith(root+path.sep)||!fs.existsSync(file)||!fs.statSync(file).isFile()){res.writeHead(404);res.end('Not found');return;}
  res.writeHead(200,{'Content-Type':mime[path.extname(file)]||'application/octet-stream','Cache-Control':'no-store'});fs.createReadStream(file).pipe(res);
 }catch{res.writeHead(400);res.end();}
}).listen(4191,'127.0.0.1',()=>console.log('Read-only audit harness: http://127.0.0.1:4191/audit'));
