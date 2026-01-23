# -------- BUILD STAGE --------
FROM oven/bun:latest AS builder

WORKDIR /app

# Install deps first (better caching)
COPY package.json bun.lockb ./
RUN bun install

# Copy source
COPY . .

# Bundle the server
RUN bun build src/index.ts \
  --outdir dist \
  --target bun \
  --minify \
  --sourcemap=external

# -------- RUNTIME STAGE --------
FROM oven/bun:slim

WORKDIR /app

# Copy only built output
COPY --from=builder /app/dist ./dist

# Optional: copy .env if needed (or inject via runtime env)
# COPY .env .env

EXPOSE 3000

CMD ["bun", "dist/index.js"]

