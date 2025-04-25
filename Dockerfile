# ---- Stage 1: Build ----
FROM node:22-slim AS builder

WORKDIR /usr/src/app

COPY package*.json tsconfig.json ./
RUN npm install

COPY api-server/ ./api-server/
RUN npm run build

# ---- Stage 2: Production ----
FROM node:22-slim

RUN groupadd -r appgroup && useradd -r -g appgroup appuser

WORKDIR /usr/src/app

COPY package*.json ./
RUN npm ci --production

COPY --from=builder /usr/src/app/dist ./dist

RUN chown -R appuser:appgroup /usr/src/app

# switch to non-root user
USER appuser

EXPOSE 3111
CMD ["node", "dist/api-server/index.js"]