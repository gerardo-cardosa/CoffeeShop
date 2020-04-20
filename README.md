# CoffeeShop
 This is the project from Udacity to apply Authentication & Authorization into a Cofffe Shop website.

This app is composed of two parts:
1. The front end
2. The back end

The `./backend` is a [Python](https://www.python.org/ app based on Flask and SQL-Alchemy. In this [document](https://github.com/gerardo-cardosa/CoffeeShop/tree/Develeopment/backend), you can find the requirements
and instructions to run the server. 

The `./frontend` is a web app based on [Ionic](https://ionicframework.com/). This [document](https://github.com/gerardo-cardosa/CoffeeShop/tree/Develeopment/frontend) contains the requirements
and instructions to serve the app. 

## API Reference

### Getting Started

Base URL: This app can be run locally and is not hosted as a base URL. The backend is 
hosted at: http://127.0.0.1:5000/ 
This is set as a proxy in the frontend configuration. 

### Error Handling

Errors are returned as JSON objest in the below format:
```
{
    "success": False,
    "eror": 404,
    "message": "Not found"
}
```
The API will return two kinds of errors:

1. 401: Unauthorized
2. 403: Forbidden
3. 404: Not found
4. 422: Not Processable 

### Endpoints

#### GET /drinks

1. General

    This endpoint will return a result object containing:

    1. success
    2. and a list of drinks


2. Sample: 
```bash
curl http://127.0.0.1/5000/drinks
```
```
{
  "drinks": [
    {
      "id": 1,
      "recipe": [
        {
          "color": "white",
          "parts": "1"
        },
        {
          "color": "green",
          "parts": "1"
        },
        {
          "color": "red",
          "parts": "1"
        }
      ],
      "title": "Vampire"
    }
  ],
  "success": true
}
```

#### POST /drinks

1. General

    1. This endpoint will create a new drink when sending and object containing title and the recipe. 
    2. The recipe is a list of objects containing name, colour and parts of the ingridient. 

2. Sample: 

```bash 
curl http://127.0.0.1/5000/drinks -X POST -H "Content-type: application/json" -d '{
	"title":"Vampire",
	"recipe": [{"color": "white", "name":"Tequila", "parts":"1"},
				{"color": "green", "name":"Lime juice", "parts":"1"},
				{"color": "red", "name":"Sangrita", "parts":"1"}
	]
}'
```

#### Delete /drink/{drink_id}

1. General: Deletes the drink of the given ID if it exists. Return the id of the deleted question and a success value. 

2. Example curl -X DELETE http://127.0.0.1:5000/questions/1


#### Get /drinks-details

1. General: This endpoint will return a detailed information from drinks.  

2. Sample: curl http://127.0.0.1:5000/categories
```
{
  "drinks": [
    {
      "id": 1,
      "recipe": [
        {
          "color": "white",
          "name": "Tequila",
          "parts": "1"
        },
        {
          "color": "green",
          "name": "Lime juice",
          "parts": "1"
        },
        {
          "color": "red",
          "name": "Sangrita",
          "parts": "1"
        }
      ],
      "title": "Vampire"
    }
  ],
  "success": true
}
```
#### PATCH /drinks

1. General

    1. This endpoint will update the drink information when providing a new title and/or recipe 

2. Sample: 

```bash 
curl http://127.0.0.1/5000/drinks -X PATCH -H "Content-type: application/json" -d '{
	"title":"Margarita"
}'
```