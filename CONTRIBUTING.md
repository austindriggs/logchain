# CONTRIBUTING

Thanks for contributing! Please keep some of these guidelines in mind when setting up, coding, and building!


## Setup the Repo

Clone (using HTTPS):
```sh
git clone https://github.com/austindriggs/logchain.git
```

## Install Docker for your Environment

For the most up to date instructions, follow the official [Install Docker Engine on Ubuntu](https://docs.docker.com/engine/install/ubuntu/). 

Run the following command to uninstall all conflicting packages:
```sh
sudo apt remove $(dpkg --get-selections docker.io docker-compose docker-compose-v2 docker-doc podman-docker containerd runc | cut -f1)
```

Set up Docker's apt repository:
```sh
# Add Docker's official GPG key:
sudo apt update
sudo apt install ca-certificates curl
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc

# Add the repository to Apt sources:
sudo tee /etc/apt/sources.list.d/docker.sources <<EOF
Types: deb
URIs: https://download.docker.com/linux/ubuntu
Suites: $(. /etc/os-release && echo "${UBUNTU_CODENAME:-$VERSION_CODENAME}")
Components: stable
Signed-By: /etc/apt/keyrings/docker.asc
EOF

sudo apt update
```

To install the latest version, run:
```sh
sudo apt install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin docker-compose
```

Verify that Docker is running:
```sh
sudo systemctl status docker
```

You may want to add your user to the docker group:
```sh
sudo usermod -aG docker $USER
```


## Making your Changes

Checkout your own branch:
```sh
cd logchain
git checkout -b <your-branch-name>
```

> Keep the branches short and code reviews often.

A description of the files is found below:
```sh
driggs@driggs-HP-PD:~/code/logchain$ tree
.
├── CONTRIBUTING        # todo
├── Dockerfile          # todo
├── LICENSE             # todo
├── README.md           # todo
├── TODO.md             # todo
├── cpe493              # todo
│   ├── README.md       # todo
│   └── proposal.md     # todo
├── docker-compose.yml  # todo
├── logchain.yaml       # todo
├── requirements.txt    # todo
└── src                 # todo
    └── app.py          # todo

3 directories, 11 files
```

## Run the Container

Build and run the container:
```sh
docker build -t <tag_name> .
docker run -p 5000:5000 <tag_name>
```

Or simply run:
```sh
docker-compose up --build
```

And then open the webpage https://localhost:5000/ in your browser to verify the container is running.

When you are done running the container, run:
```sh
docker-compose down
```


## Submitting Changes

- Again, keep your branches short and code reviews often.
- Commit specific changes with descriptive messages.
- Push to your fork or branch and open a pull request against main.
