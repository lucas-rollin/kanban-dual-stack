# Stage 1: Common Base Layer
FROM node:22-alpine AS base
WORKDIR /app
RUN corepack enable && corepack prepare pnpm@latest --activate
COPY package*.json pnpm-lock.yaml* ./
RUN pnpm install --frozen-lockfile
COPY . .

# Stage 2: Development Target
FROM base AS development
EXPOSE 5173

CMD ["pnpm", "dev", "--", "--host"]

# Stage 3: Build Asset Layer
FROM base AS builder

RUN pnpm run build

# Stage 4: Production Target
FROM nginx:1.27-alpine AS production
COPY --from=builder /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
