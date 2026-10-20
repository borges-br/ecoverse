import assert from 'node:assert/strict';
import { execFileSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';

const root = fileURLToPath(new URL('../../', import.meta.url));
const env = { ...process.env, ECOVERSE_IMAGE_TAG: 'validation' };
for (const key of ['POSTGRES_PASSWORD', 'REDIS_PASSWORD', 'STORAGE_PASSWORD', 'AUTH_SECRET', 'JWT_SECRET', 'JWT_REFRESH_SECRET', '2FA_KEY']) env[`ECOVERSE_${key}`] = 'a'.repeat(64);
const docker = process.env.DOCKER_BIN || 'docker';
const stack = JSON.parse(execFileSync(docker, ['compose', '--env-file', '.env.portainer.example', '-f', 'docker-compose.prod.yml', 'config', '--format', 'json'], { cwd: root, env, encoding: 'utf8' }));
assert.equal(stack.name, 'ecoverse');
assert.deepEqual(Object.keys(stack.services).sort(), ['ecoverse-api', 'ecoverse-db', 'ecoverse-redis', 'ecoverse-storage', 'ecoverse-web']);
for (const service of Object.values(stack.services)) {
  assert.equal(service.ports?.length || 0, 0, 'Production must not publish host ports');
  assert(!service.container_name, 'Avoid global container names');
  for (const mount of service.volumes || []) assert.equal(mount.type, 'volume', 'Portainer stack must not depend on a host bind path');
}
const database = new URL(stack.services['ecoverse-api'].environment.DATABASE_URL);
assert.equal(database.hostname, 'ecoverse-db');
assert.equal(database.pathname, '/ecoverse');
assert.equal(database.username, 'ecoverse');
assert.equal(stack.services['ecoverse-db'].environment.POSTGRES_DB, 'ecoverse');
for (const name of ['ecoverse_db_data', 'ecoverse_redis_data', 'ecoverse_storage_data']) assert.equal(stack.volumes[name].name, name);
assert.equal(stack.services['ecoverse-storage'].environment.AWS_ACCESS_KEY_ID, 'ecoverse_storage');
assert(stack.services['ecoverse-storage'].environment.AWS_SECRET_ACCESS_KEY);
assert(stack.services['ecoverse-storage'].image.includes('@sha256:'));
for (const name of ['ecoverse-api', 'ecoverse-db', 'ecoverse-redis', 'ecoverse-storage']) assert(!stack.services[name].networks.ecoverse_proxy, 'Only web joins the shared proxy network');
assert(stack.services['ecoverse-web'].networks.ecoverse_proxy);
assert.equal(stack.services['ecoverse-web'].environment.INTERNAL_API_URL, 'http://ecoverse-api:3001');
assert(stack.services['ecoverse-api'].healthcheck.test.join(' ').includes('/health/ready'));
console.log('PASS: independent EcoVerse database and three own volumes');
console.log('PASS: no host ports or bind mounts; only web joins the proxy');
console.log('PASS: internal API routing and dependency readiness');
const local = JSON.parse(execFileSync(docker, ['compose', '--env-file', '.env.example', '-f', 'docker-compose.yml', 'config', '--format', 'json'], { cwd: root, env, encoding: 'utf8' }));
assert.equal(local.name, 'ecoverse-local');
assert(local.services['ecoverse-storage']);
assert.equal(local.services['ecoverse-api'].environment.MINIO_ENDPOINT, 'ecoverse-storage');
assert(local.services['ecoverse-api'].depends_on['ecoverse-storage']);
console.log('PASS: local quickstart resolves the storage service correctly');
