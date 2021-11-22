Translating Pig Latin with Apache Camel
==========================================

This example show how to use Camel to translate any phrase into Pig Latin via a RESTful service.  
It makes use of Spring Boot and can run either standalone or on Kubernetes.

## Prerequisites

1. Java 11+
2. Maven 3.8+

## Build

You can build this example using

```
    mvn package
```

## Run the example

Using the shell:

 1. Start the springboot service:

```
  $ mvn spring-boot:run
```

## Test the example:

Using Insomnia, import the Swagger spec using the following url:

```
     http://localhost:8080/camel/api-doc
```

You can test the transformation using any phrase you like in the body:

```
     {'phrase':'Giving Your Legacy Applications an API Facelift with Kong'}
```

Where you can find information about the services and its state.
     
## Deploying to Kubernetes

To deploy to AWS (EKS), we need to follow these steps.

## Prerequisites

1. Java 11+
2. Docker
3. Terraform
4. An AWS account, with AWS Access Key and Secret Access Key credentials
5. AWS CLI
6. kubectl

## Provision

1. Login to AWS CLI using your credentials:

```bash
$ aws configure
AWS Access Key ID [None]: YOUR_AWS_ACCESS_KEY_ID
AWS Secret Access Key [None]: YOUR_AWS_SECRET_ACCESS_KEY
Default region name [None]: YOUR_AWS_REGION
Default output format [None]: json
```

2. Via the CLI, run terraform.  This will take roughly 7-10 minutes:

```
cd src/tf-provision
terraform init
terraform plan # verify terraform can connect to AWS and create EKS cluster
terraform apply # provision cluster on EKS.  Accept apply by typing "yes"
```

3. Once provisioning is complete, setup `kubectl` to point to your new EKS cluster and test:

```bash
aws eks --region $(terraform output -raw region) update-kubeconfig --name $(terraform output -raw cluster_name)
kubectl get all
```

4.  Via the EC2 management web console, create a new ECR public repo called `pig-latin-translator`.

5. Via the CLI (/camel-spring-boot-translator directory), running the following commands to build the Docker image locally:

```bash
mvn clean spring-boot:build-image
```

6. Login to the public ECR repo (using the push commands popup), then tag the docker image and push it to the the ECR repo using your correct repo ID:

```bash
aws ecr-public get-login-password --region us-east-1 | docker login --username AWS --password-stdin public.ecr.aws/b9p7h9h8
docker tag camel-spring-boot-translator:1.0.0 public.ecr.aws/b9p7h9h8/pig-latin-translator:1.0.0
docker push public.ecr.aws/b9p7h9h8/pig-latin-translator:1.0.0
```

7. Update the repo ID in `src/k8s/deployment.yaml` to point to the correct ECR repo:

```yaml
    spec:
      containers:
      - image: public.ecr.aws/b9p7h9h8/pig-latin-translator:1.0.0
        name: camel-spring-boot-translator
        resources: {}
status: {}
```

8. Deploy the image and service to EKS:

```bash
kubectl apply -f src/k8s/deployment.yaml 
```

9. Run the following command and copy the `LoadBalancer Ingress` hostname:

```bash
kubectl describe service camel-spring-boot-translator
```

10.   Using the above hostname, test the service with the following command:

```bash
curl a72d5cbca16194294b2036694bdba160-1454608839.us-east-1.elb.amazonaws.com/camel/api-doc
```

11.  You can import the above URL into Insomnia and test the endpoint using the Swagger.  Try the following body payload:

```json
{"phrase": "Giving Your Legacy Applications an API Facelift with Kong"}
```

12.  If the request is successful, you should receive the following response:

```json
{
  "translatedPhrase": "ivinggay ouryay egacylay applicationsyay anyay apiyay aceliftfay ithway ongkay "
}





You can build this example using

```
    mvn package
```