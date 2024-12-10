## ABOUT

This repository contains code for [playlist2vec.com](https://playlist2vec.com/), a website built to demo the vector search model described in our paper, "Representation, Exploration, & Recommendation of Playlists". 

## FEATURES

- [x] Intuitive search interface and Spotify integration
- [x] Microservices architecture for seamless scalability.
- [x] Docker containers for a streamlined deployment.
- [x] Utilization of low-cost libraries ([SQLite](https://www.sqlite.org/) and [Usearch Vector Search](https://github.com/unum-cloud/usearch)) to minimize app footprint.
- [x] MMAP-based vector search enabling the application to operate efficiently on budget-friendly machines such as Raspberry Pi.
- [x] NGINX configuration for a robust traffic handling.
- [x] Rate limiting implemented to safeguard against DDoS attacks.
- [x] NGINX caching to optimize server resource usage.
- [ ] Auto-scaling capabilities using Kubernetes.

## INSTALLATION

*Note: This setup has been tested on Ubuntu 22.04 for both x86_64 and aarch64 architectures.*

### 1. Install Docker
1. Follow the instructions to install Docker from this link: [Install Docker On Ubuntu](https://docs.docker.com/engine/install/ubuntu/).
2. Make sure to complete the post-installation steps outlined [here](https://docs.docker.com/engine/install/linux-postinstall/).

### 2. Install Nginx
Install Nginx by following the guide available at: [How to Install Nginx on Ubuntu 22.04](https://www.digitalocean.com/community/tutorials/how-to-install-nginx-on-ubuntu-22-04).

### 3. Install NodeJS

You can install Node.js by referring to this tutorial: [How to install Node.js on Ubuntu 22.04](https://www.digitalocean.com/community/tutorials/how-to-install-node-js-on-ubuntu-22-04).

### 4. Download Code

Run the following command to clone the repository:

```
`git clone https://github.com/piyp791/playlist2vec.git`
```

### 5. Download Additional Resources
1. Download the [SQLite](https://www.sqlite.org/) database from [this link](https://filedn.com/lh14Jds6qK88cdaUD0PxR5j/playlist2vec/playlist2vec.db) and copy that to the following locations:
    - autocomplete-service/src
    - search-service/src

2. Download the [vector search index](https://github.com/unum-cloud/usearch) from [this link](https://filedn.com/lh14Jds6qK88cdaUD0PxR5j/playlist2vec/playlist_tree.usearch) and copy that to the following location:
    - search-service/src


### 6. Nginx Setup
1. Copy the `nginx/nginx.conf` file to `/etc/nginx/`.
2. Copy the `nginx/site_config` file to `/etc/nginx/sites-available/<YOURSITENAME>`.
3. Create a symbolic link from `sites-available` to `sites-enabled` with the following command:

    ```
    sudo ln -s /etc/nginx/sites-available/<YOURSITENAME> /etc/nginx/sites-enabled/
    ```

4. Remove the default configuration file by executing: 

    ```
    sudo rm /etc/nginx/sites-enabled/default
    ```
5. Create a cache directory for NGINX:

    ```
    sudo mkdir /var/cache/nginx
    ```

6. Verify the configuration is correct by running:

    ```
    sudo nginx -t
    ```

7. Restart NGINX with the command:

    ```
    sudo systemctl restart nginx
    ```

### 7. Install the Application

Navigate to the project directory and execute the build script:
```
cd playlist2vec
./build.sh.
``` 

This will create an HTTP version of the website, which can be integrated with a service like a [Cloudflare tunnel](https://www.cloudflare.com/en-ca/products/tunnel/) for an HTTPS frontend.

### RUN IN DEV MODE

### Setting up Search Service:
```
cd search-service
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn src.server:app --port 3001
```

### Setting up Autocomplete Service:
```
cd autocomplete-service
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn src.server:app --port 3002
```
### Setting up Web-Server:
```
cd web-server
npm install
npm run start-dev-mode
```

### RUN TESTS

```
cd web-server
npm run test-dev
```

## CITATION

```
Papreja, P., Venkateswara, H., Panchanathan, S. (2020). Representation, Exploration and Recommendation of Playlists. In: Cellier, P., Driessens, K. (eds) Machine Learning and Knowledge Discovery in Databases. ECML PKDD 2019. Communications in Computer and Information Science, vol 1168. Springer, Cham. https://doi.org/10.1007/978-3-030-43887-6_50
```
