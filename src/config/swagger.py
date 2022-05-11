template = {

    "swagger": "2.0",

    "info":{

        "title": "Bookmarks API",
        "description": "This an API for bookmarks.",     
        "contact": {
            "name": "James Omare",
            "url": "http://www.example.com/support",
            "email": "jamesomare922@gmail.com"
        },
        "license": {
            "name": "Apache 2.0",
            "url": "https://www.apache.org/licenses/LICENSE-2.0.html"
        },
        "version": "1.0.1"
    },

    "basePath": "/api/v1", #base path for blueprint registration
    "schemes": [
        "http",
        "https"
    ],

    "securityDefinitions": {
        "Bearer": {
            "type": "apiKey",
            "name": "Authorization",
            "in": "header",
            "description": "JWT Authorization header using the Bearer scheme."+
            "Example: \"Authorization: Bearer {token}\""
        }
    }


}

swagger_config = {

    "headers": [

    ],

    "specs": [
        {
            "endpoint": 'apispec',
            "route": '/apispec.json',
            "rule_filter": lambda rule: True, #all in
            "model_filter": lambda tag: True, #all in
        }
    ],

    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/"


}