# Atlas mini-site — static docs served by nginx.
# No build step: the site is just the repo's markdown rendered client-side by index.html,
# so the image only needs to serve the static files.
FROM nginx:1.27-alpine

# Declare UTF-8 on text responses (default charset_types covers text/plain, text/html,
# text/css, application/javascript) so em-dashes etc. in llms.txt / llms-full.txt and the
# pages don't render as mojibake. Also disable caching: this is a docs preview, and a stale
# cached Content-Type (without charset) is exactly what makes the mojibake stick on reload.
# conf.d/*.conf is included in nginx's http context.
RUN printf 'charset utf-8;\nadd_header Cache-Control "no-store" always;\n' > /etc/nginx/conf.d/charset.conf

# The served site = the repo's static files (index.html, styles.css, llms.txt) plus the
# markdown the page fetches and renders (README.md, STRUCTURE.md, method/*.md).
# .dockerignore keeps .git / tooling out of the image.
COPY . /usr/share/nginx/html

# nginx:alpine already serves /usr/share/nginx/html on port 80 with index.html as the index.
EXPOSE 80
HEALTHCHECK --interval=30s --timeout=3s --start-period=3s \
  CMD wget -qO- http://127.0.0.1/ >/dev/null 2>&1 || exit 1
