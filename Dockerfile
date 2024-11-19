FROM node:16-alpine as builder

WORKDIR /app

# Copy only what we need
COPY frontend ./frontend/
COPY .env ./backend/.env
COPY generate-config.js .

# Generate the config file
RUN node generate-config.js

# Use nginx to serve the static files
FROM nginx:alpine
COPY --from=builder /app/frontend /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]