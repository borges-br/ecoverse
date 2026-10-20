const {test}=require('node:test');
const assert=require('node:assert/strict');
const fs=require('node:fs/promises');
const os=require('node:os');
const path=require('node:path');
const Fastify=require('fastify');
const storagePlugin=require('../dist/plugins/storage').default;

async function withStorage(run){
 const root=await fs.mkdtemp(path.join(os.tmpdir(),'ecoverse-storage-test-'));
 const previous=process.env.UPLOADS_DIR;
 process.env.UPLOADS_DIR=path.join(root,'uploads');
 const app=Fastify();
 try{await app.register(storagePlugin);await app.ready();await run(app.storage,root);}
 finally{
  await app.close();
  if(previous===undefined)delete process.env.UPLOADS_DIR;else process.env.UPLOADS_DIR=previous;
  assert.equal(path.dirname(path.resolve(root)),path.resolve(os.tmpdir()));
  assert(path.basename(root).startsWith('ecoverse-storage-test-'));
  await fs.rm(root,{recursive:true,force:true});
 }
}
async function bytes(object){const parts=[];for await(const part of object.stream)parts.push(part);return Buffer.concat(parts);}
const png=Buffer.from('89504e470d0a1a0a00000000','hex');
const input={userId:'synthetic-user',target:'avatar',filename:'image.png',contentType:'image/png',buffer:png};

test('persistent upload keys preserve bytes, MIME, size and immutable public URLs',()=>withStorage(async(store)=>{
 await store.checkConnection();
 const first=await store.putImage(input),second=await store.putImage({...input,buffer:Buffer.from('second image')});
 assert.notEqual(first.key,second.key);
 assert.equal(first.url,'/api/backend/uploads/'+encodeURIComponent(first.key));
 const object=await store.getObject(first.key);
 assert.equal(object.contentType,'image/png');assert.equal(object.size,png.length);
 assert.deepEqual(await bytes(object),png);
}));

test('stored-image lookup rejects traversal, encoded paths and unrelated file extensions',()=>withStorage(async(store)=>{
 for(const key of ['../package.json','..%2fsecret.png','/etc/passwd','image.svg','..','folder/image.png'])await assert.rejects(store.getObject(key));
 await assert.rejects(store.getObject('missing.png'));
}));

test('stored-image lookup refuses symlinks to files outside the upload directory',async(t)=>{
 if(process.platform==='win32'){t.skip('Symlink privilege is not assumed on Windows; runs on Linux CI.');return;}
 await withStorage(async(store,root)=>{
  const secret=path.join(root,'outside.txt');await fs.writeFile(secret,'synthetic private data');
  await fs.symlink(secret,path.join(root,'uploads','linked.png'));
  await assert.rejects(store.getObject('linked.png'));
 });
});
