from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy

app=Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+mysqldb://root:<password>@127.0.0.1:3306/mydb"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db=SQLAlchemy(app)

#user model for db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)

with app.app_context():
    db.create_all()

    #  Post routes
@app.post("/signup")
def signup():
    data=request.get_json()
    user_name= data.get("username")
    email=data.get("Email")
    user_password=data.get("password")

    exist_user=User.query.filter_by(username=user_name).first()
    if exist_user:
        return f" User already exists"
    
    new_user=User(username=user_name,email=email,password=user_password)
    db.session.add(new_user)
    db.session.commit()

    return {"meassage":f"User {user_name} ragister suscessfully"}


@app.post("/login")
def login():
    data=request.get_json()
    user_name= data.get("username")
    user_password=data.get("password")

    user=User.query.filter_by(username=user_name,password=user_password).first()

    if user:
        return {"message":f"Welcome {user_name}"}
    return {"msg":f'Enter correct details'},401


@app.get("/users")
def get():
    users=User.query.all()
    result=[]
    for i in users:
        result.append({"id":i.id,"username":i.username,"email":i.email})
    return {'Users':result}


#   --> change user detaild via id
@app.put("/user/<int:u_id>")
def updaate_user(u_id):
    data=request.get_json()
    user=User.query.get(u_id)

    if not user:
        return f" User not Found "
    if "username" in data:
        user.username=data["username"]
    if "Email" in data:
        user.email=data["Email"]
    if 'password' in data:
        user.password=data["password"]

    db.session.commit()
    return f" userid {u_id} details succesfully changes"

@app.delete("/user/<int:u_id>")
def delete_user(u_id):
    user=User.query.get(u_id)
    if not user:
        return f" User not Found "
    
    db.session.delete(user)
    db.session.commit()

    return f" user_id {u_id} sucesfully deleted from your database "





@app.get("/")
def home():
    return "Home page"

# @app.get("/welcome")
# def welcome():
#     user=request.args.get("user","guest")
#     return render_template("welcome.html", title="Welcome Page", user=user)

# @app.get("/hello/<name>")
# def hello_name(name):
#     return f"Hello {name}"

# @app.get("/greet/<user>/<int:age>")
# def greet(user,age):
#     return f"Hello {user} you are {age} years old"

# @app.get("/cube/<int:n>")
# def cube(n):
#     return {"cube": n**3}

# @app.get("/add")
# def add():
#     a=request.args.get("a",type=int, default=0)
#     b=request.args.get("b",type=int, default=0)
#     return {"a": a, "b":b, "Sum": a+b}


# #  Post routes
# users=[]

# @app.post("/signup")
# def signup():
#     data=request.get_json()
#     user_name= data.get("username")
#     email=data.get("Email")
#     user_password=data.get("password")

#     for u in users:
#         if u["username"]==user_name:
#             return {"Meassage":"User already exist"},400
        
#     user={"username":user_name,"Email":email,"Pasword":user_password}
#     users.append(user)

#     return {"meassage":f"User {user_name} ragister suscessfully"}


# @app.post("/login")
# def login():
#     data=request.get_json()
#     user_name= data.get("username")
#     user_password=data.get("password")

#     if user_name=="admin" and user_password=="admin123":
#         return {"message":f"Welcome {user_name}"}
   
#     return {"msg":f'Enter correct details'},401

# @app.get("/users")
# def get():
#     return {"Users":users}


#    Put routes (update)

# @app.put("/users/<user_name>")
# def update_user(user_name):
#     data=request.get_json()
#     for u in users:
#         if u["username"]==user_name:
#             u["Email"]=data.get("Email",u["Email"])
#             u["Pasword"]=data.get("Pasword",u["Pasword"])

#             return {"Meassage": f" User {user_name} update sucsesfully "}
#     return f" User not found "


# #  Delete user

# @app.delete("/users/<user_name>")
# def delete_user(user_name):
#     for u in users:
#         if u["username"]==user_name:
#             users.remove(u)

#             return f"User {user_name} delete sucessfully"
#         return f" User not found"

    
    
if __name__ == "__main__":
    app.run(debug=True)