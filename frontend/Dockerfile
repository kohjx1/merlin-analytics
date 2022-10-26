FROM node:gallium-alpine
# ARG API_URL=https://sherlock.intellism.tech
# ENV VITE_API_URL=$API_URL

# install dependencies
WORKDIR /app
COPY package.json pnpm-lock.yaml ./
RUN npm i -g pnpm
RUN pnpm i

# Copy all local files into the image.
COPY . .

RUN pnpm run build

EXPOSE 3000
CMD ["node", "build"]
