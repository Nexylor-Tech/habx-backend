FROM oven/bun:latest AS builder

WORKDIR /app

COPY package.json bun.lock ./
RUN bun install --frozen-lockfile

COPY . .

RUN bun build \
  --compile \
  --minify-whitespace \
  --minify-syntax \
  --target bun-linux-x64 \
  --outfile server \
  src/index.ts

# ---------- RUNTIME ----------

FROM gcr.io/distroless/base-debian12

WORKDIR /app

COPY --from=builder /app/server /app/server

EXPOSE 3000

CMD ["/app/server"]

