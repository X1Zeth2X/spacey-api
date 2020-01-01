# Spacey REST API Design.

Features needed:
* A service that returns random space facts stored in a DB.
* CRUD for the space facts.
* Planet facts and cool information + facts (Added by users), also CRUD.
* Facts/Information management pages.
* Entry keys, Rate limiting, and Role system.

Possible endpoints:
* `[Status: WIP]` `/api/facts`: Returns an array of objects that are randomly selected from the database.
* `[Status: WIP]` `/api/facts/{planet: "earth"}`: Returns an object that contains information about the planet
which also includes IDs for space facts (also randomly selected) that belong to the planet.
* `[Status: Done]` `/api/fact/<create, delete, update, get>`: Fact CRUD route.
  - `POST`: Creates a new fact.
  - `DELETE`: Deletes a fact by its public id.
  - `PUT`: Updates a fact, identified by its public id.
  - `GET`: Get a single fact using its public id.
* If possible, add media support (mainly images for reading about facts/large information).