## Review microservice

This repository adds a review microservice to the [Google Microservice Demo](https://github.com/GoogleCloudPlatform/microservices-demo). The review microservice presents relevant user reviews on each product's page. It receives the product id from the viewed product and matches it with the product id in a list of product reviews for all products. All reviews for a viewed product are displayed below the product information. Reviews can be added in the `reviews.json` file located in inside `src/reviewservice`.

## Installation Guide

The collection of microservices is run inside a local Kubernetes cluster.

1. To launch **Minikube**. Please ensure that the local Kubernetes cluster has at least:

      * 4 CPUs
      * 4 GiB of memory

  by running `minikube start --cpus=4 --memory 4096`

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
