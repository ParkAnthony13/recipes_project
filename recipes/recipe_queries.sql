INSERT INTO users (first_name,last_name,email,password,created_at, updated_at)
VALUES('test','test','test@test.com','password',NOW(), NOW());

INSERT INTO recipes (name,time,instructions,description,created_at, updated_at,user_id)
VALUES('Chips and Guac','Yes','Buy guac and chips put em in separate bowls','easy yum',NOW(), NOW(),1);

SELECT * FROM users;

SELECT * FROM recipes;

SELECT * FROM users
JOIN recipes ON users.id = recipes.user_id;

SELECT * FROM users
LEFT JOIN recipes ON users.id = recipes.user_id;

SELECT * FROM recipes
JOIN users on users.id = recipes.user_id;



INSERT INTO users(first_name,last_name,email,password,created_at,updated_at)
VALUES('first_name','last_name','email','password',NOW(),NOW());

INSERT INTO recipes(name,time,instructions,descriptions,created_at,updated_at,user_id)
VALUES('name','time','instructions','descriptions',NOW(),NOW());



DELETE FROM users WHERE id=1;

DELETE FROM recipes WHERE id=1;