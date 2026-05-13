FROM nginx:alpine

# Copy nginx configuration
COPY nginx.conf /etc/nginx/nginx.conf

# Copy site root (index.html + static assets)
COPY index.html /usr/share/nginx/html/index.html
COPY static/ /usr/share/nginx/html/static/
COPY portfolio/ /usr/share/nginx/html/portfolio/

EXPOSE 80
