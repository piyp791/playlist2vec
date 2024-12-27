# syntax=docker/dockerfile:1
ARG NODE_VERSION=20.18.0

FROM node:${NODE_VERSION}-alpine

RUN apk add --no-cache curl

# Use production node environment by default.
ENV NODE_ENV production
WORKDIR /usr/src/app

COPY package*.json .

RUN npm ci --only=production

COPY . .

# Set permissions for the logs directory
RUN mkdir -p src/logs &&chown -R node:node src/logs

# Run the application as a non-root user.
USER node

# Expose the port that the application listens on.
EXPOSE 3000

# Run the application.
ENV PORT 3000
CMD node src/index.js