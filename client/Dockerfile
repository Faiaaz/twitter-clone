# Use Node.js image
FROM node:18-alpine

# Set working directory
WORKDIR /app

# Copy package.json and package-lock.json first
COPY package.json package-lock.json ./

# Ensure dependencies install correctly
RUN npm install --legacy-peer-deps

# Explicitly install react-scripts
RUN npm install -g react-scripts

# Copy the entire frontend code
COPY . .

# Fix OpenSSL issue for Webpack
ENV NODE_OPTIONS=--openssl-legacy-provider

# Expose frontend port
EXPOSE 3000

# Start React in development mode
CMD ["npm", "start"]
