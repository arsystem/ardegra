# ARDegra
ARDegra is a simple system that crawl data to gather data from every source in internet. 

### Installation
Because this is not a library, you need to download the whole source file from this repository:
1. `docker pull franziz/ardegra`
2. `git clone http://github.com/arsystem/ardegra`
3. `cd ardegra`
4. `mkdir config`
5. `touch config/database.json`
6. `docker run -d --name ardegra -v $(pwd):/root/app -w /root/app franziz/ardegra python run.py`

### System Architecture
Programming Language Python 3.5.2
Database: MongoDB Driver (pymongo)

### database.json
database.json is a config file to save ardegra data. Basic template as follow:
```json
{
	"azure-document-db":{
		"database": "xxx",
		"collection": "xxx",
		"host": "xxx",
		"port": xxx,
		"username": "xxx",
		"password": "xxx",
		"connectionString": "xxx"
	}
}
```