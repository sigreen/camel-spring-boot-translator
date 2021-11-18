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
     
## Help and contributions

If you hit any problem using Camel or have some feedback, then please
https://camel.apache.org/support.html[let us know].

We also love contributors, so
https://camel.apache.org/contributing.html[get involved] :-)

The Camel riders!
