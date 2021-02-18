## Installation Guide

The collection of microservices is run inside a local Kubernetes cluster.

1. To launch **Minikube**. Please ensure that the local Kubernetes cluster has at least:

  * 4 CPUs
  * 4 GiB of memory
  * 32 GB of disk space

    `minikube start --cpus=4 --memory 4096 --disk-size 32g`

2. Run `kubectl get nodes` to verify you're connected to the respective control plane.

3. Run `skaffold run` (first time will be slow, it can take ~20 minutes)

4. Run `kubectl get pods` to verify the Pods are ready and running

5. Access the web frontend through your browser

  * **Minikube** requires you to run a command to access the frontend service:

    `minikube service frontend-external`

## Adding reviews

To add an review to be displayed on the store page, open `reviews.json` located in inside 
`src/reviewservice`. Fill the fields

  * id
  * name
  * user
  * stars
  * review

with the desired content, and reload the page.

## Cleanup

If you've deployed the application with `skaffold run` command, you can run skaffold deleteto clean up deployed resources.
