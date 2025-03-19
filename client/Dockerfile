# Use Node.js image
FROM node:18-alpine

# Set working directory
WORKDIR /app

# Copy package.json first and install dependencies
COPY package.json package-lock.json ./
RUN npm install --legacy-peer-deps


# Install serve globally
RUN npm install -g serve

# Copy all files
COPY . .

# Fix OpenSSL error
ENV NODE_OPTIONS=--openssl-legacy-provider

# Build React app
RUN npm run build

# Ensure the correct directory for serving
#WORKDIR /app/build

# Install react-scripts explicitly to avoid missing module errors
RUN npm install -g react-scripts

# Expose frontend port
EXPOSE 3000

# Serve the frontend
#CMD ["npx", "serve", "-s", "build", "-l", "3000","--no-clipboard"]

# Start React in development mode
CMD ["npm", "start"]