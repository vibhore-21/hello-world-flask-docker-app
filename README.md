# hello-world-flask-docker-app
Hello world flask app with docker & k8s 

### Build hello-world docker image
```sh
cd hello-world
docker build --build-arg PORT=4000 -t vibhorem/flask-hello-world-app:0.1.0 -f Dockerfile .
```

---
### Run hello-world container natively
```sh
# on linux
docker container run --network host -it vibhorem/flask-hello-world-app:0.1.0  # or v2

# on mac host networking is not available, hence ports have to be explicitly
# published.
docker container run -p 4100:4000 -it vibhorem/flask-hello-world-app:0.1.0  # or v2
```
Now you can access you container from bowser at port 4100 for mac & 4000 for linux

---
### Run hello-world container in a K8s Pod
```sh
cd kube-deploys
kubectl apply -f hello-world-namespace.yaml
kubectl apply -f hello-world-svc.yaml
kubectl apply -f hello-world-deployment.yaml
```
Access the hello-world service at :

```sh
# If you are running k8s on your local 
curl http://localhost:$(kubectl -n hello-world get svc \
    -o jsonpath='{.items[0].spec.ports[0].nodePort}')/
```
```sh
# If you are running on a k8s cluser on cloud 
curl http://<nodeip>:$(kubectl -n hello-world get svc \
    -o jsonpath='{.items[0].spec.ports[0].nodePort}')/
```
Note <node-ip> is, IP of any worker node in k8s cluster. 