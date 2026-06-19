# Atlas framework site — a small Flask app that renders the repo's markdown.
# Pages, raw .md, /llms.txt and /llms-full.txt are all produced on request from the
# same markdown files — nothing is pre-generated.
FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Version stamp — CI passes the git SHA + build time; exposed at /version and the
# X-Atlas-Version header so freshness is a one-line check.
ARG ATLAS_VERSION=dev
ARG ATLAS_BUILT=""
ENV ATLAS_VERSION=${ATLAS_VERSION} \
    ATLAS_BUILT=${ATLAS_BUILT}

EXPOSE 80
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1/llms.txt')" || exit 1

# gunicorn serves the WSGI app; 2 workers is plenty for a docs site.
CMD ["gunicorn", "--bind", "0.0.0.0:80", "--workers", "2", "app:app"]
