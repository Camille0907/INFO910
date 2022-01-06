# On récupère l'image d'nginx
FROM nginx

# On enlève le fichier nginx.conf par défaut...
RUN rm /etc/nginx/conf.d/default.conf

# ... Pour mettre celui que l'on veut à la place
COPY nginx.conf /etc/nginx/conf.d/
