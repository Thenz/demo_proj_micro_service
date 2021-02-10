We decided to implement a review micro service that presents information about
the presented product directly under the product itself.

We have decided on Python as our backend language. Our first goal is to duplicate
an existing microservice in order to stay consistent with the microservice
structure. We choose the recommendation service as it was written in Python and
located conveniently below the product on the store-page where we imagine our
recommendation service to be.

Our first intermediate goal is to implement a perfect copy of the recommendation
service that will serve as a template out of which we can sculpt our review
service. Explicitly we want to

* have a separate source folder reviewservice that is successfully being built
and integrated into the rest of the application
* have that reviewservice communicate with the html via its own RPCs

Fulfilling our that first goal was easy enough as we got to copy the
recommendaitonservice folder, rename it to be reviewservice and replace each
reference to recommendationservice with reviewservice. 
