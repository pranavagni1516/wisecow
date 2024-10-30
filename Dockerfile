# Use an official Node.js runtime as a base image
FROM node:18

# Set the working directory in the container
WORKDIR /app

# Copy the package.json and package-lock.json files
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy the entire application code to the working directory
COPY . .

# Expose the port the app listens on (e.g., 3000)
EXPOSE 4499

# Run the application
CMD ["npm", "start"]
