Docker Bingosync
===

This is a fork of the Bingosync.com repository focused on wrapping the project into a nice Docker Compose application to allow easy deployment anywhere

This also has a WhiteNoise static file server so that you don't have to worry about serving the static files yourself

## SSL certificates

You will need SSL certificates to be able to run this server, I recommend using Certbot to get one.
With Certbot, once you have your SSL certificates, you want to export the 'fullchain.pem' and 'privkey.pem' files into a .pfx certificate.

the Docker Compose application expects you to have these environment variables set on your system:

- SSL_CERT_PATH: The directory where the certificates are (i.e.: /path/to/certs/)
- SSL_CERT_FILE: The .pfx certificate file name (i.e.: the-certificate.pfx)
- SSL_CERT_PASSWORD: The certificate's password
- PUBLIC_DOMAIN: The address to your public domain where this bingosync instance is hosted

## Deployment:

- Install docker on the target machine
- Get the SSL certificates on the target machine and export them as a .pfx file
- Clone this repository
* Secrets:
  - Edit the `secrets.env` file to reflect your configuration
  - Set the SSL environment variables
  - Check if the variables are getting picked up by Docker Compose by running `docker compose convert`

- Run `docker compose up -d` in the repo's root directory, (-d makes it run in the background)
- Run `docker compose down` to stop the server

---

This is the repository powering [bingosync.com](http://bingosync.com/),
a web application that lets people collaboratively work on "bingo boards"
when speedrunning games.

For more information on speedrunning and bingo, you can read:
  - [the bingosync about page](http://bingosync.com/about)
  - [the speedrunslive faq](https://www.speedrunslive.com/rules-faq/faq)
  - [the about section of an SRL bingo card](https://www.speedrunslive.com/tools/bingo/oot)

#### Fun Implementation Details! :D

Bingosync is implemented using a combination of the [django](https://www.djangoproject.com/)
and [tornado](http://www.tornadoweb.org/) web servers. The django web server
(bingosync-app) hosts the main website content, serves most of the pages,
and talks to the database. The tornado web server (bingosync-websocket)
maintains all websocket connections to the site and passes messages along
to the clients in a "publish and subscribe" kind of model.

The actual site is hosted on one of my personal machines. It's running behind 
an [nginx](http://wiki.nginx.org/Main) proxy that serves static files and splits
traffic to the django and tornado servers. I use [postgres](http://www.postgresql.org/)
for the database. Conveniently, this machine is the same one that I run 
[bingobot](https://github.com/kbuzsaki/bingobot) off of. Maybe there's some 
opportunity for integration there in the future :)
