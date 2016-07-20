import pymongo

client = pymongo.MongoClient('localhost', 27017)
db = client.mvp
db.authenticate('mvpUser', 'iGingoMvp')

init_document = {
    "fund": 800000,
    "products": [
        {
            "name": "prod1",
            "salePrice": 5,
            "discounts": [
                {"threshold": 100, "discount": 0.9},
                {"threshold": 200, "discount": 0.8}
            ],
            "lowerLimit": 50
        },
        {
            "name": "prod2",
            "salePrice": 7,
            "discounts": [
                {"threshold": 50, "discount": 0.8}
            ],
            "lowerLimit": 30
        },
        {
            "name": "prod3",
            "salePrice": 13,
            "discounts": [
                {"threshold": 150, "discount": 0.88},
                {"threshold": 300, "discount": 0.85}
            ],
            "lowerLimit": 100
        }
    ]
}


def get_collection(coll_name):
    return db[coll_name]


def init_collection(coll_name):
    return db[coll_name].insert_one(init_document)


if __name__ == '__main__':
    result = init_collection('scenario')
    print(result.inserted_id)
