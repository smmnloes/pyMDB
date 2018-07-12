Welcome to pyMDB, an app that downloads IMDB datasets, extracts the most essential information and enables the user to search the data via a web interface. Further information (such as credits, budget, etc.) is aquired via __themoviedb.org__-API.

### Prerequisites
* NPM -> `sudo apt-get install npm`
* Python 3.5
* Pipenv -> `sudo apt-get install pip && pip install pipenv`

### Installation
1. Clone the repository
2. In the root directory of the project, execute `pipenv install`
3. In `/angular-frontend/` execute `npm install`

### Before the first start
Before you can use the application, you have to register on __themoviedb.org__ to get your own API-Key. Create a new file named `tmdb-api-key.ts` in `/angular-frontend/src/app/` with the content `export const TMDB_API_KEY = "<your API KEY>";`
You can also set `TMDB_API_KEY` to null or any other value, if you don't want to use this functionality. You need to create the file however, or else the project will not compile.

### Starting the application
You will have to start the python backend as well as the angular frontend.
#### Frontend
Go to `/angular-frontend/` and execute `npm start`. This will start the Development server at `localhost:4200`.

#### Backend
In `/py-backend/src/` execute `pipenv shell`, in the resulting shell execute `python3 main.py`. This will start the backend as well as the command line interface.

### Using the app
#### First run
On the first run, you have to download the Imdb data and create your database. In the backend-CLI, enter `update`. This will download the files from __https://datasets.imdbws.com__ one by one and read them into a SQLite database at `/DB_Data_Local/`.
For info on the tables in this database, please refer to `py-backend/src/DatabaseServices/DatabaseModel.py`.
The resulting database contains only information about movies, excluding adult films. Also not every value which is available from the datasets is read into the database.

#### Search filters
On `localhost:4200` you will find the search interface. Some quick notes on the search filters:
* __Title__: Search by movie title. This also matches partial names, e.g. "Star Wa" matches "Star Wars".
* __Genres__: Select up to 3 Genres
* __Min. Rating__: Only show results with rating higher than this value. This also implies that a certain threshold for number of votes will be applied. This value can be changed in `py-backend/src/DatabaseServices/QueryServies` under __MIN_NUM_VOTES__.
* __Min. Year/Max. Year__: Get only results from certain time period
* __Director__: Get only results with this director. *Important*: Only full matches will be accepted (vs. Title search)
* __Writer__: Get only results with this writer. *Important*: Only full matches will be accepted (vs. Title search)
* __Top billed actors__: Include only movies which star these top-billed actors. Up to 3 can be specified. *Important*: This does not check all of the credits, only the top-billed ones. Usually this will include up to 5 actors who are the most well-known ones in a movie.
* __Results__: Results to display per page
* __Sort by__: Choose which category to sort by (Title, Year or Rating)

#### Detailed information view
By clicking on the title of a search result, you will get to the Detailed View. This contains information like a more complete cast list or the movie budget for example. Note that the information for this is obtained from the free *themoviedb.org*-API. For some movies only limited information might be available, or none at all.

#### Command line options
The command line interface of the backend application supports the following commands:
* __update__: Loads the new datasets from imdb and reads them into the sqlite-Database. This happens one dataset at a time.  It can take some time, depending on your download speed and CPU power. Requires ~1.5GB of free disk space, as the uncompressed datasets can be quite big. The resulting database will be <500mb in size. If the update process is interrupted, it will roll back to the database version before updating.
* __download__: asks for which dataset to download and downloads and unpacks it to the folder `DB_Data_Remote`. Allowed  dataset names: "basics", "names", "crew", "principals" or "ratings"
* __read__: allows to specify a specific dataset which is read into the existing database, names similar to download
* __backup__: copies the current database to the `last_version`-folder
* __restore__: restores database from `last_version`-folder
* __exit__: exit application



### Legal disclaimer
Imdb does only allow the database information to be used for personal and non-commercial use. Therefore you are not allowed to deploy this application publicly or use it in any way not permitted by Imdb.


That's it. Have fun! Contributions and feedback always welcome!
