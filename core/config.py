ç#RECON CONFIG
BASE_IMAGE=debian
BASE_IMAGE_TAG=latest
REDTEAM_IMAGE_NAME="adastra/reddocker"


#Tags for the containers
REDTEAM_BASE_TAG="base" #Base image with the needed software.
REDTEAM_RECON_TAG="recon" #Recon image
REDTEAM_weaponization_TAG="weapon" #Recon image


CONTAINER_RECON="recon-container"
DOCKERFILE_PATH=../config/docker/Dockerfile-recon