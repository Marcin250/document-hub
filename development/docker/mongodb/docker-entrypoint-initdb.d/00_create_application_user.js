print("Adding application user..");

db = db.getSiblingDB("admin");
db.createUser({
    user: "db_user",
    pwd: "db_password",
    roles: [{role: "readWrite", db: "documents"}]
});

print("Application user added.");