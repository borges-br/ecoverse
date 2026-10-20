import { randomBytes } from 'node:crypto';
import { readFile, writeFile } from 'node:fs/promises';
import { fileURLToPath } from 'node:url';
import path from 'node:path';

const root = fileURLToPath(new URL('../../', import.meta.url));
const destination = path.join(root, '.env.portainer');
let content = await readFile(path.join(root, '.env.portainer.example'), 'utf8');
for (const name of ['POSTGRES_PASSWORD', 'REDIS_PASSWORD', 'STORAGE_PASSWORD', 'AUTH_SECRET', 'JWT_SECRET', 'JWT_REFRESH_SECRET', '2FA_KEY', 'ADMIN_PASSWORD']) {
  content = content.replace(new RegExp(`^ECOVERSE_${name}=.*$`, 'm'), `ECOVERSE_${name}=${randomBytes(32).toString('hex')}`);
}
try {
  await writeFile(destination, content, { flag: 'wx', mode: 0o600 });
  console.log('Arquivo privado criado: .env.portainer');
  console.log('Preencha o email do administrador e o SMTP antes da publicação. As senhas não foram exibidas.');
} catch (error) {
  if (error.code === 'EEXIST') {
    console.error('.env.portainer já existe; nenhum segredo foi alterado.');
    process.exitCode = 1;
  } else throw error;
}
