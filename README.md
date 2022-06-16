# communitas

## Developing with Poetry

Add packages with `poetry add PACKAGENAME`, and run `poetry install`.

To run the development server, activate a shell by `poetry shell`, and run `python app.py`.

## Deployment

### Heroku

When deploying to Heroku use the Docker container. Use the Heroku CLI, and make sure to set the stack to container: `heroku stack:set container`
