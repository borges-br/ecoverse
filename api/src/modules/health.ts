// api/src/modules/health.ts
import { FastifyInstance } from 'fastify';

export default async function healthRoutes(fastify: FastifyInstance) {
  fastify.get('/', async () => {
    return { status: 'ok', timestamp: new Date().toISOString() };
  });

  fastify.get('/ready', async (_request, reply) => {
    async function probe(check: () => Promise<unknown>) {
      let timeout: ReturnType<typeof setTimeout> | undefined;
      try {
        await Promise.race([
          check(),
          new Promise((_, reject) => { timeout = setTimeout(() => reject(new Error('Readiness timeout')), 3000); }),
        ]);
        return 'ok';
      } catch { return 'unavailable'; }
      finally { clearTimeout(timeout); }
    }
    const [database, redis, storage] = await Promise.all([
      probe(() => fastify.prisma.$queryRaw`SELECT 1`),
      probe(() => fastify.redis.ping()),
      probe(() => fastify.storage.checkConnection()),
    ]);
    const ready = [database, redis, storage].every(status => status === 'ok');
    return reply.code(ready ? 200 : 503).send({
      status: ready ? 'ready' : 'unavailable',
      dependencies: { database, redis, storage },
    });
  });
}
